from flask_restful import Resource 
import pandas as pd
from flask import request
import sqlalchemy
import time
import json

import os


class Samples(Resource):

    def get(self):

        self.provided_study_id=request.json['study_id']


        self.database_relative_address='./additional_files/sample_ingester_database.db'

        engine=sqlalchemy.create_engine(f"sqlite:///{self.database_relative_address}")



        connection=engine.connect()
        temp_cursor=connection.execute(
            f'''
            select * from study_table where study_id="{self.provided_study_id}"
            '''
        )

        if (temp_cursor.rowcount <= 0):
            connection.close()
            #https://stackoverflow.com/questions/8645250/how-to-close-sqlalchemy-connection-in-mysql
            engine.dispose()
            print('row count of final result cursor less than 1')
            return 'fail'
        else:
            temp_result=json.dumps([dict(r) for r in temp_cursor])
            connection.close()
            #https://stackoverflow.com/questions/8645250/how-to-close-sqlalchemy-connection-in-mysql
            engine.dispose()
            #print(temp_result)
            return temp_result   