from flask import Flask, jsonify, request
from database import db
from flask_cors import CORS
from models import User, Order

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deliveries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

CORS(app)

with app.app_context():
    db.create_all()  # Cria as tabelas no banco de dados

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data or 'user_type' not in data:
        return jsonify({"message": "Invalid input"}), 400
    
    new_user = User(username=data['username'], password=data['password'], user_type=data['user_type'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(client_id=data['client_id'], address=data['address'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order created successfully'}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        return jsonify({'id': order.id, 'status': order.status, 'address': order.address})
    return jsonify({'message': 'Order not found'}), 404

@app.route('/orders/all', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()  # Pega todas as ordens do banco de dados
    orders_list = [{
        'id': order.id,
        'client_id': order.client_id,
        'address': order.address,
        'status': order.status
    } for order in orders]  # Cria uma lista de dicionários para cada ordem
    return jsonify(orders_list), 200  # Retorna a lista de ordens em formato JSON

if __name__ == '__main__':
    app.run(debug=True)
