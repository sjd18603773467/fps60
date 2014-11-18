from flask import render_template, request
from app import app
from manage_db import manage
import urllib2
from weibo import APIClient

APP_KEY = '1857093371'
APP_SECRET = '92b57e2f9e8a9065588a9ac6b67a548b'

uid = 1

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    #response = urllib2.urlopen("https://api.weibo.com/oauth2/authorize?client_id=1857093371&reponse_type=code&redirect_uri=apps.weibo.com/socialfaqfaq")
    '''
    print "index"
    signed_request = request.form['signed_request']
    print signed_request
    client = APIClient(APP_ID, APP_SECRET, 'http://app.weibo.com/socialfaqfaq')
    data = client.parse_signed_request(signed_request)
    user_id = data.get('uid', '')
    auth_token = data.get('oauth_token', '')
    print user_id, "  **  ", auth_token
    if not user_id or not auth_token:
        return render_template("auth.html")
    expires = data.expires
    client.set_access_token(auth_token, expires)
    print client.statuses.user_timeline.get()
    print client.statuses.update.post(status="send weibo")
    '''
    return render_template("index.html")

@app.route('/question', methods = ['GET'])
def question():
    if not request.args.get('question_type'):
        question_type = 0 #return render_template('question.html', id = 0)
    else:
        question_type = int(request.args['question_type'])
    if question_type == 0:
        form = manage.all_select()
    elif question_type == 1:
        form = manage.all_blank()
    else:
        form = manage.all_answer()
    print question_type, "**"
    return render_template('question.html', question_type = question_type, form = form)

@app.route('/add_select', methods = ['GET', 'POST'])
def add_select():
    global uid
    if(uid):
        if(request.method == 'GET'):
            return render_template('add_select.html')
        if(request.method == 'POST'):
            manage.add_select(uid, request.form)
            return render_template('question.html')
    return render_template('index.html')

@app.route('/add_blank', methods = ['GET', 'POST'])
def add_blank():
    global uid
    if(uid):
        if(request.method == 'GET'):
            return render_template('add_blank.html')
        if(request.method == 'POST'):
            manage.add_blank(uid, request.form)
            return render_template('question.html')
    return render_template('index.html')

@app.route('/add_answer', methods = ['GET', 'POST'])
def add_answer():
    global uid
    if(uid):
        if(request.method == 'GET'):
            return render_template('add_answer.html')
        if(request.method == 'POST'):
            manage.add_answer(uid, request.form)
            return render_template('question.html')
    return render_template('index.html')

@app.route('/test', methods = ['GET', 'POST'])
def manage_question():
    global uid
    if(uid):
        if(request.method == 'POST'):
            manage.add_test(uid, request.form)
        all_test = manage.all_test(uid)
        return render_template('test.html', all_test = all_test)
    return render_template('index.html')

@app.route('/add_test')
def add_test():
    global uid
    if(uid):
        return render_template('add_test.html', all_select = manage.all_select(), all_blank = manage.all_blank(), all_answer = manage.all_answer())
    return render_template('index.html')

@app.route('/invate', methods = ['GET', 'POST'])
def invate():
    if(request.method == 'GET'):
        return render_template('invate.html')
    return render_template('invate.html')

@app.route('/score')
def score():
    return render_template('score.html')

'''
@app.route('/answer', methods = ['GET', 'POST'])
def answer():
    if(request.method == 'GET'):
        t = []
        rr = manage.get_test(tid = request.args['tid'])
        r = 0
        for r in rr:
            r = r
        t.append(r[5])
        s = r[2].split(' ')
        a = []
        for k in s:
            a.append(manage.get_select(qid = long(k)))
        t.append(a)
        a = []
        s = r[3].split(' ')
        print "************************ ", s
        for k in s:
            print "*********** ", k
            a.append(manage.get_blank(qid = long(k) - 10000)[2])
        t.append(a)
        s = r[4].split(' ')
        a = []
        for k in s:
            a.append(manage.get_answer(qid = long(k) - 1000000))
        t.append(a)
        return render_template('answer.html', t = t)
    #if(request.method == 'POST'):
        #return render_template('answer.html', t = t)
'''
