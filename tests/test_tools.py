import pdf_reports.tools as tools
import pandas

dataframe = pandas.DataFrame.from_records(
    {
        "Name": ["Anna", "Bob", "Claire", "Denis"],
        "Age": [12, 22, 33, 44],
        "Height (cm)": [140, 175, 173, 185],
    },
    columns=["Name", "Age", "Height (cm)"],
)


def test_tr_modifier():
    html = tools.dataframe_to_html(dataframe)

    def tr_modifier(tr):
        if "Anna" in tr.text:
            tools.add_css_class(tr, "is-anna")

    new_html = tools.style_table_rows(html, tr_modifier)
    assert "is-anna" in new_html

    def tr_modifier(tr):
        if "Emma" in tr.text:
            tools.add_css_class(tr, "is-emma")

    new_html = tools.style_table_rows(html, tr_modifier)
    assert "is-emma" not in new_html


def test_JupyterPDF():
    pdf = tools.JupyterPDF("some_url.pdf")
    assert len(pdf._repr_html_()) > 40


def test_now():
    now = tools.now(fmt="%Y-%m-%d %H:%M")
    assert now[4] == "-" and now[13] == ":" and len(now) == 16


def test_wrap():
    text = "abcde"
    assert tools.wrap(text, col_width=4) == "abcd\ne"
