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

cache_file = lambda filename: Path().resolve().joinpath(*['cache', filename])

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
    print('Submitting query')
    j = client().query(query=query, job_config=jobConfig())
    with tqdm() as pbar:
        while True:
            try:
                j.result(timeout=1)
            except TimeoutError:                
                pbar.update(1)
            else:
                break
    return j

def fetchQuery(query):
    j = run_job(query)
    df = j.to_dataframe()
    
    return df

def fetchSubredditData(subreddit):
    """should create bot table to call on"""
    query = f"""SELECT subreddit, author, COUNT(created_utc) as weight
                FROM `fh-bigquery.reddit_comments.2017_06`
                WHERE author in (SELECT author
                                 FROM `aerobic-datum-126519.sms_18_sample_subreddits.mainSubInCounts`
                                 WHERE (subreddit = '{subreddit}') AND (authorInCount > 2) AND
                                         author not in (SELECT author
                                                         FROM `fh-bigquery.reddit_comments.bots_201505`)
                                        AND (lower(author) NOT LIKE '%bot%')
                                        AND (author NOT LIKE 'JlmmyButler')
                                        AND (author NOT LIKE 'TotesMessenger'))
                GROUP BY subreddit, author
                HAVING weight > 2"""

    data = fetchQuery(query)
    
    return data
    
def get_node_ids_dict(edgelist):
    node_ids = list(edgelist.subreddit.unique()) + list(edgelist.author.unique())
    return dict(zip(node_ids, range(len(node_ids))))

def get_edges(edgelist, subreddit):
    node_ids_dict = get_node_ids_dict(edgelist)
    #start = time.time()
    edgelist = edgelist[edgelist['subreddit']!=subreddit]
    edges = pd.DataFrame({'subreddit':edgelist.subreddit.map(lambda x: node_ids_dict[x]),
                          'author':edgelist.author.map(lambda x: node_ids_dict[x]),
                          'weight':edgelist.weight})
    edges = edges[['subreddit','author','weight']]
    #end = time.time()

    #elapsed = end-start
    #print(f'that took {elapsed} seconds')
    
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
    #csr.sum_duplicates()

    sub_net = csr.dot(csr.T).tolil()
    sub_net.setdiag(0)
    
    return sub_net
    
def get_network_density(sub_net):
    assert sub_net.shape[0]==sub_net.shape[1], 'matrix is not square'

    N = sub_net.shape[0]
    E = sub_net.getnnz()

    return (E-N+1)/(N*(N-3)+2)
    
def get_degrees(network, network_type):
    degrees = pd.DataFrame(np.count_nonzero(network.todense(), axis=1), columns=[f'{network_type}_degrees'])
    weighted_degrees = pd.DataFrame(network.sum(axis=1),columns=[f'{network_type}_weighted_degrees'])
    
    return degrees, weighted_degrees
    
def get_stats_df(data, subreddit):
    #print('getting subreddit network...')
    sub_net = project_unipartite_network(data, subreddit)
    subreddit_density = get_network_density(sub_net)
    #subreddit_degrees, subreddit_weighted_degrees = get_degrees(sub_net, 'subreddit')
    
    #print('getting author network...')
    author_net = project_unipartite_network(data, subreddit,row='author', col='subreddit')
    author_density = get_network_density(author_net)
    #author_degrees, author_weighted_degrees = get_degrees(author_net, 'author')

    print('compiling stats...')
    stats = {'sub_counts':data.subreddit.value_counts().describe(),
             'author_counts':data.author.value_counts().describe(),
             'bipartite_edge_weights':data.weight.describe(),
             'sub_net_density':subreddit_density,
             #'subreddit_degrees':subreddit_degrees['subreddit_degrees'].describe(),
             #'subreddit_weighted_degrees':subreddit_weighted_degrees['subreddit_weighted_degrees'].describe(),
             'author_net_density':author_density,
             #'author_degrees':author_degrees['author_degrees'].describe(),
             #'author_weighted_degrees':author_weighted_degrees['author_weighted_degrees'].describe()
            }

    stats_df = pd.DataFrame.from_dict(stats)
    stats_df.index.name = 'stat'
    stats_df['subreddit'] = subreddit
    return stats_df
    
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
                                 FROM `aerobic-datum-126519.sms_18_sample_subreddits.randomSubredditAuthors`
                                 WHERE (subreddit = '{subreddit}') AND (authorInCOunt > 2) AND
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
     
def saveStatsDfs(subreddit):
    data = fetchSubredditData(subreddit)
    data.columns = ['subreddit','author','weight']
    stats_df = get_stats_df(data, subreddit)
    stats_df.to_csv(cache_file(f'{subreddit}_stats_df.csv'))
    print(f'done with {subreddit}!')

sublist = fetchSubList()

path = str(cache_file('*_stats_df.csv'))
files = glob.glob(path)
completed = [file.replace(str(cache_file('')), '').replace('_stats_df.csv', '').lstrip('/') for file in files]

sampleSubs = sublist.subreddit.sample(10)
for subreddit in sampleSubs:
    if subreddit not in completed:
        print(subreddit)
        saveStatsDfs(subreddit)


    
    