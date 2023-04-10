from flask import Blueprint, jsonify, request
from os import remove
from .utils import ROOT


api = Blueprint("api", __name__, url_prefix="/api")


@api.delete("/files")
def delete_file():
    file = request.form.get("file")
    if not file:
        return jsonify({
            "status": "error",
            "message": "Empty file!"
        })
    path = ROOT / file
    try:
        path.unlink()
        pass
    except Exception as exc:
        return jsonify({
            "status": "error",
            "message": str(exc)
        })
    return jsonify({
        "status": "success",
        "message": "File deleted"
    })
