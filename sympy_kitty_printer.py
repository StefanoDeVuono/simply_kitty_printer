'''
SymPy Kitty Printer
===================
Pretty print SymPy expressions in kitty terminal.
'''

# This is the file to pretty print sympy expressions in kitty terminal.

# Usage example:
# from sympy_kitty_printer import *
#
# init_printing(pretty_printer=sympy_kitty)
#
# or 
#
# init_session(pretty_printer=sympy_kitty)

# NOTE: not yet working
from io import BytesIO
from sympy import preview, init_session, init_printing
from PIL.Image import open
from term_image.image import KittyImage
from term_image.utils import get_fg_bg_colors
from sympy.core.symbol import Symbol
from sympy.printing.latex import LatexPrinter
from sympy.printing.printer import print_function
from sympy.core.function import Function
from sympy.interactive import init_printing
from pdb import set_trace

__all__ = ['SympyKittyPrinter', 'sympy_kitty', 'init_session', 'init_printing']

class SympyKittyPrinter(LatexPrinter):
    """Pretty Printing for LaTeX in kitty compatible terminals.
    """
    printmethod = "_sympy_kitty_printer"
    KittyImage.forced_support = True

    def __init__(self, settings=None):
        LatexPrinter.__init__(self, settings)

    def _sympy_kitty_printer(self, expr):
        set_trace()

    def _pretty(self, printer):
        set_trace()

    def _latex(self, printer):
        set_trace()
        
    def _warp_sympy(self, expr):
        set_trace()
        
    def set_size(self, image):
        height, width = int(image.rendered_height / 8), int(image.rendered_width / 8)
        image.set_size(width, height)

    def dvi_options(self):
        dpi = 196
        bg = 'Transparent'
        image_size = 'bbox'
        return ['-D', f'{dpi}', '-bg', f'{bg}', '-T', f'{image_size}']
    
    def extra_preamble(self):
        fg_colour, _ = get_fg_bg_colors()
        return '\\usepackage[dvipsnames]{xcolor}\n' \
                f'\\color[RGB]{{{', '.join(map(str, fg_colour))}}}'
    
    def doprint(self, expr):
        tex = LatexPrinter.doprint(self, expr)
        obj = BytesIO()

        preview(
            f'${tex}$',
            output='png',
            dvioptions=self.dvi_options(),
            viewer='BytesIO',
            outputbuffer=obj,
            extra_preamble=self.extra_preamble()
        )
        # obj.
        img = open(obj)
        image = KittyImage(img)

        self.set_size(image)

        print("{:1.1}".format(image))
        return ''

@print_function(SympyKittyPrinter)
def sympy_kitty(expr, **settings):
    return SympyKittyPrinter(settings).doprint(expr)

