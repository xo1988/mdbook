# coding=utf8

import argparse
import os

books = {
    'one': 'One',
    'two': 'Two'
}

def makeBook(book, title):
    with open('book_template.toml', 'r') as f, open('book.toml','w+') as tf:
        doc = f.read()
        doc = doc.replace('__book__', book)
        doc = doc.replace('__title__', title)
        tf.write(doc)
    
    os.system('mdbook build')
    os.system('scp -r books/{book}/* root@8.8.8.8:/usr/share/nginx/html/books/{book}'.format(book=book))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', type=str)
    args = parser.parse_args()

    if args.b in books:
        makeBook(args.b, books[args.b])
        makeBook('{}_en'.format(args.b), books[args.b])
        exit(0)

    for book in books:
        makeBook(book, books[book])
        makeBook('{}_en'.format(book), books[book])
        