from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required


def get_match_bp(db: SQLAlchemy) -> Blueprint:
    from ..models import User

    match = Blueprint('match', __name__)

    @match.route('/matches-undecided', methods=['GET'])
    @login_required
    def matches_undecided():
        undecided = current_user.possible_matches_undecided()
        # TODO - filtrowanie po preferencjach
        return jsonify([
            [match.user1_id, match.user2_id] for match in undecided
        ])

    return match


