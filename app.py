import MyLogger1
from CustomerFacade2 import CustomerFacade2
from UserFacade import userFacade2
from User_db import User
from Db_Customers import Customer
from flask import Flask, request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from MyLogger1 import Logger
from functools import wraps
from datetime import datetime, timedelta
import jwt

customerFacade = CustomerFacade2()
userFacade = userFacade2()
logger = MyLogger1.Logger.get_instance()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'RoyDuvdevroy'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer ')
            data = jwt.decode(token, app.config['SECRET_KEY'])
     #   if 'Authorization' in request.headers:
      #      token = request.headers['Authorization']
       #     token = token.removeprefix('Bearer')
        #logger.logger.info(f'app run: received token')
        #if not token:
         #   logger.logger.error(f'app run: Token is missing')
        #    return make_response({'message': 'Token is missing !!'}, 401)
       # try:
       #     payload = jwt.decode(token, app.config['SECRET_KEY'])
       # except():
      #      logger.logger.error(f'app run: token is invalid')
     #       return make_response('status: user token is invalid', 401)
        return f(*args, **kwargs)

    return decorated


@app.route("/")
def home():
    return '''
        <html>
            Ready!
        </html>
    '''


# url/<resource> <--- GET POST
@app.route('/customers', methods=['GET', 'POST'])
@token_required
def get_or_post_customer():
    if request.method == 'GET':
        logger.logger.info(f'app run: getting customers')
        customers = customerFacade.get_all_customers()
        answer = str(customers)
        return answer
    if request.method == 'POST':
        logger.logger.info(f'app run: posting new customer')
        new_customer = request.form
        customer = Customer(id=new_customer.get("id"), name=new_customer.get("name"),
                            address=new_customer.get("address"))
        p = customerFacade.add_customer(customer)
        print(p)
        if p is not None:
            logger.logger.info(f'app run: customer id number {customer.id} add successfully ')
            return make_response('status: success', 201)
        else:
            logger.logger.error(f'app run: failed to post new customer')
            return make_response('status: failed', 404)


@app.route('/customers/<int:id>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
@token_required
def get_customer_by_id(id):
    return "hello"
    if request.method == 'GET':
        logger.logger.info(f'app run: getting customer by id: {id}')
        customer = customerFacade.get_by_id(id)
        if customer:
            logger.logger.info(f'app run: successfully get customer id number: {id}')
            return str(customer)
        else:
            logger.logger.error(f'app run: failed get customer')
            return make_response('status: failed to get customer by id', 404)
    if request.method == 'PUT':
        logger.logger.info(f'app run: starting updating procedure for customer id: {id}')
        customer = customerFacade.get_by_id(id)
        logger.logger.info(f'app run: getting customer by id {id}')
        if customer:
            logger.logger.info(f'app run: updating customer')
            modified_customer = customerFacade.update_customer(customer)
            if modified_customer:
                logger.logger.info(f'app run: successfully updated customer id number {id}')
                return make_response('status: customer updated successfully', 201)
            else:
                logger.logger.error(f'app run: failed updating customer')
                return make_response('status: failed to update customer', 404)
    if request.method == 'PATCH':
        logger.logger.info(f'app run: starting updating procedure for customer id: {id}')
        logger.logger.info(f'app run: getting customer by id {id}')
        customer = customerFacade.get_by_id(id)
        if customer:
            logger.info(f'app run: updating customer')
            modified_customer = customerFacade.update_customer(customer)
            if modified_customer:
                logger.logger.info(f'app run: successfully updated customer id {id}')
                return make_response('status: customer updated successfully', 201)
            else:
                logger.logger.info(f'app run: failed to update customer id: {id}')
                return make_response('status: failed to update customer', 404)
    if request.method == 'DELETE':
        logger.logger.info(f'app run: starting deleting procedure for customer id: {id}')
        customer = customerFacade.get_by_id(id)
        logger.logger.info(f'app run: getting customer by id: {id}')
        print(customer)
        if customer:
            logger.logger.info(f'app run: removing customer by id: {id}')
            p = customerFacade.remove_customer(customer)
            if p is None:
                logger.logger.info(f'app run: successfully deleted customer id: {id}')
                return make_response('status: customer updated successfully', 201)
            else:
                logger.logger.info(f'app run: failed to delete customer id: {id}')
                return make_response('status: failed to delete customer', 404)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    username = data.get('user_name')
    print(username)
    password1 = data.get('password')
    user = userFacade.get_by_name(username)
    if user:
        logger.logger.error(f'app run: user already exist')
        return make_response('user already exist', 404)
    else:
        logger.logger.info(f'app run:insert a new user')
        new_user = User(id=None, user_name=username, password=password1)
        userFacade.add_user(new_user)
        logger.logger.info(f'app run:insert a new user - {new_user}')
        return make_response('status: success', 201)


@app.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data.get('user_name')
    password1 = data.get('password')
    if not data or not username or not password1:
        logger.logger.error(f'app run: password and username is required')
        return make_response('password and username is required', 401, {'WWW-Authenticate': 'Basic realm="Login '
                                                                                            'required'})
    user = userFacade.get_by_user_and_password(username, password1)
    print(user)
    if user is None:
        logger.logger.error(f'app run: user dose not exist or wrong password')
        return make_response('user dose not exist or wrong password', 401, {'WWW-Authenticate': 'Basic realm="user '
                                                                                                'dose not exist'})

    logger.logger.info(f'app run: user login successfully')
    token = jwt.encode({
        'public_id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET_KEY'])

    return make_response(jsonify({'token': token.decode('UTF-8')}), 201)


app.run(host='127.0.0.53', port=8443, debug=True)
