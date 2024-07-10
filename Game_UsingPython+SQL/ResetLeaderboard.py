import mysql.connector

cn = mysql.connector.connect(
    host='sql12.freesqldatabase.com',
    user='sql12717584',
    password="TDeaTpMLXd",
)

cur = cn.cursor()
databaseName = "sql12717584"
tableName = 'leaderboard'

# cur.execute(f"CREATE DATABASE IF NOT EXISTS {databaseName}")
cur.execute(f"USE {databaseName}")


def showAll():
    global cn
    global cur
    
    query="select * from leaderboard order by score desc"
    cur.execute(query)
    results = cur.fetchall()

    return results

query = f"Delete from {tableName}"
cur.execute(query)
results = cur.fetchall()
print(results)
cur.execute("select * from leaderboard")
results = cur.fetchall()
print(results)
print(showAll())
cn.commit()
cn.close()