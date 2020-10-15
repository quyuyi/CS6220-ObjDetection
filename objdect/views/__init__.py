"""
objDect index (main) view.

URLs include:
/
"""
import flask
import objdect

@objdect.app.route('/', methods=["GET", "POST"])
def show_index():
    context = {}
    # flask.render_template() will find "index.html"
    # in a directory called "templates" inside the python module
    return flask.render_template("index.html", **context)