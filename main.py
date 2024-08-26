from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

@app.route('/search', methods=['GET'])
def search_youtube():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    # Construire l'URL pour l'API YouTube Data v3
    params = {
        'part': 'snippet',
        'q': query,
        'key': YOUTUBE_API_KEY,
        'type': 'video',
        'maxResults': 1  # Vous pouvez ajuster ce nombre
    }

    response = requests.get(YOUTUBE_API_URL, params=params)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from YouTube"}), response.status_code

    data = response.json()

    if not data.get('items'):
        return jsonify({"error": "No video found for the given query"}), 404

    video_id = data['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    return jsonify({"videoUrl": video_url})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
