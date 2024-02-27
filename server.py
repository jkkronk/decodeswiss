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
    regional_dialect: str = Field(..., description="The regional dialect of the swiss german text.")
    is_swiss_german: bool = Field(..., description="Whether the input text is swiss german.")

def translate_text(text, openai_api_key=None):
    if openai_api_key == "":
        client = instructor.patch(OpenAI())
    else:
        client = instructor.patch(OpenAI(api_key=openai_api_key))

    prompt = f"Translate this swiss german to english: {text}. If possible also indicate the regional dialect."

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

    # Return the translated text as a JSON response
    return jsonify({
        'original_text': text_to_translate,
        'en_translation': result.en_translation,
        'de_translation': result.de_translation,
        'regional_dialect': result.regional_dialect,
        'is_swiss_german': result.is_swiss_german
    })


if __name__ == '__main__':
    app.run(debug=True)
