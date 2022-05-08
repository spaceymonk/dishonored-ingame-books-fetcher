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
    transcript_html = ''
    tag = soup.find(id='Transcript')
    if tag is None:
        print('No transcript found, failsafe activated')
        tag = soup.select_one('#mw-content-text > div.mw-parser-output > h2')
        while tag != None and not ('location' in str(tag.string).strip().lower() and tag.name == 'h2'):
            if tag.name == 'p':
                text = tag.get_text().strip().replace('\n', '<br />')
                transcript_html += text
            if tag.name == 'h2':
                text = str(tag.string)
                transcript_html += f'<h2>{text}</h2>'
            tag = tag.next_sibling
    else:
        tag = tag.parent.next_sibling
        while tag != None and tag.name != 'h2':
            if tag.name == 'p':
                text = tag.get_text().strip().replace('\n', '<br />')
                transcript_html += f'<p>{text}</p>'
            tag = tag.next_sibling
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
