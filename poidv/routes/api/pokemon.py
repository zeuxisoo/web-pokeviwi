from flask import Blueprint
from flask import request, jsonify
from pgoapi import PGoApi

blueprint = Blueprint('api_pokemon', __name__)

@blueprint.route('/pokemon/all', methods=['POST'])
def all():
    username    = request.json['username']
    password    = request.json['password']
    auth_method = request.json['auth_method']

    api = PGoApi()
    api.set_position(0, 0, 0)

    if not api.login(auth_method, username, password):
        return jsonify(
            ok=False,
            message="Invalid account information"
        )
    else:
        api.get_inventory()

        response_dict   = api.call()
        all_pokemons    = []
        inventory_items = response_dict['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']

        for i in inventory_items:
            if 'pokemon_data' in i['inventory_item_data'] and 'is_egg' not in i['inventory_item_data']['pokemon_data']:
                pokemon = i['inventory_item_data']['pokemon_data']

                all_pokemons.append(dict(
                    id               = pokemon['id'],
                    pokemon_id       = pokemon['pokemon_id'],
                    cp               = pokemon['cp'],
                    hp               = pokemon['stamina'],
                    hp_max           = pokemon['stamina_max'],
                    move1            = pokemon['move_1'],
                    move2            = pokemon['move_2'],
                    height_m         = pokemon['height_m'],
                    weight_kg        = pokemon['weight_kg'],
                    attack           = pokemon['individual_attack'] if 'individual_attack' in pokemon else 0,
                    defense          = pokemon['individual_defense'] if 'individual_defense' in pokemon else 0,
                    stamina          = pokemon['individual_stamina'] if 'individual_stamina' in pokemon else 0,
                    cp_multiplier    = pokemon['cp_multiplier'],
                    nickname         = pokemon['nickname'] if 'nickname' in pokemon else "",
                    pokeball         = pokemon['pokeball'],
                    creation_time_ms = pokemon['creation_time_ms'],
                ))

        return jsonify(
            pokemons=all_pokemons
        )
