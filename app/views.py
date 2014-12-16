# -*- coding: utf-8 -*-

from app import app
from manage_db import manage
from flask import render_template, request, session
from weibo.weibo import APIClient
from weibo_api.weibo_api import get_name, get_friend, send_weibo

APP_KEY = '1857093371'
APP_SECRET = '92b57e2f9e8a9065588a9ac6b67a548b'

app.debug = True                                                               
app.secret_key = APP_SECRET

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    signed_request = request.form['signed_request']
    client = APIClient(APP_KEY, APP_SECRET, 'http://app.weibo.com/socialfaqfaq')
    data = client.parse_signed_request(signed_request)
    user_id = data.get('uid', '')
    auth_token = data.get('oauth_token', '')
    if not user_id or not auth_token:
        return render_template("auth.html")
    expires = data.expires
    client.set_access_token(auth_token, expires)
    user_name = get_name(client = client, auth_token = auth_token, user_id = user_id)
    
    session['user_id'] = user_id
    session['auth_token'] = auth_token
    session['expires'] = expires
    session['user_name'] = user_name
    
    return render_template("index.html")

@app.route('/question', methods = ['GET'])
def question():
    user_name = session['user_name']
    return render_template('question.html', all_select = manage.all_select(user_name), all_blank = manage.all_blank(user_name), all_answer = manage.all_answer(user_name))

@app.route('/details', methods = ['GET'])
def details():
    question_id = long(request.args['question_id'])
    l = []
    if question_id >= 1000000:
        l.append(2)
    	t = manage.get_answer(long(question_id) - 1000000)
    	for r in t:
        	l.append(r[2])
        	l.append(r[3])
    elif question_id >= 10000:
        l.append(1)
    	t = manage.get_blank(long(question_id) - 10000)
    	for r in t:
        	s = r[2].split('^_^')
        	l.append(s[0] + "____" + s[2])
        	l.append(s[1])
    else:
        l.append(0)
    	t = manage.get_select(long(question_id))
    	for r in t:
        	l.append(r[2])
        	l.append(r[3])
        	l.append(r[4])
        	l.append(r[5])
        	l.append(r[6])
        	l.append(r[7])
    return render_template('details.html', question = l)

@app.route('/add_select', methods = ['GET', 'POST'])
def add_select():
    user_name = session['user_name']
    if(request.method == 'GET'):
        return render_template('add_select.html')
    manage.add_select(user_name, request.form)
    return render_template('question.html')

@app.route('/add_blank', methods = ['GET', 'POST'])
def add_blank():
    user_name = session['user_name']
    if(request.method == 'GET'):
        return render_template('add_blank.html')
    manage.add_blank(user_name, request.form)
    return render_template('question.html')

@app.route('/add_answer', methods = ['GET', 'POST'])
def add_answer():
    user_name = session['user_name']
    if(request.method == 'GET'):
        return render_template('add_answer.html')
    manage.add_answer(user_name, request.form)
    return render_template('question.html')

@app.route('/test', methods = ['GET', 'POST'])
def test():
    user_name = session['user_name']
    if(request.method == 'POST'):
        manage.add_test(user_name, request.form)
    all_test = manage.all_test(user_name)
    return render_template('test.html', all_test = all_test)

@app.route('/add_test')
def add_test():
    user_name = session['user_name']
    return render_template('add_test.html', all_select = manage.all_select(user_name), all_blank = manage.all_blank(user_name), all_answer = manage.all_answer(user_name))

