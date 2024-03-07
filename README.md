# Swiss German Translator

## Introduction

The Swiss German Translator is a web application designed to translate texts from Swiss German into High German and 
English. It supports multiple dialects, providing insights into the rich linguistic diversity of Switzerland. 
Utilizing chat gpt-3, this tool aims to bridge communication gaps and promote understanding.

## Features

- Translation: Converts Swiss German text into High German and English.
- (Beta) Dialect Recognition: Identifies specific Swiss German dialects, including Bernese, Basel, Lucerne, Zurich, and more.
- Responsive Design: Ensures a seamless user experience across various devices and screen sizes.

## Getting Started

### Prerequisites
Python 3.8 or higher
Flask
SQLAlchemy
An OpenAI API key for translation services

### Installation
Clone the repository to your local machine and install the required packages using pip:
```bash
git clone https://github.com/yourgithub/swiss-german-translator.git
cd swiss-german-translator
pip install -r requirements.txt
```
### Set environment variables
```bash
export OPEN_AI_API_KEY="your-api-key"
export FLASK_APP=server
export DECODE_SWISS_MODEL="your-finetuned-model or pure gpt-3"
```
### Running the Application
To start the application, run the following command in your terminal:
```bash
gunincorn server:app
```
Access the application by navigating to http://localhost:8000 in your web browser.

Or head to live deployment at:
https://swissdic.onrender.com/

## Finetuning the Model
To finetune the model, you first need to collect a good dataset. It needs to be in the correct openai format. See 
https://beta.openai.com/docs/guides/datasets for more information. `refactor_data.py` is a script that can help you
refactor your data into the correct format. Run it with the following command:
```bash
python refactor_data.py "Translate this text to Swiss German." "Translate this text to English." "Translate this text to German." kanton True
```
When you have your dataset, you can run the following command to finetune the model:
```bash
python refactor_data.py "Translate this text to Swiss German." "Translate this text to English." "Translate this text to German." Zurich True
```
You can then set the environment variable `DECODE_SWISS_MODEL` to the path of the finetuned model.
```bash
export DECODE_SWISS_MODEL="your-finetuned-model"
```

