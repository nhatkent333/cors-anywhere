import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/fetch-metadata', methods=['GET'])
def fetch_metadata():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}  # Adding a User-Agent header to avoid being blocked
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'No title available'
        
        return jsonify({'title': title})
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/proxy', methods=['GET'])
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.content, response.status_code, {'Content-Type': response.headers['Content-Type']}
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
