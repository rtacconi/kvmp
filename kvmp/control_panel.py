from flask import Flask, render_template, request
from flask_assets import Bundle, Environment
from kvmp.todo import todos
import libvirt

# https://testdriven.io/blog/flask-htmx-tailwind/

app = Flask(__name__)
assets = Environment(app)
css = Bundle("src/main.css", output="dist/main.css")

assets.register("css", css)
css.build()

@app.route("/")
def hello_world():
    conn = libvirt.open('qemu:///system')
    if conn == None:
      print('Failed to connecto to the hypervizor')
      exit(1)

    return render_template('index.html', instances=conn.listDefinedDomains())

@app.route("/system")
def system():
    conn = libvirt.open('qemu:///system')
    return conn.getSysinfo()

@app.route("/search", methods=["POST"])
def search_todo():
    search_term = request.form.get("search")

    if not len(search_term):
        return render_template("todo.html", todos=[])

    res_todos = [todo for todo in todos if search_term in todo["title"]]

    return render_template("todo.html", todos=res_todos)
