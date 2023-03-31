import pandas as pd
from flask_restful import Resource 
from flask import request


class GenerateSubstringMatches(Resource):

    def read_files(self):
        # with open(f'additional_files/NearestNeighbors_{self.header}.bin','rb') as f:
        #     self.nearest_neighbors=pickle.load(f)
        # with open(f'additional_files/tfidfVectorizer_{self.header}.bin','rb') as f:
        #     self.tfidf_vectorizer=pickle.load(f)
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')
        # self.vocabulary=pd.read_pickle(f'additional_files/unique_valid_strings_{self.header}.bin')[0].values

        # with open('additional_files/ngram_limits_per_heading.json', 'r') as fp:
        #     self.ngram_limits_per_heading_json=json.load(fp)




    def generate_substring_matches(self):
        '''
        '''
        self.temp_values=self.conglomerate_vocabulary_panda.loc[
            self.conglomerate_vocabulary_panda['valid_string'].str.startswith(self.substring.lower())
        ].drop_duplicates(subset=('main_string')).sort_values(['use_count','valid_string'],ascending=[False,True])[['valid_string','main_string']].agg(' AKA '.join, axis=1).tolist()

        #return temp_values

    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''

        self.header=request.json['header']
        self.substring=request.json['substring']


        self.read_files()
        self.generate_substring_matches()
        


        return self.temp_values
        # self.append_to_conglomerate_panda()
        # self.train_models()
        # self.write_files_and_models()