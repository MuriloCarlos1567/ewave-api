from flask import request, url_for
from requests import post
from sql_alchemy import db

MAILGUN_DOMAIN = 'sandboxcd6e3d3a28924932a46f0cfd7ab0e482.mailgun.org'
MAILGUN_API_KEY = 'key-9bdeb61166dc40225c87da70b618fa0b'
FROM_TITLE = 'No-Reply'
FROM_EMAIL = 'no-reply@ewaveapi.com'

class UserModel(db.Model):
    __tablename__ = 'users'

    userId = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    confirmed = db.Column(db.Boolean, default=False) 
    adminconfirmed = db.Column(db.Boolean, default=False) 

    def __init__(self, login, email, password, confirmed, adminconfirmed):
        self.login = login
        self.email = email
        self.password = password
        self.confirmed = confirmed
        self.adminconfirmed = adminconfirmed

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirmed', userId=self.userId)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth=('api', '{}'.format(MAILGUN_API_KEY)),
                    data={'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                            'to': self.email,
                            'subject': 'Register confirmation',
                            'text': 'Confirm your registration by clicking on the link: {}'.format(link),
                            'html': '<html><p>\
                                Confirm your registration by clicking on the link: <a href="{}">Confirm Email</a>\
                                </p></html>'.format(link)
                        }
                    )

    def json(self):
        return {
            'userId': self.userId,
            'login': self.login,
            'email': self.email,
            'confirmed': self.confirmed,
            'adminconfirmed': self.adminconfirmed
        }
    
    @classmethod
    def find_user(cls, userId):
        user = cls.query.filter_by(userId=userId).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None
    
    @classmethod
    def check_password(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user.password
        return None
    
    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()