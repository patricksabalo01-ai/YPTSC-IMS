import os
import qrcode
from flask import current_app
#QR CODE GENERATOR
def generate_qr(data):
    #CHECK FLASK CONTEXT
    if not current_app:
        raise RuntimeError(
            "Flask application context missing.")
    #GET STATIC DIRECTORY
    static_folder = current_app.static_folder
    if not static_folder:
        raise RuntimeError(
            "Static folder is not configured.")
    #QR STORAGE DIRECTORY
    qr_folder = os.path.join(static_folder,"qr_codes")
    os.makedirs(qr_folder,exist_ok=True)
    # FILE NAME
    filename = (f"{data}.png")
    filepath = os.path.join(qr_folder,filename)
    #GENERATE QR IMAGE
    qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image()
    qr_image.save(filepath)
    #VERIFY FILE CREATION
    if not os.path.exists(filepath):
        raise RuntimeError(
            f"QR file was not created: {filepath}")
    print("==============================")
    print("QR GENERATED SUCCESS")
    print("DATA:", data)
    print("LOCATION:", filepath)
    print("SIZE:", os.path.getsize(filepath), "bytes")
    print("==============================")
    #RETURN STATIC PATH
    return (f"qr_codes/{filename}")
