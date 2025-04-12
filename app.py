from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import nltk
from nltk.tokenize import word_tokenize

# Add your nltk_data path manually (optional but safer if you've set a custom path)
  # Make sure this path matches where you downloaded it

# Ensure 'punkt' is available, else raise a clean error
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    raise LookupError("NLTK 'punkt' tokenizer not found. Please run: nltk.download('punkt') manually.")

app = Flask(__name__)
CORS(app)

# Basic rule-based responses
responses = {
    "greeting": ["Hi there! How are you feeling today?", "Hello! I'm here to support you."],
    "sad": ["I'm really sorry to hear that. Do you want to talk about it?", "Sadness can be heavy. I'm listening."],
    "happy": ["That's great to hear! What made you feel this way?", "Joy is worth sharing. 😊"],
    "angry": ["It’s okay to feel anger. Do you want to tell me what happened?", "Let's unpack that anger together."],
    "anxious": ["Anxiety can be tough. Deep breaths. Want to talk about what's causing it?", "I'm here with you. Would it help to talk it through?"],
    "default": ["Can you tell me more about how you're feeling?", "I'm here to listen. Go on."]
}

# Keyword map to category
keywords = {
    "greeting": ["hi", "hello", "hey"],
    "sad": ["sad", "depressed", "unhappy", "cry", "down"],
    "happy": ["happy", "joyful", "excited", "glad"],
    "angry": ["angry", "mad", "furious", "annoyed"],
    "anxious": ["anxious", "nervous", "worried", "panic", "scared"]
}

def classify_input(user_input):
    tokens = word_tokenize(user_input.lower())
    for category, words in keywords.items():
        if any(word in tokens for word in words):
            return category
    return "default"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    category = classify_input(user_input)
    response = random.choice(responses[category])
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
