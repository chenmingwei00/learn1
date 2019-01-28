import random

from flask import Flask,g,render_template
from ext import db
from users import User

app=Flask(__name__,template_folder='../../templates')

app.config.from_object('config')
db.init_app(app)


def get_current_user():
    users=User.query.all()
    return random.choice(users)
"""
在处理函数第一次会使用，
"""
@app.before_first_request
def setup():
    db.drop_all()
    db.create_all()
    fake_users=[
        User('xiaoming','xiaoming@163.com'),
        User('dongweiming','dongweiming@163.com'),
        User('admin','admin@163.com')
    ]
    db.session.add_all(fake_users)
    db.session.commit()

"""
每一次请求之前都会使用
"""
@app.before_request
def before_request():
    g.user=get_current_user()

"""
不管是否有异常，注册函数都会在每次请求之后调用
"""
@app.teardown_appcontext
def teardown(exc=None):
    if exc is None:
        db.session.commit()
    else:
        db.session.rollback()
    db.session.remove()
    g.user=None
"""
上下文处理的装饰器，返回字典中的键可以在上下文中使用
"""
@app.context_processor
def template_extras():
    return {'enumerate':enumerate,'current_user':g.user}
@app.errorhandler(404)
def page_not_found(error):
    return 'this page dose not exits',404
@app.template_filter('capitalize')
def reverse_filter(s):
    return s.capitalize()
@app.route('/users')
def user_view():
    users=User.query.all()
    return render_template('users.html',users=users)
if __name__ == '__main__':
    app.run(port=9001)