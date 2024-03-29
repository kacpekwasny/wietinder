from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from ..tools.response import resp
from ..models import MatchChoice

def get_match_bp(db: SQLAlchemy) -> Blueprint:
    from ..models import User

    match = Blueprint('match', __name__)

    @match.route('/matches-undecided', methods=['GET'])
    @login_required
    def matches_undecided():
        # TODO - filtrowanie po preferencjach
        possibleMatchesID = []
        print(current_user.possible_matches_undecided())
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
        other_user_public_id = j.get("other_user_public_id")
        my_choice = j.get("my_choice")
        
        User.change_match_choice(current_user, MatchChoice(my_choice), other_user_public_id)
        db.session.commit()

        return resp(200, 'success')
    
    @match.route('/who-likes-me', methods=['GET'])
    @login_required
    def get_who_likes_me():
        return jsonify([
            match.get_other_user(current_user.public_id).json()
            for match in User.likes_me(current_user)
        ])
            
    
    @match.route('/my-matches', methods=['GET'])
    @login_required
    def get_matches():
        matchesID = []
        for match in User.my_matches(current_user):
            matchesID.append(match.get_other_user(current_user.public_id).public_id)
        
        return jsonify(matchesID)

    return match


