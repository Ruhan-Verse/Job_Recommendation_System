from flask import Blueprint, jsonify
from services.job_fetcher import fetch_jobs

jobs_bp = Blueprint("jobs_bp", __name__, url_prefix="/api/jobs")

@jobs_bp.route("/fetch", methods=["GET"])
def get_jobs():
    jobs = fetch_jobs()
    return jsonify(jobs)
