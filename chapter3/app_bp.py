from flask import Flask

from chapter3.sql_alchemy import users

app=Flask(__name__)

app.register_blueprint(users.bp)



if __name__ == '__main__':
    app.run(port=9000)