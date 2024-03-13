from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

import os 
USER = os.environ.get('USER')
PASS = os.environ.get('PASS')

import subprocess
def write(filename, s):
    f = open(filename, "w")
    f.write(s)
    f.close()

def run(code, stdin):
    write("foo.py", code)
    write("in.txt", stdin)
    inputStream = open("in.txt", "r")
    result = subprocess.run(
        ['python', 'foo.py'],
        stdin = inputStream,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        universal_newlines = True 
    )
    return {"output": result.stdout, "log": result.stderr}

def check(body):
    keys = ['code', 'username', 'password', 'input']
    for key in keys:
        if key not in body:
            return False
    return True

class root(Resource):
    def get(self):
        return {'documentation': 'Post {"code":"", "input":""} and receive {"output":""}, the output of the given code with given input'}
    def post(self):
        args = request.get_json()
        if check(args):
            if ((USER == args['username']) and (PASS == args['password'])):
                return run(args['code'], args['input'])
            else:
                return {"log": "invalid auth", "output": ""}
        else:
            return {"log":"invalid payload", "output": ""}

api.add_resource(root, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
