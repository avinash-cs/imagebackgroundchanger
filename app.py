import cv2
import os
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask,request,render_template

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','webp'])

if 'static' not in os.listdir('.'):
    os.mkdir('static')

if 'uploads' not in os.listdir('static/'):
    os.mkdir('static/uploads')

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# def remove_background(input_path,output_path):
#     input = Image.open(input_path)
#     output = remove(input)
#     output.save(output_path)


def remove_background(input_path, output_path, custom_background_path):
    # Remove the background
    input_image = Image.open(input_path)
    removed_bg_image = remove(input_image)

    # Open the custom background
    custom_background = Image.open(custom_background_path)
    # Resize the custom background to match the size of the removed background
    custom_background = custom_background.resize(removed_bg_image.size, Image.Resampling.LANCZOS)

    # Combine the removed background image with the custom background
    final_image = Image.alpha_composite(custom_background.convert("RGBA"), removed_bg_image)

    # Save the final image
    final_image.save(output_path)

@app.route('/')
def home():
    return render_template('home.html')

# @app.route('/remback',methods=['POST'])
# def remback():
#     file = request.files['file']
#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         rembg_img_name = filename.split('.')[0]+"_rembg.png"
#         remove_background(UPLOAD_FOLDER+'/'+filename,UPLOAD_FOLDER+'/'+rembg_img_name)
#         return render_template('home.html',org_img_name=filename,rembg_img_name=rembg_img_name)


@app.route('/remback', methods=['POST'])
def remback():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Specify the path to your custom background image
        custom_background_path = 'blackjpg.jpg'

        rembg_img_name = filename.split('.')[0] + "_rembg.png"
        final_img_name = filename.split('.')[0] + "_final.png"

        remove_background(os.path.join(app.config['UPLOAD_FOLDER'], filename),
                          os.path.join(app.config['UPLOAD_FOLDER'], rembg_img_name),
                          custom_background_path)

        return render_template('home.html', org_img_name=filename, rembg_img_name=rembg_img_name, final_img_name=final_img_name)






if __name__ == '__main__':
    app.run(debug=True)