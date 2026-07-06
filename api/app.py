"""
OctoAcme Project Management API

Provides REST endpoints to access OctoAcme project management documentation.
"""

import os
from flask import Flask, jsonify, abort

app = Flask(__name__)

_DOCS_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "docs"))

# Each entry stores a pre-computed, trusted absolute filepath alongside metadata.
# File paths are built at module load time from hardcoded filenames so that no
# user-supplied input is ever used in a path construction call.
DOCS_METADATA = {
    "octoacme-project-management-overview.md": {
        "title": "OctoAcme Project Management Overview",
        "description": "Concise introduction to how OctoAcme runs projects.",
        "filepath": os.path.join(_DOCS_DIR, "octoacme-project-management-overview.md"),
    },
    "octoacme-project-initiation.md": {
        "title": "Project Initiation",
        "description": "Steps and artifacts for kicking off a new project.",
        "filepath": os.path.join(_DOCS_DIR, "octoacme-project-initiation.md"),
    },
    "octoacme-project-planning.md": {
        "title": "Project Planning",
        "description": "Planning scope, resources, milestones and dependencies.",
        "filepath": os.path.join(_DOCS_DIR, "octoacme-project-planning.md"),
    },
    "octoacme-execution-and-tracking.md": {
        "title": "Execution and Tracking",
        "description": "Guidelines for building, tracking and iterating during delivery.",
        "filepath": os.path.join(_DOCS_DIR, "octoacme-execution-and-tracking.md"),
    },
    "octoacme-risks-and-communication.md": {
        "title": "Risks and Communication",
        "description": "Risk management and communication strategies.",
        "filepath": os.path.join(_DOCS_DIR, "octoacme-risks-and-communication.md"),
    },
    "octoacme-release-and-deployment.md": {
        "title": "Release and Deployment",
        "description": "Process for deploying and announcing releases.",
        "filepath": os.path.join(_DOCS_DIR, "octoacme-release-and-deployment.md"),
    },
    "octoacme-retrospective-and-continuous-improvement.md": {
        "title": "Retrospective and Continuous Improvement",
        "description": "Capturing learnings and driving process improvement.",
        "filepath": os.path.join(
            _DOCS_DIR, "octoacme-retrospective-and-continuous-improvement.md"
        ),
    },
    "octoacme-roles-and-personas.md": {
        "title": "Roles and Personas",
        "description": "Defined roles, responsibilities and personas in OctoAcme projects.",
        "filepath": os.path.join(_DOCS_DIR, "octoacme-roles-and-personas.md"),
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
    for doc_name, meta in DOCS_METADATA.items():
        docs.append(
            {
                "filename": doc_name,
                "title": meta["title"],
                "description": meta["description"],
            }
        )
    return jsonify({"docs": docs, "count": len(docs)})


@app.route("/api/docs/<string:filename>", methods=["GET"])
def get_doc(filename):
    """Return the content of a specific process documentation file."""
    meta = DOCS_METADATA.get(filename)
    if meta is None:
        abort(404, description=f"Document '{filename}' not found.")

    # Use the pre-computed trusted filepath from our metadata dict,
    # never the user-supplied filename, to prevent path traversal.
    filepath = meta["filepath"]
    if not os.path.isfile(filepath):
        abort(404, description="Document file is not available.")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

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
    app.run(debug=False, port=5000)
