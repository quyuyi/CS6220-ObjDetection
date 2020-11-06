"""REST API for upload file."""
import os
import shutil
import tempfile
import hashlib
import flask
import objdect



@objdect.app.route('/api/upload/',
                    methods=["GET", "POST"])
def upload():
    """Upload video for analysis."""
    context = {
        "message": "success"
    }
    code = 200
    # TODO
    # store the uploaded file in /var
    print("try to save to local!")
    print(flask.request.files['video'])
    print(hash_upload_file())
    return flask.jsonify(**context), code


@objdect.app.route('/api/get_video',
                    methods=["GET"])
def get_movie():
    """Return video for analysis."""
    filename = 'var/uploads/man-walking-with-a-laggage.mov'
    return flask.send_file(filename, mimetype='mov')


def hash_upload_file():
    """Save the file to var/uploads and return the name of the file."""
    # Save POST request's file object to a temp file
    dummy, temp_filename = tempfile.mkstemp()
    file = flask.request.files['video']
    file.save(temp_filename)

    # Compute filename
    filename = os.path.join(
        objdect.app.config["UPLOAD_FOLDER"],
        file.filename
    )

    # Move temp file to permanent location
    shutil.move(temp_filename, filename)

    return filename