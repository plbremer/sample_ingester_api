



# from flask import Flask,request
from flask_restful import Resource #Api, Resource, reqparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.exceptions import NotFittedError
import json
import pickle
import pandas as pd
from flask import request


# from newvocabularyuploadchecker import NewVocabularyUploadChecker



class TrainVocabularyResource(Resource):


    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''
        # print('in post')
        self.header=request.json['header']
        # self.written_strings=request.json['new_vocabulary']
        

        self.read_files()



        # self.validate_training_request()
        
        # # print(self.NewVocabularyUploadChecker.error_list)
        # if len(self.NewVocabularyUploadChecker.error_list)>0:
        #     return {'errors':self.NewVocabularyUploadChecker.error_list}

        # print('we can do training - no errors')

        # self.append_to_conglomerate_panda()
        self.train_models()
        self.write_models()
        
        return {'errors':False}



    def read_files(self):
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

        with open('additional_files/ngram_limits_per_heading.json', 'r') as fp:
            self.ngram_limits_per_heading_json=json.load(fp)


    def train_models(self):
    #for temp_key in new_vocab_dict.keys():
        self.model_vocabulary=self.conglomerate_vocabulary_panda['valid_string'].unique()
        self.TfidfVectorizer=TfidfVectorizer(
            analyzer='char',
            ngram_range=self.ngram_limits_per_heading_json[self.header],
            use_idf=False,
            norm=None
        )
        self.tfidf_matrix=self.TfidfVectorizer.fit_transform(self.model_vocabulary)

        self.NN_model=NearestNeighbors(
            n_neighbors=50,
            n_jobs=5,
            metric='cosine'
        )
        self.NN_model.fit(self.tfidf_matrix)


    def write_models(self):

        with open(f'additional_files/tfidfVectorizer_{self.header}.bin','wb') as fp:
            pickle.dump(self.TfidfVectorizer,fp)

        with open(f'additional_files/NearestNeighbors_{self.header}.bin','wb') as fp:
            pickle.dump(self.NN_model,fp)

        # self.conglomerate_vocabulary_panda.to_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

        output_vocab_panda=pd.DataFrame.from_dict(
            self.model_vocabulary
        )

        output_vocab_panda.to_pickle(f'additional_files/unique_valid_strings_{self.header}.bin')