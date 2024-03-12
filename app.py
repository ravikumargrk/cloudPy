from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('code', type=str)
parser.add_argument('input', type=str)

import os 
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

class root(Resource):
    def get(self):
        return {'documentation': 'Post {"code":"", "input":""} and receive {"output":""}, the output of the given code with given input'}
    def post(self):
        args = parser.parse_args()
        code = args['code']
        stdin = args['input']
        return {"output": run(code, stdin)}

api.add_resource(root, '/')

if __name__ == '__main__':
    app.run(debug=True)
