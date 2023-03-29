# from flask import Flask,request
from flask_restful import Resource #Api, Resource, reqparse
from sklearn.exceptions import NotFittedError
import json
import pickle
import pandas as pd
import os
from flask import request

# request

# #get the headers and their subset definitions
# with open('additional_files/subset_per_heading.json', 'r') as fp:
#     subset_per_heading_json=json.load(fp)
#get the headers and their n gram limits
# with open('additional_files/ngram_limits_per_heading.json', 'r') as fp:
#     ngram_limits_per_heading_json=json.load(fp)
#get all of the models
# nearest_neighbors_dict=dict()
# tfidf_vectorizer_dict=dict()
# model_files=os.listdir('additional_files/')
# for temp_file_name in model_files:
#     temp_header=temp_file_name.split('.')[0].split('_')[-1]
#     if 'NearestNeighbors' in temp_file_name:
#         with open(f'additional_files/{temp_file_name}', 'rb') as f:
#             nearest_neighbors_dict[temp_header]=pickle.load(f)
#     elif 'tfidfVectorizer' in temp_file_name:
#         with open(f'additional_files/{temp_file_name}', 'rb') as f:
#             tfidf_vectorizer_dict[temp_header]=pickle.load(f)
# #get all of the vocabulary dicts
# conglomerate_vocabulary_panda_dict=dict()
# for temp_file_name in model_files:
#     temp_header=temp_file_name.split('.')[0].split('_')[-1]
#     if 'conglomerate_vocabulary_panda' in temp_file_name:
#         temp_panda=pd.read_pickle(f'additional_files/{temp_file_name}')
#         #temp panda has header 0 not "valid string unique" for some reason
#         conglomerate_vocabulary_panda_dict[temp_header]=temp_panda
# #get the vocaulary for each header. used to infer the valid_string from locattion.
# #nearest neighbors model outputs location of match on list.
# vocabulary_dict=dict()
# for temp_file_name in model_files:
#     temp_header=temp_file_name.split('.')[0].split('_')[-1]
#     if 'unique_valid_strings' in temp_file_name:
#         temp_panda=pd.read_pickle(f'additional_files/{temp_file_name}')
#         #temp panda has header 0 not "valid string unique" for some reason
#         vocabulary_dict[temp_header]=temp_panda[0].values
#         #vocabulary_dict[temp_header]=temp_panda




class PredictVocabularyTermsResource(Resource):

    def read_files(self):
        with open(f'additional_files/NearestNeighbors_{self.header}.bin','rb') as f:
            self.nearest_neighbors=pickle.load(f)
        with open(f'additional_files/tfidfVectorizer_{self.header}.bin','rb') as f:
            self.tfidf_vectorizer=pickle.load(f)
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')
        self.vocabulary=pd.read_pickle(f'additional_files/unique_valid_strings_{self.header}.bin')[0].values






    def post(self):
        '''
        '''

        self.header=request.json['header']
        self.written_string=request.json['written_string']


        # self.read_files()
        # self.get_neighbors()
        # self.append_use_count_property()
        # print('')
        # print(self.neighbors_df)
        # print('')

        # return json.dumps(self.neighbors_df.to_dict('records'))

