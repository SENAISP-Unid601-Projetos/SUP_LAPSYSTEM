from flask import Flask, jsonify, request
from database import db
from flask_cors import CORS
from models import User, Order
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deliveries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Configurando CORS para permitir requisições de qualquer origem
CORS(app, resources={r"/*": {"origins": "*"}}) 



with app.app_context():
    db.create_all()  # Cria as tabelas no banco de dados

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Invalid input"}), 400

    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.password == data['password']:  # Aqui você deve usar uma verificação segura de senha
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data or 'email' not in data or 'cpf' not in data:
        return jsonify({"message": "Invalid input"}), 400

    new_user = User(
        username=data['username'],
        password=data['password'],
        email=data['email'],
        cpf=data['cpf']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(client_id=data['client_id'], address=data['address'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Ordem criada com sucesso'}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        return jsonify({'id': order.id, 'status': order.status, 'address': order.address})
    return jsonify({'message': 'Ordem não encontrada'}), 404

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


# Defina o diretório onde os arquivos enviados serão salvos
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Certifique-se de que a pasta existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    print("entrei")
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return jsonify({"message": f"File uploaded successfully to {file_path}"}), 200


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)

