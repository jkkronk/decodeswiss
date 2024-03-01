from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import ast

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///translations.db'
db = SQLAlchemy(app)


# Create a database model
class TranslationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.String, unique=True, nullable=False)
    en_translation = db.Column(db.String, nullable=False)
    de_translation = db.Column(db.String, nullable=False)
    dialects = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


def get_existing_translation(text):
    translation = TranslationModel.query.filter_by(original_text=text).first()
    if translation:
        return translation
    return None


def save_translation(text, en_translation, de_translation, dialects):
    new_translation = TranslationModel(original_text=text, en_translation=en_translation, de_translation=de_translation,
                                       dialects=str(dialects))
    db.session.add(new_translation)
    db.session.commit()


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
              f"Indicate True if the input text is in swiss german. If you can't tell it probably should be False."
              f"Indicate what dialect the input text could be. The format is a list "
              f"of most likely dialect or dialects. For example 'hoi zäme' it should be ['zurich']. "
              f"Or for example for 'Zum Znüni hät's feine Schoggigipfeli gha, da chame würkli nid klage.' "
              f"Should the answer be ['bern'] but for 'Mir göhn später in d'Stadt zum e bitzeli shoppe.' the answer"
              f"could be ['basel', 'solothurn', 'zurich']. wallis is called wallis and graubunden is called grisons. "
              f"If you get it right you will get a bonus.")

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

    existing_translation = get_existing_translation(text_to_translate)
    if existing_translation:
        print("Translation already exists in the database.")
        return jsonify({
            'original_text': text_to_translate,
            'en_translation': existing_translation.en_translation,
            'de_translation': existing_translation.de_translation,
            'is_swiss_german': True,
            'is_bernese_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'bern'),
            'is_basel_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'basel'),
            'is_solothurn_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'solothurn'),
            'is_aargau_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'aargau'),
            'is_lucerne_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'lucerne'),
            'is_zug_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'zug'),
            'is_zurich_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'zurich'),
            'is_stgallen_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'stgallen'),
            'is_thurgau_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'thurgau'),
            'is_appenzell_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'appenzell'),
            'is_schaffhausen_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'schaffhausen'),
            'is_grisons_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'grisons'),
            'is_wallis_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'wallis'),
            'is_glarus_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'glarus'),
            'is_uri_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'uri'),
            'is_schwyz_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'schwyz'),
            'is_obwalden_dialect': list2bool(ast.literal_eval(existing_translation.dialects), 'obwalden'),
        })

    # Perform translation
    if check_and_update_count():
        result = translate_text(text_to_translate)
    else:
        return jsonify(
            {'error': 'The maximum number of translations has been reached for today. Please try again tomorrow.'})

    if result.is_swiss_german:
        save_translation(text_to_translate, result.en_translation, result.de_translation, result.dialects)
    else:
        return jsonify(
            {'error': "This doesn't seem to be swiss german."})

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


def check_and_update_count():
    '''
    OBS: THIS IS A NON-OPTIMAL SOLUTION. IT WOULD BE BETTER TO USE A DATABASE TO STORE THE COUNT.
    Check if the number of translations for today has been reached and update the count if necessary.
    :return: True if the number of translations for today has not been reached, else False.
    '''
    try:
        with open('translate_count.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {'count': 0, 'last_reset': str(datetime.now().date())}

    last_reset = datetime.strptime(data['last_reset'], '%Y-%m-%d').date()
    # Check if the last reset was more than 24 h ago and reset the count if necessary
    if (datetime.now().date() - last_reset).days >= 1:
        data = {'count': 0, 'last_reset': str(datetime.now().date())}

    if data['count'] >= 150:
        return False

    data['count'] += 1
    with open('translate_count.json', 'w') as f:
        json.dump(data, f)
    return True


if __name__ == '__main__':
    app.run(debug=True)
