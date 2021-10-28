"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, redirect
from api.models import db, User
from api.utils import generate_sitemap, APIException

import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from datetime import datetime

from flask import Flask, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

api = Blueprint('api', __name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#Registrar ususario

@api.route('/register', methods=['POST'])
def register():
    #congif cloudinary
    cloudinary.config(
        cloud_name= os.getenv('CLOUD_NAME'),
        api_key= os.getenv('API_KEY'),
        api_secret= os.getenv('API_SECRET')
    )
    email = request.form.get('email')
    password  =request.form.get('password')
    image_url = None 
    #para subir solo una imagen
    file_upload = request.files.get('file')
    print(file_upload)
    if file_upload:
        print(file_upload.filename)

        #validar la extension del archivo
        if file_upload.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            print("si")
            upload_result = cloudinary.uploader.upload(file_upload)
            if upload_result:
                image_url = upload_result.get('secure_url')
                file_name = file_upload.filename
            
            user = User( email=email, password=password, is_active=True, image_url=image_url)
            user.save()
            response_body = {
                        "message": "save image"
                        }
            return jsonify(response_body), 200
    return jsonify("Image format invalid"), 400
    
    

    
@api.route('/hello', methods=['POST', 'GET'])
def handle_hello(app):

    response_body = {
        "message": "Hello! I'm a message that came from the backend"
    }

    return jsonify(response_body), 200

#subir imagen a un registro ya existente
@api.route('/upload-file', methods=['POST'])
def upload_file():
    #el usuario que se le ingresa la imagen
    user = User.query.get(1)

    #congif cloudinary
    cloudinary.config(
        cloud_name= os.getenv('CLOUD_NAME'),
        api_key= os.getenv('API_KEY'),
        api_secret= os.getenv('API_SECRET')
    )

    #para subir solo una imagen
    file_upload = request.files.get('file')
    print(file_upload)
    if file_upload:
        print(file_upload.filename)
        file_name=file_upload.filename
        #validar la extension del archivo
        if file_upload.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
            print("si")
            upload_result = cloudinary.uploader.upload(file_upload)
            if upload_result:
                user.image_url = upload_result.get('secure_url')
                user.save()
                if os.path.exists('./src/front/img/' + file_name):
                    print("existe")
                    now = datetime.now()
                    url_Img = str(now).replace(' ', '') + file_name
                print("no xiste")
                url_Img = str(file_name).replace(' ', '')
                filename = secure_filename(file_upload.filename)
                file_upload.save(os.path.join('./src/front/img/', filename))
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                response_body = {
                        "message": "save image"
                        }     
                return jsonify(response_body), 200
    return jsonify("Image format invalid"), 400

    #para subir varia imagenes
    # files = request.files
    # print(files.get('file'))
    # for file_key in files:
    #     file_to_upload = files.get(file_key)

    #     if file_to_upload:
    #         upload_result = cloudinary.uploader.upload(file_to_upload)
    #         return jsonify(upload_result) 
        # cloudinary.uploader.upload(file, 
        #     folder = "/", 
        #     public_id = "profile",
        #     overwrite = True,  
        #     resource_type = "image")
    #return jsonify('success'),200