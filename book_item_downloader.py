from bs4 import BeautifulSoup
import requests
import base64


BASE_URL = 'https://dishonored.fandom.com'


def generate_book(book_item, base_url=BASE_URL):
    title, href = book_item
    url = base_url + href
    if base_url.startswith('http'):
        with requests.get(url) as response:
            soup = BeautifulSoup(response.text, 'html.parser')
            transcript_html = parse_transcript(soup)
            image_html = parse_image(soup)
    else:
        with open(url, 'r') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            transcript_html = parse_transcript(soup)
            image_html = parse_image(soup)

    html_doc = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
    </head>
    <body>
        <h2>{title}</h2>
        {image_html}
        {transcript_html}
    </body>
    </html>
    """
    return html_doc


def parse_transcript(soup):
    paragraphs = []
    tag = soup.find(id='Transcript')
    if tag is None:
        raise Exception('No transcript found')
    tag = tag.parent.next_sibling
    while tag != None and tag.name != 'h2':
        if tag.name == 'p':
            text = tag.get_text().strip().replace('\n', '<br />')
            paragraphs.append(text)
        tag = tag.next_sibling
    transcript_html = ''
    for paragraph in paragraphs:
        transcript_html += f'<p>{paragraph}</p>'
    return transcript_html


def parse_image(soup):
    tag = soup.select_one('#mw-content-text > div > figure')
    if tag is None:
        return ''
    with requests.get(tag.a.img['src']) as response:
        image_data = response.content
        image_base64 = base64.b64encode(image_data)
        figure_html = f"""
        <figure style="{tag['style']}">
            <img src="data:image/png;base64,{image_base64.decode()}" width="{tag.a.img['width']}" height="{tag.a.img['height']}">
            <figcaption>{tag.figcaption.get_text()}</figcaption>
        </figure>
        """
    return figure_html
