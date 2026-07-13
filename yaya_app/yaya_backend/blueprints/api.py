from flask import Blueprint, jsonify
from models import Event, Job, Manual, Testimony

api_bp = Blueprint("api", __name__)

@api_bp.route("/api/events")
def api_events():

    events = Event.query.all()

    data = []

    for event in events:

        data.append({

            "id": event.id,
            "title": event.title,
            "date": str(event.date)

        })

    return jsonify(data)

@api_bp.route("/api/testimonies")
def api_testimonies():

    testimonies = Testimony.query.filter_by(
        is_approved=True
    ).all()

    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "title": t.title,
            "content": t.content
        }
        for t in testimonies
    ])

@api_bp.route("/api/manuals")
def api_manuals():

    manuals = Manual.query.all()

    return jsonify([
        {
            "id": m.id,
            "title": m.title,
            "file": m.file_url
        }
        for m in manuals
    ])

@api_bp.route("/api/jobs")
def api_jobs():

    jobs = Job.query.all()

    return jsonify([
        {
            "id": j.id,
            "title": j.title,
            "company": j.company
        }
        for j in jobs
    ])

