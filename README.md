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

::: {#6f896698-cfa9-4826-b1c4-a7bff6cec5fe}
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

::: {#886b6e37-2712-4656-ae00-d0b85ce98c48}
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

::: {#9f3533c8-6ea6-48d5-bb59-6214211900da}
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
In \[129\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    ! jupyter nbconvert --to markdown README.ipynb
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
    [NbConvertApp] Converting notebook README.ipynb to markdown
    //anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/filters/datatypefilter.py:41: UserWarning: Your element with mimetype(s) dict_keys(['application/javascript', 'application/vnd.bokehjs_load.v0+json']) is not able to be represented.
      mimetypes=output.keys())
    //anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/filters/datatypefilter.py:41: UserWarning: Your element with mimetype(s) dict_keys(['application/javascript', 'application/vnd.bokehjs_exec.v0+json']) is not able to be represented.
      mimetypes=output.keys())
    [NbConvertApp] Writing 6695 bytes to README.md
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[130\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    ! conda install pandoc -y
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
    Fetching package metadata .............
    Solving package specifications: .

    Package plan for installation in environment //anaconda/envs/python3.6:

    The following packages will be UPDATED:

        pandoc: 1.19.2.1-ha5e8f32_1 --> 2.2.1-hde52d81_0 conda-forge

    pandoc-2.2.1-h 100% |################################| Time: 0:00:02   5.03 MB/s       | ETA:  0:00:01   3.97 MB/s
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[131\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    ! jupyter nbconvert --template=nbextensions --to=html README.ipynb
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
    Traceback (most recent call last):
      File "//anaconda/envs/python3.6/bin/jupyter-nbconvert", line 11, in <module>
        load_entry_point('nbconvert==5.3.1', 'console_scripts', 'jupyter-nbconvert')()
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/jupyter_core/application.py", line 267, in launch_instance
        return super(JupyterApp, cls).launch_instance(argv=argv, **kwargs)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/traitlets/config/application.py", line 658, in launch_instance
        app.start()
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/nbconvertapp.py", line 325, in start
        self.convert_notebooks()
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/nbconvertapp.py", line 493, in convert_notebooks
        self.convert_single_notebook(notebook_filename)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/nbconvertapp.py", line 464, in convert_single_notebook
        output, resources = self.export_single_notebook(notebook_filename, resources, input_buffer=input_buffer)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/nbconvertapp.py", line 393, in export_single_notebook
        output, resources = self.exporter.from_filename(notebook_filename, resources=resources)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/exporter.py", line 174, in from_filename
        return self.from_file(f, resources=resources, **kw)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/exporter.py", line 192, in from_file
        return self.from_notebook_node(nbformat.read(file_stream, as_version=4), resources=resources, **kw)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/html.py", line 85, in from_notebook_node
        return super(HTMLExporter, self).from_notebook_node(nb, resources, **kw)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/templateexporter.py", line 295, in from_notebook_node
        output = self.template.render(nb=nb_copy, resources=resources)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/templateexporter.py", line 111, in template
        self._template_cached = self._load_template()
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/nbconvert/exporters/templateexporter.py", line 266, in _load_template
        return self.environment.get_template(template_file)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/jinja2/environment.py", line 830, in get_template
        return self._load_template(name, self.make_globals(globals))
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/jinja2/environment.py", line 804, in _load_template
        template = self.loader.load(self, name, globals)
      File "//anaconda/envs/python3.6/lib/python3.6/site-packages/jinja2/loaders.py", line 408, in load
        raise TemplateNotFound(name)
    jinja2.exceptions.TemplateNotFound: nbextensions
:::
:::
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[ \]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    ! pandoc -s -r html README.html -o README.md
:::
:::
:::
:::
:::
:::
:::
