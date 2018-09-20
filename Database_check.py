from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras
import pprint

app = Flask(__name__)


class PostgresConnection(object):

    instance = None
    con = None

    def __new__(cls):
        if PostgresConnection.instance is None:
            PostgresConnection.instance = object.__new__(cls)
        return PostgresConnection.instance

    def __init__(self):
        if PostgresConnection.con is None:
            try:
                PostgresConnection.con = psycopg2.connect("dbname=postgres user=postgres password=openpg123")
                print('Database connection opened.')
            except psycopg2.DatabaseError as db_error:
                print("Error :(0)".format(db_error))
        else:
            print(PostgresConnection.con)

    def __del__(self):
        if PostgresConnection.con is not None:
            PostgresConnection.con.close()
            print('Database connection closed.')


# obj1=PostgresConnection()
# cur=obj1.con.cursor()
# cur.execute("CREATE TABLE student(id serial PRIMARY KEY, name varchar(20), age integer NOT NULL)")
# cur.execute("SELECT * FROM VOTE")
# row= cur.fetchall()
# print(row)