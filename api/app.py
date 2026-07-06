"""
OctoAcme Project Management API

Provides REST endpoints to access OctoAcme project management documentation.
"""

import os
from flask import Flask, jsonify, abort

app = Flask(__name__)

DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")

DOCS_METADATA = {
    "octoacme-project-management-overview.md": {
        "title": "OctoAcme Project Management Overview",
        "description": "Concise introduction to how OctoAcme runs projects.",
    },
    "octoacme-project-initiation.md": {
        "title": "Project Initiation",
        "description": "Steps and artifacts for kicking off a new project.",
    },
    "octoacme-project-planning.md": {
        "title": "Project Planning",
        "description": "Planning scope, resources, milestones and dependencies.",
    },
    "octoacme-execution-and-tracking.md": {
        "title": "Execution and Tracking",
        "description": "Guidelines for building, tracking and iterating during delivery.",
    },
    "octoacme-risks-and-communication.md": {
        "title": "Risks and Communication",
        "description": "Risk management and communication strategies.",
    },
    "octoacme-release-and-deployment.md": {
        "title": "Release and Deployment",
        "description": "Process for deploying and announcing releases.",
    },
    "octoacme-retrospective-and-continuous-improvement.md": {
        "title": "Retrospective and Continuous Improvement",
        "description": "Capturing learnings and driving process improvement.",
    },
    "octoacme-roles-and-personas.md": {
        "title": "Roles and Personas",
        "description": "Defined roles, responsibilities and personas in OctoAcme projects.",
    },
}


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "OctoAcme Project Management API"})


@app.route("/api/docs", methods=["GET"])
def list_docs():
    """Return a list of all available process documentation files."""
    docs = []
    for filename, meta in DOCS_METADATA.items():
        docs.append(
            {
                "filename": filename,
                "title": meta["title"],
                "description": meta["description"],
            }
        )
    return jsonify({"docs": docs, "count": len(docs)})


@app.route("/api/docs/<string:filename>", methods=["GET"])
def get_doc(filename):
    """Return the content of a specific process documentation file."""
    if filename not in DOCS_METADATA:
        abort(404, description=f"Document '{filename}' not found.")

    filepath = os.path.join(DOCS_DIR, filename)
    if not os.path.isfile(filepath):
        abort(404, description=f"Document file '{filename}' is not available.")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta = DOCS_METADATA[filename]
    return jsonify(
        {
            "filename": filename,
            "title": meta["title"],
            "description": meta["description"],
            "content": content,
        }
    )


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "message": str(error)}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed", "message": str(error)}), 405


if __name__ == "__main__":
    app.run(debug=True, port=5000)
