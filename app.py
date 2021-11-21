import os

from flask import (
    Flask, 
    request, 
    redirect,
    jsonify, 
    url_for, 
    render_template
)

from flask_restx import (
    Resource, 
    Api 
)

from flask_uploads import (
    UploadSet, 
    IMAGES
)

from flask_wtf import FlaskForm

from wtforms import SubmitField

from flask_wtf.file import (
    FileField, 
    FileAllowed, 
    FileRequired
)

from werkzeug.utils import secure_filename

from dog_breed_classifier.app import predict

# References:
# https://hackersandslackers.com/flask-wtforms-forms/
# https://www.encora.com/insights/how-to-create-an-api-and-web-applications-with-flask

images = UploadSet('images', IMAGES)

app = Flask(__name__)

api = Api(app)

class UploadForm(FlaskForm):
    ''' Image Upload Form '''
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(images, 'Images only!')
    ])

    ''' Submit Field '''
    submit = SubmitField('Predict Dog Breed')

class Image(Resource):
    def post(self, image):
        form = UploadForm()
        if form.validate_on_submit():
            f = form.photo.data
            filename = secure_filename(f.filename)
            file_destination_path = os.path.join(app.instance_path, 'photos', filename)
            f.save(file_destination_path)
            detection = predict(file_destination_path)
        return render_template("imageupload.jinja2", form=form, template="form-template", detection=detection)
        #detection=detection, file_destination_path=file_destination_path) #redirect(request.referrer)

api.add_resource(Image, "/upload")