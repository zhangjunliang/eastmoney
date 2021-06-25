import os
from flask import Blueprint, jsonify, request

file_path =os.path.abspath(os.path.dirname(__file__))
father_path = os.path.dirname(file_path)
action = Blueprint('item', __name__)

@action.route('/',methods=['GET','POST'])
def index():
    return 'test'

@action.route('/run',methods=['GET','POST'])
def run():
    o = request.args.get("o", "")
    f = request.args.get("f", "")
    p = request.args.get("p", "")
    t = request.args.get("t", "")
    shell = 'python run.py -o={} -f={} -p={} -t={}'.format(o,f,p,t)
    print(shell)
    return os.popen(shell, "r").read().replace("\n","<br>")