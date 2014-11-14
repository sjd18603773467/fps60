import MySQLdb
#from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

def connect_db():
    #conn = MySQLdb.connect(host = MYSQL_HOST, user = MYSQL_USER, passwd = MYSQL_PASS, db = MYSQL_DB, port = int(MYSQL_PORT), charset = 'utf8')
    conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '123456asdf', db = 'app_socialfaq')
    return conn, conn.cursor()

def disconnect_db(conn, cur):
    cur.close()
    conn.close()

def check(username, password):
    conn, cur = connect_db()
    n = cur.execute('select user_password from user where user_name=%s', username)
    if n:
        for p in cur:
            if p[0] == password:
                disconnect_db(conn, cur)
                return True
    disconnect_db(conn, cur)
    return False

def get_userid(username):
    conn, cur = connect_db()
    cur.execute('select user_id from user where user_name=%s', username)
    for p in cur:
        return p[0]

def add_select(uid, form):
    conn, cur = connect_db()
    cur.execute('insert into select_question (user_id, question, answer_a, answer_b, answer_c, answer_d, answer_right) values (%d, "%s", "%s", "%s", "%s", "%s", "%s")' % (uid, form['question'], form['a'], form['b'], form['c'], form['d'], form['right_select']))
    disconnect_db(conn, cur)

def add_blank(uid, form):
    conn, cur = connect_db()
    cur.execute('insert into blank_question (user_id, question) values (%d, "%s")' % (uid, form['question']))
    disconnect_db(conn, cur)

def add_answer(uid, form):
    conn, cur = connect_db()
    cur.execute('insert into answer_question (user_id, question, answer) values (%d, "%s", "%s")' % (uid, form['question'], form['answer']))
    disconnect_db(conn, cur)

def all_select():
    conn, cur = connect_db()
    cur.execute('select * from select_question')
    disconnect_db(conn, cur)
    return cur

def all_blank():
    conn, cur = connect_db()
    cur.execute('select * from blank_question')
    disconnect_db(conn, cur)
    return cur

def all_answer():
    conn, cur = connect_db()
    cur.execute('select * from answer_question')
    disconnect_db(conn, cur)
    return cur

def add_test(uid, form):
    conn, cur = connect_db()
    sids = ""
    bids = ""
    aids = ""
    for (k, v) in form.items():
        if k != 'introduction':
            if int(k) > 1000000:
                aids = aids + " " + str(int(k)-1000000)
            elif int(k) > 10000:
                bids = bids + " " + str(int(k)-10000)
            else:
                sids = sids + " " + k
    print sids, bids, aids
    cur.execute('insert into test (user_id, select_ids, blank_ids, answer_ids, introduction) values (%d, "%s", "%s", "%s", "%s")' % (uid, sids, bids, aids, form['introduction']))
    disconnect_db(conn, cur)

def all_test(uid):
    conn, cur = connect_db()
    cur.execute('select * from test')
    disconnect_db(conn, cur)
    return cur

def get_test(tid):
    conn, cur = connect_db()
    cur.execute('select * from test where test_id = %d' % long(tid))
    disconnect_db(conn, cur)
    return cur

def get_select(qid):
    conn, cur = connect_db()
    cur.execute('select * from select_question where qestion_id = %d' % long(qid))
    disconnect_db(conn, cur)
    return cur

def get_blank(qid):
    conn, cur = connect_db()
    cur.execute('select * from blank_question where qestion_id = %d' % long(qid))
    disconnect_db(conn, cur)
    return cur

def get_answer(qid):
    conn, cur = connect_db()
    cur.execute('select * from answer_question where qestion_id = %d' % long(qid))
    disconnect_db(conn, cur)
    return cur
