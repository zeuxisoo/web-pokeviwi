import requests
import time

from flask import Blueprint
from flask import request, jsonify, session, current_app
from pgoapi import pgoapi, exceptions
from ...utils import require_login

blueprint = Blueprint('api_auth', __name__)

@blueprint.route('/login/ptc', methods=['POST'])
def login_ptc():
    username    = request.json['username']
    password    = request.json['password']

    ok      = False
    message = ""
    player  = dict()

    api = pgoapi.PGoApi()
    api.set_position(0, 0, 0)

    try:
        api.set_authentication(provider='ptc', username=username, password=password)

        response_dict = api.get_player()

        if 'responses' not in response_dict:
            message = "Cannot find player information"
        else:
            ok          = True
            player_data = response_dict['responses']['GET_PLAYER']['player_data']

            currencies = dict()
            for c in player_data['currencies']:
                currencies[c['name'].lower()] = c['amount'] if 'amount' in c else 0

            player = dict(
                username            = player_data['username'],
                currencies          = currencies,
                max_pokemon_storage = player_data['max_pokemon_storage'],
                max_item_storage    = player_data['max_item_storage'],
                created_at          = player_data['creation_timestamp_ms'],
            )

            session['username'] = player_data['username']
            current_app.api_container.add(player_data['username'], api)
    except exceptions.AuthException as e:
        message = "Invalid account information"

    return jsonify(
        ok      = ok,
        message = message,
        player  = player
    ), 200 if ok is True else 401

@blueprint.route('/login/google', methods=['POST'])
def login_google():
    auth_code = request.json['auth_code']

    ok      = False
    message = ""
    player  = dict()

    response = requests.post("https://accounts.google.com/o/oauth2/token", data={
        'grant_type'    : 'authorization_code',
        'redirect_uri'  : 'urn:ietf:wg:oauth:2.0:oob',
        'scope'         : 'openid email https://www.googleapis.com/auth/userinfo.email',
        'client_secret' : 'NCjF1TLi2CcY6t5mt0ZveuL7',
        'client_id'     : '848232511240-73ri3t7plvk96pj4f85uj8otdat2alem.apps.googleusercontent.com',
        'code'          : auth_code
    })

    data = response.json()

    if 'error' in data:
        message = data['error_description']
    else:
        access_token  = data['id_token']
        refresh_token = data['refresh_token']
        expires_in    = data['expires_in']

        api = pgoapi.PGoApi()
        api.set_position(0, 0, 0)

        try:
            api.set_authentication(provider = 'google', oauth2_refresh_token="oauth2rt_{0}".format(refresh_token))

            api.get_auth_provider()._access_token        = access_token
            api.get_auth_provider()._access_token_expiry = time.time() + expires_in
            api.get_auth_provider()._login               = True

            response_dict = api.get_player()

            if 'responses' not in response_dict:
                message = "Cannot find player information"
            else:
                ok          = True
                player_data = response_dict['responses']['GET_PLAYER']['player_data']

                currencies = dict()
                for c in player_data['currencies']:
                    currencies[c['name'].lower()] = c['amount'] if 'amount' in c else 0

                player = dict(
                    username            = player_data['username'],
                    currencies          = currencies,
                    max_pokemon_storage = player_data['max_pokemon_storage'],
                    max_item_storage    = player_data['max_item_storage'],
                    created_at          = player_data['creation_timestamp_ms'],
                )

                session['username'] = player_data['username']
                current_app.api_container.add(player_data['username'], api)
        except exceptions.AuthException as e:
            message = "Invalid account information"

    return jsonify(
        ok      = ok,
        message = message,
        player  = player,
    ), 200 if ok is True else 401

@blueprint.route('/logout', methods=['GET'])
@require_login
def logout():
    if 'username' in session:
        current_app.api_container.remove(session['username'])

        session.pop('username')

    return jsonify(
        ok      = True,
        message = "Logout successfully"
    )
