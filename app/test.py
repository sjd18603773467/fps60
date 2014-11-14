from manage_db import manage

conn, cur = manage.connect_db()

print cur.execute('select * from user')

manage.disconnect_db(conn, cur)
