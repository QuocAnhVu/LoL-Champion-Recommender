#!./env/bin/python
import sqlite3

conn = sqlite3.connect('db/gamedata.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS champions 
          (champid  int            UNIQUE NOT NULL,
          name      varchar(24)    NOT NULL)''')
conn.commit()
conn.close()

conn = sqlite3.connect('db/summoner.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS summoners 
          (id   int         PRIMARY KEY,
          name  varchar(24) NOT NULL)''')
conn.commit()
conn.close()

conn = sqlite3.connect('db/matchid.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS matchids
          (id int PRIMARY KEY)''')
conn.commit()
conn.close()

conn = sqlite3.connect('db/matchdata.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS matches 
          (id       int  PRIMARY KEY,
          timestamp int  NOT NULL,  
          blueWin   bool NOT NULL,
          b1        int  NOT NULL,
          b2        int  NOT NULL,
          b3        int  NOT NULL,
          b4        int  NOT NULL,
          b5        int  NOT NULL,
          r1        int  NOT NULL,
          r2        int  NOT NULL,
          r3        int  NOT NULL,
          r4        int  NOT NULL,
          r5        int  NOT NULL)''')
conn.commit()
conn.close()