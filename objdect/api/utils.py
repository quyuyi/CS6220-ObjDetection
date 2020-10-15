"""Views utility functions."""
import os
import shutil
import tempfile
import hashlib
import flask
import objdect


def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


def hash_upload_file():
    """Return the hashed name of the file."""
    # Save POST request's file object to a temp file
    dummy, temp_filename = tempfile.mkstemp()
    file = flask.request.files["file"]
    # if not allowed_file(file.filename): flask.abort(403)
    file.save(temp_filename)

    # Compute filename
    hash_txt = sha256sum(temp_filename)
    dummy, suffix = os.path.splitext(file.filename)
    hash_filename_basename = hash_txt + suffix
    hash_filename = os.path.join(
        objdect.app.config["UPLOAD_FOLDER"],
        hash_filename_basename
    )

    # Move temp file to permanent location
    shutil.move(temp_filename, hash_filename)

    return hash_filename_basename