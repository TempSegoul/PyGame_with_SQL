import mysql.connector

cn = mysql.connector.connect(
    host='sql12.freesqldatabase.com',
    user='sql12717584',
    password="TDeaTpMLXd",
    # host="localhost",
    # user='root',
    # password="admin"
)

cur = cn.cursor()
databaseName = "sql12717584"
tableName = 'leaderboard'

# cur.execute(f"CREATE DATABASE IF NOT EXISTS {databaseName}")
cur.execute(f"USE {databaseName}")

cur.execute("SHOW TABLES LIKE 'leaderboard'")
if not cur.fetchone():
    cur.execute(f"CREATE TABLE {tableName} (Srno int, Name varchar(30), Score bigint)")

def showAll():
    global cn
    global cur
    
    query="select * from leaderboard order by score desc"
    cur.execute(query)
    results = cur.fetchall()
    
    # print("--------------------------------------------------")
    # print('%5s'%"Player no",'%15s'%'Pname','%12s'%'Score')
    # print("--------------------------------------------------")
    
    count=0
    

    
    # print("-------------- TOTAL RECORD : ",count,"--------------")

    return results

def searchplayer():
    global cn,cur
    
    print("SEARCH PLAYER FORM*")
    
    en = int(input("Enter Player Number To Be Searched :"))
    query="select * from leaderboard where P_no="+str(en)
    cur.execute(query)
    results = cur.fetchall()
    if cur.rowcount<=0:
        print("\## SORRY! NO MATCHING DETAILS AVAILABLE ##")
    
    else:
        print("--------------------------------------------------")
        print('%5s'%"Player no",'%15s'%'Player name','%12s'%'Score')
        print("--------------------------------------------------")
        
        for row in results:
            print('%5s' % row[0],'%15s'%row[1],'%12s'%row[2])

    print("-"*50)

def editid():
    global cn,cur

    print("EDIT PLAYER FORM*")
    
    P_no = int(input("Enter Player Number To Edit :"))
    query="select * from leaderboard where P_no="+str(P_no)
    cur.execute(query)
    results = cur.fetchall()
    
    if cur.rowcount<=0:
        print("\## SORRY! NO MATCHING DETAILS AVAILABLE ##")
    
    else:
        print("--------------------------------------------------")
        print('%5s'%"Player no",'%15s'%'Player name','%12s'%'Score')
        print("--------------------------------------------------")
    
        for row in results:
            print('%5s' % row[0],'%15s'%row[1],'%12s'%row[2])
    
    print("-"*50)
    
    ans = input("Are you sure to update ? (y/n)")
    
    if ans=="y" or ans=="Y":
        New_name = input("Enter new name to update (enter old value if not to update) :")
        query="update leaderboard set P_name='"+New_name+"' where empno="+str(P_no)
        cur.execute(query)
        cn.commit()
    
        print("\n## RECORD UPDATED  ##")

def addplayer(n: int, name: str, s: int) -> bool:
    global cn,cur
    try:
        print("ADD NEW PLAYER*")
        
        # P_no = int(input("Enter Player Number :"))
        # P_name = input("Enter Player Name :")
        # score = int(input("Enter Player Score:"))
        P_no = n
        P_name = name
        score = s
        query=f"insert into leaderboard values({P_no} , '{P_name}',{score})"
        cur.execute(query)
        cn.commit()

        print("\n ## RECORD ADDED SUCCESSFULLY!")
        return True
    
    except Exception:
        return False

def delplayer():
    global cn,cur

    print("DELETE PLAYER FORM*")
    
    P_no = int(input("Enter Player number to delete :"))
    query="select * from leaderboard where P_no="+str(P_no)
    cur.execute(query)
    results = cur.fetchall()
    
    if cur.rowcount<=0:
        print("\## SORRY! NO MATCHING DETAILS AVAILABLE ##")
    
    else:
        print("")
        print('%5s'%"Player no",'%15s'%'Player name','%12s'%'Score')
        print("")
    
        for row in results:
            print('%5s' % row[0],'%15s'%row[1],'%12s'%row[2])
    
    print("-"*50)
    
    ans = input("Are you sure to delete ? (y/n)")
    
    if ans=="y" or ans=="Y":
        query="delete from leaderboard where P_no="+str(P_no)
        cur.execute(query)
        cn.commit()
    
        print("\n## RECORD DELETED  ##")
         
def Functions(a):
    print("1. SHOW PLAYER LIST ")
    print("2. ADD NEW PLAYER")
    print("3. SEARCH PLAYER ")
    print("4. EDIT PLAYER ")
    print("5. DELETE PLAYER ")
    print("6. CONTACT US")
    print("0. EXIT")
    
    # ans = int(input("Enter your choice :"))
    ans = int(a)
    
    if ans==1:
        return showAll()
    
    elif ans==2:
        return addplayer()
    
    elif ans==3:
        searchplayer()
    
    elif ans==4:
        editid()
    
    elif ans==5:
        delplayer()
        
    elif ans==6:
        print("*"*100)
        print(" "*20,"AUTHOR : Lakshay Battu , Ishaan Singh , Shaurya Chawala ")
        print(" "*20,"EMAIL  : lakshayishaanshaurya@GMAIL.COM")
        print("*"*100)
    
    elif ans==0:
        print("\nBye!!")
        cn.close()
    
    else:
        print("wrong input error")

def CloseConnection():
    cn.close()