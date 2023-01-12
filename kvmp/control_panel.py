from flask import Flask, render_template, request, g, redirect, session, url_for
import libvirt
import sys
from flask_seasurf import SeaSurf
from werkzeug.wrappers import Response
import psycopg2
import kvmp.db as db

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='./static'
)
app.secret_key = 'gfdsgsfdgfdgdsfgdfgfdgdfgsgfdgdfg55efdgfsdt5estdt'
csrf = SeaSurf(app)

@csrf.exempt
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        users = db.get_user(session['user_id'])
        if len(users) > 0:
            g.user = users[0]
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        users = db.user_login(username, password)

        if len(users) > 0:
            session['user_id'] = users[0]['id']
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@csrf.exempt
@app.route('/profile')
def profile():
    if not g.user: return redirect(url_for('login'))

    return render_template('profile.html')

@csrf.exempt
@app.route("/")
def index():
    return render_template('index.html')


@csrf.exempt
@app.route("/system")
def system():
    conn = libvirt.open('qemu:///system')
    return conn.getSysinfo()


@csrf.exempt
@app.route("/search", methods=["POST"])
def search_instance():
    if not g.user: return redirect(url_for('login'))

    search_term = request.form.get("search")

    if not len(search_term):
        return render_template("instance.html", instances=[])

    res_instances = [instance for instance in instances if search_term in instance["name"]]

    return render_template("instance.html", instances=res_instances)

@csrf.exempt
@app.route("/render_instances")
def render_instances():
    if not g.user: return redirect(url_for('login'))
    return render_template("instance.html", instances=[])
    
# @app.route("/print", methods=["GET", "POST"])
# def print():
#     if not g.user: return redirect(url_for('login'))
#     name = request.form["name"]
#     uri = request.form["uri"]

#     print("{}".format(name), file=sys.stderr)
#     print("{}".format(uri), file=sys.stdout)
#     return render_template("form.html")

@app.route('/icons', methods=["GET"])
def icons():
    return render_template("icons.html")

@app.route('/security', methods=["GET"])
def security():
    return render_template("security.html")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404