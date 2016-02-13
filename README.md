
# jademagic
> an [IPython](http://ipython.org/) [magic](https://ipython.org/ipython-doc/dev/interactive/tutorial.html) for authoring HTML in [Jade ne Pug](https://github.com/pugjs).

## Install
From the command line (or with `!` in a notebook cell):
```bash
pip install jademagic
```

## Enable
### Ad-hoc
In the notebook, you can use the `%load_ext` or `%reload_ext` line magic.


```python
%reload_ext jademagic
```

### Configuration
In your profile's `ipython_kernel_config.py`, you can add the following line to automatically load `jademagic` into all your running kernels:

```python
c.InteractiveShellApp.extensions = ['jade_magic']
```

## Use
The `%%jade` cell magic will either act as simple parser:


```python
%%jade
ul
    each x in [1, 2, 3, 4, 5]
        li: i.fa.fa-gift(class='fa-#{x}x')
```


    <IPython.core.display.Javascript object>






<ul>
  <li><i class="fa fa-gift fa-1x"></i>
  </li>
  <li><i class="fa fa-gift fa-2x"></i>
  </li>
  <li><i class="fa fa-gift fa-3x"></i>
  </li>
  <li><i class="fa fa-gift fa-4x"></i>
  </li>
  <li><i class="fa fa-gift fa-5x"></i>
  </li>
</ul>



which can be accessed by the special last result variable `_`:


```python
_
```





<ul>
  <li><i class="fa fa-gift fa-1x"></i>
  </li>
  <li><i class="fa fa-gift fa-2x"></i>
  </li>
  <li><i class="fa fa-gift fa-3x"></i>
  </li>
  <li><i class="fa fa-gift fa-4x"></i>
  </li>
  <li><i class="fa fa-gift fa-5x"></i>
  </li>
</ul>



Or will update a named variable with the parsed document:


```python
%%jade spock
i.fa.fa-spock.fa-5x
```


    <IPython.core.display.Javascript object>



```python
spock
```




    '<i class="fa fa-spock fa-5x"></i>'



## Contribute
[Issues](https://github.com/bollwyvl/jademagic/issues) and [pull requests](https://github.com/bollwyvl/jademagic/pulls) welcome!

## License
`jademagic` is released as free software under the [BSD 3-Clause license](./LICENSE).

## Thank
- [@lbustelo](http://github.com/lbustelo) for challenging me to an alternative to `%%html`
