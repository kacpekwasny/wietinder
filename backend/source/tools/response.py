from flask import Response, jsonify

def resp(code: int, info=None) -> tuple[Response, int]:
    ok = code == 200
    data = dict(ok=ok)

    if isinstance(info, str):
        data |= dict(info=info)

    return jsonify(data), code