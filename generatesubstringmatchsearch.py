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
        # self.append_to_conglomerate_panda()
        # self.train_models()
        # self.write_files_and_models()