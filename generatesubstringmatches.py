import pandas as pd
from flask_restful import Resource 
from flask import request


class GenerateSubstringMatches(Resource):

    def read_files(self):
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

    def generate_substring_matches(self):
        '''
        '''
        # print(self.conglomerate_vocabulary_panda.loc[
        #     self.conglomerate_vocabulary_panda['valid_string'].str.contains(self.substring.lower())
        # ])
        try:
            self.temp_values=self.conglomerate_vocabulary_panda.loc[
                self.conglomerate_vocabulary_panda['valid_string'].str.contains(self.substring.lower())
            ].drop_duplicates(subset=('main_string')).sort_values(['use_count','valid_string'],ascending=[False,True])[['valid_string','main_string']].agg(' AKA '.join, axis=1).tolist()
        except AttributeError:
            self.temp_values=[]

    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''

        self.header=request.json['header']
        self.substring=request.json['substring']

        self.read_files()
        self.generate_substring_matches()

        return self.temp_values
