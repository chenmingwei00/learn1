from flask import Flask,render_template,request
from flask.views import View

app=Flask(__name__,template_folder='./templates')

class BaseView(View):
    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self,context):
        return render_template(self.get_template_name(),**context)

    def dispatch_request(self):

        if request.method!='GET':
            return 'unsupported!'
        context={'users':self.get_users()}
        return self.render_template(context)
class UserView(BaseView):
    def get_template_name(self):
        return 'users.html'

    def get_users(self):
        return [{
            'username':'chen',
            'avatar':'http://lorempixel.com/100/100/nature/'
        }]
app.add_url_rule('/users',view_func=UserView.as_view('userview'))
"""app.add_url首先会运行as_view的函数
   dispatch_request函数；
   然后运行self.get_user()
   然后运行self.render_template（）
   然后运行get_template_name
   
"""
if __name__ == '__main__':
    app.run(port=9000)