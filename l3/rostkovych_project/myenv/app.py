from flask import Flask, render_template
from flask_bootstrap import Bootstrap
#create the object of Fla
import os

app  = Flask(__name__)
bootstrap = Bootstrap(app)
print(os.name)


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
    mylist = ["java", "c++", "python"]
    if id==None:
     return render_template('skills.html', data=mylist)
    else:
      mylist = [mylist[id]]  
      return render_template('skills.html', data=mylist)


#run flask app
if __name__ == "__main__":
    app.run(debug=True)