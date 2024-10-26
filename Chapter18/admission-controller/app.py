from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/admission-controller', methods=['POST'])
def admission_controller():
    # Log the incoming request for debugging
    app.logger.info(f"Received request: {request.json}")
    # Your admission logic goes here
    return "OK"

    # Get the admission review request
    admission_review = request.get_json()

    # Implement your logic here (for example, check for a specific label)
    if "metadata" in admission_review["request"]["object"]:
        labels = admission_review["request"]["object"]["metadata"].get("labels", {})
        if labels.get("app") == "forbidden-app":
            # Deny the request
            admission_response = {
                "response": {
                    "uid": admission_review["request"]["uid"],
                    "allowed": False,
                    "status": {
                        "message": "The 'forbidden-app' label is not allowed."
                    }
                }
            }
            return jsonify(admission_response), 200

    # Allow the request
    admission_response = {
        "response": {
            "uid": admission_review["request"]["uid"],
            "allowed": True
        }
    }
    return jsonify(admission_response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, ssl_context=('admission-controller.crt', 'admission-controller.key'))  # Ensure you have SSL certificates
