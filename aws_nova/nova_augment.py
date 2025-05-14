import json
import re
import sys
import boto3
import os
from datetime import datetime
import yaml

def load_config(filepath):
  with open(filepath, 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)
  return config


def read_md_file(filename: str) -> str:
  try:
    with open(filename, "r", encoding="utf-8") as file:
      return file.read()
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    sys.exit(1)


def read_description_from_front_matter(filename: str) -> str:
  with open(filename, 'r', encoding='utf-8') as file:
    content = file.read()
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
      front_matter = yaml.safe_load(match.group(1))
      return front_matter.get('title', '')
      # return front_matter.get('description', '')
  return ''


def summarize_text(text: str, model) -> str:
  from transformers import pipeline
  summarizer = pipeline("summarization", model=model)
  # Handle long content by summarizing in chunks (Bart's max is ~1024 tokens)
  max_chunk = 1000
  chunks = [text[i:i + max_chunk] for i in range(0, len(text), max_chunk)]
  summary = ''
  for chunk in chunks:
    out = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
    summary += out[0]['summary_text'] + '\n'
  return summary


def generate_image_with_nova(prompt: str, model_name: str, config, color: bool = None) -> None:
  bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')  # adjust region

  nova_request = json.dumps(
    {
      "taskType": "TEXT_IMAGE",
      "textToImageParams": {
        "text": prompt
      },
      "imageGenerationConfig": {
        "cfgScale": config["cfgScale"],
        "seed": config["seed"],
        "width": config["width"],
        "height": config["height"],
        "numberOfImages": config["numberOfImages"],
        "quality": "standard"
      }
    }
  )

  if color:
    nova_request = json.dumps(
      {
        "colorGuidedGenerationParams": {
          "text": prompt,
          "colors":
            config["colors"]
        },
        "taskType": "COLOR_GUIDED_GENERATION",
        "imageGenerationConfig": {
          "cfgScale": config["cfgScale"],
          "seed": config["seed"],
          "width": config["width"],
          "height": config["height"],
          "numberOfImages": config["numberOfImages"],
        }
      }
    )

  response = bedrock.invoke_model(
    modelId=model_name,
    body=nova_request,
    contentType='application/json',
    accept='application/json'
  )

  result = json.loads(response['body'].read())
  from base64 import b64decode

  # Check if images are available in the response
  # make directory 'generated/current_date'
  folder_name = datetime.now().strftime("%Y-%m-%d")
  os.makedirs(f"generated/{folder_name}", exist_ok=True)

  if 'images' in result and result['images']:
    for idx, image_data in enumerate(result['images']):
      if image_data:
        with open(f"generated/{folder_name}/output_image_{idx}.png", "wb") as f:
          f.write(b64decode(image_data))
        print(f"Image saved to output_image_{idx}.png")
      else:
        print(f"No image data returned for image {idx}.")
  else:
    print("No images found in the response.")


if __name__ == '__main__':
  print(sys.argv)
  if len(sys.argv) != 2:
    print("Usage: python nova_augment <filename.md>")
    sys.exit(1)

  filename = sys.argv[1]
  config = load_config('./scripts/nova.yaml')

  # read desc from md file
  description = read_description_from_front_matter(f"_posts/{filename}")

  print("\n--- Description extracted from front matter ---")
  print(description)

  summary = None
  print("\n What to use as a summary?")
  print("1. Direct input")
  print("2. Generate based on content")
  call = "\nYour choice (1/2"
  if description:
    print("3. Use current Description")
    call += "/3"
  choice = input(f"\n{call}): ").strip()

  if choice == '1':
    final_text = input("Enter your custom text:\n> ").strip()
  elif choice == '2':
    content = read_md_file(f"_posts/{filename}")
    final_text = summarize_text(content, config["summaryModel"])
    print(f"\n--- Generated Summary by {config['summaryModel']} model---")
    print(final_text)
  elif choice == '3':
    final_text = description
  else:
    print("Invalid choice, using description by default.")
    final_text = description

  print("\nColor Guided Generation:")
  print(f"1. Apply color guided generation {config['colors']}")
  print("2. Skip color guided generation")
  choice = input("\nDo you want Color Guided Generation (1/2): ").strip()

  color = False
  if choice == '1':
    color = True

  print(f"Generating {config['numberOfImages']} images ({config['width']}x{config['height']}) ...")
  # call nova
  generate_image_with_nova(prompt=final_text,
                           model_name='amazon.nova-canvas-v1:0',
                           config=config)
