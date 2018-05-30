from google.cloud import bigquery
import pandas as pd
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
from sqlalchemy import create_engine
import google.auth
from google.cloud import storage
import time
import scipy as sp
import pickle
import inspect
from pathlib import Path
from functools import wraps

CACHE = Path('./cache')


def client():

    credsfile = 'antiechochambers-1ba7f7f4c68e.json'
    return bigquery.Client.from_service_account_json(credsfile)

def jobConfig():
    config = bigquery.QueryJobConfig()
    config.query_parameters = (bigquery.ScalarQueryParameter('size', 'INT64', 10),)
    config.use_legacy_sql = False
    config.maximum_bytes_billed = int(5e9)

    return config

def fetchQuery(query):
    j = client().query(query=query, job_config=jobConfig())
    df = j.to_dataframe()

    return df

def fetchSubList():
    query = """SELECT*
                 FROM `aerobic-datum126519.sms_18_sample_subreddits.randomSubreddits`
                 """

    data = fetchQuery(query)

    return data

def cache(pattern):
    
    def wrapper(f):
        sig = inspect.signature(f)
        
        @wraps(f)
        def wrapped(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            path = CACHE / pattern.format(**bound.arguments)
            
            if path.exists():
                return pickle.loads(path.read_bytes())
            
            result = f(*args, **kwargs)
            
            path.parent.mkdir(exist_ok=True, parents=True)
            path.write_bytes(pickle.dumps(result))
            
            return result
        return wrapped
    return wrapper

@cache('{subreddit}')
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

def checkCompleted(database_name):
    conn = get_engine(database_name)
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    completed = []
    for name in res:
        completed.append(name[0])
    
    return completed

def getBipartiteNetwork(df):
    B = nx.Graph()
    B.add_nodes_from(df.subreddit.unique(), bipartite=0)
    B.add_nodes_from(df.author.unique(), bipartite=1)
    B.add_weighted_edges_from(
            list(df.itertuples(index=False, name=None)))
            
    return B

def add_edges_fast(names, adj):
    G = nx.Graph()
    G._node = {n: {} for n in names}
    G._adj = {n: {} for n in names}
    coo =  adj.tocoo()
    for u, v, w in zip(coo.row, coo.col, coo.data):
        if u != v:
            G._adj[names[u]][names[v]] = {'weight': w}
    
    return G

def projection_fast(df):
    top = df.subreddit.values
    bot = df.author.values
    
    top_unique, top_indices = sp.unique(top, return_inverse=True)
    bot_unique, bot_indices = sp.unique(bot, return_inverse=True)
    
    data = sp.ones(len(top))
    incidence = sp.sparse.coo_matrix((data, (top_indices, bot_indices)))
    adj = incidence.dot(incidence.T)
    
    G = add_edges_fast(top_unique, adj)
    node_stats = pd.DataFrame(
    {
    'degree':dict(nx.degree(G)),
    'degree_centrality':nx.degree_centrality(G),
    'core_number':nx.core_number(G)
    })
    
    return node_stats

def projection_slow(df):
    B = getBipartiteNetwork(df)
    G = bipartite.weighted_projected_graph(B, df.subreddit.unique())
    node_stats = pd.DataFrame(
        {
        'degree':dict(nx.degree(G)),
        'degree_centrality':nx.degree_centrality(G),
        'core_number':nx.core_number(G)
        })
    return node_stats

def runStats(subreddit):
    start_time = time.time()
    database_name = 'subNetstats'
    df = fetchSubredditData(subreddit)
    df = df[df['subreddit']!=subreddit]
    node_stats = projection_fast(df)
    saveSQL(node_stats, subreddit, database_name=database_name, if_exists='replace')
    
    elapsed_time = time.time() - start_time
    print('that took', elapsed_time)
   


""" LOCAL STORAGE """
def get_engine(database_name):
    return create_engine('sqlite:///{}.db'.format(database_name), echo=False)

def saveSQL(df, table_name, database_name, **kwargs):
    engine = get_engine(database_name=database_name)
    df.to_sql(name=table_name, con=engine,  **kwargs)
    
def loadSQL(table_name, database_name, index_col='index'):
    engine = get_engine(database_name=database_name)
    df = pd.read_sql_table(table_name=table_name, con=engine, index_col=index_col)
    
    return df



""" GOOGLE STORAGE FUNCTIONS """

def get_storage_client():
    credentials, project = google.auth.default() # why returning empty project name?
    project = 'aerobic-datum-126519'
    return storage.Client(project=project,
                             credentials=credentials)
    
def upload_blob(bucket_name, file_name):
    """Uploads a file to the bucket."""
    storage_client = get_storage_client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(file_name)

    print(f'File {file_name} uploaded.')   
    

if __name__ == "__main__":
    subreddits = fetchSubList()
    sample = subreddits['subreddit'].head(2)
    
    database_name = 'subNetstats'
    completed = checkCompleted(database_name)
    n = 1
    for subreddit in sample:
        if subreddit not in completed:
            print(n, subreddit.upper())
            runStats(subreddit)
        else:
            print(n, subreddit.upper(), 'already done')
        n+=1
    
    upload_blob('network-analysis', 'subNetstats.db')