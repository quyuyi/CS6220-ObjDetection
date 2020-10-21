"""REST API for upload file."""
import sqlite3
import flask
import objdect


@objdect.app.route('/api/upload/',
                    methods=["GET", "POST"])
def upload():
    """Upload video for analysis."""
    context = {}
    code = 200
    
    return flask.jsonify(**context), code

@objdect.app.route('/api/get_video',
                    methods=["GET"])
def get_movie():
    """Return video for analysis."""
    filename = 'var/uploads/man-walking-with-a-laggage.mov'
    return flask.send_file(filename, mimetype='mov')