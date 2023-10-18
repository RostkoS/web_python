from flask import Flask, render_template
from flask_bootstrap import Bootstrap
#create the object of Fla
import os
from datetime import datetime
from flask import request
app  = Flask(__name__)
bootstrap = Bootstrap(app)


@app.context_processor
def inject_user():
    return dict(data=os.name, user_agent=request.headers.get('User-Agent'),t=datetime.now().strftime("%H:%M:%S"))
#creating our routes
@app.route('/')
def home():
    return render_template('home.html')



#contact routes
@app.route('/education')
def education():
    return render_template('education.html')


#contact routes
@app.route('/skills')
@app.route('/skills/<int:id>')
def skills(id=None):
    mylist = ["Java", "C++", "Python"]
    if id==None:
     return render_template('skills.html', data=mylist)
    else:
      mylist = [mylist[id]]  
      return render_template('skills.html', data=mylist)


#run flask app
if __name__ == "__main__":
    app.run(debug=True)