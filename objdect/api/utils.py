"""Views utility functions."""
import os
import io
from PIL import Image
import shutil
import tempfile
import hashlib
import base64
import numpy as np
import cv2
import flask
import objdect


def readb64(s):
    z = s[s.find('/9'):]
    # im = Image.open(io.BytesIO(base64.b64decode(z))).save('result.jpg')
    im = Image.open(io.BytesIO(base64.b64decode(z)))
    return im


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