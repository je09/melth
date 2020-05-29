from datetime import datetime

from flask_restful import Api, Resource, reqparse

from models import db, Deadline, Client

api = Api()


def return_deadlines(deadlines_query):
    from json import dumps
    deadlines = deadlines_query.all()

    result = {}
    for deadline in deadlines:
        try:
            result[str(deadline.final_date)].append(
                {
                    'id': deadline.id,
                    'text': deadline.description,
                    'time': str(deadline.final_date)
                }
            )
        except KeyError:
            result[str(deadline.final_date)] = []

    return result


def token_check(client_id, token):
    from hashlib import sha1
    tmp_salt = '1DL8p598YPAT5XNorQMb'

    return sha1(str(client_id).encode() + tmp_salt.encode()).hexdigest() == str(token)


class BareApiRecourse(Resource):
    def get(self, token):
        return {'status': 'no method provided'}, 400


class DeadlineGetRecourse(Resource):
    def get(self, token, client_id):
        if token_check(client_id, token):
            deadlines = Deadline.query.filter_by(
                client_id=client_id
            )

            return return_deadlines(deadlines), 200
        else:
            return {'status': 'wrong api key'}, 403


class DeadlineRecourse(Resource):
    args = reqparse.RequestParser()
    args.add_argument('client_id', type=int)
    args.add_argument('deadline_id', type=int)
    args.add_argument('description', type=str)
    args.add_argument('final_date', type=lambda x: datetime.strptime(x,'%Y-%m-%d'))

    def get(self, token):
        args = self.args.parse_args()
        if token_check(args['client_id'], token):
            deadlines = Deadline.query.get_or_404(args['client_id'])

            return return_deadlines(deadlines), 200
        else:
            return {'status': 'wrong api key'}, 403

    def post(self, token):
        args = self.args.parse_args()

        if token_check(args['client_id'], token):

            is_client = Client.query.filter_by(
                id=args['client_id']
            ).first()

            if not is_client:
                new_client = Client(id=args['client_id'])
                db.session.add(new_client)
                db.session.commit()

            new_deadline = Deadline(
                client_id=args['client_id'],
                description=args['description'],
                final_date=args['final_date']
            )
            db.session.add(new_deadline)
            db.session.commit()

            return {'status': 'success'}, 201
        else:
            return {'status': 'wrong api key'}, 403

    def delete(self, token):
        args = self.args.parse_args()

        if token_check(args['client_id'], token):
            Deadline.query.filter_by(id=args['deadline_id']).delete()
            db.session.commit()

            return {'status': 'success'}, 202
        else:
            return {'status': 'wrong api key'}, 403


api.add_resource(BareApiRecourse, '/')
api.add_resource(DeadlineRecourse, '/deadline/<token>')
api.add_resource(DeadlineGetRecourse, '/deadline/<token>/<int:client_id>')
