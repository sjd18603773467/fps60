from flask import render_template, request
from app import app
from manage_db import manage

uid = 1

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if(manage.check(username, password)):
            global uid
            uid = manage.get_userid(username)
            print "index: ", uid
            return render_template("index.html", username = username)
        return render_template("index.html")

@app.route('/login')
def login():
    return render_template('login.html', title = 'Sign In')

@app.route('/add_question')
def add_question():
    global uid
    print "aq: ", uid
    if(uid):
        return render_template('add_question.html')
    return render_template('index.html')

@app.route('/add_select', methods = ['GET', 'POST'])
def add_select():
    global uid
    if(uid):
        if(request.method == 'GET'):
            return render_template('add_select.html')
        if(request.method == 'POST'):
            manage.add_select(uid, request.form)
            return render_template('add_question.html')
    return render_template('index.html')

@app.route('/add_blank', methods = ['GET', 'POST'])
def add_blank():
    global uid
    if(uid):
        if(request.method == 'GET'):
            return render_template('add_blank.html')
        if(request.method == 'POST'):
            manage.add_blank(uid, request.form)
            return render_template('add_question.html')
    return render_template('index.html')

@app.route('/add_answer', methods = ['GET', 'POST'])
def add_answer():
    global uid
    if(uid):
        if(request.method == 'GET'):
            return render_template('add_answer.html')
        if(request.method == 'POST'):
            manage.add_answer(uid, request.form)
            return render_template('add_question.html')
    return render_template('index.html')

@app.route('/manage_question', methods = ['GET', 'POST'])
def manage_question():
    global uid
    if(uid):
        if(request.method == 'GET'):
            all_test = manage.all_test(uid)
            return render_template('manage_question.html', all_test = all_test)
        if(request.method == 'POST'):
            all_test = manage.all_test(uid)
            manage.add_test(uid, request.form)
            return render_template('manage_question.html', all_test = all_test)
    return render_template('index.html')

@app.route('/add_test')
def add_test():
    global uid
    if(uid):
        return render_template('add_test.html', all_select = manage.all_select(), all_blank = manage.all_blank(), all_answer = manage.all_answer())
    return render_template('index.html')

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
