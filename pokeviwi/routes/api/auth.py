from flask import Blueprint
from flask import request, jsonify, current_app
from pgoapi import PGoApi

blueprint = Blueprint('api_auth', __name__)

@blueprint.route('/login', methods=['POST'])
def login():
    username    = request.json['username']
    password    = request.json['password']
    auth_method = request.json['auth_method']

    api = PGoApi()
    api.set_position(0, 0, 0)

    if not api.login(auth_method, username, password):
        return jsonify(
            ok=False,
            message="Invalid account information"
        ), 401
    else:
        api.get_player()

        response_dict = api.call()
        player_data   = response_dict['responses']['GET_PLAYER']['player_data']

        #
        currencies = dict()

        for c in player_data['currencies']:
            currencies[c['name'].lower()] = c['amount'] if 'amount' in c else 0

        #
        player = dict(
            username            = player_data['username'],
            currencies          = currencies,
            max_pokemon_storage = player_data['max_pokemon_storage'],
            max_item_storage    = player_data['max_item_storage'],
            created_at          = player_data['creation_timestamp_ms'],
        )

        #
        current_app.api = api

        return jsonify(
            player=player
        )
