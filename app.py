from flask import Flask, render_template, request, send_file
import qrcode
import os
# pip install Flask qrcode[pil]
app = Flask(__name__)

cf_port = os.getenv("PORT")

# Ensure the directory for storing QR codes exists
QR_CODE_DIR = os.path.join('static', 'qr_codes')
os.makedirs(QR_CODE_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input from the form
        input_data = request.form['input_data']
       
        # Split the input data into multiple parameters (you can customize this logic)
        params = input_data.split(',')
       
        # Generate QR codes for each parameter
        qr_images = []
        st_array = []
        for i, param in enumerate(params):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=4,
            )
            qr.add_data(param.strip())
            qr.make(fit=True)
           
            img = qr.make_image(fill_color="black", back_color="white")
            img_path = os.path.join(QR_CODE_DIR, f'qr_{i}.png')
            img.save(img_path)
            #qr_images.append(f'/static/qr_codes/qr_{i}.png')
            qr_images.append([f'/static/qr_codes/qr_{i}.png', param])
            #c = [*qr_images, *st_array]
       
        return render_template('index.html', qr_images=qr_images)
   
    return render_template('index.html', qr_images=None)

#if __name__ == '__main__':
#    app.run(debug=True)
if __name__ == '__main__':
   if cf_port is None:
       app.run(host='0.0.0.0', port=5000, debug=True)
   else:
       app.run(host='0.0.0.0', port=int(cf_port), debug=True)    