import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from flask import abort


database_name = "trivia"
database_path = "postgres://{}:{}@{}:{}/{}".format('hamedeach','11112013','localhost','5432',database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(String)
  difficulty = Column(Integer)

  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    error =True
    try:
      db.session.add(self)
      db.session.commit()
      error=False
    except:
      db.session.rollback()
      print(sys.exc_info())
      error=True
    finally:
      db.session.close()
    
    if error:
       print('insert : Failed error exist')
       abort(422)
    else:
       print('insert: pass')
    
  def update(self):
      error=True
      try:
        db.session.commit()
        error=False
      except:
        db.session.rollback()
        print(sys.exc_info())
        error=True
      finally:
        db.session.close()
            
      if error:
          print('update : failed error exist')
      else:
          print('update : pass')

  def delete(self):
      error=True
      try:
         db.session.delete(self)
         db.session.commit()
         error=False
      except:
         db.session.rollback()
         print(sys.exc_info())
         error=True
      finally:
         db.session.close()
            
      if error:
        print('delete : failed error exist')
      else:
        print('delete : pass')

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }