{% extends "python.tpl" %}

{%- block header %}# coding: utf-8
{% endblock header %}

{% block markdowncell scoped %}
{{ cell.source | wrap_text(79 - '# '.__len__()) | comment_lines }}
{% endblock markdowncell %}
