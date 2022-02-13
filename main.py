import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from external_apis import classifyImage, check_for_endangered

UPLOAD_FOLDER = '/Users/olunusi/PycharmProjects/flask-project/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return render_template("index.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'static/' + filename))
            return redirect(url_for("upload_success", img_name = filename))
    return redirect('index.html')

@app.route('/upload_success/<img_name>')
def upload_success(img_name):
    animal_details = classifyImage(img_name)
    name_of_animal = animal_details[0]
    family_of_animal = animal_details[1]
    type_of_feeder = animal_details[3]
    is_animal_endangered, url = check_for_endangered(name_of_animal)
    print(animal_details)
    animal_image = '/static/' + img_name
    POSTS = [name_of_animal, family_of_animal, type_of_feeder, is_animal_endangered, animal_image, url]
    return render_template("animal_page.html", posts=POSTS)

if __name__ == '__main__':
    app.run(debug=True)