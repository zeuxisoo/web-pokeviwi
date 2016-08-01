from flask import Blueprint
from flask import request, jsonify, session, current_app
from enum import Enum
from ...utils import require_login

blueprint = Blueprint('api_pokemon', __name__)

class ReleaseResultType(Enum):
    UNSET                = 0
    SUCCESS              = 1
    POKEMON_DEPLOYED     = 2
    FAILED               = 3
    ERROR_POKEMON_IS_EGG = 4

@blueprint.route('/all', methods=['POST'])
@require_login
def all():
    api = current_app.api_container.get(session['username'])

    response_dict   = api.get_inventory()
    all_pokemons    = []
    inventory_items = response_dict['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']

    for i in inventory_items:
        if 'pokemon_data' in i['inventory_item_data'] and 'is_egg' not in i['inventory_item_data']['pokemon_data']:
            pokemon = i['inventory_item_data']['pokemon_data']

            all_pokemons.append(dict(
                id                       = str(pokemon['id']),
                pokemon_id               = pokemon['pokemon_id'],
                cp                       = pokemon['cp'],
                hp                       = pokemon['stamina'] if 'stamina' in pokemon else 0,
                hp_max                   = pokemon['stamina_max'] if 'stamina_max' in pokemon else 0,
                move1                    = pokemon['move_1'],
                move2                    = pokemon['move_2'],
                height_m                 = pokemon['height_m'],
                weight_kg                = pokemon['weight_kg'],
                attack                   = pokemon['individual_attack'] if 'individual_attack' in pokemon else 0,
                defense                  = pokemon['individual_defense'] if 'individual_defense' in pokemon else 0,
                stamina                  = pokemon['individual_stamina'] if 'individual_stamina' in pokemon else 0,
                cp_multiplier            = pokemon['cp_multiplier'],
                additional_cp_multiplier = pokemon['additional_cp_multiplier'] if 'additional_cp_multiplier' in pokemon else 0,
                nickname                 = pokemon['nickname'] if 'nickname' in pokemon else "",
                creation_time_ms         = pokemon['creation_time_ms'],
            ))

    return jsonify(
        ok              = True,
        message         = "",
        pokemons        = all_pokemons,
        inventory_items = inventory_items
    )

@blueprint.route('/release', methods=['POST'])
@require_login
def release():
    pokemon_id = request.json['pokemon_id']

    status  = True
    message = ""
    candy   = 0

    if pokemon_id is None or pokemon_id == "":
        status  = False
        message = "Please provide pokemon id to transfer"
    else:
        api = current_app.api_container.get(session['username'])

        response_dict  = api.release_pokemon(pokemon_id=int(pokemon_id))
        release_result = response_dict['responses']['RELEASE_POKEMON']['result']

        if release_result != ReleaseResultType.SUCCESS.value:
            message = "Cannot transfer pokemon, Please make sure this pokemon is exists"
        else:
            message = "Pokemon transferred"
            candy   = response_dict['responses']['RELEASE_POKEMON']['candy_awarded']

    return jsonify(
        ok      = status,
        message = message,
        candy   = candy
    ), 200 if status is True else 400
