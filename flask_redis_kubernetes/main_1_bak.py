from flask import Flask
from redis import Redis
import socket,os

app = Flask(__name__)
redis = Redis(host=os.environ.get("REDIS_MASTER_SR_SERVICE_HOST"),
              port=int(os.environ.get("REDIS_MASTER_SR_SERVICE_PORT")))


@app.route('/')
def hello():
    redis.incr('hits')
    return f'This Compose/Flask demo has been viewed {redis.get("hits")} time(s) on {socket.gethostname()}.'


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)