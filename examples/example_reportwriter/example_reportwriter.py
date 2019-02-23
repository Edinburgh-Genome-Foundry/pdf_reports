from pdf_reports import ReportWriter

# DEFINE A WRITER WITH DEFAULT TEMPLATE AND VALUES
report_writer = ReportWriter(
    default_stylesheets=["style.css"],
    default_template="template.pug",
    title="My default title",
    version="0.1.2"
)

# THEN LATER IN YOUR CODE:
html = report_writer.pug_to_html(my_name="Zulko", my_organization="EGF")
report_writer.write_report(html, "example_reportwriter.pdf")