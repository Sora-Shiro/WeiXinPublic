# -*- coding: utf-8 -*-
# filename: main.py
import web

from handler import Handle

g_urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    app = web.application(g_urls, globals())
    app.run()
