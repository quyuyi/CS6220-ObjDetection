"""objdect development configuration."""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = (
    b'\x0c\xfd\xd6\xf3^\xd0\xd1\xea\xc1\x86\xd4 '
    b'\xe9\x91)\xb7\x8d\x8c\xc7\xf2\x05Nyv'
)
SESSION_COOKIE_NAME = 'login'

# The __file__ variable contains the path to
# the file that Python is currently importing.
# You can use this variable inside a module
# to find the path of the module.

# File Upload to var/uploads/
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'uploads'
)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4'])
