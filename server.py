__author__ = 'signalpillar'


from adengine import app

from flask.ext.script import Manager


if __name__ == '__main__':
    manager = Manager(app.create_app('development'))
    manager.run()
