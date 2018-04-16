import os
from pdf_reports import pug_to_html, write_report
from PyPDF2 import PdfFileReader

def test_basics(tmpdir):
    template_path = os.path.join('tests', 'data', "example_template.pug")
    assert os.path.exists(template_path)
    pdf_path = os.path.join(str(tmpdir), 'test.pdf')
    html = pug_to_html(template_path, title="Summary of your order")
    write_report(html, pdf_path)
    with open(pdf_path, "rb") as f:
        reader = PdfFileReader(f)
        assert reader.numPages == 2

    pdf_data = write_report(html)
    assert len(pdf_data) > 10000
