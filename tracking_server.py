from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Dictionary to store which ads each user has clicked
user_ad_clicks = {}

@app.route('/')
def index():
    return "Welcome to the Ad Tracking Server!"

# Route to track ad clicks
@app.route('/track/<int:ad_id>', methods=['GET'])
def track_ad_click(ad_id):
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Log the ad view for this user
    now = datetime.now()
    if user_id not in user_ad_clicks:
        user_ad_clicks[user_id] = []

    user_ad_clicks[user_id].append({"ad_id": ad_id, "timestamp": now})

    print(f"User {user_id} clicked ad {ad_id} at {now}")
    
    return jsonify({"message": f"Ad {ad_id} clicked by user {user_id}"}), 200

# Route to check if a user clicked a specific ad
@app.route('/has_clicked_ad', methods=['GET'])
def has_clicked_ad():
    user_id = request.args.get('user_id')
    ad_id = int(request.args.get('ad_id'))

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    if user_id in user_ad_clicks:
        for ad in user_ad_clicks[user_id]:
            if ad["ad_id"] == ad_id:
                return jsonify({"clicked": True}), 200

    return jsonify({"clicked": False}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
