{%- extends 'full.tpl' -%}
## remove input cells
{% block input_group -%}
{% endblock input_group %}
## change the appearance of execution count
{% block in_prompt %}
# [{{ cell.execution_count if cell.execution_count else ' ' }}]:
{% endblock in_prompt %}