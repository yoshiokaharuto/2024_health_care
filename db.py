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

def user_profile(user_id,birthday,height,weight,target_weight,target_sleep,daily_excercise):
    
    sql = "INSERT INTO profiles VALUES(default,%s,%s,%s,%s,%s,%s,%s)"
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        cursor.execute(sql,(user_id,birthday,height,weight,target_weight,target_sleep,daily_excercise))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count

def insert_meal(user_id, date, meal_type):
    sql = "INSERT INTO meals VALUES (default,%s, %s, %s) RETURNING meal_id"
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (user_id, date, meal_type))
        meal_id = cursor.fetchone()

        if meal_id:
            meal_id = meal_id[0]
            connection.commit()
        else:
            meal_id = None

    except psycopg2.DatabaseError as e:
        meal_id = None
    finally:
        cursor.close()
        connection.close()

    return meal_id

def insert_meal_item(meal_id,meal_detail):
    sql = "INSERT INTO meal_items VALUES (default,%s,%s)"
    result = True
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (meal_id,meal_detail))
        connection.commit()
    except psycopg2.DatabaseError:
        result = False
    finally:
        cursor.close()
        connection.close()
    return result

def insert_exercise_record(user_id,date,exercise_time,exercise_detail):
    
    sql = "INSERT INTO exercise_records VALUES (default,%s,%s,%s,%s)"
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(user_id,date,exercise_detail,exercise_time))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count 

def insert_health_record(user_id,date,sleep_time,weight,water_intake):
    
    sql = "INSERT INTO health_records VALUES (default,%s,%s,%s,%s,%s)"
    
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(user_id,date,sleep_time,weight,water_intake))
        count = cursor.rowcount
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()
    return count 

def meal_list(user_id):
    sql = "SELECT meals.date, meals.meal_type, meal_items.food_name FROM meals INNER JOIN meal_items ON meals.meal_id = meal_items.meal_id WHERE meals.user_id =%s;"
    
    connection = get_connection()
    cursor  = connection.cursor()
    
    cursor.execute(sql,(user_id,))
    
    rows = cursor.fetchall()
    
    connection.close()
    cursor.close()
    
    return rows

def meal_search(user_id,meal_date):
    sql = "SELECT meals.date, meals.meal_type, meal_items.food_name FROM meals INNER JOIN meal_items ON meals.meal_id = meal_items.meal_id WHERE meals.user_id =%s AND meals.date = %s;"
    
    connection = get_connection()
    cursor  = connection.cursor()
    
    cursor.execute(sql,(user_id,meal_date))
    
    rows = cursor.fetchall()
    
    connection.close()
    cursor.close()
    
    return rows

def health_list(user_id):
    sql = "SELECT date,sleep_hours,weight,water_intake FROM health_records WHERE user_id = %s;"
    
    connection = get_connection()
    cursor  = connection.cursor()
    
    cursor.execute(sql,(user_id,))
    
    rows = cursor.fetchall()
    
    connection.close()
    cursor.close()
    
    return rows

def health_search(user_id,health_date):
    sql = "SELECT date,sleep_hours,weight,water_intake FROM health_records WHERE user_id = %s AND date = %s;"
    
    connection = get_connection()
    cursor  = connection.cursor()
    
    cursor.execute(sql,(user_id,health_date))
    
    rows = cursor.fetchall()
    
    connection.close()
    cursor.close()
    
    return rows