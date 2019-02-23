from pdf_reports import pug_to_html, write_report, preload_stylesheet

css = preload_stylesheet('style.scss')
html = pug_to_html("template.pug", title="My report", my_name='Zulko')
write_report(html, "example.pdf", extra_stylesheets=[css])