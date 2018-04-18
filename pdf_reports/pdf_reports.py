import os
import weasyprint
import jinja2
import tempfile
from io import BytesIO
from . import tools
from functools import lru_cache

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
SEMANTIC_UI_CSS = os.path.join(THIS_PATH, 'css', 'semantic.min.css')
STYLESHEET = os.path.join(THIS_PATH, 'css', 'style.css')
EGF_LOGO_URL = os.path.join(THIS_PATH, 'css', 'egf-logo.svg')

GLOBALS = {
    "egf_logo_url": EGF_LOGO_URL,
    'list': list,
    'pdf_tools': tools
}

@lru_cache(maxsize=1)
def get_semantic_ui_CSS():
    return weasyprint.CSS(filename=SEMANTIC_UI_CSS)

def pug_to_html(path=None, string=None, **context):
    """Convert a Pug template, as file or string, to html.

    path
      Path to a .pug template file. The ``string`` parameter can be provided
      instead.

    string
      A string of a Pug template. The ``filepath`` parameter can be provided
      instead.

    **variables
      Keyword arguments indicating the variables to use in the Pug template
      (if it contains variables). For instance ``title='My title'``.

    """
    default = {k: v for (k, v) in GLOBALS.items()}
    default.update(context)
    context = default
    if string is not None:
        template_path = tempfile.mktemp(suffix='.pug')
        with open(template_path, 'w+') as f:
            f.write(string)
        if path is None:
            path = template_path
    else:
        template_path = path
    basepath, filename = os.path.split(template_path)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(basepath if basepath else '.'),
        extensions=['pypugjs.ext.jinja.PyPugJSExtension']
    )

    template = env.get_template(filename)
    return template.render(context)


def write_report(html, target=None, base_url=None, use_default_styling=True,
                 extra_stylesheets=()):
    """Write the provided HTML in a PDF file.

    Parameters
    ----------
    html
      A HTML string

    target
      A PDF file path or file-like object, or None for returning the raw bytes
      of the PDF.

    base_url
      The base path from which relative paths in the HTML template start.

    use_default_styling
      Setting this parameter to False, your PDF will have no styling at all by
      default. This means no Semantic UI, which can speed up the rendering.

    extra_stylesheets
      List of paths to other ".css" files used to define new styles or
      overwrite default styles.

    """
    weasy_html = weasyprint.HTML(string=html, base_url=base_url)
    if use_default_styling:
        stylesheets = (get_semantic_ui_CSS(), STYLESHEET,) + extra_stylesheets
    else:
        stylesheets = extra_stylesheets
    if target is None:
        with BytesIO() as buffer:
            weasy_html.write_pdf(buffer, stylesheets=stylesheets)
            pdf_data = buffer.getvalue()
        return pdf_data
    else:
        weasy_html.write_pdf(target, stylesheets=stylesheets)
