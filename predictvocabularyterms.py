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


        # self.nearest_neighbors
        # self.tfidf_vectorizer
        # self.conglomerate_vocabulary_panda
        # self.vocabulary


    def get_neighbors(self):
        try:
            vectorized_string=self.tfidf_vectorizer.transform([str(self.written_string)])
        except NotFittedError:

            output_df=pd.DataFrame.from_dict(
                {
                    'guessed_valid_strings':[None],
                    'guessed_valid_string_distances':[None]
                }
            )

        #if there are fewer neighbors to retrieve than we want, set the neighbors to the max available
        if (self.nearest_neighbors.n_samples_fit_) < self.neighbors_to_retrieve:
            self.neighbors_to_retrieve=self.nearest_neighbors.n_samples_fit_

        #kn_ind is an array of indices of the nieghbors in the training matrix
        similarities,kn_ind=self.nearest_neighbors.kneighbors(
            vectorized_string,
            self.neighbors_to_retrieve
        )
        #print(similarities)
        #print(kn_ind[0])
        #print(vocabulary_dict[temp_header_core_vocabulary])
        #print('2345678982345678904356789034567890-4567890-34567892345678982345678904356789034567890-4567890-3456789')
        #ISSUE 33
        # vocabulary_dict[temp_header]=temp_panda[0].values
        # output_dict[temp_header][temp_written_string]=vocabulary_dict[temp_header_core_vocabulary][kn_ind[0]]
        # output_dict[temp_header][temp_written_string]=(
        #     similarities[0],
        #     vocabulary_dict[temp_header_core_vocabulary][0].values[kn_ind[0]]
        # )
        self.neighbors_df=output_df=pd.DataFrame.from_dict(
            {
                'guessed_valid_strings':self.vocabulary[kn_ind[0]],
                'guessed_valid_string_distances':similarities[0],

            }
        )       
        #return output_df 

        # self.nearest_neighbors
        # self.tfidf_vectorizer
        # self.conglomerate_vocabulary_panda
        # self.vocabulary

    def append_use_count_property(self):
        #originally we had a for loop, but the problem with that was taht was that we were getting a result for each 
        #valid string that the written string mapped to. this meant that we coudl get the same main strin multiple times.
        # temp_relevant_nodes_rows=conglomerate_vocabulary_panda_dict[temp_header_core_vocabulary].loc[
        #     #i think isin is the wrong choice here? i think it should be equal?
        #     #is in is fine... just ahve to reorder
        #     #conglomerate_vocabulary_panda_dict[temp_header]['valid_string'].isin(valid_string_neighbors[temp_header][temp_written_string])
        #     conglomerate_vocabulary_panda_dict[temp_header_core_vocabulary]['valid_string'].isin(valid_string_neighbors[temp_header][temp_written_string])
        # ]
        #print(conglomerate_vocabulary_panda_dict[temp_header_core_vocabulary])

        self.neighbors_df=self.neighbors_df.merge(
            self.conglomerate_vocabulary_panda,
            how='left',
            left_on='guessed_valid_strings',
            right_on='valid_string'
        ).drop_duplicates(subset=('main_string')).sort_values(by=['use_count','guessed_valid_string_distances'],ascending=[False,True])

        # temp_concatenated=pd.concat(
        self.neighbors_df.drop(
            ['guessed_valid_strings','node_id','ontology'],
            axis='columns',
            inplace=True
        )
        #print(temp_relevant_nodes_rows)
        
        
        #this is where things are getting rearranged. 
        #just checking if it is in a list is obliterating the order of the list that we are using to check
        #instead what we want to do is then for each value, sort
        #eventually we might want some kind of hybrid function that takes a balance of cosine similarity and use_count
        #ok so, for the moment, we do not sort by use_count, instead only by cosine score
        #
        # temp_relevant_nodes_rows['valid_string']=pd.Categorical(
        #     temp_relevant_nodes_rows['valid_string'],
        #     categories=valid_string_neighbors[temp_header][temp_written_string]
        # )
        # temp_relevant_nodes_rows=temp_relevant_nodes_rows.sort_values('valid_string')

        #ISSUE 24
        #we add this condition as the partner condition to the tfidf is fitted check
        #if there are no nodes in the conglomerate panda, then provide these options as a null
        # if (len(temp_relevant_nodes_rows.index)==0) or (temp_relevant_nodes_rows.applymap(pd.isnull).all().all() == True):
        #     output_dict[temp_header][temp_written_string].append(
        #             {
        #                 'label':'no options available',
        #                 'value':'no options available'
        #             }
        #         )
        #     continue
            
        # for index,series in temp_relevant_nodes_rows.iterrows():
        #     #in each of the options, having "thing AKA thing" is 
        #     #print(series)
        #     if series['valid_string']==series['main_string'].lower():            
        #         output_dict[temp_header][temp_written_string].append(
        #             {
        #                 'label':series['valid_string'],#+' NODE '+series['node_id'],
        #                 'value':series['valid_string']+' AKA '+series['main_string']                
        #             }
        #         )
        #     else:
        #         output_dict[temp_header][temp_written_string].append(
        #             {
        #                 'label':series['valid_string']+' AKA '+series['main_string'],#+' NODE '+series['node_id'],
        #                 'value':series['valid_string']+' AKA '+series['main_string']#+' NODE '+series['node_id']                
        #             }
        #         )






    def post(self):
        '''
        '''

        self.header=request.json['header']
        self.written_string=request.json['written_string']
        self.neighbors_to_retrieve=request.json['neighbors_to_retrieve']


        self.read_files()
        self.get_neighbors()
        self.append_use_count_property()
        print('')
        print(self.neighbors_df)
        print('')

        return json.dumps(self.neighbors_df.to_dict('records'))



        # dropdown_triplet_selection_value=request.json["dropdown_triplet_selection_value"]
        # slider_percent_present_value=request.json["slider_percent_present_value"]
        # toggle_average_true_value=request.json["toggle_average_true_value"]
        # radio_items_filter_value=request.json["radio_items_filter_value"]
        
        # my_VennTableQuery=VennTableQuery()
        # my_VennTableQuery.build_query(
        #     dropdown_triplet_selection_value,
        #     slider_percent_present_value,
        #     toggle_average_true_value,
        #     radio_items_filter_value
        # )

        # connection=my_engine.connect()
        # temp_cursor=connection.execute(
        #     my_VennTableQuery.query
        # )

        # if (temp_cursor.rowcount <= 0):
        #     connection.close()
        #     #https://stackoverflow.com/questions/8645250/how-to-close-sqlalchemy-connection-in-mysql
        #     my_engine.dispose()
        #     print('row count of final result cursor less than 1')
        #     return 'fail'
        # else:
        #     temp_result=json.dumps([dict(r) for r in temp_cursor])
        #     connection.close()
        #     #https://stackoverflow.com/questions/8645250/how-to-close-sqlalchemy-connection-in-mysql
        #     my_engine.dispose()
        #     #print(temp_result)
        #     return temp_result   
