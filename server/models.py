from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from email_validator import validate_email, EmailNotValidError

db = SQLAlchemy()

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f'Customer: {self.name}, age: {self.age}, email: {self.email}'

    @validates('email')
    def validate_email_format(self, key, email):
        try:
            validate_email(email)
            return email
        except EmailNotValidError as e:
            raise ValueError(f'Invalid email address: {email}') from e
