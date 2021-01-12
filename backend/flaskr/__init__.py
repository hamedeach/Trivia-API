import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category
import random
import sys

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
 
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app,resources={'/': {'origins': '*'}})
  

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
    

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories',methods=['GET'])
  def get_all_categories():
      # if page args not exist in the request args make it = 1 
      allCategories = Category.query.all()
      if allCategories is None or not  allCategories or len(allCategories) <= 0:
        print('No categories exist !')
        abort(404)
      else :
        print('route : /categories GET  all categories :{}'.format(allCategories))
        formatted_categories = [cat.format() for cat in allCategories]
        
        categories_type_dict = {}
        for cat in allCategories:
              categories_type_dict[cat.id] = cat.type
        
        return jsonify({
        'formatted_Categories'  :formatted_categories,
        'categories' :categories_type_dict,
        'success' : True,
        'Total_Categories' :len(formatted_categories)
        
         })
      
      
      
    


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  
  '''
  @app.route('/questions', methods=['GET'])
  def get_all_questions():
    allquestions = Question.query.all()
    total_questions = len(allquestions)
    
    if total_questions <=0 :
      print('No questions exist !')
      abort(404)
      
    
    formatted_all_question  = [question.format() for question in allquestions]
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    pg_all_questions = formatted_all_question[start:end]
    
    print('*-*-*-*-*-*-*-*-*-*-*-*-*')
    allCategories = Category.query.all()
    if allCategories is None or not  allCategories or len(allCategories) <= 0:
        print('No categories exist !')
        abort(404)
        
    categories_type_dict = {}
    for cat in allCategories:
        categories_type_dict[cat.id] = cat.type
        
    
    
    
    return jsonify({
            'success': True,
            'questions': pg_all_questions,
            'total_questions': total_questions,
            'categories': categories_type_dict
     })
    
    
  
  
  
  
  

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:q_id>' , methods=['DELETE'])
  def delete_question(q_id):
    del_question = Question.query.filter_by(id =  q_id).one_or_none()
    if del_question is None:
      print('no question has id = {} to be deleted'.format(q_id))
      abort(404)
    try:
      del_question.delete()  
      return jsonify({
        'success' :True,
        'deleted' : q_id
      })
    except:
      abort(422)
  

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  
  @app.route('/questions' , methods=['POST'])
  def insert_new_question():
    req_body = request.get_json()
    
    if req_body is None :
      print('Bad insert new question request no req body')
      abort(400)
      
     # load data from body
    new_question = req_body.get('question')
    new_answer = req_body.get('answer')
    new_difficulty = req_body.get('difficulty')
    new_category = req_body.get('category')  
    
    if new_question is None or new_answer is None or new_difficulty is None or new_category is None :
      print('Bad insert new question request missing data')
      abort(400)
      
    try:
      my_question = Question(question= new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)
      my_question.insert()
      
      all_Questions = Question.query.order_by(Question.id).all()
      total_questions = len(all_Questions)
      
      formatted_all_question  = [question.format() for question in all_Questions]
      page = request.args.get('page', 1, type=int)
      start = (page -1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      pg_all_questions = formatted_all_question[start:end]
      
      
      return jsonify({
        'success': True,
        'created': new_question,
        'question_created': new_question,
        'questions': pg_all_questions,
        'total_questions': total_questions
      })
        
    except:
      print(sys.exc_info())
      abort(422)
        
    
    
      
   

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/likequestions' , methods=['POST'])
  def search_question():
    req_body = request.get_json()
    
    if req_body is None :
      print('Bad search, request has no body')
      abort(400)
    
    serach_term = req_body['searchTerm']  
    search_results = Question.query.filter(Question.question.like('%'+serach_term+'%')).all()
    res_length = len(search_results)
    print('####################################################################################################')
    print(res_length)
    if search_results is None or res_length <=0 :
      print('search result not exist : {}'.format(serach_term))
      abort(404)
      
    formatted_all_question  = [question.format() for question in search_results]
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    pg_all_questions = formatted_all_question[start:end] 
    
    return jsonify({
      'success' :True,
      'questions': pg_all_questions,
      'total_questions' : res_length
    })
  
  
  
  
  

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 
  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
  def get_category_all_questions(cat_id):
    mycategory = Category.query.filter_by(id = cat_id).one_or_none()
    if mycategory is None :
      print('/categories/{}/questions category not exist'.format(cat_id))
      abort(404)
    
    mycategory_questions = Question.query.filter_by(category = cat_id).all()
    formatted_all_question  = [question.format() for question in mycategory_questions]
    page = request.args.get('page', 1, type=int)
    start = (page -1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    pg_category_questions = formatted_all_question[start:end]
    
    return jsonify({
      'success' : True,
      'questions' : pg_category_questions,
      'total_questions' : len(pg_category_questions),
      'current_category' : mycategory.type
    })
    
    
      
      
      
  


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  
  @app.route('/quizzes',methods=['POST'])
  def quez_questions():
    req_body = request.get_json()
    if(req_body is None):
      abort(400)
    
    old_questions = req_body['previous_questions']
    print('****** old questions :{}'.format(old_questions))
    selected_category = req_body['quiz_category']
    
    if ((selected_category is None) or (old_questions is None)):
      abort(400)
    
    my_questions=''
    if(selected_category['id'] == 0) :  
      my_questions = Question.query.all()
    else :
      my_questions =Question.query.filter_by(category=selected_category['id']).all()
    
    new_question = None
    
    print('start searching for new question .....')
    
   # loop to get not repeated  random question 
    while (True):
      random_q = random.choice(my_questions)
      if not random_q.id in old_questions:
        new_question = random_q
        break
      elif  (len(my_questions)<=len(old_questions)):
        new_question=None
        break
      
    if(new_question is None):
      return jsonify({'success':True})
    else :
      return jsonify({
        'success':True,
        'question' :new_question.format()
        
      })
    
  

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def not_found(error):
     return jsonify({
            'success' : False,
            'error': 400,
            'message' :'Bad Request'
       }),400
     
  
  @app.errorhandler(404)
  def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

  @app.errorhandler(422)
  def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
  
  return app
  
  

    