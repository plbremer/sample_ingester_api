import pandas as pd
from flask_restful import Resource 
from flask import request


class UpdateUseCountResource(Resource):

    def read_files(self):
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

    def update_use_count(self):
    #now, for each key in this dict, append to the corresponding panda in the conglomerate dict, then output it again
        self.conglomerate_vocabulary_panda['use_count']=self.conglomerate_vocabulary_panda['use_count'].where(
            (~self.conglomerate_vocabulary_panda.main_string.isin(self.main_strings)),
            other=1
        )

    def write_file(self):

        self.conglomerate_vocabulary_panda.to_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')


    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''

        self.header=request.json['header']
        self.main_strings=request.json['main_strings']


        self.read_files()
        self.update_use_count()
        self.write_file()


        return 'use_count update successful'