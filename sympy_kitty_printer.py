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

from io import BytesIO
from sympy import preview
from PIL.Image import open
from term_image.image import KittyImage
from term_image.utils import get_fg_bg_colors
from sympy.printing.latex import LatexPrinter
from sympy.printing.printer import print_function
from pdb import set_trace
from sympy import init_session, init_printing

__all__ = ['SympyKittyPrinter', 'sympy_kitty', 'init_session', 'init_printing']

class SympyKittyPrinter(LatexPrinter):
    """Pretty Printing for LaTeX in kitty compatible terminals.
    """
    printmethod = "_sympy_kitty_printer"
    KittyImage.forced_support = True


    def __init__(self, settings=None):
        LatexPrinter.__init__(self, settings)
        self.line_height_scale = settings.get('line_height_scale', 28) if settings else 28

    def _sympy_kitty_printer(self, expr):
        set_trace()

    def _pretty(self, printer):
        set_trace()

    def _latex(self, printer):
        set_trace()
        
    def _warp_sympy(self, expr):
        set_trace()
        
    def _print_ImaginaryUnit(self, expr):
        return r"i"

    def dvi_options(self):
        dpi = 300
        bg = 'Transparent'
        image_size = 'tight'
        return ['-D', f'{dpi}', '-bg', f'{bg}', '-T', f'{image_size}']
        # Remove image_size = 'bbox' to prevent height normalization
        # return ['-D', f'{dpi}', '-bg', f'{bg}']
    
    def extra_preamble(self):
        fg_colour, _ = get_fg_bg_colors()
        return '\\usepackage[dvipsnames]{xcolor}\n' \
                f'\\color[RGB]{{{', '.join(map(str, fg_colour))}}}'
    
    def doprint(self, expr):
        tex = LatexPrinter.doprint(self, expr)
        # print(f"DEBUG LaTeX: {tex}")  # Add this to see the LaTeX
        obj = BytesIO()

        # Convert LaTeX expression to PNG stored in BytesIO object
        preview(
            f'${tex}$',
            output='png',
            dvioptions=self.dvi_options(),
            viewer='BytesIO',
            outputbuffer=obj,
            extra_preamble=self.extra_preamble()
        )
        img = open(obj)
        
        # Use PIL dimensions directly, not KittyImage's auto-scaled dimensions
        pil_width, pil_height = img.size
        
        # Terminal cells are ~2x taller than wide, so adjust accordingly
        # Calculate terminal size from original PIL dimensions
        height = max(1, int(pil_height / self.line_height_scale))
        # try dividing by 1.95
        width = max(1, int(pil_width / (self.line_height_scale / 1.95)))  # Divide by scaling factor for width
    
        # print(f"DEBUG: PIL={pil_height}x{pil_width}px, terminal={height}x{width} cells")
    
        image = KittyImage(img)
        image.set_size(width, height)
        
        print("{:1.1}".format(image))
        return ''

@print_function(SympyKittyPrinter)
def sympy_kitty(expr, **settings):
    return SympyKittyPrinter(settings).doprint(expr)

