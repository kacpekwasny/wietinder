from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required
from flask_socketio import SocketIO

from ..socket_events import login_required_sock
from ..tools.response import resp
from ..models import MatchChoice, PossibleMatch

def get_match_bp(db: SQLAlchemy, socketio: SocketIO) -> Blueprint:
    from ..models import User

    match = Blueprint('match', __name__)

    @match.route('/api/matches-undecided', methods=['GET'])
    @login_required
    def matches_undecided():
        # TODO - filtrowanie po preferencjach
        possible_matches_pid = []
        current_user: User
        for match in User.possible_matches_undecided(current_user):
            other_user = PossibleMatch.get_other_user(match, current_user.public_id)
            if current_user.sex.value in other_user.get_target_sex():
                possible_matches_pid.append(other_user.public_id)

        return jsonify(possible_matches_pid)

    @match.route('/api/update-match-choice', methods=['POST'])
    @login_required
    def update_match_choice():
        j = request.json
        other_user_public_id = j.get("other_user_public_id")
        my_choice = j.get("my_choice")
        
        User.change_match_choice(current_user, MatchChoice(my_choice), other_user_public_id)
        db.session.commit()

        return resp(200, 'success')
    
    @socketio.on('update-match-choice')
    @login_required_sock
    def update_match_choice_sock(*args, **kwargs):
        j: dict = args[0]
        other_user_public_id = j.get("other_user_public_id")
        my_choice = j.get("my_choice")
        
        User.change_match_choice(current_user, MatchChoice(my_choice), other_user_public_id)
        db.session.commit()

        return resp(200, 'success')
        


    @match.route('/api/who-likes-me', methods=['GET'])
    @login_required
    def get_who_likes_me():
        return jsonify([
            match.get_other_user(current_user.public_id).json()
            for match in User.likes_me(current_user)
        ])
    
    return match
            

