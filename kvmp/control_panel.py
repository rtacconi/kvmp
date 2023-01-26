from flask import Flask, render_template, request, g, redirect, session, url_for, jsonify
import sys
import os
from flask_seasurf import SeaSurf
from werkzeug.wrappers import Response
import psycopg2
import kvmp.db as db

db.con = psycopg2.connect(os.environ['DATABASE_URL'])
db.cur = db.con.cursor()

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
        # users = db.get_user(session['user_id'])
        # app.logger.debug('Users: %s', users)
        app.logger.debug('Session ID: %s', session['user_id'])
        g.user = session['user_id']
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        users = db.user_login(username, password)

        if users == [(1,)]:
            session['user_id'] = users[0][0]
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
    if not g.user: return redirect(url_for('login'))
    servers = db.get_servers()
    app.logger.debug(servers)
    return render_template('index.html', servers=servers)


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

@app.route("/add_server")
def add_server_form_page():
    
    return render_template("add_server.html")

@app.route("/servers/<int:id>", methods=["GET", "POST"])
def edit_server(id):
    if request.method == "GET":
        app.logger.debug('servers GET edit')
        server = db.get_server(id)
        vms = db.get_vms_by_server(id)
        return render_template("edit_server.html", server=server, vms=vms)
    elif request.method == "POST":
        if request.form.get("_method") == "put":
            app.logger.debug('servers PUT edit')
            host = request.form["host"]
            username = request.form["username"]
            key_file = request.form["key_file"]
            result = db.update_server(id, host, username, key_file)
            app.logger.debug(id, host, username, key_file)
            redirect(url_for('index'))
        else:
            app.logger.debug('servers POST edit')
            host = request.form["host"]
            username = request.form["username"]
            key_file = request.form["key_file"]
            db.add_server(host, username, key_file)
            return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route("/servers/<int:id>/vms/new", methods=["GET"])
def add_server_vms(id):
    server = db.get_server(id)
    return render_template("add_vm.html", server=server)
        
