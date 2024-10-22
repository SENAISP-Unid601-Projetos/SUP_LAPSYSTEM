from flask import Flask, jsonify, request, send_from_directory
from database import db
from flask_cors import CORS
from models import User, Order, Motoboy
import os
import json


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "database/deliveries.db")}'

db.init_app(app)

# Configurando CORS para permitir requisições de qualquer origem
CORS(app, resources={r"/*": {"origins": "*"}}) 


UPLOAD_FOLDER = os.path.join(os.getcwd(), r'BackEnd\APP_Principal\uploads')

print(os.getcwd())



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
    
    motoboy = Motoboy.query.filter_by(username=data['username']).first()

    if motoboy and motoboy.password == data['password']:
        return jsonify({"message": "Login successful", "motoboy_id": motoboy.id}), 200
    
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
    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

@app.route('/motoboys/register', methods=['POST'])
def register_motoboy():
    # Verifica se há arquivos na requisição
    if 'file1' not in request.files or 'file2' not in request.files or \
       'file3' not in request.files or 'file4' not in request.files:
        return jsonify({"message": "Todos os arquivos são obrigatórios"}), 400

    # Extrai os dados do cadastro do FormData
    cadastro_data = request.form.get('cadastro')
    if not cadastro_data:
        return jsonify({"message": "Dados do cadastro são obrigatórios"}), 400

    cadastro = json.loads(cadastro_data)  # Converte a string JSON de volta para um dicionário

    # Verifica se todos os campos necessários estão presentes
    if not all(key in cadastro for key in ['username', 'password', 'email', 'cpf']):
        return jsonify({"message": "Dados inválidos"}), 400

    new_motoboy = Motoboy(
        username=cadastro['username'],
        password=cadastro['password'],
        email=cadastro['email'],
        cpf=cadastro['cpf']
    )
    
    db.session.add(new_motoboy)
    db.session.commit()

    # Faz o upload das imagens
    for i, key in enumerate(['file1', 'file2', 'file3', 'file4']):
        file = request.files[key]
        file_path = os.path.join(UPLOAD_FOLDER, new_motoboy.username + key + ".jpg")
        file.save(file_path)

    return jsonify({"message": "Motoboy registrado com sucesso!"}), 201


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



@app.route('/upload', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(file_path)
        return "sucesso"
    
@app.route('/getImage/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)



if __name__ == '__main__':  
    app.run(host= '0.0.0.0', debug = True)  

