from . import api_bp, request, jsonify, secrets
from db import SQLDB
from time import time
from main import csrf

db = SQLDB()

@api_bp.route('/get_token', methods=['POST'])
@csrf.exempt
def get_token():
    if "code" not in request.json:
        return jsonify({'error': 'missing_code'}), 400

    code = request.json.get('code')
    token = db.get_code(code)
    if not token:
        return jsonify({'error': 'Invalid Token'}), 400
    elif time() >= token['expires']:
        db.delete_code(code)
        return jsonify({'error': 'Expired Token'}), 400
    
    # checking access token already exists
    access_token = db.get_access_token_by_id(token['user_id'])
    if access_token:
        db.delete_code(code)
        return access_token
    
    access_token = secrets.token_urlsafe(32)
    token['access_token'] = access_token
    token['expires'] = time() + 86400
    del token['code']
    
    db.add_access_token(token)
    db.delete_code(code)
    
    return jsonify({
        'access_token': access_token, 
        'token_type': 'bearer', 
        'user_id': token['user_id']
    })


@api_bp.route('/get_user', methods=['POST'])
@csrf.exempt
def get_user():
    if "access_token" not in request.json:
        return jsonify({'error': 'missing_access_token'}), 400
    elif "app_id" not in request.json or "api_key" not in request.json:
        return jsonify({'error': 'missing_app_id_or_api_key'}), 400
    else:
        access_token = request.json.get('access_token')
        app_id = request.json.get('app_id')
        api_key = request.json.get('api_key')
        
        if not access_token:
            return jsonify({'error': 'missing_access_token'}), 400
        
        token_ = db.get_access_token(access_token)
        app_data = db.get_app(app_id)

        if token_:
            if time() >= token_['expires']:
                db.delete_access_token(access_token)
                return jsonify({'error': 'invalid_access_token'}), 401
            
            if token_['app_id'] != app_id or app_data['api_key'] != api_key:
                return jsonify({'error': 'invalid_app_id_or_api_key'}), 401

            user_data = db.get_user_by_id(token_['user_id'])
            return user_data
        return jsonify({'error': 'invalid_access_token'}), 401