import MySQLdb
from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)

def connect_db():
    conn = MySQLdb.connect(host = MYSQL_HOST, user = MYSQL_USER, passwd = MYSQL_PASS, db = MYSQL_DB, port = int(MYSQL_PORT), charset = 'utf8')
    #conn = MySQLdb.connect(host = 'localhost', user = 'root', passwd = '123456asdf', db = 'app_socialfaq')
    return conn, conn.cursor()

def disconnect_db(conn, cur):
    cur.close()
    conn.close()

def add_select(user_name, form):
    conn, cur = connect_db()
    cur.execute('insert into select_question (user_name, question, answer_a, answer_b, answer_c, answer_d, answer_right) values ("%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (user_name, form['question'], form['a'], form['b'], form['c'], form['d'], form['right_select']))
    disconnect_db(conn, cur)

def add_blank(user_name, form):
    conn, cur = connect_db()
    cur.execute('insert into blank_question (user_name, question) values ("%s", "%s")' % (user_name, form['question']))
    disconnect_db(conn, cur)

def add_answer(user_name, form):
    conn, cur = connect_db()
    cur.execute('insert into answer_question (user_name, question, answer) values ("%s", "%s", "%s")' % (user_name, form['question'], form['answer']))
    disconnect_db(conn, cur)

def all_select(user_name):
    conn, cur = connect_db()
    cur.execute('select * from select_question where user_name = "%s"' % user_name)
    disconnect_db(conn, cur)
    return cur

def all_blank(user_name):
    conn, cur = connect_db()
    cur.execute('select * from blank_question where user_name = "%s"' % user_name)
    disconnect_db(conn, cur)
    return cur

def all_answer(user_name):
    conn, cur = connect_db()
    cur.execute('select * from answer_question where user_name = "%s"' % user_name)
    disconnect_db(conn, cur)
    return cur

def add_test(user_name, form):
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
    cur.execute('insert into test (user_name, select_ids, blank_ids, answer_ids, introduction) values ("%s", "%s", "%s", "%s", "%s")' % (user_name, sids, bids, aids, form['introduction']))
    disconnect_db(conn, cur)

def add_invate(from_name, to_name, test_id):
    conn, cur = connect_db()
    cur.execute('insert into invate (from_name, to_name, test_id, score) values ("%s", "%s", %d, %d)' % (from_name, to_name, long(test_id), -1))
    disconnect_db(conn, cur)
    
def cal_invate(to_name, test_id, score):
    conn, cur = connect_db()
    cur.execute('update invate set score = %d where to_name = "%s" and test_id = %d' % (score, to_name, int(test_id)))
    disconnect_db(conn, cur)

def all_test(user_name):
    conn, cur = connect_db()
    cur.execute('select * from test where user_name = "%s"' % user_name)
    disconnect_db(conn, cur)
    return cur

def get_test(tid):
    conn, cur = connect_db()
    cur.execute('select * from test where test_id = %d' % long(tid))
    disconnect_db(conn, cur)
    return cur

def get_select(qid):
    conn, cur = connect_db()
    cur.execute('select * from select_question where question_id = %d' % long(qid))
    disconnect_db(conn, cur)
    return cur

def get_blank(qid):
    conn, cur = connect_db()
    cur.execute('select * from blank_question where question_id = %d' % long(qid))
    disconnect_db(conn, cur)
    return cur

def get_answer(qid):
    conn, cur = connect_db()
    cur.execute('select * from answer_question where question_id = %d' % long(qid))
    disconnect_db(conn, cur)
    return cur

def get_question_invate(user_name):
    conn, cur = connect_db()
    cur.execute('select * from invate where from_name = "%s"' % user_name)
    disconnect_db(conn, cur)
    return cur

def get_answer_invate(user_name):
    conn, cur = connect_db()
    cur.execute('select * from invate where to_name = "%s"' % user_name)
    disconnect_db(conn, cur)
    return cur

def get_invate(test_id):
    conn, cur = connect_db()
    cur.execute('select * from invate where test_id = %d order by score desc' % long(test_id))
    disconnect_db(conn, cur)
    return cur