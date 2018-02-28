# _*_ coding: utf-8 _*_
from logbook import Logger

log = Logger("LIB.UEDITOR")

class UEditor(object):
    def __init__(self):
        self.config = {}

    def init_app(self, app):
        self.config = app.config["UEDITOR_CONFIG"]

    def get_config(self):
        return self.config