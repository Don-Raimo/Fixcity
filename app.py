from flask import Flask, request, jsonify
import uuid
import datetime

# Initialize app with standard __name__ or string "FixItCity"
app = Flask(__name__)

# Mock database to store incoming faults
fault_database = []

@app.route('/api/v1/report-fault', methods=['POST'])
def report_fault():
    """
    Endpoint to receive a municipal fault report.
    Expects JSON payload with: category, description, lat, lng
    """
    data = request.get_json()

    # Basic Validation
    if not data or not all(k in data for k in ("category", "description", "lat", "lng")):
        return jsonify({"error": "Missing required fields"}), 400

    # Generate a unique tracking ticket for the citizen 
    tracking_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"

    # Create the fault record
    new_fault = {
        "tracking_id": tracking_id,
        "category": data["category"],
        "description": data["description"],
        "location": {"lat": data["lat"], "lng": data["lng"]},
        "status": "Logged",
        "timestamp": datetime.datetime.now().isoformat()
    }

    fault_database.append(new_fault)

    # Return success response with the tracking ID
    return jsonify({
        "message": "Fault reported successfully",
        "tracking_id": tracking_id
    }), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)