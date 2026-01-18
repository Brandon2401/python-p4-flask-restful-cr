#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return {"message": "Welcome to the Newsletter RESTful API"}, 200

api.add_resource(Home, '/')

# All Newsletters
class Newsletters(Resource):
    def get(self):
        newsletters = [n.to_dict() for n in Newsletter.query.all()]
        return newsletters, 200

    def post(self):
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body']
        )
        db.session.add(new_record)
        db.session.commit()
        return new_record.to_dict(), 201

api.add_resource(Newsletters, '/newsletters')

# Single Newsletter by ID
class NewsletterByID(Resource):
    def get(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return {"error": "Newsletter not found"}, 404
        return record.to_dict(), 200

    def put(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return {"error": "Newsletter not found"}, 404

        record.title = request.form['title']
        record.body = request.form['body']
        db.session.commit()
        return record.to_dict(), 200

    def patch(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return {"error": "Newsletter not found"}, 404

        if 'title' in request.form:
            record.title = request.form['title']
        if 'body' in request.form:
            record.body = request.form['body']
        db.session.commit()
        return record.to_dict(), 200

    def delete(self, id):
        record = Newsletter.query.filter_by(id=id).first()
        if not record:
            return {"error": "Newsletter not found"}, 404

        db.session.delete(record)
        db.session.commit()
        return {"message": f"Newsletter {id} deleted"}, 200

api.add_resource(NewsletterByID, '/newsletters/<int:id>')

# -----------------------
# Run the App
# -----------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)