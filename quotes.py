from flask import Flask,render_template,request,redirect,flash,abort,session
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
#DEVELOPMENT
#app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://postgres:Welcome1@10.10.10.45/quotes'
#PROD
    #NOTE on heroku engine is wrong tldr postgres:// was long deprecated, you should use postgresql://
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://cqvfsstxhnchzp:cf18c4fce2620a6c35bcf2d72904e36d9ff1afa5322543e817088fbeb930fcbf@ec2-52-0-234-93.compute-1.amazonaws.com:5432/dbbq2jou531jck'
# postgres://cqvfsstxhnchzp:cf18c4fce2620a6c35bcf2d72904e36d9ff1afa5322543e817088fbeb930fcbf@ec2-52-0-234-93.compute-1.amazonaws.com:5432/dbbq2jou531jck
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #this is tracking mechanism, that may take a lot of resources

#Create and instance of class 
db = SQLAlchemy(app)

class tblFavquotes(db.Model):
    Id = db.Column(db.Integer,primary_key=True)
    Author = db.Column(db.String(30))
    Quote = db.Column(db.String(2000))

@app.route('/')
def index():
    result = tblFavquotes.query.all()
    #result = [{"Author":"Frank Moody","Quote":"You know why love stories have happy endings? I shake my head. 'Because they end too early,' she continues. 'They always end right at the kiss. You never have to see all the bullshit that comes later. You know, Life"},{"Author":"Frank Moody","Quote":"A morning of awkwardness is far better then a night of loneliness"},{"Author":"Frank Moody","Quote":"She said one thing and I said another and the next thing I knew I wanted to spend the rest of my life in the middle of that conversation."}]
    # return render_template('index.html',quotes=quotes)#to passon the session add codes, then edit index.html
    return render_template('index.html',quotes=result)

@app.route('/quotes')
def quotes():   
    # ,quote="I wont go down in history but I will go down on your sister",quotes=quotes            
    return render_template('quotes.html')

@app.route('/process',methods=['GET','POST'])
def process():   
    #Request object gives access to the form data      
    if request.method == 'POST':
        # form_values = dict(author = request.form['author'],quote = request.form['quote'])        
        author = request.form['author']
        quote = quote=request.form['quote']
        quotedata = tblFavquotes(Author=author,Quote=quote)
        #Add information to DB Session
        db.session.add(quotedata)
        db.session.commit()
        
        #return render_template('index.html',form_values=form_values)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('pagenotfound.html'),404 #when 4040 occurs it will return the template

if __name__ == "__main__":       
    app.run()