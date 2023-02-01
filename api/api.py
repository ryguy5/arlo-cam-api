import flask
import threading
import sqlite3
import functools
import os
from arlo.camera import Camera
from flask import send_file
import io

app = flask.Flask(__name__)
app.config["DEBUG"] = False
app.use_reloader = False


def validate_camera_request(body_required=True):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            camera = Camera.from_db_serial(kwargs['serial'])
            if camera is None:
                flask.abort(404)
            kwargs['camera'] = camera

            if body_required:
                req_body = flask.request.get_json()
                if req_body is None:
                    flask.abort(400)
                kwargs['req_body'] = req_body

            return f(*args, **kwargs)
        return wrapper
    return decorator


@app.route('/', methods=['GET'])
def home():
    return "PING"


@app.route('/camera', methods=['GET'])
def list():
    with sqlite3.connect('arlo.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM camera")
        rows = c.fetchall()
        cameras = []
        if rows is not None:
            for row in rows:
                (ip, serial_number, hostname,
                 registration, status, friendly_name) = row
                cameras.append({"ip": ip, "hostname": hostname,
                               "serial_number": serial_number, "friendly_name": friendly_name})

        return flask.jsonify(cameras)


@app.route('/camera/<serial>', methods=['GET'])
@validate_camera_request(body_required=False)
def status(serial, camera):
    if camera.status is None:
        return flask.jsonify({})
    else:
        return flask.jsonify(camera.status.dictionary)


@app.route('/camera/<serial>/registration', methods=['GET'])
@validate_camera_request(body_required=False)
def registration(serial, camera):
    if camera.registration is None:
        return flask.jsonify({})
    else:
        return flask.jsonify(camera.registration.dictionary)


@app.route('/camera/<serial>/statusrequest', methods=['POST'])
@validate_camera_request(body_required=False)
def status_request(serial, camera):
    result = camera.status_request()
    return flask.jsonify({"result": result})


@app.route('/camera/<serial>/userstreamactive', methods=['POST'])
@validate_camera_request()
def user_stream_active(serial, req_body, camera):
    active = req_body["active"]
    if active is None:
        flask.abort(400)

    result = camera.set_user_stream_active(int(active))
    return flask.jsonify({"result": result})


@app.route('/camera/<serial>/arm', methods=['POST'])
@validate_camera_request()
def arm(serial, req_body, camera):
    result = camera.arm(req_body)
    return flask.jsonify({"result": result})


@app.route('/camera/<serial>/pirled', methods=['POST'])
@validate_camera_request()
def pir_led(serial, req_body, camera):
    result = camera.pir_led(req_body)
    return flask.jsonify({"result": result})


@app.route('/camera/<serial>/quality', methods=['POST'])
@validate_camera_request()
def set_quality(serial, req_body, camera):
    if req_body['quality'] is None:
        flask.abort(400)
    else:
        result = camera.set_quality(req_body)
        return flask.jsonify({"result": result})


@app.route('/camera/<serial>/snapshot', methods=['POST'])
@validate_camera_request()
def request_snapshot(serial, req_body, camera):
    if req_body['url'] is None:
        flask.abort(400)
    else:
        result = camera.snapshot_request(req_body['url'])
        return flask.jsonify({"result": result})


@app.route('/camera/<serial>/audiomic', methods=['POST'])
@validate_camera_request()
def request_mic(serial, req_body, camera):
    if req_body['enabled'] is None:
        flask.abort(400)
    else:
        result = camera.mic_request(req_body['enabled'])
        return flask.jsonify({"result": result})


@app.route('/camera/<serial>/audiospeaker', methods=['POST'])
@validate_camera_request()
def request_speaker(serial, req_body, camera):
    if req_body['enabled'] is None:
        flask.abort(400)
    else:
        result = camera.speaker_request(req_body['enabled'])
        return flask.jsonify({"result": result})


@app.route('/camera/<serial>/record', methods=['POST'])
@validate_camera_request()
def request_record(serial, req_body, camera):
    if req_body['duration'] is None:
        flask.abort(400)
    else:
        result = camera.record(req_body['duration'], req_body['is4k'])
        return flask.jsonify({"result": result})


@app.route('/camera/<serial>/friendlyname', methods=['POST'])
@validate_camera_request()
def set_friendlyname(serial, req_body, camera):
    if req_body['name'] is None:
        flask.abort(400)
    else:
        camera.friendly_name = req_body['name']
        camera.persist()

        return flask.jsonify({"result": True})


@app.route('/camera/<serial>/activityzones', methods=['POST', 'DELETE'])
@validate_camera_request()
def set_activity_zones(serial, req_body, camera):
    if flask.request.method == 'DELETE':
        result = camera.unset_activity_zones()
    else:
        result = camera.set_activity_zones(req_body)

    return flask.jsonify({"result": result})


@app.route('/snapshot/<identifier>/', methods=['POST'])
def receive_snapshot(identifier):
    if 'file' not in flask.request.files:
        flask.abort(400)
    else:
        file = flask.request.files['file']
        if file.filename == '':
            flask.abort(400)
        else:
            start_path = os.path.abspath('/tmp')
            target_path = os.path.join(start_path, f"{identifier}.jpg")
            common_prefix = os.path.commonprefix([target_path, start_path])
            if (common_prefix != start_path):
                flask.abort(400)
            else:
                file.save(target_path)
            return ""


@app.route('/snapshot/<identifier>', methods=['GET'])
def get_snapshot(identifier):
    start_path = os.path.abspath('/tmp')
    target_path = os.path.join(start_path, f"{identifier}.jpg")
    common_prefix = os.path.commonprefix([target_path, start_path])
    if (common_prefix != start_path or not os.path.isfile(target_path)):
        flask.abort(400)
    else:
        # read the file into memory
        return_data = io.BytesIO()
        with open(target_path, 'rb') as fo:
            return_data.write(fo.read())
        # after writing, cursor will be at last byte, so move it to start
        return_data.seek(0)
        # delete the file
        os.remove(target_path)
        # send it to client
        return send_file(return_data, mimetype='image/jpeg', attachment_filename=f'{identifier}.jpg')


def get_thread():
    return threading.Thread(target=app.run(host='0.0.0.0'))
