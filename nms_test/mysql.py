##!/usr/bin/python
# -*- coding: utf-8 -*-

"""Methods for handling MySQL database"""

import MySQLdb

class MysqlClass:
    """Class that works with SQL database"""

    def __init__(self):
        """While initilizing instance, nothing happend, so this call is cheap,
           actual connect will be done while executing connect"""
        self._db_link = None
        self._cursor = None
        self.connect_flag = False

    def connect(self, host="127.0.0.1", port=3306, user="rebrain", passwd="test", db="test"):
        """Connect to Database. link is stored in self._db_link"""

        try:
            db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db)
            self.connect_flag = True
            self._db_link = db
            cursor = db.cursor(MySQLdb.cursors.DictCursor)
            self._cursor = cursor
        except:
            raise Exception("Db connection params are invalid")


    def execute_query(self, query, commit=False):
        """Execute select/update/insert/delete/drop query"""

        try:
            print(f"Executing query: {query}")
            self._cursor.execute(query)
            if commit:
                self._db_link.commit()
            result = self._cursor.fetchall()
            return result
        except:
            return None

    def select_list(self, query, column):
        """Return items in specific column as a list"""
        result = self.execute_query(query)
        list = []
        for row in result:
            if column in row:
                list.append(row[column])
        return list

    def select_row(self, query):
        """Execute query and return first row of result as a dictionary"""

        try:
            print(f"Executing query: {query}")
            self._cursor.execute(query)
            result = self._cursor.fetchone()
            return result
        except:
            return None


    def disconnect(self):
        """Close connection and disconnect from DB"""

        if self.connect_flag == True:
            self._cursor.close()
            self._db_link.close()
            self.connect_flag == False
