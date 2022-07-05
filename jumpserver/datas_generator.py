import mysql.connector
import uuid
import random
import string
from faker import Faker
import json

host = '10.1.12.203'
user = 'root'
passwd = 'Password123@mysql'


class MySQLConnector():
    def __init__(self, host, user, passwd, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            passwd=passwd,
            database=database
        )
        self.cursor = self.conn.cursor()

    def rollback(self):
        self.conn.rollback()

    def quit(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()


def uuid_gen():
    return str(uuid.uuid4())


def random_str():
    length_of_string = 8
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))


insert_to_cloud_server = 'INSERT INTO cloud_server (' \
             'id, instance_uuid, workspace_id, account_id, instance_id, ' \
             'instance_name,  instance_status, last_sync_timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

val_of_cloud_server = (uuid_gen(),
                       uuid_gen(),
                       '874df351-906c-4542-9256-155cce629a20',
                       '4e0bfa40-391f-4ff8-8de7-972644d0975e',
                       random_str(),
                       random_str(),
                       'Running',
                       1624597246059)


def execute_sql(cursor, sql, val):
    cursor.execute(sql, val)


if __name__ == '__main__':
    faker = Faker()
    mysqldb = MySQLConnector(host, user, passwd, 'fit2cloud')
    mysqldb.cursor.execute("select count(id) from cloud_server")
    count = mysqldb.cursor.fetchone()
    print(count[0])
    mysqldb.cursor.execute("select management_ip from cloud_server")
    ids = mysqldb.cursor.fetchall()
    # for i in ids:
    #     print(json.dumps(list(i)))
    for id in ids:
        sql = "UPDATE cloud_server SET  ip_array=\'" + json.dumps(list(id)) + "\' WHERE management_ip='"+ str(id[0]) + "';"
        # print(sql)
        try:
            mysqldb.cursor.execute(sql)
            mysqldb.conn.commit()
        except:
            mysqldb.rollback()
    mysqldb.quit()






