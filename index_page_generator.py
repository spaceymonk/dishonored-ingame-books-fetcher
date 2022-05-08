from bs4 import BeautifulSoup


CONTENTS = ""


def add_index_entry(href, title=None):
    global CONTENTS
    if title is None:
        title = href.replace(".html", "")
    CONTENTS += ("\n<li><a href=\"" + href + "\">" + title + "</a></li>")


def generate_page(pretty=False):
    html_doc =  f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Table of Contents</title>
</head>
<body>
    <h1>Table of Contents</h1>
    <ul>{CONTENTS}
    </ul>
</body>
</html>
"""
    if pretty:
        return BeautifulSoup(html_doc, "html.parser").prettify()
    return html_doc
