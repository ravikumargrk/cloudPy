from flask import Flask
from flask_restful import Resource, Api, request
app = Flask(__name__)
api = Api(app)
from waitress import serve

import os
auth = os.environ.get('APPAUTH')

from io import StringIO
import subprocess

class cloudRun(Resource):
    
    def post(self):
        reqAuth = request.headers.get('Authorization')
        if auth!=reqAuth:
            return {'log': 'unauthorised', 'output': ''}
        
        # read contents
        data = {name: content for (name, content) in request.files.items()}
        
        # save code to local
        if 'code' not in data:
            return {'log': 'required code file.'}
        else:
            data['code'].save('code')
        
        # set input stream
        if 'stdin' not in data:
            in_fp = StringIO('')
        else:
            in_fp = data['stdin'].stream

        # run process
        result = subprocess.run(
            ['python', 'code'],
            stdin = in_fp,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            universal_newlines = True 
        )
        if 'code' in os.listdir():
            os.remove('code')
        return {"output": result.stdout, "log": result.stderr}

api.add_resource(cloudRun, '/')

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    serve(app, host="127.0.0.1", port=5000)
