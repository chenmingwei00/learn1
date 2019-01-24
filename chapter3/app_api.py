from flask import Flask,jsonify
from flask.views import MethodView

app=Flask(__name__)

class UserAPI(MethodView):
    def get(self):
        return jsonify({
            'username':'chen',
            'avatar':'http://lorempixel.com/100/100/nature/'
        })
    def post(self):
        return 'unspoort'

app.add_url_rule('/users',methods=['GET'],view_func=UserAPI.as_view('userview'))

if __name__ == '__main__':
    app.run(port=9000)