from sqlalchemy import create_engine
from consts import DB_URI


eng=create_engine(DB_URI
                  )
with eng.connect() as con:
    con.execute("drop table if EXISTS users")
    con.execute('create table users(Id INT PRIMARY KEY AUTO_INCREMENT,Name VARCHAR (25))')
    con.execute('insert into users(Name) values ("xiaoming")')
    con.execute("insert into users(Name) values ('chentian')")
    rs=con.execute('select * from users')
    for row in rs:
        print(row)
