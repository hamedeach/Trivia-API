import unittest
import json
from models import setup_db,Category,Question
from flaskr import create_app,jsonify
import os
from flask_sqlalchemy import SQLAlchemy
import models
import sys



class triviaAPI_TestCases(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = models.database_path
        setup_db(self.app, self.database_path)
        
    def teardown(self):
        print('after run the test..')
        
    # test get all categories ################ 
    def test_get_all_categories(self):
        my_response  = self.client().get('/categories')
        response_body = json.loads(my_response.data)
        
        self.assertEqual(my_response.status_code,200)
        self.assertEqual(response_body['success'],True)
        self.assertTrue(response_body['categories'])
        self.assertTrue(response_body['formatted_Categories'])
        self.assertTrue(response_body['Total_Categories'])
     # count = 1   
    def test_404_get_all_categories(self):
        my_response  = self.client().get('/categories123',json={})
        response_body = json.loads(my_response.data)
        
       
        self.assertEqual(my_response.status_code,404)
        self.assertEqual(response_body['success'],False)
        self.assertEqual(response_body['error'],404)  
        self.assertEqual(response_body['message'],'resource not found')
         # count = 2
    ###############################################################
    
    
    #test get all question #################################
    def test_get_all_questions(self):
        my_response  = self.client().get('/questions')
        response_body = json.loads(my_response.data)
        
        self.assertEqual(my_response.status_code,200)
        self.assertEqual(response_body['success'],True)
        self.assertTrue(response_body['questions'])
        self.assertTrue(response_body['categories'])
        self.assertTrue(response_body['total_questions'])
         # count = 3
    def test_404_get_all_questions(self):
        my_response  = self.client().get('/questionsxyz',json={})
        response_body = json.loads(my_response.data)
        
       
        self.assertEqual(my_response.status_code,404)
        self.assertEqual(response_body['success'],False)
        self.assertEqual(response_body['error'],404)  
        self.assertEqual(response_body['message'],'resource not found')
     # count = 4
    
    
    ################################################################
    
    
    
    
     #test insert question #########################################
    def test_insert_new_question(self):
        self.new_question ={
            'question':'Why do the chicken cross the road ?',
            'answer' : 'to stretch her legs',
            'difficulty' :5,
            'category':1
        }
        
        my_response = self.client().post('/questions',json=self.new_question)
        response_body = json.loads(my_response.data)
        
        self.assertEqual(my_response.status_code,200)
        self.assertEqual(response_body['success'],True)
        self.assertTrue(response_body['created'])
        self.assertTrue(response_body['question_created'])
        self.assertTrue(response_body['questions'])
        self.assertTrue(response_body['total_questions'])
         # count = 5
        
    def test_422_insert_new_question(self):
        self.new_question ={
            'question':'Why do the chicken cross the road ?',
            'answer' : 'to stretch her legs',
            'difficulty' :5,
            'category':'dgfdfd'
        }
        my_response = self.client().post('/questions',json=self.new_question)
        response_body = json.loads(my_response.data)
        
       
        self.assertEqual(my_response.status_code,422)
        self.assertEqual(response_body['success'],False)
        self.assertEqual(response_body['error'],422)  
        self.assertEqual(response_body['message'],'unprocessable')    
    # count = 6
        
        
    def test_400_insert_new_question(self):
        self.new_question ={
            'answer' : 'to stretch her legs',
            'difficulty' :5,
            'category':1
        }
        my_response = self.client().post('/questions',json=self.new_question)
        response_body = json.loads(my_response.data)
        
       
        self.assertEqual(my_response.status_code,400)
        self.assertEqual(response_body['success'],False)
        self.assertEqual(response_body['error'],400)  
        self.assertEqual(response_body['message'],'Bad Request')         
     # count = 7
    
    ################################################################
    
    #test delete question ##########################################
    def test_delete_question(self):
       my_response = self.client().delete('/questions/55')
       response_body = json.loads(my_response.data)
       self.assertEqual(my_response.status_code,200)
       self.assertEqual(response_body['success'],True)
       self.assertEqual(response_body['deleted'],55)
     #count = 8 
         
    def test_404_delete_question(self):
        my_response  = self.client().delete('/questions/100000',json={})
        response_body = json.loads(my_response.data)
        
       
        self.assertEqual(my_response.status_code,404)
        self.assertEqual(response_body['success'],False)
        self.assertEqual(response_body['error'],404)  
        self.assertEqual(response_body['message'],'resource not found')     
    # count = 9
    
    ################################################################
    
    #test search ###############################################
    def test_search_question(self):
        self.searchterm ={
            'searchTerm':'chicken'
        }
        
        my_response = self.client().post('/likequestions',json=self.searchterm)
        response_body = json.loads(my_response.data)
        
        self.assertEqual(my_response.status_code,200)
        self.assertEqual(response_body['success'],True)
        self.assertTrue(response_body['questions'])
        self.assertTrue(response_body['total_questions'])
    # count = 10
    
    def test_400_search_question(self):
        my_response  = self.client().post('/likequestions')
        response_body = json.loads(my_response.data)
        
       
        self.assertEqual(my_response.status_code,400)
        self.assertEqual(response_body['success'],False)
        self.assertEqual(response_body['error'],400)  
        self.assertEqual(response_body['message'],'Bad Request')     
    # count = 11
    
    def test_404_search_question(self):
        my_response  = self.client().post('/likequestions',json={'searchTerm':'ofa7'})
        response_body = json.loads(my_response.data)
        
       
        self.assertEqual(my_response.status_code,404)
        self.assertEqual(response_body['success'],False)
        self.assertEqual(response_body['error'],404)  
        self.assertEqual(response_body['message'],'resource not found')     
    # count = 12

    ##############################################################
    
    #test quizzes ##############################################
    def test_quizzes(self):
        
        my_response = self.client().post('/quizzes',json={
            'previous_questions':[20],
            'quiz_category' : {'type':'Science','id':'1'}
            })
        print(my_response.data)
        response_body = json.loads(my_response.data)
       
        self.assertEqual(my_response.status_code,200)
        self.assertEqual(response_body['success'],True)
        self.assertTrue(response_body['question'])
        self.assertNotEqual(response_body['question']['id'], 20)
        # count = 13
        

    def test_400_quizzes(self):
        
        my_response = self.client().post('/quizzes')
        # load response data
        response_body = json.loads(my_response.data)

        # check response status code and message
        self.assertEqual(my_response.status_code, 400)
        self.assertEqual(response_body['success'], False)
        self.assertEqual(response_body['message'], 'Bad Request')
        # count = 14
    
    
    ###############################################################
            
        
        
        
    
    
        
        







if __name__ == "__main__":
   unittest.main()           