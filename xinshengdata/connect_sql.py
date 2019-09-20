import pymysql


# 执行sql语句
class Create_Query:
    def __init__(self):
        '''实例化的时候创建连接'''
        self.conn = pymysql.connect(user='root', password='qwe123', database='xscm', charset='utf8')
        self.cur = self.conn.cursor()

    def my_qurey(self, sql):
        '''sql语句的编写'''
        self.cur.execute(sql)
        return self.cur.fetchall()

    def __del__(self):
        '''关闭游标，关闭连接'''
        self.cur.close()
        self.conn.close()



if __name__ == '__main__':
    create_query = Create_Query()
    create_query.my_qurey('select * from livedata')