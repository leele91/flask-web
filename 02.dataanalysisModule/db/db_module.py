import sqlite3

def get_regional_data(date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = 'select * from region where stdDay=?;'
    cur.execute(sql, (date,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows