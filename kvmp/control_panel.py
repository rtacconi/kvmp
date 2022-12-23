from flask import Flask, render_template, request, g, redirect, session, url_for
from flask_assets import Bundle, Environment
from kvmp.instance import instances
import libvirt
import sys
from flask_seasurf import SeaSurf

# https://testdriven.io/blog/flask-htmx-tailwind/


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Test', password='password'))
users.append(User(id=2, username='Riccy_DJ', password='test '))


app = Flask(__name__)
app.secret_key = 'gfdsgsfdgfdgdsfgdfgfdgdfgsgfdgdfg55efdgfsdt5estdt'
assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

csrf = SeaSurf(app)


def protect():
    if not g.user: return redirect(url_for('login'))


@csrf.exempt
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')


@csrf.exempt
@app.route('/profile')
def profile():
    protect()

    conn = libvirt.open('qemu:///system')
    if conn == None:
      print('Failed to connect to the hypervizor')
      exit(1)

    return render_template('index.html', instances=instances)


@csrf.exempt
@app.route("/")
def hello_world():
    return redirect(url_for('login'))


@csrf.exempt
@app.route("/system")
def system():
    conn = libvirt.open('qemu:///system')
    return conn.getSysinfo()


@csrf.exempt
@app.route("/search", methods=["POST"])
def search_instance():
    protect()

    search_term = request.form.get("search")

    if not len(search_term):
        return render_template("instance.html", instances=instances)

    res_instances = [instance for instance in instances if search_term in instance["name"]]

    return render_template("instance.html", instances=res_instances)


@csrf.exempt
@app.route("/render_instances")
def render_instances():
    protect()
    return render_template("instance.html", instances=instances)


@app.route("/test")
def test():
    protect()
    return render_template("form.html")
    

@app.route("/print", methods=["GET", "POST"])
def index():
    protect()
    name = request.form["name"]
    uri = request.form["uri"]

    print("{}".format(name), file=sys.stderr)
    print("{}".format(uri), file=sys.stdout)
    return render_template("form.html")
