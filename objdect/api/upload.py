"""REST API for upload file."""
import sqlite3
import flask
import objdect


@insta485.app.route('/api/upload/',
                    methods=["GET", "POST"])
def upload():
    """Upload video for analysis."""
    context = {}
    code = 200
    
    return flask.jsonify(**context), code