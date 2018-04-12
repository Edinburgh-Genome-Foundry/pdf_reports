from bs4 import BeautifulSoup

def dataframe_to_html(dataframe, extra_classes=(), index=False, escape=False):
    """Return a HTML version of a dataframe with Semantic UI CSS style classes.

    By default it applies the following Semantic UI classes:
    'ui', 'compact', 'celled', 'striped', 'table', 'groups'
    """
    classes = ('ui', 'compact', 'celled', 'striped',
               'table', 'groups') + extra_classes
    return dataframe.to_html(classes=classes, index=index, escape=escape)

def style_table_rows(table_html, tr_modifier):
    soup = BeautifulSoup(table_html, "html.parser")
    for tr in soup.find_all("tr"):
        tr_modifier(tr)
    return str(soup)

def add_css_class(element, cls):
    attrs = element.attrs
    new_class = (attrs["class"] + " " if "class" in attrs else "") + cls
    element.attrs["class"] = new_class
