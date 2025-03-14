import psycopg2
import bcrypt
#!!!!!!!!!!!!!!!!!!!!
#storage_url=environ.get("EMP_STORAGE_URI")

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
       # params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.conn = psycopg2.connect(host="10.152.183.23",
                                                database="postgresdb",
                                                user="admin",
                                                password="pslicom")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        #print('PostgreSQL database version:')

        # sql = """INSERT INTO users (username, password, created_on )
        #              VALUES(%s) RETURNING id;"""
        # command= "INSERT INTO users (username, password, created_on ) VALUES ( 'icom_nikos2',  crypt('icom_nikos_!', gen_salt('bf')), current_timestamp);"
        # cur.execute(command)
        #
        # id = cur.fetchone()[0]
        # # commit the changes to the database
        # conn.commit()
        #


        #query!!!
        # postgreSQL_select_Query= "SELECT id FROM users  WHERE username = 'icom_nikos' AND password = crypt('icom_nikos_!', password);"
        _username='###'
        _password='####!'
        postgreSQL_select_Query= "SELECT id FROM users  WHERE username = '" +_username + "' AND password = crypt('"+_password+"', password);"
        cur.execute(postgreSQL_select_Query)
        print("CHECK IF USER EXISTS")
        users = cur.fetchall()
        if not users:
            print("User not authorized")
        else:
            print("User authorized")

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)

        # insert user
        cur.execute('SELECT version()')
        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


# def insert_users(username, passowrd):
#     try:
#         print(a)
#     except Exception as ce_:
#         raise Exception("An exception occurred :", ce_)
#


if __name__ == '__main__':
    connect()



#how to create table
#CREATE TABLE users( id SERIAL PRIMARY KEY, role TEXT NOT NULL, username TEXT NOT NULL UNIQUE, email TEXT UNIQUE, password TEXT NOT NULL, token TEXT, created_on TIMESTAMP);


#how to insert user:
# INSERT INTO users (username, password, created_on ) VALUES (
#   'icom_nikos',
#   crypt('testp@assword', gen_salt('bf'), current_timestamp)
# );


# INSERT INTO users (role, username, password, created_on ) VALUES ( 'user', 'icom_user', crypt('icom_user_!@', gen_salt('bf')), current_timestamp);


#UPDATE

#sql_update_query = """Update mobile set price = %s where id = %s"""
#cursor.execute(sql_update_query, (price, mobileId))
#how to check validate user
# SELECT id FROM users  WHERE username = 'icom_nikos' AND password = crypt('icom_nikos_1', password);


#how to connect (deployed using k8s)
#kubectl exec -it postgres-7dd79fb55c-rkpd7 -n piedge-system --  psql -h localhost -U admin --password -p 5432 postgresdb