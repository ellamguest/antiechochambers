---
title: README
---

::: {#notebook .border-box-sizing tabindex="-1"}
::: {#notebook-container .container}
::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
Table of Contents[]{.tocSkip}
=============================

::: {.toc}
-   [Introduction](#Introduction)
-   [Descriptive Analysis](#Descriptive-Analysis)
:::
:::
:::
:::

::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
Introduction[¶](#Introduction){.anchor-link} {#Introduction}
============================================
:::
:::
:::

::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
Blah blah. This is what I\'m talking about. Blah Blah.
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[105\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    %autoreload 2

    from network_stats import *
    import seaborn as sns
    from bokeh.plotting import figure, output_notebook, show, ColumnDataSource, Row, Column
    from bokeh.models import HoverTool

    output_notebook(hide_banner=True)
:::
:::
:::
:::

::: {.output_wrapper}
::: {.output}
::: {.output_area}
::: {.prompt}
:::

::: {#7f68a7bf-3ad6-42a7-a130-9f77cc6a7940}
:::

::: {.output_subarea .output_javascript}
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[117\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
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
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[103\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    df = getDensityDf()
    num_subs = df.subreddit.unique().shape[0]
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
This analysis looks at {{num\_subs}} subreddits: r/The\_Donald,
r/changemyview, and {{num\_subs-2}} random baseline communities.

**Warning: Some of the sampled subreddits as NSFW. Please keep this in
mind when looking at names**
:::
:::
:::

::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
Descriptive Analysis[¶](#Descriptive-Analysis){.anchor-link} {#Descriptive-Analysis}
============================================================
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[118\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    densityPlot = scatterPlot(df, "authorNetDensity", "subredditNetDensity", "Comparison of One-Mode Network Densities")
    countPlot = scatterPlot(df, "numAuthors", "numSubreddits", "Comparison of Node Counts by Type")

    show(Row(densityPlot, countPlot))
:::
:::
:::
:::

::: {.output_wrapper}
::: {.output}
::: {.output_area}
::: {.prompt}
:::

::: {.output_html .rendered_html .output_subarea}
::: {.bk-root}
::: {#3aa5cf8d-e13f-45e2-8ccd-e0cf950ed5a8 .bk-plotdiv}
:::
:::
:::
:::

::: {.output_area}
::: {.prompt}
:::

::: {#aed8abbd-39ad-477c-bcd1-6916992bb92a}
:::

::: {.output_subarea .output_javascript}
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[124\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    authorEdgePlot = scatterPlot(df, "numEdges", "authorNetDensity", None)
    subredditEdgePlot = scatterPlot(df, "numEdges", "subredditNetDensity", None)

    show(Row(authorEdgePlot, subredditEdgePlot))
:::
:::
:::
:::

::: {.output_wrapper}
::: {.output}
::: {.output_area}
::: {.prompt}
:::

::: {.output_html .rendered_html .output_subarea}
::: {.bk-root}
::: {#c24f8f84-df04-43c4-9d03-7898659a8c95 .bk-plotdiv}
:::
:::
:::
:::

::: {.output_area}
::: {.prompt}
:::

::: {#e7076808-322a-4751-a214-6c73d7a0914f}
:::

::: {.output_subarea .output_javascript}
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[140\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    %%writefile nbextensions.tpl
    {%- extends 'full.tpl' -%}
    ## remove input cells
    {% block input_group -%}
    {% endblock input_group %}
    ## change the appearance of execution count
    {% block in_prompt %}
    # [{{ cell.execution_count if cell.execution_count else ' ' }}]:
    {% endblock in_prompt %}

    {% block output_group -%}
    {%- if cell.metadata.hide_output -%}
    {%- else -%}
        {{ super() }}
    {%- endif -%}
    {% endblock output_group %}
:::
:::
:::
:::

::: {.output_wrapper}
::: {.output}
::: {.output_area}
::: {.prompt}
:::

::: {.output_subarea .output_stream .output_stdout .output_text}
    Overwriting nbextensions.tpl
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[141\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    ! jupyter nbconvert --template=nbextensions --to=html README.ipynb
    ! pandoc -s -r html README.html -o README.md
:::
:::
:::
:::

::: {.output_wrapper}
::: {.output}
::: {.output_area}
::: {.prompt}
:::

::: {.output_subarea .output_stream .output_stdout .output_text}
    [NbConvertApp] Converting notebook README.ipynb to html
    [NbConvertApp] Writing 613864 bytes to README.html
:::
:::
:::
:::
:::
:::
:::
