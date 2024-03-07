from openai import OpenAI
import sys
# Run with the following command:
# python train.py train.jsonl valid.jsonl
train_json = sys.argv[1] # Path to the training JSON file
valid_json = sys.argv[2] # Path to the validation JSON file

client = OpenAI()

train_file = client.files.create(
  file=open(train_json, "rb"),
  purpose="fine-tune"
)

valid_file = client.files.create(
  file=open(valid_json, "rb"),
  purpose="fine-tune"
)


client.fine_tuning.jobs.create(
  training_file=train_file.id,
  validation_file=valid_file.id,
  model="gpt-3.5-turbo"
)
