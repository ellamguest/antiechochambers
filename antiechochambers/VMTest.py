from google.cloud import bigquery
import pandas as pd
from pathlib import Path
import numpy as np
import networkx as nx
from networkx.algorithms import bipartite

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
    query = """SELECT *
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

def getBipartiteNetwork(df):
    B = nx.Graph()
    B.add_nodes_from(df.subreddit.unique(), bipartite=0)
    B.add_nodes_from(df.author.unique(), bipartite=1)
    B.add_weighted_edges_from(
            list(df.itertuples(index=False, name=None)))
            
    return B

def getNodeStats(G):
    degree = nx.degree(G)
    degree_centrality = nx.degree_centrality(G)