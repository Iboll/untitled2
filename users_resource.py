from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.jobs import Jobs
from data.users import User
from par import parser


def abort_if_news_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'user': user.to_dict(
            only=('email', 'name', 'surname', 'age', 'position', 'speciality', 'about'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(User).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(User).all()
        return jsonify({'news': [item.to_dict(
            only=('email', 'name', 'surname', 'age', 'position', 'speciality', 'about')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            email=args['email'],
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            about=args['about']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})