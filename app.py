
from extraction import extrair_dados
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_swagger_ui import get_swaggerui_blueprint
import datetime

app = Flask(__name__)

# Configurações JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Chave secreta para JWT
jwt = JWTManager(app)

# Swagger UI config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # JSON do Swagger
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Embrapa Data API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Rota de login para gerar token JWT
@app.route('/login', methods=['POST'])
def login():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({'msg': 'Faltam credenciais'}), 400

    username = request.json['username']
    password = request.json['password']

    # Validação de usuário simples (somente para exemplo)
    if username != 'admin' or password != 'password':
        return jsonify({'msg': 'Usuário ou senha inválidos'}), 401

    # Gera o token JWT
    expires = datetime.timedelta(days=1)
    access_token = create_access_token(identity={'username': username}, expires_delta=expires)
    return jsonify(access_token=access_token), 200

# Rota protegida que faz a extração dos dados
@app.route('/extrair', methods=['GET'])
@jwt_required()  # Exige um token JWT para acessar essa rota
def extrair():
    ano = request.args.get('ano')
    opcao = request.args.get('opcao')
    subopcao = request.args.get('subopcao')

    if not ano or not opcao or not subopcao:
        return jsonify({'error': 'Parâmetros insuficientes: ano, opcao, subopcao são obrigatórios'}), 400

    dados = extrair_dados(ano, opcao, subopcao)

    if dados:
        return jsonify(dados), 200
    else:
        return jsonify({'error': 'Não foi possível extrair os dados ou dados não encontrados'}), 500

if __name__ == '__main__':
    app.run(debug=True)