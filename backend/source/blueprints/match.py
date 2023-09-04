from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from ..tools.response import resp
from ..models import change_user_choice

def get_match_bp(db: SQLAlchemy) -> Blueprint:
    from ..models import User

    match = Blueprint('match', __name__)

    @match.route('/matches-undecided', methods=['GET'])
    @login_required
    def matches_undecided():
        # TODO - filtrowanie po preferencjach
        possibleMatchesID = []
        for match in current_user.possible_matches_undecided():
            if current_user.public_id == match.user1_public_id:
                possibleMatchesID.append(match.user2_public_id)
            else:
                possibleMatchesID.append(match.user1_public_id)

        return jsonify(possibleMatchesID)

    @match.route('/update-match-choice', methods=['POST'])
    @login_required
    def update_match_choice():
        j = request.json
        user1 = current_user.public_id
        user2 = j.get("user2_public_id")
        choice = j.get("choice")
        print(j)
        change_user_choice(user1, user2, choice)
        return resp(200, 'success')

    
    

    return match

    
   

