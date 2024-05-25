from flask import Flask, request, jsonify
from chat import get_response

app = Flask(__name__)

@app.route('/messages', methods=['POST'])
def receive_message():
    text = request.get_json().get("message")
    response = get_response(text)
    
    response = get_response(text)
    
    # Возвращаем ответ в формате JSON
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True, host='192.168.0.103', port=5000)
