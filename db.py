import os,psycopg2,string,random,hashlib

def get_connection():
    url = os.environ['DATABASE_URL1']
    connection = psycopg2.connect(url)
    return connection

def get_salt():
    charset = string.ascii_letters + string.digits
    salt = ''.join(random.choice(charset,k=30))
    return salt

def get_hash(password,salt):
    b_pw = bytes(password,'urf-8')
    b_salt = bytes(salt,'utf-8')
    
    hashed_pw = hashlib.pbkdf2_hmac('sha-256',b_pw,b_salt,1000).hex()
    
    return hashed_pw