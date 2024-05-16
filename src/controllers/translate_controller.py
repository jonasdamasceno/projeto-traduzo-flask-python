from flask import Blueprint, render_template
from models.language_model import LanguageModel

translate_controller = Blueprint("translate_controller", __name__)


@translate_controller.route("/", methods=["GET"])
def index():
    # Obter todos os idiomas
    all_languages = LanguageModel.list_dicts()

    # Definir os dados padrão para o template
    default_data = {
        "languages": all_languages,
        "text_to_translate": "O que deseja traduzir?",
        "translate_from": "pt",
        "translate_to": "en",
        "translated": "What do you want to translate?",
    }

    # Renderizar o template com os dados padrão
    return render_template("index.html", **default_data)
