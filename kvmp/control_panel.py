from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from kvmp.instance import instances
import libvirt
import sys
from flask_seasurf import SeaSurf

# https://testdriven.io/blog/flask-htmx-tailwind/

app = Flask(__name__)
app.secret_key = 'gfdsgsfdgfdgdsfgdfgfdgdfgsgfdgdfg55efdgfsdt5estdt'
assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

csrf = SeaSurf(app)


@csrf.exempt
@app.route("/")
def hello_world():
    conn = libvirt.open('qemu:///system')
    if conn == None:
      print('Failed to connect to the hypervizor')
      exit(1)

    return render_template('index.html', instances=instances)


@csrf.exempt
@app.route("/system")
def system():
    conn = libvirt.open('qemu:///system')
    return conn.getSysinfo()


@csrf.exempt
@app.route("/search", methods=["POST"])
def search_instance():
    search_term = request.form.get("search")

    if not len(search_term):
        return render_template("instance.html", instances=instances)

    res_instances = [instance for instance in instances if search_term in instance["name"]]

    return render_template("instance.html", instances=res_instances)


@csrf.exempt
@app.route("/render_instances")
def render_instances():
    return render_template("instance.html", instances=instances)


@app.route("/test")
def test():
    return render_template("form.html")
    

@app.route("/print", methods=["GET", "POST"])
def index():
    name = request.form["name"]
    uri = request.form["uri"]

    print("{}".format(name), file=sys.stderr)
    print("{}".format(uri), file=sys.stdout)
    return render_template("form.html")