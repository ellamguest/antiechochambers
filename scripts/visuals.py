from network_stats import *
from bokeh.plotting import figure, output_notebook, show, ColumnDataSource, Row, Column
from bokeh.models import HoverTool
import subprocess

output_notebook(hide_banner=True)

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

def scatterPlot(df, xaxis, yaxis, title, balance=False):
    source = ColumnDataSource(data=df)

    hover = HoverTool(tooltips=[
        ("subreddit", "@subreddit"),
        ("author density", "@authorNetDensity{1.111}"),
        ("subreddit density", "@subredditNetDensity{1.111}"),
        ("# authors", "@numAuthors{int}"),
        ("# subreddits", "@numSubreddits{int}"),
        ("# author-subreddit edges", "@numEdges{int}"),
        ],names=["scatter"])

    tools = [hover, "box_select", "reset", "wheel_zoom"]
    
    p = figure(plot_width=500, plot_height=500, tools= tools,
               title=title)

    p.circle(xaxis, yaxis, size=5, color='grey', alpha=0.3, source=source, name='scatter')

    main = df[df['subreddit'].isin(['The_Donald', 'changemyview'])].copy()
    main['color'] = ['blue','orange']
    main_source = ColumnDataSource(data=main)

    p.circle(xaxis, yaxis, size=10, color='color', line_color='black', source=main_source, name='scatter')

    if balance == True:
        balance = np.array([df[xaxis].max(), df[yaxis].max()]).min()
        p.line([0,balance],[0,balance], line_width=2, color='black', alpha=0.5)

    p.xaxis.axis_label = xaxis
    p.yaxis.axis_label = yaxis

    p.xaxis.minor_tick_line_color = None 
    p.yaxis.minor_tick_line_color = None 

    p.xgrid.visible = False
    p.ygrid.visible = False

    return p



def saveWithoutInputCells():
    """need to figure out %%writefile nbextensions.tpl"""
    subprocess.call("jupyter nbconvert --template=nbextensions --to=html README.ipynb")
    subprocess.call("pandoc -s -r html README.html -o README.md")
    
def saveMD():
    subprocess.call("jupyter nbconvert --to=markdown README.ipynb")