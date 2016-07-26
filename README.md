
# WhateverForever

> Build simple, powerful jigs for your Jupyter notebook.

## Install
From the command line (or with `!` in a notebook cell):
```bash
pip install whatever4e
```

## Enable
### Ad-hoc
In the notebook, you can use the `%load_ext` or `%reload_ext` line magic.


```python
from whatever4e import Chain, Whatever
```

## Create
The missing `%%markdown` magic.


```python
from jinja2 import Template
from pandas.util.testing import makeTimeDataFrame
df = makeTimeDataFrame()
@Whatever.cell('markdown', lang='markdown')
def render_template_globals(cell):
    return Template(cell).render(**globals())
```

    /Users/tfast/anaconda/lib/python3.5/site-packages/pytz/__init__.py:29: UserWarning: Module toolz was already imported from /Users/tfast/anaconda/lib/python3.5/site-packages/toolz/__init__.py, but /Users/tfast/w4e is being added to sys.path
      from pkg_resources import resource_stream



    <IPython.core.display.Javascript object>



```python
%%markdown
# This is markdown

It has syntax highlighting because `lang` is defined.

{{df.head(2).to_html()}}
```


# This is markdown

It has syntax highlighting because `lang` is defined.

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
      <th>D</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2000-01-03</th>
      <td>-1.659650</td>
      <td>-0.370966</td>
      <td>0.026096</td>
      <td>2.450970</td>
    </tr>
    <tr>
      <th>2000-01-04</th>
      <td>-1.754256</td>
      <td>0.846297</td>
      <td>0.196810</td>
      <td>0.231307</td>
    </tr>
  </tbody>
</table>


Or will update a named variable with the parsed document:


```python
from pyjade import process
Whatever.cell('jade', process, lang='jade', display='HTML')
```


    <IPython.core.display.Javascript object>





    <whatever4e.Whatever at 0x11593c588>




```python
%%jade spock
span.badge 10
```


<span class="badge">10</span>



```python
spock
```




    '<span class="badge">10</span>'



## Contribute
[Issues](https://github.com/bollwyvl/jademagic/issues) and [pull requests](https://github.com/bollwyvl/jademagic/pulls) welcome!

## License
`whatever4e` is released as free software under the [BSD 3-Clause license](./LICENSE).

## Thank
- [@lbustelo](http://github.com/lbustelo) for challenging me to an alternative to `%%html`
