import os

from flask import (
    Flask, 
    request, 
    redirect,
    jsonify, 
    url_for, 
    render_template,
    session
)

from flask_restx import (
    Resource, 
    Api 
)

from flask_uploads import (
    UploadSet, 
    IMAGES,
    configure_uploads
)


from flask_wtf import (
    FlaskForm,
    csrf
)

from wtforms import SubmitField, StringField

from flask_wtf.file import (
    FileField, 
    FileAllowed, 
    FileRequired,
    DataRequired
)

from werkzeug.utils import secure_filename

from werkzeug.datastructures import FileStorage

from dog_breed_classifier.app import predict

# References:
# https://hackersandslackers.com/flask-wtforms-forms/
# https://www.encora.com/insights/how-to-create-an-api-and-web-applications-with-flask
# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask


app = Flask(__name__)

app.config['SECRET_KEY']='123'

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # restrict file size to 1MiB

app.config['UPLOADED_IMAGES_DEST']=os.path.join(app.instance_path, 'photos') 
images = UploadSet('images', IMAGES)
configure_uploads(app, images)

api = Api(app)

upload_parser = api.parser()
upload_parser.add_argument('file', 
                           location='files',
                           type=FileStorage)

class UploadForm(FlaskForm):
    # Image Upload Form 
    photo = FileField(validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])

class Image(Resource):
    def check_session(self):
        if session.get('big'):
            message = "session['big'] contains {} elements<br>".format(len(session['big']))
        else:
            message = "There is no session['big'] set<br>"
        message += "session['secret'] is {}<br>".format(session.get('secret'))
        message += "session['csrf_token'] is {}<br>".format(session.get('csrf_token'))
        return message
    @api.expect(upload_parser)
    def post(self):
        file_=request.files['file']
        filenames = file_.filename
        print(request.url)
        form = UploadForm(request.files, csrf_enabled=False)
        print(f"Uploaded Form: {request.form}")
        print(form.data)
        #print(form.email)
        print(form.photo)
        csrf.generate_csrf()
        message = self.check_session()
        print(f"message = {message}")

        filename = secure_filename(filenames)
        file_destination_path = os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename)
        if not os.path.exists(app.config['UPLOADED_IMAGES_DEST']):
            os.makedirs(app.config['UPLOADED_IMAGES_DEST'])
        file_.save(file_destination_path)
        print(f"File Destination Path: {file_destination_path}")
        detection = predict(file_destination_path)
        print(f"detection string = {detection}")
        '''
        else:
            print(f"Errors: {form.errors}")
            '''
        return render_template("imageupload.jinja2", form=form, template="form-template", detection=detection, url=request.url)

api.add_resource(Image, "/upload")