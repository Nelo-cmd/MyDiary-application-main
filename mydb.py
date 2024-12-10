#import connector
import mysql.connector
import os

#create connection function
def connect_db():

    #set the mysql connector to connect to your database
    mydb = mysql.connector.connect(host = "diarydb-2.c328y0qm82x3.us-west-2.rds.amazonaws.com",
                                   user = "root",
                                   password = os.getenv('SECRET_KEY')[0:-1],
                                   database = "diarydb")
    
    #check if database is connected
    if mydb.is_connected():
        print("database connected.")
    else:
        print("error connecting to database")

    #return connection pool
    return mydb

#function to get data from database
def getusernamecolumn(username):
    connect = connect_db()
    conn = connect.cursor()
    conn.execute("SELECT * FROM user_info where username = '{}'".format(username))
    data = conn.fetchall()
    return data

def getEmailcolumn(Email):
    connect = connect_db()
    conn = connect.cursor()
    conn.execute("SELECT * FROM user_info where Email = '{}'".format(Email))
    data = conn.fetchall()
    return data

#fuction to add user to database
def adduser(Username, Email, Password):
    connect = connect_db()
    conn = connect.cursor()
    inputdata = (Username,Email,Password)
    query = "INSERT INTO user_info(username, email, password) VALUES('{0}','{1}','{2}')".format(inputdata[0], inputdata[1], inputdata[2])
    conn.execute(query)
    connect.commit()
    conn.close()
    
#function to get the password using the user email
def getpassword(Email,Username):
    connect = connect_db()
    conn = connect.cursor()
    conn.execute("SELECT password FROM user_info where Email = '{}' or Username = '{}'".format(Email,Username))
    data = conn.fetchone()
    conn.close()
    return data[0]



def getuser_id(Username, Email):
    connect = connect_db()
    conn = connect.cursor()
    conn.execute("SELECT user_id FROM user_info where username = '{}' or Email = '{}'".format(Username, Email))
    data = conn.fetchone()
    conn.close()
    return data[0]

def getposts():
    connect = connect_db()
    conn = connect.cursor()
    conn.execute("""  SELECT post_id, post_content,file_extension, file_data, time, user_info.username
                    FROM posts
                    JOIN user_info ON posts.user_id = user_info.user_id
                    ORDER BY time DESC;""")
    data = conn.fetchall()
    conn.close()
    return data

def getmyposts(user_id):
    connect = connect_db()
    conn = connect.cursor()
    conn.execute("""  SELECT post_id, post_content,file_extension, file_data, time, user_info.username
                    FROM posts
                    JOIN user_info ON posts.user_id = user_info.user_id
                    WHERE posts.user_id = '{}'
                    ORDER BY time DESC;;""".format(user_id))
    data = conn.fetchall()
    conn.close()
    return data

def get_post_id_post(post_id):
    connect = connect_db()
    conn = connect.cursor()
    conn.execute("""  SELECT post_id, post_content,file_extension, file_data, time, user_info.username
                    FROM posts
                    JOIN user_info ON posts.user_id = user_info.user_id
                    WHERE posts.post_id = '{}'
                    ORDER BY time DESC;;""".format( post_id))
    data = conn.fetchone()
    conn.close()
    return data


def addentry(Entry,user_id, file_extension,file_data, time):
    connect = connect_db()
    conn = connect.cursor()
    query = "INSERT INTO posts(post_content, user_id, file_extension, file_data, time) VALUES(%s,%s,%s,%s,%s)"
    values = (Entry, user_id, file_extension, file_data, time)
    conn.execute(query,values)
    connect.commit()
    conn.close()

def getpostuserid(post_id):
    connect = connect_db()
    conn = connect.cursor()
    conn.execute("SELECT user_id FROM posts where post_id = '{}'".format(post_id))
    data = conn.fetchone()
    conn.close()
    return data

def deleteuserpost(post_id):
    connect = connect_db()
    conn = connect.cursor()
    query = "delete from posts where post_id = '{}'".format(post_id)
    conn.execute(query)
    connect.commit()
    conn.close()