@app.route('/invate', methods = ['GET', 'POST'])
def invate():
    expires = session['expires']
    auth_token = session['auth_token']
    user_id = session['user_id']
    user_name = session['user_name']
    client = APIClient(APP_KEY, APP_SECRET, 'http://apps.weibo.com/socialfaqfaq')
    client.set_access_token(auth_token, expires)
    
    if(request.method == 'GET'):
        l = client.friendships.friends.get(access_token = auth_token, uid = user_id)
        l = l['users']
        a = []
        for i in range(len(l)):
            a.append(l[i]['name'])
        return render_template('invate.html', friend = a, test = manage.all_test(user_name))    #get_friend(client, auth_token, user_id)
    
    form = request.form
    manage.add_invate(from_name = user_name, to_name = form['to_name'], test_id = form['test_id'])
    client.statuses.update.post(status = "@" + form['to_name'] + u"，我有一些问题想考考你，请点击http://apps.weibo.com/socialfaqfaq/answer?test_id=" + form['test_id'])
    #send_weibo(client, auth_token, user_id, to_name = form['to_name'], test_id = form['test_id'])
    return render_template('hehe.html', hehe = u"邀请已发送")

@app.route('/score')
def score():
    expires = session['expires']
    auth_token = session['auth_token']
    user_id = session['user_id']
    user_name = session['user_name']
    client = APIClient(APP_KEY, APP_SECRET, 'http://apps.weibo.com/socialfaqfaq')
    client.set_access_token(auth_token, expires)
    
    score_list = []
    a = []
    l = manage.get_question_invate(user_name)
    for i in l:
        a.append(i)
    while len(a) != 0:
        t = a[0][3]
        s = 0
        score_l = []
        ta = []
        for x in a:
            if int(x[3]) == int(t):
                s = s + 1
            else:
                ta.append(x)
        a = ta
        ta = []
        lt = manage.get_test(long(t))
        for i in lt:
	        score_l.append(i[5])
        score_l.append(0)
        score_l.append(s)
        score_l.append(t)
        score_list.append(score_l)
        
    a = []
    l = manage.get_answer_invate(user_name)
    for i in l:
        a.append(i)
    while len(a) != 0:
        t = a[0][3]
        s = 0
        score_l = []
        my_score = 0
        all_score = []
        for x in a:
            if x[3] == t:
                if x[2] == user_name:
                    my_score = x[4]
                all_score.append(x[4])
                a.remove(x)
                s = s + 1
        all_score.sort(reverse = True)
        lt = manage.get_test(long(t))
        for i in lt:
	        score_l.append(i[5])
        score_l.append(all_score.index(my_score) + 1)
        score_l.append(s)
        score_l.append(t)
        score_list.append(score_l)
        
    #return render_template('hehe.html', hehe = y)
    return render_template('score.html', score_list = score_list)

@app.route('/answer', methods = ['GET', 'POST'])
def answer():
    signed_request = request.form['signed_request']
    client = APIClient(APP_KEY, APP_SECRET, 'http://app.weibo.com/socialfaqfaq')
    data = client.parse_signed_request(signed_request)
    user_id = data.get('uid', '')
    auth_token = data.get('oauth_token', '')
    if not user_id or not auth_token:
        return render_template("auth.html")
    expires = data.expires
    client.set_access_token(auth_token, expires)
    user_name = get_name(client = client, auth_token = auth_token, user_id = user_id)
    
    session['user_id'] = user_id
    session['auth_token'] = auth_token
    session['expires'] = expires
    session['user_name'] = user_name

    if(1):
        t = []
        rr = manage.get_test(tid = request.args['test_id'])

        for r in rr:
            t.append(r[5])
        
        s = str(r[2]).split(' ')
        a = []
        for k in s:
            if k != '':
                w = manage.get_select(qid = long(k))
                m = 0
                for m in w:
                    m = m
                a.append(m)
        t.append(a)
        a = []
        
        s = str(r[3]).split(' ')
        for k in s:
            if k != '':
                w = manage.get_blank(qid = long(k))
                m = 0
                for m in w:
                    m = m
                a.append(m)
        t.append(a)
        #return render_template('hehe.html', hehe = a)
        
        s = str(r[4]).split(' ')
        a = []
        for k in s:
            if k != '':
                w = manage.get_answer(qid = long(k))
                m = 0
                for m in w:
                    m = m
                a.append(m)
        t.append(a)
        
        t.append(request.args['test_id'])
        
    return render_template('answer.html', t = t)
    
