# _*_coding:utf-8 _*_
from flask_script import Manager
from app import create_app

app = create_app("testing")

manager = Manager(app)
if __name__ == '__main__':
    manager.run()
