# -*- coding: utf-8 -*-
# filename: main.py
import web

urls = (
    '/wx', 'Handle',
)


class Handle(object):
    def GET(self):
        return "Hello World!!"


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
