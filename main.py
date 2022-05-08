import os
from bs4 import BeautifulSoup
from book_item_downloader import generate_book
from index_page_generator import add_index_entry, generate_page
from remote_index_parser import parse_index_page


WORKDIR = './dishonored_books/'

if not os.path.exists(WORKDIR):
    os.makedirs(WORKDIR)

book_items = parse_index_page()
for i in range(len(book_items)):
    title, _ = book_items[i]
    file_name = "".join([x if x.isalnum() else '_' for x in title]) + ".html"
    file_path = WORKDIR + file_name
    if not os.path.exists(file_path):
        try:
            with open(file_path, 'w') as fp:
                print("Generating:", title, '...', i+1, "out of", len(book_items))
                book = generate_book(book_items[i])
                fp.write(BeautifulSoup(book, 'html.parser').prettify())
                add_index_entry(file_name, title)
        except Exception as e:
            print("Failed to generate:", title)
            print("ERROR:", e)
            os.remove(file_path)
    else:
        print("Skipping:", title)
        add_index_entry(file_name, title)

with open(WORKDIR + 'index.html', 'w') as fp:
    print('Generating index page...')
    fp.write(generate_page(pretty=True))

print("Done!")
