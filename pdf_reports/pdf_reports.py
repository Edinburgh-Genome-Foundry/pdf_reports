import os
import weasyprint
import pypugjs
import jinja2

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
STYLESHEET = os.path.join(THIS_PATH, 'css', 'style.css')
EGF_LOGO_URL = os.path.join(THIS_PATH, 'css', 'egf-logo.svg')

def pug_to_html(filepath=None, string=None, **variables):
    """Convert a Pug template, as file or string, to html.

    filepath
      Path to a .pug template file. The ``string`` parameter can be provided
      instead.

    string
      A string of a Pug template. The ``filepath`` parameter can be provided
      instead.

    **variables
      Keyword arguments indicating the variables to use in the Pug template
      (if it contains variables). For instance ``title='My title'``.

    """
    if filepath is not None:
        with open(filepath, "r") as f:
            string = f.read()
    jinja_template = pypugjs.simple_convert(string)
    return jinja2.Template(jinja_template).render(**variables)


def write_report(html, target, base_url=None, use_default_styling=True,
                 extra_stylesheets=()):
    """Write the provided HTML in a PDF file.

    Parameters
    ----------
    html

    target
      A PDF file path or file-like object

    base_url
      The base path from which relative paths in the HTML template start.

    use_default_styling
      Setting this parameter to False, your PDF will have no styling at all by
      default.

    extra_stylesheets
      List of paths to other ".css" files used to define new styles or
      overwrite default styles.

    """
    weasy_html = weasyprint.HTML(string=html, base_url=base_url)
    stylesheets = use_default_styling * (STYLESHEET,) + extra_stylesheets
    weasy_html.write_pdf(target, stylesheets=stylesheets)
