from flask import Blueprint
from flask import jsonify, current_app
from enum import Enum

blueprint = Blueprint('api_player', __name__)

class PokeBallType(Enum):
    BASE   = 1
    GREAT  = 2
    ULTRA  = 3
    MASTER = 4

@blueprint.route('/inventory', methods=['POST'])
def inventory():
    api = current_app.api

    api.get_inventory()

    response_dict   = api.call()
    inventory_items = response_dict['responses']['GET_INVENTORY']['inventory_delta']['inventory_items']

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

    return jsonify(
        poke_balls = poke_balls
    )
