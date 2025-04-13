from flask import Flask, request, jsonify
from function import handler

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_request():
    req = request.data.decode("utf-8")  
    res = handler.handle(req)  
    return res 

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)