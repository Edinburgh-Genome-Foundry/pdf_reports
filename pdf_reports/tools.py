"""Utilities for report generation.

The module contains in particular routines the creation of tables, plots, etc.
inside the templates. Functions in this module are available from inside the
templates under the domain name ``pdf_tools``. For instance
``pdf_tools.dataframe_to_html()``.
"""
from bs4 import BeautifulSoup
import base64
import pandas
from io import BytesIO
import datetime
import textwrap


def dataframe_to_html(
    dataframe,
    extra_classes=(),
    index=False,
    header=True,
    use_default_classes=True,
    escape_html=False,
):
    """Return a HTML version of a dataframe with Semantic UI CSS style classes.

    By default it applies the following Semantic UI classes:
    'ui', 'compact', 'celled', 'striped', 'table', 'groups'

    Parameters
    ----------

    dataframe
      The pandas dataframe to convert to PDF

    extra_classes
      Classes to add to the default, which are 'ui', 'compact', 'celled',
      'striped', 'table', 'groups', selected to create nicely-formatted
      Semantic UI tables. For instance 'definition' can be added to add
      special emphasis on the first column. See Semantic UI documentation.

    index
      Whether to display the dataframe's index.

    header
      Whether to display the dataframe's headers.

    escape_html
      Whether the content of the dataframe should be html-escaped. Leave to
      false if your dataframe contains images or any kind of HTML formatting.
    """
    default_classes = ()
    if use_default_classes:
        default_classes = (
            "ui",
            "compact",
            "celled",
            "striped",
            "table",
            "groups",
        )
    classes = default_classes + tuple(extra_classes)
    current_colwidth = pandas.get_option("display.max_colwidth")
    # pandas.set_option("display.max_colwidth", -1)
    result = dataframe.to_html(
        classes=classes, index=index, header=header, escape=escape_html
    )
    pandas.set_option("display.max_colwidth", current_colwidth)
    return result


def style_table_rows(table_html, tr_modifier):
    """Return a new HTML string of the table, with rows modified.

    Parameters
    ----------

    table_html
      A string "<table>...</table>" of an HTML table.

    tr_modifier
      A function that takes a BeautifulSoup ``tr`` element as argument
      and changes its attributes inplace. for instance with
      ``tr.text = new_text``, or with the ``add_css_class`` method.
    """
    soup = BeautifulSoup(table_html, "html.parser")
    for tr in soup.find_all("tr"):
        tr_modifier(tr)
    return str(soup)


def add_css_class(element, cls):
    """Add a given class to the given BeautifulSoup HTML element."""
    attrs = element.attrs
    new_class = (attrs["class"] + " " if "class" in attrs else "") + cls
    element.attrs["class"] = new_class


class JupyterPDF(object):
    """Class to display PDFs in a Jupyter / IPython notebook.

    Just write this at the end of a code Cell to get in-browser PDF preview:

    >>> from pdf_reports import JupyterPDF
    >>> JupyterPDF("path_to_some.pdf")

    Credits to StackOverflow's Jakob: https://stackoverflow.com/a/19470377
    """

    def __init__(self, url, width=600, height=800):
        self.url = url
        self.width = width
        self.height = height

    def _repr_html_(self):
        return """
            <center>
                <iframe src={self.url} width={self.width} height={self.height}>
                </iframe>
            </center>
        """.format(
            self=self
        )


def now(fmt="%Y-%m-%d %H:%M"):
    now = datetime.datetime.now()
    if fmt is not None:
        now = now.strftime(fmt)
    return now


def figure_data(fig, size=None, fmt="png", bbox_inches="tight", **kwargs):
    """Return a HTML-embeddable string of the figure data.

    The string can be embedded in an image tag as ``<img src="{DATA}"/>``.

    Parameters
    ----------

    fig
      A Matplotlib figure. A Matplotlib "ax" can also be provided, at which
      case the whole ``ax.figure`` will be displayed (i.e. all axes in the
      same figure).

    size
      Size or resolution (width, height) of the final figure image, in inches.

    fmt
      Image format, for instance "png", "svg", "jpeg". SVG is vectorial (non
      pixelated) but sometimes more difficult to work with inside HTML/PDF
      documents.

    bbox_inches
      Keeping this option to "tight" will ensure that your plot's delimitation
      is optimal.

    **kwargs
      Any other option of Matplotlib's figure.savefig() method.
    """
    if "AxesSubplot" in str(fig.__class__):
        # A matplotlib axis was provided: take its containing figure.
        fig = fig.figure
    output = BytesIO()
    original_size = fig.get_size_inches()
    if size is not None:
        fig.set_size_inches((int(size[0]), int(size[1])))
    fig.savefig(output, format=fmt, bbox_inches=bbox_inches, **kwargs)
    fig.set_size_inches(original_size)
    data = output.getvalue()
    if fmt == "svg":
        svg_txt = data.decode()
        svg_txt = "\n".join(svg_txt.split("\n")[4:])
        svg_txt = "".join(svg_txt.split("\n"))
        content = base64.b64encode(svg_txt.encode("utf-8"))
    else:
        content = base64.b64encode(data)
    result = b"data:image/%s+xml;base64,%s" % (fmt.encode("utf-8"), content)
    return result.decode("utf-8")


def wrap(text, col_width):
    return "\n".join(textwrap.wrap(text, col_width))
