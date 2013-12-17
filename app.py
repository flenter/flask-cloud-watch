import os
import redis

from flask import Flask
from flask import redirect, render_template

app = Flask(__name__)
app.redis = redis.StrictRedis(
    host=os.getenv('WERCKER_REDIS_HOST', 'localhost'),
    port=6379,
    db=0
)
app.debug = True
app.secret_key = "$=q=p__8@-)pwvZl2nw!&c{wVn|0*6!:8@n(92_@r(9lkbbeb2"
app.config.static = os.environ.get("STATIC_URL", "/static")

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import Required


class CloudForm(Form):
    classification = TextField('classification', validators=[Required()])


@app.route("/add", methods=['GET', 'POST'])
def add_cloud():

    form = CloudForm(csrf_enabled=False)

    if form.validate_on_submit():
        app.redis.rpush('clouds', form.classification.data)
        return redirect('/')
    return render_template('submit.html', form=form)


@app.route("/")
def clouds():
    data = app.redis.lrange("clouds", 0, -1)
    return render_template('index.html', data=data)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
