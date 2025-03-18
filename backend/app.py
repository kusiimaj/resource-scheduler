from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/schedule', methods=['GET'])
def get_schedule():
    return jsonify({"message": "Scheduler API is running!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
