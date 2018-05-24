
<h1>Table of Contents<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Introduction" data-toc-modified-id="Introduction-1">Introduction</a></span></li><li><span><a href="#Descriptive-Analysis" data-toc-modified-id="Descriptive-Analysis-2">Descriptive Analysis</a></span></li></ul></div>

# Introduction

Blah blah. This is what I'm talking about. Blah Blah.


```python
%autoreload 2

from network_stats import *
import seaborn as sns
from bokeh.plotting import figure, output_notebook, show, ColumnDataSource, Row, Column
from bokeh.models import HoverTool

output_notebook(hide_banner=True)
```




```python
def getDensityDf():
    df = load_stats_df()
    density = (df[df['stat']=='count']
               .set_index('subreddit')
               .rename(columns=
                       {'author_net_density':'author',
                           'sub_net_density':'sub',
                       'bipartite_edge_weights':'edge_count'}))

    density['count_ratio'] = density['author_counts']/density['sub_counts']
    density['density_ratio'] = density['author']/density['sub']
    density = density.reset_index(drop=False)

    density = density.rename(columns={'author':'authorNetDensity',
                           'sub':'subredditNetDensity',
                           'author_counts':'numAuthors',
                           'sub_counts':'numSubreddits',
                           'edge_count': 'numEdges'})
    
    return density



def scatterPlot(df, xaxis, yaxis, title):
    source = ColumnDataSource(data=df)

    hover = HoverTool(tooltips=[
        ("subreddit", "@subreddit"),
        ("author density", "@authorNetDensity{1.111}"),
        ("subreddit density", "@subredditNetDensity{1.111}"),
        ("# authors", "@numAuthors{int}"),
        ("# subreddits", "@numSubreddits{int}"),
        ("# author-subreddit edges", "@numEdges{int}"),
    ])

    tools = [hover, "box_select", "reset", "wheel_zoom"]
    
    p = figure(plot_width=500, plot_height=500, tools= tools,
               title=title)

    p.circle(xaxis, yaxis, size=5, color='grey', alpha=0.3, source=source)

    main = df[df['subreddit'].isin(['The_Donald', 'changemyview'])].copy()
    main['color'] = ['blue','orange']
    main_source = ColumnDataSource(data=main)

    p.circle(xaxis, yaxis, size=10, color='color', line_color='black', source=main_source)

    p.xaxis.axis_label = xaxis
    p.yaxis.axis_label = yaxis

    p.xaxis.minor_tick_line_color = None 
    p.yaxis.minor_tick_line_color = None 

    p.xgrid.visible = False
    p.ygrid.visible = False

    return p
```


```python
df = getDensityDf()
num_subs = df.subreddit.unique().shape[0]
```

This analysis looks at 767 subreddits: r/The_Donald, r/changemyview, and 765 random baseline communities.

**Warning: Some of the sampled subreddits as NSFW. Please keep this in mind when looking at names**

# Descriptive Analysis


```python
densityPlot = scatterPlot(df, "authorNetDensity", "subredditNetDensity", "Comparison of One-Mode Network Densities")
countPlot = scatterPlot(df, "numAuthors", "numSubreddits", "Comparison of Node Counts by Type")

show(Row(densityPlot, countPlot))
```



<div class="bk-root">
    <div class="bk-plotdiv" id="3aa5cf8d-e13f-45e2-8ccd-e0cf950ed5a8"></div>
</div>





```python
authorEdgePlot = scatterPlot(df, "numEdges", "authorNetDensity", None)
subredditEdgePlot = scatterPlot(df, "numEdges", "subredditNetDensity", None)

show(Row(authorEdgePlot, subredditEdgePlot))
```



<div class="bk-root">
    <div class="bk-plotdiv" id="c24f8f84-df04-43c4-9d03-7898659a8c95"></div>
</div>





```python
! jupyter nbconvert --to markdown README.ipynb
```

    Traceback (most recent call last):
      File "//anaconda/envs/python3.6/bin/jupyter-nbconvert", line 11, in <module>
        load_entry_point('nbconvert==5.3.1', 'console_scripts', 'jupyter-nbconvert')()
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/jupyter_core/application.py", line 267, in launch_instance
        return super(JupyterApp, cls).launch_instance(argv=argv, **kwargs)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/traitlets/config/application.py", line 658, in launch_instance
        app.start()
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/nbconvertapp.py", line 325, in start
        self.convert_notebooks()
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/nbconvertapp.py", line 483, in convert_notebooks
        self.exporter = cls(config=self.config)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/templateexporter.py", line 243, in __init__
        super(TemplateExporter, self).__init__(config=config, **kw)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/exporter.py", line 105, in __init__
        self._init_preprocessors()
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/exporter.py", line 259, in _init_preprocessors
        self.register_preprocessor(preprocessor, enabled=True)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/exporter.py", line 220, in register_preprocessor
        preprocessor_cls = import_item(preprocessor)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/traitlets/utils/importstring.py", line 34, in import_item
        module = __import__(package, fromlist=[obj])
    ModuleNotFoundError: No module named 'pre_pymarkdown'



```python
! which python
```

    //anaconda/envs/python3.6/bin/python

