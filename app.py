from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import requests
import base64
from dotenv import load_dotenv
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder

app = Flask(__name__)
CORS(app)

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
STABILITY_API_KEY = os.getenv('STABILITY_API_KEY')

# OpenAI GPT Story Generation
def generate_story(prompt):
    openai.api_key = OPENAI_API_KEY
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a creative storyteller. Write a 5-sentence short story."},
            {"role": "user", "content": f"Write a short 5-sentence story about: {prompt}"}
        ],
    )
    return response.choices[0].message.content

# Stable Diffusion Image Generation (Stability.ai)
def generate_image(prompt):
    url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "application/json",
    }

    multipart_data = MultipartEncoder(
        fields={
            "prompt": prompt,
            "output_format": "jpeg",  # Required (can be "png" too)
            "cfg_scale": "7",
            "steps": "50",
            "width": "412",
            "height": "412"
        }
    )

    headers["Content-Type"] = multipart_data.content_type
    response = requests.post(url, headers=headers, data=multipart_data)

    if response.status_code == 200:
        try:
            image_data = response.json().get("image")
            if image_data:
                return image_data  # Return Base64 image string directly
            else:
                return None
        except Exception as e:
            print(f"❌ Error processing image: {e}")
            return None
    else:
        print(f"❌ API request failed: {response.text}")
        return None

# API Route: Generate Story
@app.route("/generate_story", methods=["POST"])
def generate_story_api():
    data = request.json
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    story = generate_story(prompt)
    return jsonify({"story": story})

# API Route: Generate Image
@app.route("/generate_image", methods=["POST"])
def generate_image_api():
    data = request.json
    story = data.get("story")
    
    if not story:
        return jsonify({"error": "Story is required"}), 400

    image_data = generate_image(story)
    
    if image_data:
        return jsonify({"image": image_data})  # Base64 encoded string
    else:
        return jsonify({"error": "Failed to generate image"}), 500

if __name__ == "__main__":
    app.run(debug=True)
