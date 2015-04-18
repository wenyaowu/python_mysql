__author__ = 'evanwu'
from mysql.connector import Error, MySQLConnection

from python_mysql_dbconfig import read_db_config


def connection_test():

    db_config = read_db_config()

    try:
        print 'Connecting to database: {0}...'.format(db_config['database'])
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print 'Connection established.'
        else:
            print 'Connection failed.'

    except Error as e:
        print e.message

    finally:
        conn.close()
        print 'Connection closed.'


def connect():

    db_config = read_db_config()

    try:
        print 'Connecting to database: {0}...'.format(db_config['database'])
        conn = MySQLConnection(**db_config)

        if conn.is_connected():
            print 'Connection established.'
            return conn
        else:
            print 'Connection failed.'

    except Error as e:
        print e.message



def query_with_fetchone(query):

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)

    # Fetchone() method to fetch the next row in the result set
    row = cursor.fetchone()

    while row is not None:
        print(row)
        row = cursor.fetchone()

    cursor.close()
    conn.close()


def query_with_fetchall(query):

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    print 'Total Row(s) is {0}'.format(cursor.rowcount)
    for row in rows:
        print(row)

    cursor.close()
    conn.close()


def iter_row(cursor, size):
    while True:
        rows = cursor.fetchmany(size)
        if not rows:
            break
        for row in rows:
            yield row


def query_with_fetchmany(query, size=10):

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query)

    for row in iter_row(cursor, size):
        print(row)

    cursor.close()
    conn.close()


def query_insert(table, query_dict):

    columns = query_dict.keys()
    args = tuple(query_dict.values())
    query = 'INSERT INTO '+table+'('+','.join(columns)+') '\
    +'VALUES' + '(' +','.join(['%s' for i in range(len(columns))])+')'

    query_print = query
    for arg in args:
        query_print = query_print.replace("%s", arg, 1)
    print('executing: '+query_print)

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, args)

    if cursor.lastrowid:
        print 'Last insert ID:' + str(cursor.lastrowid)
    else:
        print 'Last insert ID not found'

    conn.commit()

    cursor.close()
    conn.close()


def query_insertmany(table, columns, value_list):

    query = 'INSERT INTO '+table+'('+','.join(columns)+') '\
    + 'VALUES' + '(' +','.join(['%s' for i in range(len(columns))])+ ')'

    if value_list:
        value_s = str(value_list[0])
    for i in range(1,len(value_list)):
        value_s += (','+str(value_list[i]))

    query_print = 'INSERT INTO '+table+'('+','.join(columns)+') '\
    + 'VALUES' + value_s
    print('executing: '+query_print)

    conn = connect()
    cursor = conn.cursor()
    cursor.executemany(query, value_list)

    conn.commit()

    cursor.close()
    conn.close()

def query_update(table, new_value, filter_condition):
    """
    Update the data in the table.
    :param table: (String) Name of the table to be updated.
    :param new_value: (Dictionary) COLUMN NAME:NEW VALUE pairs.
    :param filter_condition: (String) Filter condition clause.
    """
    if not filter_condition.startswith('WHERE'):
        filter_condition = 'WHERE ' + filter_condition

    data = tuple(new_value.values())
    columns = new_value.keys()

    for i in range(len(columns)):
        columns[i] += '=%s'

    query = 'UPDATE ' + table + ' SET ' + ','.join(columns)+' '+filter_condition

    column_value_pair = ['{0}={1}'.format(key, value) for key, value in new_value.items()]
    query_print = 'UPDATE ' + table + ' SET ' + ','.join(column_value_pair)+' '+filter_condition
    print 'executing: ' + query_print

    # Update the data
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, data)
    # Commit the change
    conn.commit()
    # Close the connection
    cursor.close()
    conn.close()