@app.route('/preview', methods = ['GET', 'POST'])
def preview():
    expires = session['expires']
    auth_token = session['auth_token']
    user_id = session['user_id']
    user_name = session['user_name']
    client = APIClient(APP_KEY, APP_SECRET, 'http://apps.weibo.com/socialfaqfaq')
    client.set_access_token(auth_token, expires)
    
    t = []
    rr = manage.get_test(tid = request.args['test_id'])

    for r in rr:
        t.append(r[5])
       
        s = str(r[2]).split(' ')
        for k in s:
            if k != '':
                w = manage.get_select(qid = long(k))
                m = 0
                for m in w:
                    m = m
                t.append([0, m[2], m[3], m[4], m[5], m[6], m[7]])
                
        s = str(r[3]).split(' ')
        for k in s:
            if k != '':
                w = manage.get_blank(qid = long(k))
                m = 0
                for m in w:
                    m = m
                t.append([1, m[2]])
        
        s = str(r[4]).split(' ')
        a = []
        for k in s:
            if k != '':
                w = manage.get_answer(qid = long(k))
                m = 0
                for m in w:
                    m = m
                t.append([2, m[2], m[3]])
        
    #return render_template('hehe.html', hehe = t)
    return render_template('preview.html', preview_list = t)
        
@app.route('/cal', methods = ['GET', 'POST'])
def cal():
    expires = session['expires']
    auth_token = session['auth_token']
    user_id = session['user_id']
    user_name = session['user_name']
    client = APIClient(APP_KEY, APP_SECRET, 'http://apps.weibo.com/socialfaqfaq')
    client.set_access_token(auth_token, expires)
    
    if request.method == 'POST':
        rr = manage.get_test(tid = request.form['test_id'])
        r = 0
        for r in rr:
            r = r
            
        correct = 0
        discorrect = 0
        
        s = r[2].split(' ')
        a = []
        for k in s:
            if k != '':
                w = manage.get_select(qid = int(k))
                m = 0
                for m in w:
                    m = m
                if int(m[7]) == int(request.form[str(k)]):
                    correct += 1
                else:
                    discorrect += 1
        
        s = r[3].split(' ')
        for k in s:
            if k != '':
                w = manage.get_blank(qid = long(k))
                m = 0
                for m in w:
                    m = m
                if m[2].split("^_^")[1] == request.form[str(int(k) + 10000)]:
                    correct += 1
                else:
                    discorrect += 1
        
        s = r[4].split(' ')
        a = []
        for k in s:
            if k != '':
                w = manage.get_answer(qid = long(k))
                m = 0
                for m in w:
                    m = m
                if m[3] == request.form[str(int(k) + 1000000)]:
                    correct += 1
                else:
                    discorrect += 1
                    
        score = 100 * correct / (correct + discorrect)
        #return render_template('hehe.html', hehe = user_name)
        manage.cal_invate(user_name, request.form['test_id'], score)
        return render_template('hehe.html', hehe = score)
    return render_template('index.html')

@app.route('/rank', methods = ['GET', 'POST'])
def rank():
    expires = session['expires']
    auth_token = session['auth_token']
    user_id = session['user_id']
    user_name = session['user_name']
    client = APIClient(APP_KEY, APP_SECRET, 'http://apps.weibo.com/socialfaqfaq')
    client.set_access_token(auth_token, expires)
    
    rr = manage.get_invate(test_id = request.args['test_id'])

    rank_list = []
    for r in rr:
        if len(rank_list) == 0:
            xx = manage.get_test(tid = r[3])
            ll = []
            for x in xx:
            	ll.append(x[5])
            ll.append(r[1])
            rank_list.append(ll)
        l = []
        l.append(r[2])
        l.append(r[4])
        rank_list.append(l)
        
    #return render_template('hehe.html', hehe = t)
    return render_template('rank.html', rank_list = rank_list)