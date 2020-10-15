# File name: main.py
# Author: Sandy Haryono <sandyharyono@gmail.com>
# Python Version: 3.7.5

import config.dev as cfg


import sys
import binascii
import socket
import struct
import json
import time
import logging


#mysql
import pymysql.cursors

#include helper
from helper.helper import get_type,BINARY_TYPES
from helper.file.FileOperation import FileOperation


#Software Info
SOFTWARENAME                    = 'Apache2 Log 2 MySQL Importer'
VERSION                         = 'v.1'

# Mysql configuration
DB_HOST                         = cfg.mysql['host']
DB_USER                         = cfg.mysql['user']
DB_PASSWORD                     = cfg.mysql['password']
DB_NAME                         = cfg.mysql['db']
#path folder
PATH_LOG_FILE                   = cfg.apache['logFolder']



 


class MySQLDatabase(object):

    #Constructor
    def __init__(self):
       self.__log = logging.getLogger(__name__)
       self.connection = pymysql.connect(
            host        =   DB_HOST,
            user        =   DB_USER,
            password    =   DB_PASSWORD,
            db          =   DB_NAME,
            cursorclass =   pymysql.cursors.SSCursor)
    
    def execute(self):
        print('please see toBigQuery()')
        self.__log.info('please see toBigQuery()')
        
    def getConnection(self):
        return self.connection
    
    def insert(self,table, datas):
        cursor = self.connection.cursor() 
        if(len(datas) > 0):
            cursor.execute(datas[0].getDeleteSQLStatement())

        print('Prepare to insert {}'.format(len(datas)))
        self.__log.info('Prepare to insert {}'.format(len(datas)))

        if type(datas) is list:
            for data in datas:
                cursor.execute(data.getInsertSQLStatement())
        #commit
        self.connection.commit()
        self.__log.info('Insert Done!')

    def getOne(self,table,field, where):
        cursor = self.connection.cursor() 
        cursor.execute('SELECT {field} FROM {table} WHERE {where} LIMIT 1'.
                        format(field = field,table = table,where = where))

        rows = cursor.fetchall()
        cursor.close()
      
        try:
            return rows[0][0]
        except:
            pass



if __name__ == '__main__':
    logging.basicConfig(
			filename='/tmp/LogFile2Mysql.log',
            format='[%(name)s - %(asctime)s]:%(message)s', 
            datefmt='%Y-%m-%d %I:%M:%S',level=logging.INFO)
    
    f = FileOperation(PATH_LOG_FILE)
    data = f.getData()
    MySQLDatabase().insert('log_ip_tmp',data)
    
    
