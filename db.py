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
    b_pw = bytes(password,'utf-8')
    b_salt = bytes(salt,'utf-8')
    
    hashed_pw = hashlib.pbkdf2_hmac('sha256',b_pw,b_salt,1000).hex()
    
    return hashed_pw

def user_register(mail,password):
    sql = "INSERT INTO health_users VALUES(default,%s,%s,%s)"
    salt = get_salt()
    hashed_pw = get_hash(password,salt)
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(mail,hashed_pw,salt))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count 