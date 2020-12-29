import sqlite3

def get_region_daily(date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = 'select * from region where stdDay=? order by incDec desc;'
    cur.execute(sql, (date,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def write_region(params):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    #print(params)
    sql = '''insert into region(createDt, gubun, deathCnt, incDec, isolClearCnt, qurRate,
            stdDay, defCnt, isolIngCnt, overFlowCnt, localOccCnt) values(?,?,?,?,?,?,?,?,?,?,?);'''
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()
    return

def get_agender_daily(date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = 'select * from agender where stdDay=?;'
    cur.execute(sql, (date,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def write_agender(params):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()
    #print(params)
    sql = '''insert into agender(stdDay, confCase, confCaseRate, death, deathRate,
            criticalRate, gubun, seq, updateDt) values(?,?,?,?,?,?,?,?,?);'''
    cur.execute(sql, params)
    conn.commit()

    cur.close()
    conn.close()
    return

def get_region_items_by_gubun(items, gubun):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from region where gubun=?;'
    cur.execute(sql, (gubun,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_region_items_by_gubun_with_date(items, gubun, start_date, end_date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from region where gubun=? and stdDay between ? and ?;'
    cur.execute(sql, (gubun, start_date, end_date))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_agender_items_by_gubun(items, gubun):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from agender where gubun=?;'
    cur.execute(sql, (gubun,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_agender_items_by_gubun_with_date(items, gubun, start_date, end_date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from agender where gubun=? and stdDay between ? and ?;'
    cur.execute(sql, (gubun, start_date, end_date))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_seoul_items_by_gu(items, gu):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from seoul where region=?;'
    cur.execute(sql, (gu,))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows

def get_seoul_items_by_condition(items, gu, start_date, end_date):
    conn = sqlite3.connect('./db/covid.db')
    cur = conn.cursor()

    sql = f'select {items} from seoul where region=? and confDay between ? and ?;'
    cur.execute(sql, (gu, start_date, end_date))
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    return rows
