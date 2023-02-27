from flask import Flask, jsonify, request, send_file, send_from_directory
from PIL import Image
import os

app = Flask(__name__)
PORT = 5000
HOST = "0.0.0.0"

UPLOAD_FOLDER_DEBUG = './debug'
UPLOAD_FOLDER_PRODUCTION = './production'
DEBUG = True

@app.route('/', methods=['GET'])
def mainPage():
    if(request.method == 'GET'):
        return 'Image Server running correctly'

@app.route('/uploadFile', methods=['GET', 'POST'])
def fileUpload():
    if(request.method == "POST"):
        file = request.files['file']
        if file:
            filename = file.filename
            print(file)
            if DEBUG:

                file.save(os.path.join(app.root_path, 'debug', filename))
                foo = Image.open(os.path.join(app.root_path, 'debug', filename))
                width, height = foo.size
                foo = foo.resize((width, height), Image.LANCZOS)
                foo.save(os.path.join(app.root_path, 'debug', filename), optimize=True, quality=50)
                return


            if DEBUG != True:
                file.save(os.path.join(app.root_path, 'production', filename))
                foo = Image.open(os.path.join(app.root_path, 'production', filename))
                width, height = foo.size
                foo = foo.resize((width, height), Image.LANCZOS)
                foo.save(os.path.join(app.root_path, 'production', filename), optimize=True, quality=50)
                return



@app.route('/getImage/<image>', methods=['GET'])
def sendImageFile(image):
    if(request.method == 'GET'):
        if(DEBUG == True):
            return send_file(os.path.join(app.root_path, 'debug', image))
        if(DEBUG == False):
            return send_from_directory(os.path.join(app.root_path, 'production', image))





if __name__ == '__main__':
    from waitress import serve
    
    print("Server started on adress: " + str(HOST) + " and port: " + str(PORT))
    serve(app, host=HOST, port=PORT)

    # DEBUG START
    # app.run(debug = True)