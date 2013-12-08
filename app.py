import os
import redis

from flask import Flask
from flask import render_template

app = Flask(__name__)
app.redis = redis.StrictRedis(
    host=os.getenv('WERCKER_REDIS_HOST', 'localhost'),
    port=6379,
    db=0
)


@app.route("/")
def clouds():
    data = app.redis.lrange("clouds", 0, -1)
    return render_template('index.html', data=data)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.config.static = os.environ.get("STATIC_URL", "/static")
    app.run(host='0.0.0.0', port=port)
