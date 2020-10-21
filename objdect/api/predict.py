"""REST API for object prediction."""
import sqlite3
import flask
import objdect


@objdect.app.route('/api/predict/<int:frame>',
                    methods=["GET"])
def predict(frame):
    print("api/predict")
    """Object prediction."""
    filename = 'var/output/ssd500/1.0FPS_'+str(frame)+'.jpg'
    return flask.send_file(filename, mimetype='jpg')
    # context = {}
    # code = 200
    # return flask.jsonify(**context), code