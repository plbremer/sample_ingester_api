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



class AddTermsToVocabularyResource(Resource):


    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''
        # print('in post')
        self.header=request.json['header']
        self.written_strings=request.json['new_vocabulary']
        

        self.validate_vocabulary_request()

        # print(self.NewVocabularyUploadChecker.error_list)
        if len(self.NewVocabularyUploadChecker.error_list)>0:
            return {'errors':self.NewVocabularyUploadChecker.error_list}

        self.read_files()



        
        


        # print('we can do training - no errors')

        self.append_to_conglomerate_panda()
        # self.train_models()
        self.write_files()
        
        return {'errors':self.NewVocabularyUploadChecker.error_list}


    def read_files(self):
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')



        # with open('additional_files/ngram_limits_per_heading.json', 'r') as fp:
        #     self.ngram_limits_per_heading_json=json.load(fp)

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

        # with open(f'additional_files/tfidfVectorizer_{self.header}.bin','wb') as fp:
        #     pickle.dump(self.TfidfVectorizer,fp)

        # with open(f'additional_files/NearestNeighbors_{self.header}.bin','wb') as fp:
        #     pickle.dump(self.NN_model,fp)

        self.conglomerate_vocabulary_panda.to_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')

        # output_vocab_panda=pd.DataFrame.from_dict(
        #     self.model_vocabulary
        # )

        # output_vocab_panda.to_pickle(f'additional_files/unique_valid_strings_{self.header}.bin')