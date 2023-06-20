#!/usr/bin/env python3

import argparse
import sqlite3
import logging

logging.basicConfig(filename='/home/sergio/PythonWorkspace/emu/project/module.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(lineno)d:%(message)s')


def create_database():
    try:
        conn = sqlite3.connect('sample.db')
        c = conn.cursor()
        c.execute('CREATE TABLE clients (name TEXT, age INTEGER, address TEXT, phone TEXT)')
        c.execute("INSERT INTO clients VALUES ('John', 25, '123 Main St', '555-555-5555')")
        c.execute("INSERT INTO clients VALUES ('Jane', 30, '456 Oak Ave', '555-555-5555')")
        c.execute("INSERT INTO clients VALUES ('Bob', 35, '789 Elm St', '555-555-5555')")
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error('Error occurred while creating database', exc_info=True)
        print('Error occurred while creating database')
        return

def query_database(age):
    try:
        conn = sqlite3.connect('sample.db')
        c = conn.cursor()
        c.execute('SELECT * FROM clients WHERE age=?', (age,))
        result = c.fetchall()
        conn.close()
        return result
    except Exception as e:
        logging.error('Error occurred while querying database', exc_info=True)
        print('Error occurred while querying database')
        return

def program():
    try:
        parser = argparse.ArgumentParser(description='Query the sample database by age of clients.')
        parser.add_argument('age', type=int, help='Specify the age of the clients to query')
        parser.add_argument('-v', '--version', action='version', version='1.0', help='Display program version number')
        args = parser.parse_args()
        create_database()
        result = query_database(args.age)
        print(result)
    except Exception as e:
        logging.error('Error occurred while running program', exc_info=True)
        print('Error occurred while running program')
        return

if __name__ == '__main__':
    program()