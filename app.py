import werkzeug.utils
from diagnose import *
from flask import Flask,request,jsonify,send_from_directory
import werkzeug
import cv2

app = Flask(__name__)

@app.route('/upload',methods=["POST"])
def upload():
    if (request.method=="POST"):
        imagefile = request.files['image']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        path = './/static//uploaded/'+filename
        imagefile.save(path)
        cdr = calculate_cdr(detectOC(path,modeloc),detectOD(path,modelod))
        
        
        oc_url = f'https://e083-2409-40c2-1197-7f4a-2de1-88dc-8c4f-bfe5.ngrok-free.app/get-image-oc/{filename}'
        od_url = f'https://e083-2409-40c2-1197-7f4a-2de1-88dc-8c4f-bfe5.ngrok-free.app/get-image-od/{filename}'
        
        return jsonify({
            "message": "Image uploaded successfully",
            "oc_url": oc_url,
            "od_url": od_url,
            "cdr": cdr
        })
       
@app.route('/get-image-oc/<filename>', methods=["GET"])        
def get_image_oc(filename):
    try:
        # Send the image from the uploaded folder
        return send_from_directory(output_path_oc, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    
@app.route('/get-image-od/<filename>', methods=["GET"])        
def get_image_od(filename):
    try:
        # Send the image from the uploaded folder
        return send_from_directory(output_path_od, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


if __name__=="__main__":
    
    app.run(debug=True,port=4000)
