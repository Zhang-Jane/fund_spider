import pymysql


def get_tasks(db_host, database, table, port, user, passwd):
    result = None
    connect = pymysql.connect(
        host=db_host,
        db=database,
        port=port,
        user=user,
        passwd=passwd,
        charset='utf8'
    )
    cursor = connect.cursor()
    sql = f'SELECT fund_id, fund_title FROM {table}'
    try:
        result = cursor.execute(sql)
        connect.commit()
    except Exception:
        connect.rollback()
    finally:
        connect.close()
    if result:
        return cursor.fetchall()

