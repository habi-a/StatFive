from flask import request, json, Response, Blueprint
from flasgger import swag_from

from ..specs import specs_match
from ..models.match import Match
from ..models.team import TeamHasMatchPlayed
from ..auth.authentication import Auth
from ..helper import custom_response

match_api = Blueprint('match', __name__)


# @match_api.route('/all_match_by_date', methods=['GET'])
# @swag_from(specs_match.all_match_by_date)
# def all_match_by_date():
#     team_in_db = TeamHasMatchPlayed.query.all()
#     teams = []
#     for team in team_in_db:
#         teams.append(team.to_json())
#     return custom_response({'error': False, 'message': 'Liste de team.', 'data': teams}, 200)


@match_api.route('/stat_match_by_id/<int:id>', methods=['GET'])
@swag_from(specs_match.stat_match_by_id)
def stat_team_by_id(id):
    match_in_db = Match.query.filter_by(id=id).first()
    if not match_in_db:
        message = {'error': True, 'message': 'Le match existe pas.', 'data': None}
        return custom_response(message, 404)
    stats = []
    for stat in match_in_db.team_match_played:
        stats.append(stat.to_json())
    data = {**match_in_db.to_json(), **{'stats': stats}}
    return custom_response({'error': False, 'message': 'Match stats by id.', 'data': data}, 200)
