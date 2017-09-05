# -*- coding: utf-8 -*-
# filename: main.py
import web

from handler import Handle, read_data

g_urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    print "Starting Server"

    read_data()

    app = web.application(g_urls, globals())

    app.run()
