from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

import os 
USER = os.environ.get('USER')
PASS = os.environ.get('PASS')

def run(code, stdin):
    f = open("foo.py", "w")
    f.write(code)
    f.close()

    f = open("in.txt", "w")
    f.write(stdin)
    f.close()

    os.system("python foo.py < in.txt > out.txt")

    f = open("out.txt", "r")
    stdout = f.read()
    f.close()
    return stdout

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
                return {"log": "invalid auth"}
        else:
            return {"log":"invalid payload"}

api.add_resource(root, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
