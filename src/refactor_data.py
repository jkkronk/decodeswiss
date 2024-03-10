import sys
import json

# Run with the following command:
# python refactor_data.py "Translate this text to Swiss German." "Translate this text to English." "Translate this text to German." kanton True
CH_TEXT = sys.argv[1] # Swiss German text
EN_TEXT = sys.argv[2] # English text
DE_TEXT = sys.argv[3] # German text
DIALECT = sys.argv[4] # Canton
IS_GERMAN = sys.argv[5] == 'True'  # True if the input text is in Swiss German, False otherwise

# Format the JSON output
output = {
    "messages": [
        {
            "role": "system",
            "content": "Translate the input text in Swiss German, provide the following fields in a JSON dict, where applicable: \"english_translation\" (english), \"german_translation\", \"dialect\", and \"is_swiss_german\"."
        },
        {
            "role": "user",
            "content": CH_TEXT
        },
        {
            "role": "assistant",
            "content": json.dumps({
                "english_translation": EN_TEXT,
                "german_translation": DE_TEXT,
                "dialect": DIALECT,
                "is_swiss_german": IS_GERMAN
            }, ensure_ascii=False)
        }
    ]
}

# Print the JSON output as a single line
print(json.dumps(output, ensure_ascii=False))

