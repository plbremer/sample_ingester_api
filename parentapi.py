from pprint import pprint
from flask import Flask,request
from flask_restful import Api, Resource, reqparse
import json

# from sqlalchemy import create_engine
# from sqlalchemy import Table, String
# from sqlalchemy.dialects import postgresql

from predictvocabularyterms import PredictVocabularyTermsResource
from trainvocabularyterms import TrainVocabularyTermsResource
from updateusecount import UpdateUseCountResource
from validatetermsfortraining import ValidateTermsForTrainingResource
from generatesubstringmatches import GenerateSubstringMatches

app=Flask(__name__)
api=Api(app)

# my_server='binvestigate-parker.czbqhgrlaqbf.us-west-2.rds.amazonaws.com'
# my_database='postgres'
# my_dialect='postgresql'
# my_driver='psycopg2'
# my_username='postgres'
# my_password='S7kB93DIT46$'
# my_port='5432'
# my_connection=f'{my_dialect}+{my_driver}://{my_username}:{my_password}@{my_server}/{my_database}'
# my_engine=create_engine(my_connection)#,echo=True)


api.add_resource(PredictVocabularyTermsResource,'/predictvocabularytermsresource/')
api.add_resource(TrainVocabularyTermsResource,'/trainvocabularytermsresource/')
api.add_resource(UpdateUseCountResource,'/updateusecountresource/')
api.add_resource(ValidateTermsForTrainingResource,'/validatetermsfortraining/')
api.add_resource(GenerateSubstringMatches,'/generatesubstringmatches/')

if __name__ == '__main__':
    #app.run(debug=False,port=4999,host='0.0.0.0')
    app.run(debug=True,port=4999)
