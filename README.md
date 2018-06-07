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
In \[1\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    %autoreload 2

    from network_stats import *
    from visuals import *
:::
:::
:::
:::

::: {.output_wrapper}
::: {.output}
::: {.output_area}
::: {.prompt}
:::

::: {#be1a1a57-0e9f-4b25-8513-5fba17342331}
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
In \[2\]:
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
Terminology[¶](#Terminology){.anchor-link} {#Terminology}
------------------------------------------

-   Community vs subreddit \-- To avoid confusion between the subreddit
    being studied, and the subreddits connected to it I will use the
    term \"community\" for the {{num\_subs}} subreddits that are being
    studied.

Ex. r/changemyview is the *community* under observation, and the network
of *subreddits* it is connected to has a density of x

-   Connected \-- Subreddits are connected is they share a tie or edge
    (in network terminology). For the purposes of this analysis
    subreddits are connected if the are commented in by the same author.
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

::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
Author vs Subreddit Networks[¶](#Author-vs-Subreddit-Networks){.anchor-link} {#Author-vs-Subreddit-Networks}
----------------------------------------------------------------------------

The comment data for each community is two-mode (or bipartite). Ties
only exist between two distinct subsets of nodes: authors and
subreddits. Authors and subreddits and directly connected in an author
comments in a subreddit.

From this data we can create two types of one-mode networks: they author
network and the subreddit network. In the author network redditors are
nodes, which are connected if they comment in the same subreddits. In
the subreddit network the nodes are subreddits, which are connected by
they are commented in by the same author.

There may appear to be little difference between these types of networks
but they provide different insights

### Research Questions[¶](#Research-Questions){.anchor-link} {#Research-Questions}

-   What does each of the one-mode networks tell us about the community?
-   What is the relationship between the one-mode networks
:::
:::
:::

::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
Size[¶](#Size){.anchor-link} {#Size}
----------------------------

First lets look at the relative size of each of the networks. **Figure
1** shows the *number of authors* versus the *number of subreddits* for
each community. Logically, there is a positive relationship between the
counts. The diagonal line is an identity line, showing where the number
of subreddits and authors is equal. This helps to show that the main
cluster of communities in the bottom left corner there is a higer ratio
of subreddits to authors. However, for the larger communities in the top
and right of the figure, the number of authors start to increase faster
than the number of subreddits.

### Interpretation[¶](#Interpretation){.anchor-link} {#Interpretation}

As the number of subreddits connected to a community is dependent on the
number of authors within it, we expect the number of subreddits to
increase with number of subreddits. I present two hypotheses for why the
rate of increase slows over time:

-   **Hypothesis 1**: There is a maximum threshold on the number of
    active subreddits per month, thus limiting how many subreddits any
    community could potentially be connected to \-- To test this
    hypothesis I will look in the overlap of subreddits between
    communities to see if there is a saturation point at which all or
    most of the active subreddits in a month are included in every
    community\'s subreddit networks \-- *To compare networks I will then
    have to rank the relative weight of ties for each subreddit to
    compare across communities*
-   **Hypothesis 2**: Communities with larger numbers of authors will
    have higher rates of \'casual\' redditors - people who participate
    in fewer subreddits or over a shorter period. Casual authors will
    add fewer new subreddits to the network. \-- To test this hypothesis
    I\'ll look at the distribution of number of subreddits and comments
    per author (SMS analysis done)
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[3\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    show(scatterPlot(df, "numAuthors", "numSubreddits", "Figure 1", balance=True))
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
::: {#bad26fb9-50b3-4303-910f-92b88865cd9d .bk-plotdiv}
:::
:::
:::
:::

::: {.output_area}
::: {.prompt}
:::

::: {#86a5f840-9f10-4eb0-b213-a8717014e466}
:::

::: {.output_subarea .output_javascript}
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
Subreddit Ranks[¶](#Subreddit-Ranks){.anchor-link} {#Subreddit-Ranks}
--------------------------------------------------

Did compare the relative weights of subreddits between communities we
take all of the comments authors of a community made across subreddits,
and normalize the number of comments per subreddit by the total number
of comments for each community. *needs clarification*
:::
:::
:::

::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
**work in progress**
:::
:::
:::

::: {.cell .border-box-sizing .text_cell .rendered}
::: {.prompt .input_prompt}
:::

::: {.inner_cell}
::: {.text_cell_render .border-box-sizing .rendered_html}
Network Analysis[¶](#Network-Analysis){.anchor-link} {#Network-Analysis}
====================================================

Network Density[¶](#Network-Density){.anchor-link} {#Network-Density}
--------------------------------------------------

One of the simplest network measures of density. Density expresses what
portion of all possible ties are actually present in the network. The
number of possible ties is determined by the number of nodes. In an
undirected network density is calculated as:

\$\\frac{E}{(n\*(n-1))}\$

Where E = the observed number of edges, and n = the number of nodes.
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[6\]:
:::

::: {.inner_cell}
::: {.input_area}
::: {.highlight .hl-ipython3}
    densityPlot = scatterPlot(df, "authorNetDensity", "subredditNetDensity", "Figure 1")

    show(Row(densityPlot))
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
::: {#52d6739f-b4ba-4279-a77a-51401c84d933 .bk-plotdiv}
:::
:::
:::
:::

::: {.output_area}
::: {.prompt}
:::

::: {#f3452cd9-b797-4aca-b930-22f802b520bf}
:::

::: {.output_subarea .output_javascript}
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
**Figure 2** shows that there is a negative relationship between
*subreddit network density* and *author networks density* for many
communites. The majority of communities have low densities for both
network types
:::
:::
:::

::: {.cell .border-box-sizing .code_cell .rendered}
::: {.input}
::: {.prompt .input_prompt}
In \[7\]:
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
::: {#e192b2bb-2392-44ea-960d-ef527fb452a3 .bk-plotdiv}
:::
:::
:::
:::

::: {.output_area}
::: {.prompt}
:::

::: {#ba5f3e42-4e0c-4cd5-aa85-53c7f5bc5521}
:::

::: {.output_subarea .output_javascript}
:::
:::
:::
:::
:::
:::
:::
