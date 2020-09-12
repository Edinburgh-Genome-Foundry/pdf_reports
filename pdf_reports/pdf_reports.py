import os

try:
    from weasyprint import HTML, CSS
except (ImportError, OSError) as err:
    message = (
        "[PDF Reports] ERROR: The Weasyprint library did not load"
        "properly! You will not be able to generate PDF reports until"
        "you fix this issue.\n"
    )

    if "pango" in str(err):
        message += (
            "\nMaybe you haven't installed the Pango dependency? "
            "('brew install pango' on Mac, 'apt install libpango' "
            "on Ubuntu).\n"
        )
    if "cairo" in str(err):
        message += "\nMaybe you haven't installed the Cairo dependency?\n"

    message += (
        "\nIn any other case the weasyprint docs may be able to help:\n\n"
        "http://weasyprint.readthedocs.io/en/stable/install.html#windows\n\n"
        "The original import error was %s" % (str(err))
    )

    def HTML(*args, **kwargs):
        """%s""" % message
        raise ImportError(message)

    CSS = HTML

try:
    import sass

    LIBSASS_AVAILABLE = True
except ImportError:
    LIBSASS_AVAILABLE = False
    sass = None

import jinja2
import tempfile
import warnings
from io import BytesIO
from . import tools


try:
    from functools import lru_cache
except ImportError:
    from backports.functools_lru_cache import lru_cache

THIS_PATH = os.path.dirname(os.path.realpath(__file__))
SEMANTIC_UI_CSS = os.path.join(THIS_PATH, "css", "semantic.min.css")
STYLESHEET = os.path.join(THIS_PATH, "css", "style.css")
EGF_LOGO_URL = os.path.join(THIS_PATH, "css", "egf-logo.svg")

GLOBALS = {
    "egf_logo_url": EGF_LOGO_URL,
    "list": list,
    "len": len,
    "zip": zip,
    "enumerate": enumerate,
    "pdf_tools": tools,
}


@lru_cache(maxsize=1)
def get_semantic_ui_CSS():
    with warnings.catch_warnings():
        css = CSS(filename=SEMANTIC_UI_CSS)
    return css


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
        template_path = tempfile.mktemp(suffix=".pug")
        with open(template_path, "w+") as f:
            f.write(string)
        if path is None:
            path = template_path
    else:
        template_path = path
    basepath, filename = os.path.split(template_path)
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(basepath if basepath else "."),
        extensions=["pypugjs.ext.jinja.PyPugJSExtension"],
    )

    template = env.get_template(filename)
    return template.render(context)


def write_report(
    html, target=None, base_url=None, use_default_styling=True, extra_stylesheets=()
):
    """Write the provided HTML in a PDF file.

    Parameters
    ----------
    html
      A HTML string.

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
        extra_stylesheets = tuple(extra_stylesheets)
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
    def __init__(
        self,
        default_stylesheets=(),
        default_template=None,
        use_default_styling=True,
        default_base_url=None,
        **default_context
    ):

        self.default_template = default_template
        self.default_context = default_context if default_context else {}
        self.default_stylesheets = default_stylesheets
        self.use_default_styling = use_default_styling
        self.default_base_url = default_base_url

    def pug_to_html(self, path=None, string=None, **context):
        """See pdf_reports.pug_to_html."""
        if (path is None) and (string is None):
            path = self.default_template
        for k in self.default_context:
            if k not in context:
                context[k] = self.default_context[k]
        return pug_to_html(path=path, string=string, **context)

    def write_report(self, html, target=None, extra_stylesheets=(), base_url=None):
        return write_report(
            html,
            target=target,
            extra_stylesheets=list(self.default_stylesheets) + list(extra_stylesheets),
            base_url=base_url if base_url else self.default_base_url,
            use_default_styling=self.use_default_styling,
        )


def preload_stylesheet(path, is_scss="auto"):
    """Preload a stylesheet as a WeasyPrint CSS object once and for all.

    Returns a weasyprint.CSS object which can be provided as-is in a list of
    default_stylesheets or extra_stylesheets.

    Preloading stylesheets can save a lot of time for large CSS frameworks
    that are used several times. It prevents weasyprint from parsing the CSS
    every time.

    If the path ends with .scss or .sass and is_scss is set to "auto",
    is_scss will be set to True.

    If is_scss is true, the file is compiled using python-libsass (
    which must be installed).

    Note: if you already have a string, directly use ``sass.compile(s)`` to
    compile the string.
    """
    if is_scss == "auto" and isinstance(path, str):
        is_scss = path.lower().endswith((".scss", ".sass"))
    if hasattr(path, "read"):
        string = path.read()
    else:
        with open(path, "r") as f:
            string = f.read()
    if is_scss:
        if not LIBSASS_AVAILABLE:
            raise ImportError(
                "Cannot read scss files without python-libsass installed. "
                "Either install the library or provide a CSS file, or set "
                "is_scss to False"
            )
        string = sass.compile(string=string)
    return CSS(string=string)
