from flask import Flask 
from flask_restful import Api, Resource,reqparse,abort ,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app= Flask(__name__)
api= Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///database.db"
db=SQLAlchemy(app)

# Defining models that store information in the database
class UserModel(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False)
    nationality=db.Column(db.String(255),nullable=False)
    career=db.Column(db.String(255),nullable=False)
    age=db.Column(db.Integer,nullable=False)
    
    def __repr__(self) :
        return f"User(name= {self.name},nationality={self.nationality},career={self.career},age={self.age})"
#with app.app_context():
 #db.create_all()
 #done once to create the database and prevent it from overriding by creating another database

user_properties = reqparse.RequestParser()
user_properties.add_argument("name",type=str,help="Username required",required=True)
user_properties.add_argument("nationality",type=str,help="Nationality required",required=True)
user_properties.add_argument("career",type=str,help="Career required",required=True)
user_properties.add_argument("age",type=int,help="Age required",required=True)

user_update_properties= reqparse.RequestParser()
user_update_properties.add_argument("name",type=str,help="Username required")
user_update_properties.add_argument("nationality",type=str,help="Nationality required")
user_update_properties.add_argument("career",type=str,help="Careeer required")
user_update_properties.add_argument("age",type=int,help="Age required")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'nationality': fields.String,
    'career': fields.String,
    'age': fields.Integer
}

class Users(Resource):
    @app.route('/users,method=GET')
    @marshal_with(resource_fields)
    def get(self,id):
        result=UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="User not found")
        return result
    
    @app.route('/list_users,method=GET')
    @marshal_with(resource_fields)
    def get_users(self,id):
        result=UserModel.query.filter_by(id=id).all()
        if result is not None:
            return result
        else:
            abort(404, message="List of users not found")
        
    
    @app.route('/add_users/int:<id>, methods=POST')
    @marshal_with(resource_fields)
    def put(self,id):
        args=user_properties.parse_args()
        result=UserModel.query.filter_by(id=id).first()
        if result:
            abort(409, message="User ID already exists")
        else:
            user=UserModel(id=args[id],name=args['name'],nationality=args['nationality'],career=args['career'],age=args['age'])
            db.session.add(user)
            db.session.commit()
        return user, 201 
    
    @app.route('/update_users/int:<id>,methods=PUT')
    @marshal_with(resource_fields) 
    def patch(self):
        args=user_update_properties.parse_args()
        result=UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404,message="User does not exist")
        if  args['name']:
            result.name=args['name']  
        if args['nationality']:
            result.nationality=args['nationality']  
        if args['career']:
            result.career=args['career'] 
        if args['age']:
            result.name=args['age'] 
            
        db.session.commit()
        
    
    @app.route('/delete_users/int:<id>,methods=DELETE')
    @marshal_with(resource_fields)
    def delete(self,id):
        result=UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404,message="User does not exist")
        db.session.delete(result)
        db.session.commit()
        return '',  204
        
    #status code helps display user action completed succesfully
        
     
api.add_resource(Users,"/users/<int:id>")
api.add_resource(Users,"/list_users/<int:id>")
api.add_resource(Users,"/add_users/<int:id>")
api.add_resource(Users,"/update_users/<int:id>")
api.add_resource(Users,"/delete_users/<int:id>")

if __name__=="__main__":
    app.run(debug=True)
    #starts our application and help in development mode to spot errors