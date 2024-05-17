from flask import Blueprint, render_template, request
from models.language_model import LanguageModel
from models.history_model import HistoryModel
from deep_translator import GoogleTranslator

translate_controller = Blueprint("translate_controller", __name__)


@translate_controller.route("/", methods=["GET", "POST"])
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

    if request.method == "POST":
        text_to_translate = request.form.get("text-to-translate")
        translate_from = request.form.get("translate-from")
        translate_to = request.form.get("translate-to")

        HistoryModel({
            "text_to_translate": text_to_translate,
            "translate_from": translate_from,
            "translate_to": translate_to,
        }).save()

        translated = GoogleTranslator(
            source=translate_from, target=translate_to
        ).translate(text_to_translate)

        return render_template(
            "index.html",
            languages=all_languages,
            text_to_translate=text_to_translate,
            translate_from=translate_from,
            translate_to=translate_to,
            translated=translated,
        )
    # Renderizar o template com os dados padrão
    return render_template("index.html", **default_data)


def get_request_parameters():
    text_to_translate = request.form.get("text-to-translate")
    translate_from = request.form.get("translate-from")
    translate_to = request.form.get("translate-to")
    return text_to_translate, translate_from, translate_to


def translate_text(text_to_translate, translate_from, translate_to):
    translated_text = GoogleTranslator(
        source=translate_from, target=translate_to
    ).translate(text_to_translate)
    return translated_text


@translate_controller.route("/reverse", methods=["POST"])
def reverse():
    text_to_translate, translate_from, translate_to = get_request_parameters()

    translated_text = translate_text(
        text_to_translate, translate_from, translate_to
    )

    languages = LanguageModel.list_dicts()

    return render_template(
        "index.html",
        languages=languages,
        text_to_translate=translated_text,
        translate_from=translate_to,
        translate_to=translate_from,
        translated=text_to_translate,
    )
