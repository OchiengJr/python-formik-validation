#!/usr/bin/env python3

from random import randint
from faker import Faker
from sqlalchemy.exc import IntegrityError

from app import app
from models import db, Customer

fake = Faker()

def make_customers(num_customers=10):
    Customer.query.delete()

    for _ in range(num_customers):
        try:
            customer = Customer(
                email=fake.unique.email(),
                age=randint(18, 80),
                name=fake.name()
            )
            db.session.add(customer)
        except IntegrityError:
            db.session.rollback()  # Rollback if email is not unique

    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        make_customers(num_customers=20)  # Generate 20 customers for example
