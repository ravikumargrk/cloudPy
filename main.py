from flask import Flask, Response
from flask_restful import Resource, Api, request
app = Flask(__name__)
api = Api(app)
from waitress import serve

import os
auth = os.environ.get('APPAUTH')

from io import StringIO
import subprocess

class cloudRun(Resource):
    def get(self):
        reqAuth = request.headers.get('Authorization')
        if auth!=reqAuth:
            return Response('Unauthorised', mimetype='text/csv', status=401)
        else:
            return Response('Authorised', mimetype='text/csv', status=200)
            
    def post(self):
        reqAuth = request.headers.get('Authorization')
        if auth!=reqAuth:
            return Response('Unauthorised', mimetype='text/csv', status=401)
        
        # read contents
        data = {name: content for (name, content) in request.files.items()}
        
        # save code to local
        for name in data:
            if name != 'stdin':
                data[name].save(name)
        
        if 'main.py' not in data:
            return Response('Required main.py file', mimetype='text/csv', status=201)
        
        # set input stream
        if 'stdin' not in data:
            in_fp = StringIO('')
        else:
            in_fp = data['stdin'].stream

        # run process
        result = subprocess.run(
            ['python', 'main.py'],
            stdin = in_fp,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            universal_newlines = True 
        )

        for name in data:
            if name in os.listdir():
                os.remove(name)
                
        # response
        if len(result.stderr):
            r = result.stderr
        else:
            r = result.stdout
        return Response(
                r,
                mimetype='text/csv'
            )
        
api.add_resource(cloudRun, '/')

if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    serve(app, host="127.0.0.1", port=5000)
