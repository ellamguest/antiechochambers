from google.cloud import bigquery
import pandas as pd
from tqdm import tqdm
import numpy as np
import json
from pathlib import Path
import glob
import numpy as np
from scipy import sparse
from concurrent.futures import TimeoutError
from sqlalchemy import create_engine
import google.auth
from google.cloud import storage

cache_file = lambda filename: Path().resolve().joinpath(*['cache', filename])

""""" DATA IMPORT & EXPORT """

"""BIGQUERY FUNCTIONS"""

def client():
    """require a bigquery project and credentials, save in json in root main directory"""
    credsfile = Path().resolve().joinpath('antiechochambers-1ba7f7f4c68e.json')
    return bigquery.Client.from_service_account_json(credsfile)

def jobConfig():
    config = bigquery.QueryJobConfig()
    config.query_parameters = (bigquery.ScalarQueryParameter('size', 'INT64', 10),)
    config.use_legacy_sql = False
    config.maximum_bytes_billed = int(5e9)
    
    return config

def run_job(query):
    j = client().query(query=query, job_config=jobConfig())
    return j

def fetchQuery(query):
    j = run_job(query)
    df = j.to_dataframe()
    
    return df
    
def fetchSubList():
    """should create bot table to call on"""
    query = f"""SELECT *
                 FROM `aerobic-datum-126519.sms_18_sample_subreddits.randomSubreddits`
                 """

    data = fetchQuery(query)
    
    return data

def fetchSubredditData(subreddit):
    """should create bot table to call on"""
    query = f"""
                SELECT *
                FROM `aerobic-datum-126519.sms_18_sample_subreddits.allAuthorCommentCounts`
                WHERE author in (SELECT author
                                 FROM `aerobic-datum-126519.sms_18_sample_subreddits.subredditAuthors`
                                 WHERE (subreddit = '{subreddit}') AND (weight > 2) AND
                                         author not in (SELECT author
                                                         FROM `fh-bigquery.reddit_comments.bots_201505`)
                                        AND (lower(author) NOT LIKE '%bot%')
                                        AND (author NOT LIKE 'JlmmyButler')
                                        AND (author NOT LIKE 'TotesMessenger'))
                    AND authorCommentCount > 2
                ORDER BY subreddit, author
                """

    data = fetchQuery(query)
    
    return data
    
""" GOOGLE STORAGE FUNCTIONS """

def get_storage_client():
    credentials, project = google.auth.default() # why returning empty project name?
    project = 'aerobic-datum-126519'
    return storage.Client(project=project,
                             credentials=credentials)
def list_buckets():
    storage_client = get_storage_client()
    buckets = list(storage_client.list_buckets())
    print(buckets)
    
def create_bucket(bucket_name):
    storage_client = get_storage_client()
    bucket = storage_client.create_bucket(bucket_name)
    print('Bucket {} created.'.format(bucket.name))
    
def upload_blob(bucket_name, file_name):
    """Uploads a file to the bucket."""
    storage_client = get_storage_client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(file_name)

    print(f'File {file_name} uploaded.')    
    
    
""" NETWORK FUNCTIONS """    

def get_node_ids_dict(edgelist):
    node_ids = list(edgelist.subreddit.unique()) + list(edgelist.author.unique())
    return dict(zip(node_ids, range(len(node_ids))))

def get_edges(edgelist, subreddit):
    node_ids_dict = get_node_ids_dict(edgelist)

    edgelist = edgelist[edgelist['subreddit']!=subreddit]
    edges = pd.DataFrame({'subreddit':edgelist.subreddit.map(lambda x: node_ids_dict[x]),
                          'author':edgelist.author.map(lambda x: node_ids_dict[x]),
                          'weight':edgelist.weight})
    edges = edges[['subreddit','author','weight']]
    
    return edges

def project_unipartite_network(edgelist, subreddit, row='subreddit',col='author'):
    edges = get_edges(edgelist, subreddit)
    edges['value'] = 1
    row_ind = np.array(edges[row])
    col_ind = np.array(edges[col])
    data = np.array(edges['value'], dtype=float)
    mat_coo = sparse.coo_matrix((data, (row_ind, col_ind)))
    mat_coo.sum_duplicates()
    csr = mat_coo.tocsr()

    sub_net = csr.dot(csr.T).tolil()
    sub_net.setdiag(0)
    
    return sub_net
    
