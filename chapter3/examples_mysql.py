import pymysql
from consts import HOSTNAME,DATABASE,USERNAME,PASSWORD

try:
    con=pymysql.connect(HOSTNAME,USERNAME,PASSWORD,DATABASE)#数据库连接的一个实例
    cur=con.cursor()# 返回一个有表
    cur.execute("drop table if EXISTS users")
    cur.execute('create table users(Id INT PRIMARY KEY AUTO_INCREMENT,Name VARCHAR (25))')
    cur.execute('insert into users(Name) values ("xiaoming")')
    cur.execute("insert into users(Name) values ('chenmingwei')")
    cur.execute('select * from users')

    rows=cur.fetchall()
    for row in rows:
        print(row)
except pymysql.Error as e:
    print("Error %d:%s"%(e.args[0],e.args[1]))
    exit(1)
con.close()