#import pandas as pd
from flask_restful import Resource 
from flask import request


from newvocabularyuploadchecker import NewVocabularyUploadChecker

class UpdateUseCountResource(Resource):

    def validate_training_request(self):

        self.NewVocabularyUploadChecker=NewVocabularyUploadChecker(self.written_strings)
        self.NewVocabularyUploadChecker.check_char_length()
        self.NewVocabularyUploadChecker.verify_string_absence()

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


