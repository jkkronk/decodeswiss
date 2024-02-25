from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import instructor
from pydantic import BaseModel, Field

app = Flask(__name__)


class Translation(BaseModel):
    """
    A class that represents the translation of a swiss german text.
    """
    translation: str = Field(..., description="A translation from swiss german to english.")


def translate_text(text, openai_api_key=None):
    if openai_api_key == "":
        client = instructor.patch(OpenAI())
    else:
        client = instructor.patch(OpenAI(api_key=openai_api_key))

    prompt = f"translate swiss german to english: {text}"

    translated: Translation = client.chat.completions.create(
        model="gpt-3.5-turbo-instruct",
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
    translated_text = translate_text(text_to_translate)

    # Return the translated text as a JSON response
    return jsonify({
        'original_text': text_to_translate,
        'translated_text': translated_text
    })


if __name__ == '__main__':
    app.run(debug=True)
