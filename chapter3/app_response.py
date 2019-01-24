from flask import Flask,jsonify
from werkzeug.wrappers import Response
app=Flask(__name__)

class JSONResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response,dict):
            rv=jsonify(response)
        return super(JSONResponse,cls).force_type(rv,environ)
app.response_class=JSONResponse
@app.route('/')
def hell_word():
    return {'message':'hello worild'}

@app.route('/custom_headers')
def headers():
    return {'headers':[1,2,3]},201,[('X-requestid','100')]

if __name__ == '__main__':
    app.run(port=9000,debug=True)