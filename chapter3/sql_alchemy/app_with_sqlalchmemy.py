from flask import Flask,request,jsonify
from ext import db
from users import User
import logging
from logging.handlers import RotatingFileHandler
from flask_sqlalchemy import get_debug_queries
app=Flask(__name__)
app.config.from_object('config')
db.init_app(app)

formatter=logging.Formatter(
    "[%(asctime)s]{%(pathname)s:%(lineno)d} %(levelname)s-%(message)s"
)
handler=RotatingFileHandler('slow_query.log',maxBytes=10000,backupCount=10)
handler.setLevel(logging.WARN)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/users',methods=['GET'])
def users():
    username=request.form.get('name')
    print(username,"22222222222222222222")
    user=User(username)
    print('User id:{}'.format(user.id))

    db.session.add(user)
    db.session.commit()
    return jsonify({'id':user.id})
@app.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration>=app.config['DATABASE_QUERY_TIMEOUT']:
            app.logger.warn(
                ('Context:{}\nSLOW QUERY:{}\n Parameters:{}\n'
                 'Duration: {}\n'.format(query.context,query.statement,
                                         query.parameters,query.duration))
            )
    return response
if __name__ == '__main__':
    app.run(port=9001)