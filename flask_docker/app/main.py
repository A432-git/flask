from flask import Flask
import socket
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World from Flask on {}".format(socket.gethostname())


@app.route("/hostname")
def show_container_name():
    return "This is an example wsgi app served from {}".format(socket.gethostname())


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
