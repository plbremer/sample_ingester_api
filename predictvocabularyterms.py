from flask_restful import Resource 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.exceptions import NotFittedError
import json
import pickle
import pandas as pd
from flask import request
from pprint import pprint

class PredictVocabularyTermsResource(Resource):

    def read_files(self):
        with open(f'additional_files/NearestNeighbors_{self.header}.bin','rb') as f:
            self.nearest_neighbors=pickle.load(f)
        with open(f'additional_files/tfidfVectorizer_{self.header}.bin','rb') as f:
            self.tfidf_vectorizer=pickle.load(f)
        self.conglomerate_vocabulary_panda=pd.read_pickle(f'additional_files/conglomerate_vocabulary_panda_{self.header}.bin')
        self.vocabulary=pd.read_pickle(f'additional_files/unique_valid_strings_{self.header}.bin')[0].values

        temp_translator=pd.read_csv(f'assets/prediction_short_string_translations.tsv',sep='\t',na_filter=False)
        self.short_string_translator=dict(zip(temp_translator.short.tolist(),temp_translator.long.tolist()))

    def get_neighbors(self):
        for written_string in self.written_strings:
            try:
                vectorized_string=self.tfidf_vectorizer.transform([str(written_string)])
            except NotFittedError:
                print('not fitted')
                neighbors_df=pd.DataFrame.from_dict(
                    {
                        'guessed_valid_strings':[None],
                        'guessed_valid_string_distances':[None]
                    }
                )

                self.neighbors_panda_list.append(neighbors_df)
                continue

            #if there are fewer neighbors to retrieve than we want, set the neighbors to the max available
            if (self.nearest_neighbors.n_samples_fit_) < self.neighbors_to_retrieve:
                self.neighbors_to_retrieve=self.nearest_neighbors.n_samples_fit_

            #kn_ind is an array of indices of the nieghbors in the training matrix
            similarities,kn_ind=self.nearest_neighbors.kneighbors(
                vectorized_string,
                self.neighbors_to_retrieve
            )

            neighbors_df=pd.DataFrame.from_dict(
                {
                    'written_string':[written_string for similarity in similarities[0]],
                    'guessed_valid_strings':self.vocabulary[kn_ind[0]],
                    'guessed_valid_string_distances':similarities[0],
                    
                }
            )     
            # print(neighbors_df)  
            self.neighbors_panda_list.append(neighbors_df)

    def append_use_count_property(self):
        #originally we had a for loop, but the problem with that was taht was that we were getting a result for each 
        #valid string that the written string mapped to. this meant that we coudl get the same main strin multiple times.
        for i in range(len(self.neighbors_panda_list)):
            self.neighbors_panda_list[i]=self.neighbors_panda_list[i].merge(
                self.conglomerate_vocabulary_panda,
                how='left',
                left_on='guessed_valid_strings',
                right_on='valid_string'
            ).drop_duplicates(subset=('main_string')).sort_values(by=['use_count','guessed_valid_string_distances'],ascending=[False,True])

            self.neighbors_panda_list[i].drop(
                ['guessed_valid_strings','node_id','ontology'],
                axis='columns',
                inplace=True
            )

    def post(self):
        '''
        '''

        self.header=request.json['header']
        self.written_strings=request.json['written_strings']
        self.neighbors_to_retrieve=request.json['neighbors_to_retrieve']

        self.read_files()

        #swap things like 'wt' that are too shrot for trigrams out with longer terms
        for i in range(len(self.written_strings)):
            if self.written_strings[i] in self.short_string_translator.keys():
                self.written_strings[i]=self.short_string_translator[self.written_strings[i]]


        self.neighbors_panda_list=list()
        self.get_neighbors()
        self.append_use_count_property()
        
        self.output_panda=pd.concat(
            self.neighbors_panda_list,
            axis='index',
            ignore_index=True
        )

        # print(self.output_panda)

        return json.dumps(self.output_panda.to_dict('records'))