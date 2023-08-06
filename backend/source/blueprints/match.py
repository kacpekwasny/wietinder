from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_required


def get_match_bp(db: SQLAlchemy) -> Blueprint:
    from ..models import User

    match = Blueprint('match', __name__)

    @match.route('/pairs-undecided', methods=['GET'])
    @login_required
    def pairs_undecided():
        undecided = current_user.possible_pairs_undecided()
        # TODO - filtrowanie po preferencjach
        return jsonify([
            [pair.user1_id, pair.user2_id] for pair in undecided
        ])

    return match


