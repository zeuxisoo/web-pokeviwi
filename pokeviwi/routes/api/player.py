from flask import Blueprint
from flask import jsonify, session, current_app
from enum import Enum
from ...utils import require_login

blueprint = Blueprint('api_player', __name__)

class PokeBallType(Enum):
    BASE   = 1
    GREAT  = 2
    ULTRA  = 3
    MASTER = 4

@blueprint.route('/stats', methods=['POST'])
@require_login
def stats():
    api = current_app.api_container.get(session['username'])

    response_dict   = api.get_inventory()
    inventory_items = response_dict['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']

    #
    poke_balls = {
        'base'  : 0,
        'great' : 0,
        'ultra' : 0,
        'master': 0
    }

    for item in inventory_items:
        try:
            item_id    = item['inventory_item_data']['item']['item_id']
            item_count = item['inventory_item_data']['item']['count']

            if item_id == PokeBallType.BASE.value:
                poke_balls['base'] = item_count

            if item_id == PokeBallType.GREAT.value:
                poke_balls['great'] = item_count

            if item_id == PokeBallType.ULTRA.value:
                poke_balls['ultra'] = item_count
        except:
            continue

    #
    profile_data = {
        'level'            : 0,
        'experience'       : 0,
        'next_level_xp'    : 0,
        'pokemons_captured': 0,
        'poke_stop_visits' : 0,
    }

    for item in inventory_items:
        if 'player_stats' in item['inventory_item_data']:
            player_stats = item['inventory_item_data']['player_stats']

            if 'level' in player_stats:
                profile_data['level'] = player_stats['level']

            if 'experience' in player_stats:
                profile_data['experience']    = player_stats['experience']

            if 'next_level_xp' in player_stats:
                profile_data['next_level_xp'] = player_stats['next_level_xp']

            if 'pokemons_captured' in player_stats:
                profile_data['pokemons_captured'] = player_stats['pokemons_captured']

            if 'poke_stop_visits' in player_stats:
                profile_data['poke_stop_visits'] = player_stats['poke_stop_visits']

    return jsonify(
        player_stats = dict(
            poke_balls   = poke_balls,
            profile_data = profile_data
        )
    )
