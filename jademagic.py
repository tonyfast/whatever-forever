# -*- coding: utf-8 -*-
from __future__ import print_function

from IPython import get_ipython
from IPython.display import (
    display,
    Javascript,
    HTML,
)
from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
)
from IPython.utils.importstring import import_item

import pyjade


__version_info__ = (0, 1, 0)
__version__ = '.'.join(map(str, __version_info__))


@magics_class
class JadeMagics(Magics):
    """
    Write and load HTML with Jade in the IPython Notebook.

    Example:

        %%jade
        ul
            li: some text!
    """

    def __init__(self, shell):
        super(JadeMagics, self).__init__(shell)

    @cell_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument(
        "var_name",
        default=None,
        nargs="?",
        help="""Name of local variable to set to parsed value"""
    )

    def jade(self, line, cell):
        line = line.strip()
        args = magic_arguments.parse_argstring(self.jade, line)

        display(Javascript(
            """
            require(
                [
                    "notebook/js/codecell",
                    "codemirror/mode/jade/jade"
                ],
                function(cc){
                    cc.CodeCell.options_default.highlight_modes.magic_jade = {
                        reg: ["^%%jade"]
                    }
                }
            );
            """))

        try:
            val = pyjade.simple_convert(cell)
        except Exception as err:
            print(err)
            return

        if args.var_name is not None:
            get_ipython().user_ns[args.var_name] = val
        else:
            return HTML(val)


def load_ipython_extension(ip):
    ip = get_ipython()
    ip.register_magics(JadeMagics)
