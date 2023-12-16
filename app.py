
from flask import Flask,render_template, request, redirect, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import base64
import streamlit as st

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    label = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)  # Remove unique=True
    data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f' {self.label}{self.filename}'

#  function to convert data
def convert_data(data, file_name):
    # Convert binary format to images 
    # or files data(with given file_name)
    with open(file_name, 'wb') as file:
        file.write(data)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        _name = request.form['l_name']
        _label = request.form['select_label']
        image = request.files['image']

        if image and _name != "" and _label != "0" :
            
            filename = image.filename
            new_image = Image(name=_name, label=_label, filename=filename, data=image.read())
            db.session.add(new_image)
            db.session.commit()

    data_list = Image.query.all()

    # blob_records = YourModel.query.all()
    blob_data_list = []

    for record in data_list:
        blob_data_list.append({
            'id': record.id,
            'image': base64.b64encode(record.data).decode('utf-8'),
            'label':record.label,
            'l_name':record.name,
            'filename':record.filename

        })

    # # Specify the path to the folder containing images
    # folder_path = 'static/images'
    
    # Get a list of all files in the folder
    # files = os.listdir(folder_path)
    
    # # Filter files to only include images (you can customize this based on your image extensions)
    # image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    

    # base64_images = [base64.b64encode(images).decode("utf-8") for images.data in images]
    # # image_data_list = []

    # # for image in images:
    # #     image_data = base64.b64encode(image.data).decode('utf-8')
    # #     image_data_list.append(image_data)

    return render_template('index.html', data=blob_data_list)


@app.route('/delete/<int:id>')
def delete(id):
    todo = Image.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
