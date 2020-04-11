from flask import jsonify
from flask_restful import abort, Resource

from data import db_session
from data.jobs import Jobs
from data.users import User
from par_j import parser


def abort_if_news_not_found(jobs_id):
    session = db_session.create_session()
    news = session.query(User).get(jobs_id)
    if not news:
        abort(404, message=f"Job {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_news_not_found(jobs_id)
        session = db_session.create_session()
        news = session.query(Jobs).get(jobs_id)
        return jsonify({'jobs': news.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))})

    def delete(self, jobs_id):
        abort_if_news_not_found(jobs_id)
        session = db_session.create_session()
        news = session.query(Jobs).get(jobs_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished'))
            for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})

