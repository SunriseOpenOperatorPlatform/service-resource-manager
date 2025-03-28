import psycopg2
import bcrypt

import connexion
from swagger_server.controllers import authorization_controller
import os
import logging


# postgres_host=os.environ["SYSTEM_DATABASE_HOST"].strip()
# postgres_password=os.environ["SYSTEM_DATABASE_PASSWORD"].strip()

#postgres_host="postgres"
#postgres_password="pslicom"

def validate_user(_username, _password):
    """ Connect to the PostgreSQL database server """
    conn = None

    try:

        conn = psycopg2.conn = psycopg2.connect(host=postgres_host,
                                                database="postgresdb",
                                                user="admin",
                                                password=postgres_password)

        #conn = psycopg2.conn = psycopg2.connect(host="10.152.183.160", database="postgresdb", user="admin", password="pslicom")

        # create a cursor

        cur = conn.cursor()
        #query

        postgreSQL_select_Query = "SELECT id FROM users  WHERE username = '" + _username + "' AND password = crypt('" + _password + "', password);"

        cur.execute(postgreSQL_select_Query)
        #print("CHECK IF USER EXISTS")
        users = cur.fetchall()


        # sql_update_query = """Update users set email = %s where id = %s"""
        # cur.execute(sql_update_query, ("nikpsarom@intracom-telecom.com", 1))
        # conn.commit()
        # count = cur.rowcount
        # print(count, "Record Updated successfully ")

        if not users:
            #print("User not authorized")
            logging.info("user not found!!!")
            cur.close()
            if conn is not None:
                conn.close()
                #print('Database connection closed.')
            return None
        else:
            #print("User authorized")
            cur.close()
            if conn is not None:
                conn.close()
                #print('Database connection closed.')
            for user in users:
                user_id = user[0]
                break
            return user_id
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.warning("Can't connect to postgresdb")
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    #         print('Database connection closed.')



def update_user_info(identifier, value_id, type_input, value_input):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        conn = psycopg2.conn = psycopg2.connect(host=postgres_host,
                                                database="postgresdb",
                                                user="admin",
                                                password=postgres_password)

        # create a cursor
        cur = conn.cursor()
        # query


        if type_input is "token":
            sql_update_query = """Update users set """ + str(type_input) + """ = %s where """ + str(identifier) + """ = %s"""
          #  sql_update_query = "Update users set " + str(type_input) +  =  crypt('+ str(value_input)'+,gen_salt('bf'))  where  + str(identifier) + """ = %s"""
        else:
            sql_update_query = """Update users set """ + str(type_input) + """ = %s where """ + str(identifier) + """ = %s"""

        cur.execute(sql_update_query,(value_input, value_id))
        conn.commit()
        count = cur.rowcount
        #print(count, "Record Updated successfully ")

        if conn is not None:
            conn.close()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def check_role():
    bearer = connexion.request.headers['Authorization']
    token = bearer.split()[1]

    token_=authorization_controller.decode_token(token)

    tok=token_['sub'].split("_/_")
    conn = None
    try:
        conn = psycopg2.conn = psycopg2.connect(host=postgres_host,
                                                database="postgresdb",
                                                user="admin",
                                                password=postgres_password)
        # create a cursor
        cur = conn.cursor()
        # query
        #postgreSQL_select_Query = "SELECT role FROM users  WHERE token = '" + token + "';"
        #OR
        postgreSQL_select_Query = "SELECT role FROM users  WHERE username = '" + tok[1] + "';"

        cur.execute(postgreSQL_select_Query)
        # print("CHECK IF USER EXISTS")
        users = cur.fetchall()

        if not users:
            # print("User not authorized")
            cur.close()
            if conn is not None:
                conn.close()
                # print('Database connection closed.')
            return None
        else:

            cur.close()
            if conn is not None:
                conn.close()
            for user in users:
                user_role = user[0]
                break
            return user_role
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
