import os,psycopg2,string,random,hashlib

def get_connection():
    url = os.environ['DATABASE_URL1']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choices(charset,k=30))
    return salt

def get_hash(password,salt):
    hashed_pw = hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt.encode('utf-8'),1000).hex()
    
    return hashed_pw

def user_register(mail,password,salt):
    sql = "INSERT INTO health_users VALUES(default,%s,%s,%s)"
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(mail,password,salt))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count 