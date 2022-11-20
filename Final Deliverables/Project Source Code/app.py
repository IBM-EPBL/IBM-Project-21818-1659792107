from flask import Flask, render_template,request,redirect,url_for,session,flash
import ibm_db
#import os;
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from newsapi import NewsApiClient
app=Flask(__name__,template_folder='template')
app.secret_key='a'
try:
   conn = ibm_db.connect("DATABASE=bludb; HOSTNAME=ea286ace-86c7-4d5b-8580-3fbfa46b1c66.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=31505; SECURITY=SSL; SSLServerCertificate=DigiCertGlobalRootCA.crt; UID=rzf43026; PWD=X5xod3FomvXmvIn3",'','')
except:
   print("Unable to connect: ",ibm_db.conn_error())
    
@app.route("/")
def dash():
    return render_template('welcome.html',msg=" ")
    

@app.route('/register',methods = ['POST', 'GET'])
def register():
  msg = ' '
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    phonenumber = request.form['phonenumber']
    password1 = request.form['password1']
    password2 = request.form['password2']
    sql = "SELECT * FROM user WHERE username =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,username)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    if account:
      msg = 'Account already exists !'
    elif not username or not password1 or not email:
      msg = 'Please fill the Missing Details !'
    else:
      insert_sql = "INSERT INTO user VALUES (?,?,?,?,?)"
      prep_stmt = ibm_db.prepare(conn, insert_sql)
      ibm_db.bind_param(prep_stmt, 1, username)
      ibm_db.bind_param(prep_stmt, 2, email)
      ibm_db.bind_param(prep_stmt, 3, phonenumber)
      ibm_db.bind_param(prep_stmt, 4, password1)
      ibm_db.bind_param(prep_stmt, 5, password2)
      ibm_db.execute(prep_stmt)
      msg = 'Account created successfully'
      return render_template('login.html',msg=msg)
  return render_template('register.html',msg=msg)

@app.route('/login',methods = ['POST', 'GET'])
def login():
  msg = ' '
  if request.method == 'POST':
    email = request.form['email']
    password1 = request.form['password1']     
    sql = "SELECT * FROM user WHERE Email =?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt,1,email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_both(stmt)    
    accounts=account   
    if (account):
      if(password1 == accounts['PASSWORD1']):
        msg = 'Logged in successfully !'
        return render_template('home.html',msg=msg)
      else :
        msg='Wrong Credentials'
  return  render_template('login.html',msg=msg)

@app.route('/forget',methods=['GET','POST'])
def forget():
    error = None
    if request.method=='POST':
        username=request.form['username']
        password2=request.form['password2']
        sql="SELECT * FROM user WHERE username=? AND password2=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password2)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['USERNAME']
            session["username"]=account["USERNAME"]
            flash("Logged in successfully!")
            return redirect(url_for("home"))
        else:
            error="Incorrect username / pin"
            return render_template('login.html',error=error)
    return render_template('forget.html',error=error)

@app.route('/welcome')
def welcome_page():
    return render_template("welcome.html",msg=" ")

@app.route('/home')
def home():
    api_key = '25560f3cf53c433c9807c60595b373a6'
    
    newsapi = NewsApiClient(api_key=api_key)

    top_headlines = newsapi.get_top_headlines(sources = "bbc-news")
    all_articles = newsapi.get_everything(sources = "bbc-news")

    t_articles = top_headlines['articles']
    a_articles = all_articles['articles']

    news = []
    desc = []
    img = []
    p_date = []
    url = []

    for i in range (len(t_articles)):
        main_article = t_articles[i]

        news.append(main_article['title'])
        desc.append(main_article['description'])
        img.append(main_article['urlToImage'])
        p_date.append(main_article['publishedAt'])
        url.append(main_article['url'])

        contents = zip( news,desc,img,p_date,url)

    news_all = []
    desc_all = []
    img_all = []
    p_date_all = []   
    url_all = []

    for j in range(len(a_articles)): 
        main_all_articles = a_articles[j]   

        news_all.append(main_all_articles['title'])
        desc_all.append(main_all_articles['description'])
        img_all.append(main_all_articles['urlToImage'])
        p_date_all.append(main_all_articles['publishedAt'])
        url_all.append(main_article['url'])
        
        all = zip( news_all,desc_all,img_all,p_date_all,url_all)

    return render_template("home.html",contents=contents,all = all)
if __name__=='__main__':
    app.run(debug=True)
