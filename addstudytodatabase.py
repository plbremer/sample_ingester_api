from flask_restful import Resource 
import pandas as pd
from flask import request
import sqlalchemy
import time

import os


class AddStudyToDatabase(Resource):

    def make_author_id(self):

        self.author_id=''.join(
            [temp_char.lower() for temp_char in self.provided_author_name if(temp_char.isalpha()==True)]
        )

    def make_list_of_dataframes_for_upload(self):
        '''
        the basic idea is that we make a dataframe 
        '''

        self.study_id=time.time()

        highest_parallel_degree=0
        for temp_col in self.sample_metadata_curated_panda.columns:
            if int(temp_col.split('.')[1])>highest_parallel_degree:
                highest_parallel_degree=int(temp_col.split('.')[1])
        print('highest parallel')
        print(highest_parallel_degree)
        print('')


        self.pandas_for_db=list()
        for temp_degree in range(highest_parallel_degree+1):
            temp_column_list=[temp_col for temp_col in self.sample_metadata_curated_panda if int(temp_col.split('.')[1])==temp_degree]
            self.pandas_for_db.append(
                self.sample_metadata_curated_panda[temp_column_list].copy()
            )
            print(self.pandas_for_db[temp_degree])
            
            #always use the same function....
            temp_column_rename_function=lambda x: x.split('.')[0]
            #conveniently, degrees are the same as the indices in the panda_upload list
            self.pandas_for_db[temp_degree].rename(
                mapper=temp_column_rename_function,
                axis='columns',
                inplace=True
            )

        for i,temp_df in enumerate(self.pandas_for_db):
            temp_df['author_id']=self.author_id
            temp_df['study_id']=self.study_id
            temp_df['sample_id']=temp_df.index
            temp_df['metadata_parallel_id']=[i for element in temp_df.index]

       


    def upload_to_database(self):

        engine=sqlalchemy.create_engine(f"sqlite:///{self.database_relative_address}")
        print(engine)
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++==')

        for temp_df in self.pandas_for_db:
            print(temp_df)

            temp_df.to_sql(
                'study_table',
                con=engine,
                if_exists='append',
                index=False
            )
        


    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''

        self.database_relative_address='./additional_files/sample_ingester_database.db'

        print(os.listdir('./additional_files/'))
        print('8'*100)

        self.provided_author_name=request.json['provided_author_name']
        self.sample_metadata_curated_panda=pd.DataFrame.from_records(request.json['sample_metadata_sheet_panda'])

        print(self.provided_author_name)
        self.make_author_id()

        print(self.sample_metadata_curated_panda)

        self.make_list_of_dataframes_for_upload()


        self.upload_to_database()

        return {
            'author_id':self.author_id,
            'study_id':self.study_id
        }

        # self.header=request.json['header']
        # self.written_strings=request.json['new_vocabulary']
        

        # self.validate_vocabulary_request()

        # if len(self.NewVocabularyUploadChecker.error_list)>0:
        #     return {'errors':self.NewVocabularyUploadChecker.error_list}

        # self.read_files()

        # self.append_to_conglomerate_panda()

        # self.write_files()
        
        # return {'errors':self.NewVocabularyUploadChecker.error_list}