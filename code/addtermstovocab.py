from flask_restful import Resource 
import pandas as pd
from flask import request
import sqlalchemy

from newvocabularyuploadchecker import NewVocabularyUploadChecker



engine=sqlalchemy.create_engine(f"sqlite:///../additional_files/sample_ingester_database.db")


class AddTermsToVocabularyResource(Resource):


    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''
        self.header=request.json['header']
        self.written_strings=request.json['new_vocabulary']
        

        self.validate_vocabulary_request()

        if len(self.NewVocabularyUploadChecker.error_list)>0:
            return {'errors':self.NewVocabularyUploadChecker.error_list}

        # one of the major points of switching to db was to avoid these three steps
        # self.read_files()
        # self.append_to_conglomerate_panda()
        # self.write_files()
        self.append_new_vocab_to_table()
        
        return {'errors':self.NewVocabularyUploadChecker.error_list}


    def read_files(self):
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'../additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

    def validate_vocabulary_request(self):
        self.NewVocabularyUploadChecker=NewVocabularyUploadChecker(self.written_strings)
        self.NewVocabularyUploadChecker.check_char_length()
        self.NewVocabularyUploadChecker.verify_string_absence()


    def append_to_conglomerate_panda(self):
    #now, for each key in this dict, append to the corresponding panda in the conglomerate dict, then output it again
        appending_dict={
            'valid_string':[],
            'node_id':[],
            'main_string':[],
            'ontology':[],
            'use_count':[]
        }
        for temp_addition in self.written_strings:
            appending_dict['valid_string'].append(temp_addition)
            appending_dict['node_id'].append(temp_addition)
            appending_dict['main_string'].append(temp_addition)
            appending_dict['ontology'].append('userAdded')
            appending_dict['use_count'].append(1)
        appending_panda=pd.DataFrame.from_dict(appending_dict)

        self.conglomerate_vocabulary_panda=pd.concat(
            [self.conglomerate_vocabulary_panda,appending_panda],
            axis='index',
            ignore_index=True,
        )
        #the pattern for new suggestions is that the given string becomes the valid_string, main_string, and node_id (something like that)
        #to make sure that a user doesnt put someonething that already exists
        self.conglomerate_vocabulary_panda.drop_duplicates(subset=('valid_string','main_string'),ignore_index=True,inplace=True)


    def write_files(self):
        self.conglomerate_vocabulary_panda.to_pickle(f'../additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

    def append_new_vocab_to_table(self):
        appending_dict={
            'valid_string':[],
            'node_id':[],
            'main_string':[],
            'ontology':[],
            'use_count':[],
            'header':[]
        }
        for temp_addition in self.written_strings:
            appending_dict['valid_string'].append(temp_addition)
            appending_dict['node_id'].append(temp_addition)
            appending_dict['main_string'].append(temp_addition)
            appending_dict['ontology'].append('userAdded')
            appending_dict['use_count'].append(1)
            appending_dict['header'].append(self.header)
        appending_panda=pd.DataFrame.from_dict(appending_dict)

        # self.conglomerate_vocabulary_panda=pd.concat(
        #     [self.conglomerate_vocabulary_panda,appending_panda],
        #     axis='index',
        #     ignore_index=True,
        # )

        connection=engine.connect()

        for index,series in appending_panda.iterrows():

            try:
                series.to_sql(
                    'vocab_table',
                    connection,
                    if_exists='append',
                    index=False
                )
            except:
                continue

        connection.close()