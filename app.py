from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

""" Getting required parameters"""
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
ma = Marshmallow(app)

""" Creating class object Person"""
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class PersonSchema(ma.Schema):
    class Meta:
         fields = ('id', 'name')

person_schema = PersonSchema()
persons_schema = PersonSchema(many=True)


""" Persons endpoint get and post request"""
class PostsListResource(Resource):
    def get(self):
        return persons_schema.dump(Person.query.all())

    def post(self):
        data = request.json
        new_person = Person(name=data['name'])
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person)


""" Person endpoint get and patch and delete request"""
class PostResource(Resource):
    def get(self, person_id):
        person = Person.query.get_or_404(person_id)
        return person_schema.dump(person)

    def patch(self, person_id):
        data = request.json
        person = Person.query.get_or_404(person_id)
        if 'name' in data:
            person.name = data["name"]
            db.session.commit()
        return person_schema.dump(person)

    def delete(self, person_id):
        person = Person.query.get_or_404(person_id)
        db.session.delete(person)
        db.session.commit()
        feedback = {"feedback": "Successfully deleted person"}
        return feedback


api.add_resource(PostsListResource, '/api')
api.add_resource(PostResource, '/api/<int:person_id>')

if __name__ == "__app__":
    app.run(debug=True)


