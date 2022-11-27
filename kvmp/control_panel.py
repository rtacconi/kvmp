from flask import Flask
from flask import render_template
import libvirt

app = Flask(__name__)

def show_all_attrs(value):
    res = []
    for k in dir(value):
        res.append('%r %r\n' % (k, getattr(value, k)))
    return '\n'.join(res)

@app.route("/")
def hello_world():
    conn = libvirt.open('qemu:///system')
    if conn == None:
      print('Failed to connecto to the hypervizor')
      exit(1)

    return render_template('index.html', instances=conn.listDefinedDomains())
