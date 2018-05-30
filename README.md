
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1">Introduction</a></span></li><li><span><a href="#Descriptive-Analysis" data-toc-modified-id="Descriptive-Analysis-2">Descriptive Analysis</a></span></li></ul></div>

# Introduction

Blah blah. This is what I'm talking about. Blah Blah.


```python
%autoreload 2

from network_stats import *
from visuals import *
```




```python
df = getDensityDf()
num_subs = df.subreddit.unique().shape[0]
```

## Terminology

- Community vs subreddit
-- To avoid confusion between the subreddit being studied, and the subreddits connected to it I will use the term "community" for the {{num_subs}} subreddits that are being studied.

Ex. r/changemyview is the *community* under observation, and the network of *subreddits* it is connected to has a density of x

- Connected
-- Subreddits are connected is they share a tie or edge (in network terminology). For the purposes of this analysis subreddits are connected if the are commented in by the same author. 

This analysis looks at {{num_subs}} subreddits: r/The_Donald, r/changemyview, and {{num_subs-2}} random baseline communities.

**Warning: Some of the sampled subreddits as NSFW. Please keep this in mind when looking at names**

# Descriptive Analysis

## Author vs Subreddit Networks

The comment data for each community is two-mode (or bipartite). Ties only exist between two distinct subsets of nodes: authors and subreddits. Authors and subreddits and directly connected in an author comments in a subreddit.

From this data we can create two types of one-mode networks: they author network and the subreddit network. In the author network redditors are nodes, which are connected if they comment in the same subreddits. In the subreddit network the nodes are subreddits, which are connected by they are commented in by the same author.

There may appear to be little difference between these types of networks but they provide different insights

### Research Questions

- What does each of the one-mode networks tell us about the community?
- What is the relationship between the one-mode networks

## Size

First lets look at the relative size of each of the networks. **Figure 1** shows the *number of authors* versus the *number of subreddits* for each community. Logically, there is a positive relationship between the counts. The diagonal line is an identity line, showing where the number of subreddits and authors is equal. This helps to show that the main cluster of communities in the bottom left corner there is a higer ratio of subreddits to authors. However, for the larger communities in the top and right of the figure, the number of authors start to increase faster than the number of subreddits.

### Interpretation

As the number of subreddits connected to a community is dependent on the number of authors within it, we expect the number of subreddits to increase with number of subreddits. I present two hypotheses for why the rate of increase slows over time:


- **Hypothesis 1**: There is a maximum threshold on the number of active subreddits per month, thus limiting how many subreddits any community could potentially be connected to
-- To test this hypothesis I will look in the overlap of subreddits between communities to see if there is a saturation point at which all or most of the active subreddits in a month are included in every community's subreddit networks
-- *To compare networks I will then have to rank the relative weight of ties for each subreddit to compare across communities*
- **Hypothesis 2**: Communities with larger numbers of authors will have higher rates of 'casual' redditors - people who participate in fewer subreddits or over a shorter period. Casual authors will add fewer new subreddits to the network.
-- To test this hypothesis I'll look at the distribution of number of subreddits and comments per author (SMS analysis done)


```python
show(scatterPlot(df, "numAuthors", "numSubreddits", "Figure 1", balance=True))
```



<div class="bk-root">
    <div class="bk-plotdiv" id="bad26fb9-50b3-4303-910f-92b88865cd9d"></div>
</div>




## Subreddit Ranks

Did compare the relative weights of subreddits between communities we take all of the comments authors of a community made across subreddits, and normalize the number of comments per subreddit by the total number of comments for each community. *needs clarification*

**work in progress**

# Network Analysis
## Network Density

One of the simplest network measures of density. Density expresses what portion of all possible ties are actually present in the network. The number of possible ties is determined by the number of nodes. In an undirected network density is calculated as:

$\frac{E}{(n*(n-1))}$

Where E = the observed number of edges, and n = the number of nodes.


```python
densityPlot = scatterPlot(df, "authorNetDensity", "subredditNetDensity", "Figure 1")

show(Row(densityPlot))
```



<div class="bk-root">
    <div class="bk-plotdiv" id="52d6739f-b4ba-4279-a77a-51401c84d933"></div>
</div>




**Figure 2** shows that there is a negative relationship between *subreddit network density* and *author networks density* for many communites. The majority of communities have low densities for both network types


```python
authorEdgePlot = scatterPlot(df, "numEdges", "authorNetDensity", None)
subredditEdgePlot = scatterPlot(df, "numEdges", "subredditNetDensity", None)

show(Row(authorEdgePlot, subredditEdgePlot))
```



<div class="bk-root">
    <div class="bk-plotdiv" id="e192b2bb-2392-44ea-960d-ef527fb452a3"></div>
</div>





```python
saveMD()
```


    ------------------------------------------------------------------------

    FileNotFoundError                      Traceback (most recent call last)

    <ipython-input-9-c40f4ad93c91> in <module>()
    ----> 1 saveMD()
    

    ~/Programming/GitHub/antiechochambers/visuals.py in saveMD()
         76 
         77 def saveMD():
    ---> 78     subprocess.call("jupyter nbconvert --to=markdown README.ipynb")
    

    //anaconda/envs/python3.6/lib/python3.6/subprocess.py in call(timeout, *popenargs, **kwargs)
        265     retcode = call(["ls", "-l"])
        266     """
    --> 267     with Popen(*popenargs, **kwargs) as p:
        268         try:
        269             return p.wait(timeout=timeout)


    //anaconda/envs/python3.6/lib/python3.6/subprocess.py in __init__(self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, encoding, errors)
        707                                 c2pread, c2pwrite,
        708                                 errread, errwrite,
    --> 709                                 restore_signals, start_new_session)
        710         except:
        711             # Cleanup if the child failed starting.


    //anaconda/envs/python3.6/lib/python3.6/subprocess.py in _execute_child(self, args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, restore_signals, start_new_session)
       1342                         if errno_num == errno.ENOENT:
       1343                             err_msg += ': ' + repr(err_filename)
    -> 1344                     raise child_exception_type(errno_num, err_msg, err_filename)
       1345                 raise child_exception_type(err_msg)
       1346 


    FileNotFoundError: [Errno 2] No such file or directory: 'jupyter nbconvert --to=markdown README.ipynb': 'jupyter nbconvert --to=markdown README.ipynb'

