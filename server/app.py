from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import Customer, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/customers", methods=['GET', 'POST'])
def customers():
    if request.method == 'GET':
        try:
            customers = Customer.query.all()
            return make_response(jsonify([customer.to_dict() for customer in customers]), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    elif request.method == 'POST':
        data = request.get_json()
        if not data or not all(key in data for key in ['name', 'email', 'age']):
            return make_response(jsonify({'error': 'Missing required fields (name, email, age)'}), 400)
        
        try:
            customer = Customer(name=data['name'], email=data['email'], age=data['age'])
            db.session.add(customer)
            db.session.commit()
            return make_response(jsonify({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'age': customer.age
            }), 201)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

if __name__ == "__main__":
    app.run(port="5555", debug=True)
