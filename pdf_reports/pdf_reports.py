import os
try:
    from weasyprint import HTML, CSS
except ImportError as err:
    message = """
        [PDF Reports] ERROR: The Weasyprint library did not load properly !
        You will not be able to generate PDF reports until you fix this issue.

        Windows users, this might be useful:
        http://weasyprint.readthedocs.io/en/stable/install.html#windows

        The original import error was %s
    """ % (str(err))
    def HTML(*args, **kwargs):
        """%s""" % message
        raise ImportError(message)
    CSS = HTML



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
    'len': len,
    'pdf_tools': tools,
}

@lru_cache(maxsize=1)
def get_semantic_ui_CSS():
    return CSS(filename=SEMANTIC_UI_CSS)

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
    weasy_html = HTML(string=html, base_url=base_url)
    if use_default_styling:
        stylesheets = (get_semantic_ui_CSS(), STYLESHEET,) + extra_stylesheets
    else:
        stylesheets = extra_stylesheets
    if target in [None, "@memory"]:
        with BytesIO() as buffer:
            weasy_html.write_pdf(buffer, stylesheets=stylesheets)
            pdf_data = buffer.getvalue()
        return pdf_data
    else:
        weasy_html.write_pdf(target, stylesheets=stylesheets)

class ReportWriter:

    def __init__(self, default_stylesheets=(), default_template=None,
                 use_default_styling=True, default_base_url=None,
                 **default_context):

        self.default_template = default_template
        self.default_context = default_context if default_context else {}
        self.default_stylesheets = default_stylesheets
        self.use_default_styling = use_default_styling
        self.default_base_url = default_base_url

    def pug_to_html(self, path=None, string=None, **context):
        """See pdf_reports.pug_to_html"""
        if (path is None) and (string is None):
            path = self.default_template
        for k in self.default_context:
            if k not in context:
                context[k] = self.default_context[k]
        return pug_to_html(path=path, string=string, **context)

    def write_report(self, html, target=None, extra_stylesheets=(),
                     base_url=None):
        return write_report(
            html,
            target=target,
            extra_stylesheets=self.default_stylesheets + extra_stylesheets,
            base_url=base_url if base_url else self.default_base_url,
            use_default_styling=self.use_default_styling
        )