def get_network_density(sub_net):
    assert sub_net.shape[0]==sub_net.shape[1], 'matrix is not square'
    
    E = sub_net.getnnz() # number of observed edges
    n = sub_net.shape[0] # number of nodes
    P = (n*(n-1))*2 # number of possible unidirectional edges

    return E/P
    
def get_degrees(network, network_type):
    degrees = pd.DataFrame(np.count_nonzero(network.todense(), axis=1), columns=[f'{network_type}_degrees'])
    weighted_degrees = pd.DataFrame(network.sum(axis=1),columns=[f'{network_type}_weighted_degrees'])
    
    return degrees, weighted_degrees
    
def get_stats_df(data, subreddit):
    sub_net = project_unipartite_network(data, subreddit)
    subreddit_density = get_network_density(sub_net)
    
    author_net = project_unipartite_network(data, subreddit,row='author', col='subreddit')
    author_density = get_network_density(author_net)
 
    stats = {'sub_counts':data.subreddit.value_counts().describe(),
             'author_counts':data.author.value_counts().describe(),
             'bipartite_edge_weights':data.weight.describe(),
             'sub_net_density':subreddit_density,
             'author_net_density':author_density
            }

    stats_df = pd.DataFrame.from_dict(stats)
    stats_df.index.name = 'stat'
    stats_df['subreddit'] = subreddit
    return stats_df
    

""" DATA PROCESSING & STORAGE """
    
def getStatsDf(subreddit):
    data = fetchSubredditData(subreddit)
    data.columns = ['subreddit','author','weight']
    stats_df = get_stats_df(data, subreddit)
    stats_df.reset_index(drop=False, inplace=True)

    return stats_df

def get_engine(database_name='network_stats'):
    return create_engine('sqlite:///{}.db'.format(database_name), echo=False)

def saveSQL(df, table_name, database_name='network_stats', **kwargs):
    engine = get_engine(database_name=database_name)
    df.to_sql(name=table_name, con=engine,  **kwargs)
    
def loadSQL(table_name, index_col=None, database_name='network_stats'):
    engine = get_engine(database_name=database_name)
    df = pd.read_sql_table(table_name=table_name, con=engine, index_col=index_col)
    
    return df
    
def saveStatsDf(subreddit):
    stats_df = getStatsDf(subreddit)
    table_name='merged_stats_df'
    saveSQL(stats_df, table_name)
    print(f'done with {subreddit}!')
    
def load_stats_df():
    return loadSQL('merged_stats_df')
      
def getAuthorCounts(subreddit, data):
    authorCounts = data.subreddit.value_counts(normalize=True).sort_values(ascending=False)
    authorCounts.name = subreddit
    authorCounts = pd.DataFrame(authorCounts)
    authorCounts.index.name = 'index'
    
    return authorCounts
    
def getCommentCounts(subreddit, data):
    commentCounts = data.groupby('subreddit')['authorCommentCount'].sum()
    commentCounts = commentCounts/commentCounts.sum()
    commentCounts.name = subreddit
    commentCounts = pd.DataFrame(commentCounts)
    commentCounts.index.name = 'index'
    
    return commentCounts

def mergeTables(table_name, adding):
    existing = loadSQL(table_name, index_col='index')
    if existing.shape == (0,1):
        updated = adding
    else:
        updated = existing.merge(adding, left_index=True, right_index=True, how='outer')
    saveSQL(updated, table_name, if_exists='replace', index=True)
    
def saveSubredditWeights(subreddit):
    data = fetchSubredditData(subreddit)
    print("getting subreddit weights for {}".format(subreddit))
    authorCounts = getAuthorCounts(subreddit, data)
    commentCounts = getCommentCounts(subreddit, data)
    
    mergeTables('subredditAuthorCounts', authorCounts)
    mergeTables('subredditCommentCounts', commentCounts)
    
    

if __name__ == "__main__":
    sublist = fetchSubList()
    sampleSubs = sublist.subreddit.sample(2)
    n = 1
    for subreddit in sampleSubs:
        print(n)
        saveStatsDf(subreddit)
        n += 1
    
    upload_blob('network-analysis', 'network_stats.db')
    
            


    
    