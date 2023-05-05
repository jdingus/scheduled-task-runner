from flask import Flask, jsonify
import backup_now

app = Flask(__name__)

@app.route('/run_default_task', methods=['GET'])
def run_default_task():
    backup_now.main()
    return jsonify({"message": "Default task executed."})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
