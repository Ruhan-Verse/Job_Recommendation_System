from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
UPWORK_API_HOST = os.getenv("UPWORK_API_HOST")

@app.route("/upwork-jobs", methods=["GET"])
def get_upwork_jobs():
    limit = request.args.get("limit", 10)  # default 10 jobs

    url = f"https://{UPWORK_API_HOST}/active-freelance-1h"
    querystring = {"limit": str(limit)}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": UPWORK_API_HOST
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        return jsonify({"success": True, "jobs": data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
