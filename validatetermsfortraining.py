from flask_restful import Resource 
from flask import request


from newvocabularyuploadchecker import NewVocabularyUploadChecker

class ValidateTermsForTrainingResource(Resource):

    def validate_training_request(self):

        self.NewVocabularyUploadChecker=NewVocabularyUploadChecker(self.new_vocabulary)
        self.NewVocabularyUploadChecker.check_char_length()
        self.NewVocabularyUploadChecker.verify_string_absence()

    def post(self):
        '''
        takes a set of words and add them to the vocabularies and models
        '''

        
        self.new_vocabulary=request.json['new_vocabulary']

        if self.new_vocabulary==None:
            return {'errors':[]}


        self.validate_training_request()

        return {'errors':self.NewVocabularyUploadChecker.error_list}
