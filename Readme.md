用轻量云服务器做一个简单的博客，或者说明手册还是非常好的。
现在流行的写博客或者说明手册的语言基本上就算是markdown了。编写规则简单，并且大体上满足基本的写作要求。
目前使用比较火的自己发布博客框架，可能是 mdbook 吧。
本例子主要是使用这个编写了一些使用手册，由于mdbook一般来说需要接入一些统计分析之类的，为了避免重复工作，最好还是在一个模版上来完成这个事情，然后把多本书嵌入进来完成这个需求。

mdbook 的使用手册地址 [https://rust-lang.github.io/mdBook/](https://rust-lang.github.io/mdBook/)

具体的使用问题比在细说，主要关注于如何在一个主题下编译发布多本书，涉及到使用 python 脚本，很多问题使用 python 脚本还是能够轻松解决的。

新建项目，multibooks

```bash
mdbook init --theme multibooks
```

文件结构如下：

```bash
book # 编译好的手册内容
book.toml # 配置文件
src # 书的markdown
theme # 主题，一般来说需要改一下这个东西
```

接下来修改一下目录结构，想把书都放在books这个文件夹下，对应的 src下也有相应的书的目录，以one、two两本书为例，修改后的文件结构如下：

```bash
books # 编译好的书
  | - one
  | - two
src # 书的markdown
  | - one
  | - two
book.toml # 配置文件
theme # 主题
```

接下来新建一个 book_template.toml
内容如下：

```
[book]
authors = ["xx"]
language = "en"
multilingual = false
src = "src/__book__"
title = "__title__"

[build]
build-dir = "books/__book__"
```

之后需要做的就是写个脚本替换相应的内容，并且把编译好的结果推送到服务器上去了。
脚本 genBook.py 内容如下：

```python
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
```

使用上来说如下：

```bash
python genBook.py -b one # 可以单独编译其中一个并推送
python genBook.py # 全部编译并全部推送
```

直接把books整体推送到一个轻量服务器的静态代理地址下，就能愉快的发布多本书了。

<img src="https://github.com/xo1988/mdbook/blob/master/bmc_qr.png" width="180">