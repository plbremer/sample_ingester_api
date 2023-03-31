# from flask import Flask,request
from flask_restful import Resource #Api, Resource, reqparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.exceptions import NotFittedError
import json
import pickle
import pandas as pd
from flask import request


from newvocabularyuploadchecker import NewVocabularyUploadChecker

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




class TrainVocabularyTermsResource(Resource):

    def read_files(self):
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

        with open('additional_files/ngram_limits_per_heading.json', 'r') as fp:
            self.ngram_limits_per_heading_json=json.load(fp)


    def validate_training_request(self):
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

    

    def write_files_and_models(self):

        with open(f'additional_files/tfidfVectorizer_{self.header}.bin','wb') as fp:
            pickle.dump(self.TfidfVectorizer,fp)

        with open(f'additional_files/NearestNeighbors_{self.header}.bin','wb') as fp:
            pickle.dump(self.NN_model,fp)

        self.conglomerate_vocabulary_panda.to_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

        output_vocab_panda=pd.DataFrame.from_dict(
            self.model_vocabulary
        )

        output_vocab_panda.to_pickle(f'additional_files/unique_valid_strings_{self.header}.bin')

    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''

        self.header=request.json['header']
        self.written_strings=request.json['written_strings']
        

        self.read_files()


        self.validate_training_request()
        if len(self.NewVocabularyUploadChecker.error_list)>0:
            return {'errors':self.NewVocabularyUploadChecker.error_list}



        self.append_to_conglomerate_panda()
        self.train_models()
        self.write_files_and_models()
        
        return {'errors':self.NewVocabularyUploadChecker.error_list}
