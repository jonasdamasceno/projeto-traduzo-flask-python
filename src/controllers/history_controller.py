from flask import Blueprint, jsonify
from models.history_model import HistoryModel
import json

history_controller = Blueprint("history_controller", __name__)


@history_controller.route("/", methods=["GET"])
def index():
    history_data = json.loads(HistoryModel.list_as_json())
    return jsonify(history_data), 200
