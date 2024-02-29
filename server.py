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
    dialects: list[str] = Field(..., description="List of dialects that the input text could be. "
                                      "For example for Zurich and Bern it should be in this format ['zurich', 'bern']."
                                      "But for Basel and Solothurn it should be in this format ['basel', 'solothurn']."
                                                 "But for Zurich only it should be in this format ['zurich'].")

def translate_text(text, openai_api_key=None):
    if openai_api_key == "":
        client = instructor.patch(OpenAI())
    else:
        client = instructor.patch(OpenAI(api_key=openai_api_key))

    prompt = (f"Translate this swiss german to english and german: {text}. "
              f"Indicate if the input text is in swiss german."
              f"Indicate what dialect the input text could be. The format is a list "
              f"of most likely dialect or dialects. For example 'hoi zäme' it should be ['zurich']. "
              f"Or for example for 'Zum Znüni hät's feine Schoggigipfeli gha, da chame würkli nid klage.' "
              f"Should the answer be ['bern'] but for 'Mir göhn später in d'Stadt zum e bitzeli shoppe.' the answer"
              f"could be ['basel', 'solothurn', 'zurich']. If you get it right you will get a bonus.")

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
        'is_bernese_dialect': list2bool(result.dialects, 'bern'),
        'is_basel_dialect': list2bool(result.dialects, 'basel'),
        'is_solothurn_dialect': list2bool(result.dialects, 'solothurn'),
        'is_aargau_dialect': list2bool(result.dialects, 'aargau'),
        'is_lucerne_dialect': list2bool(result.dialects, 'lucerne'),
        'is_zug_dialect': list2bool(result.dialects, 'zug'),
        'is_zurich_dialect': list2bool(result.dialects, 'zurich'),
        'is_stgallen_dialect': list2bool(result.dialects, 'stgallen'),
        'is_thurgau_dialect': list2bool(result.dialects, 'thurgau'),
        'is_appenzell_dialect': list2bool(result.dialects, 'appenzell'),
        'is_schaffhausen_dialect': list2bool(result.dialects, 'schaffhausen'),
        'is_grisons_dialect': list2bool(result.dialects, 'grisons'),
        'is_wallis_dialect': list2bool(result.dialects, 'wallis'),
        'is_glarus_dialect': list2bool(result.dialects, 'glarus'),
        'is_uri_dialect': list2bool(result.dialects, 'uri'),
        'is_schwyz_dialect': list2bool(result.dialects, 'schwyz'),
        'is_obwalden_dialect': list2bool(result.dialects, 'obwalden'),
    })

def list2bool(dialects, city):
    dialects = [dialect.lower() for dialect in dialects]
    dialects = [dialect.replace('ü', 'u') for dialect in dialects]
    dialects = [dialect.replace(' ', '') for dialect in dialects]
    dialects = [dialect.replace('.', '') for dialect in dialects]
    dialects = [dialect.replace('-', '') for dialect in dialects]
    if city in dialects:
        return True
    return False



if __name__ == '__main__':
    app.run(debug=True)
