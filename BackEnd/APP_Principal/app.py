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

# Configurando CORS
CORS(app)

# Diretórios de upload
UPLOAD_FOLDERS = {
    'file1': os.path.join(os.getcwd(), r'BackEnd\APP_Principal\uploads\FotoDoRosto'),
    'file2': os.path.join(os.getcwd(), r'BackEnd\APP_Principal\uploads\CopiaCNH'),
    'file3': os.path.join(os.getcwd(), r'BackEnd\APP_Principal\uploads\FotoMoto(ComPlaca)'),
    'file4': os.path.join(os.getcwd(), r'BackEnd\APP_Principal\uploads\DocumentoDaMoto'),
}

with app.app_context():
    db.create_all()  # Cria as tabelas no banco de dados

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Invalid input"}), 400

    user = User.query.filter_by(username=data['username']).first() or \
           Motoboy.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        return jsonify({"message": "Login successful", f"{type(user).__name__.lower()}_id": user.id}), 200
    
    return jsonify({"message": "Invalid username or password"}), 401

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    if not data or 'username' not in data or 'password' not in data or 'email' not in data or 'cpf' not in data:
        return jsonify({"message": "Invalid input"}), 400

    new_user = User(**data)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuário registrado com sucesso!"}), 201

@app.route('/motoboys/register', methods=['POST'])
def register_motoboy():
    if not all(file in request.files for file in UPLOAD_FOLDERS):
        return jsonify({"message": "Todos os arquivos são obrigatórios"}), 400

    cadastro_data = request.form.get('cadastro')
    if not cadastro_data:
        return jsonify({"message": "Dados do cadastro são obrigatórios"}), 400

    cadastro = json.loads(cadastro_data)
    if not all(key in cadastro for key in ['username', 'password', 'email', 'cpf']):
        return jsonify({"message": "Dados inválidos"}), 400

    new_motoboy = Motoboy(**cadastro)
    db.sess ion.add(new_motoboy)
    db.session.commit()

    for file_key in UPLOAD_FOLDERS:
        file = request.files[file_key]
        file_path = os.path.join(UPLOAD_FOLDERS[file_key], f"{new_motoboy.username}{file_key}.jpg")
        file.save(file_path)

    return jsonify({"message": "Motoboy registrado com sucesso!"}), 201

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(**data)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Ordem criada com sucesso'}), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    return jsonify({'id': order.id, 'status': order.status, 'address': order.address}) if order else \
           jsonify({'message': 'Ordem não encontrada'}), 404

@app.route('/orders/all', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    orders_list = [{'id': order.id, 'client_id': order.client_id, 'address': order.address, 'status': order.status} for order in orders]
    return jsonify(orders_list), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    f = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDERS['file2'], f.filename)
    f.save(file_path)
    return jsonify({"message": "Upload bem-sucedido"}), 201

@app.route('/getImage/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDERS['file2'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
