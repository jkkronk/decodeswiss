from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field

app = Flask(__name__)


class Translation(BaseModel):
    """
    A class that represents the translation of a swiss german text.
    """
    en_translation: str = Field(..., description="Translation from swiss german to english.")
    de_translation: str = Field(..., description="Translation from swiss german to high german.")
    is_swiss_german: bool = Field(..., description="True if input text is in swiss german, else false.")
    is_bernese_dialect: bool = Field(..., description="True if input text could be in bernese dialect, else false.")
    is_basel_dialect: bool = Field(..., description="True if input text could be in basel dialect, else false.")
    is_solothurn_dialect: bool = Field(..., description="True if input text could be in solothurn dialect, else false.")
    is_aargau_dialect: bool = Field(..., description="True if input text could be in aargau dialect, else false.")
    is_lucerne_dialect: bool = Field(..., description="True if input text could be in lucerne dialect, else false.")
    is_zug_dialect: bool = Field(..., description="True if input text is could be zug dialect, else false.")
    is_zurich_dialect: bool = Field(..., description="True if input text is could be zurich dialect, else false.")
    is_stgallen_dialect: bool = Field(..., description="True if input text is could be st. gallen dialect, else false.")
    is_thurgau_dialect: bool = Field(..., description="True if input text is could be thurgau dialect, else false.")
    is_appenzell_dialect: bool = Field(..., description="True if input text is could be appenzell dialect, else false.")
    is_schaffhausen_dialect: bool = Field(..., description="True if input text could be in schaffhausen dialect, else false.")
    is_grisons_dialect: bool = Field(..., description="True if input text could be in grisons dialect, else false.")
    is_wallis_dialect: bool = Field(..., description="True if input text could be in wallis dialect, else false.")
    is_glarus_dialect: bool = Field(..., description="True if input text could be in glarus dialect, else false.")
    is_uri_dialect: bool = Field(..., description="True if input text is could be uri dialect, else false.")
    is_schwyz_dialect: bool = Field(..., description="True if input text is could be schwyz dialect, else false.")
    is_obwalden_dialect: bool = Field(..., description="True if input text is could be obwalden or nidwalden dialect, else false.")


def translate_text(text, openai_api_key=None):
    if openai_api_key == "":
        client = instructor.patch(OpenAI())
    else:
        client = instructor.patch(OpenAI(api_key=openai_api_key))

    prompt = (f"Translate this swiss german to english and german: {text}. "
              f"Indicate if the input text is in swiss german."
              f"Indicate if the input text could be of a certain dialect of swiss german.")

    translated: Translation = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=Translation,
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_retries=2,
    )

    return translated


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    # Extract text and language information from the JSON request
    data = request.get_json()
    text_to_translate = data['text']

    # Perform translation
    result = translate_text(text_to_translate)

    print(result)
    # Return the translated text as a JSON response
    return jsonify({
        'original_text': text_to_translate,
        'en_translation': result.en_translation,
        'de_translation': result.de_translation,
        'is_swiss_german': result.is_swiss_german,
        'is_bernese_dialect': result.is_bernese_dialect,
        'is_basel_dialect': result.is_basel_dialect,
        'is_solothurn_dialect': result.is_solothurn_dialect,
        'is_aargau_dialect': result.is_aargau_dialect,
        'is_lucerne_dialect': result.is_lucerne_dialect,
        'is_zug_dialect': result.is_zug_dialect,
        'is_zurich_dialect': result.is_zurich_dialect,
        'is_stgallen_dialect': result.is_stgallen_dialect,
        'is_thurgau_dialect': result.is_thurgau_dialect,
        'is_appenzell_dialect': result.is_appenzell_dialect,
        'is_schaffhausen_dialect': result.is_schaffhausen_dialect,
        'is_grisons_dialect': result.is_grisons_dialect,
        'is_wallis_dialect': result.is_wallis_dialect,
        'is_glarus_dialect': result.is_glarus_dialect,
        'is_uri_dialect': result.is_uri_dialect,
        'is_schwyz_dialect': result.is_schwyz_dialect,
        'is_obwalden_dialect': result.is_obwalden_dialect
    })


if __name__ == '__main__':
    app.run(debug=True)
