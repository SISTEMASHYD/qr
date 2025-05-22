import os
import csv
import qrcode
from PIL import Image, ImageDraw

def agregar_logo(qr_img, logo_path, logo_size_ratio=0.2):
    logo = Image.open(logo_path).convert("RGBA")
    qr_width, qr_height = qr_img.size
    logo_size = int(qr_width * logo_size_ratio), int(qr_height * logo_size_ratio)
    logo = logo.resize(logo_size, Image.Resampling.LANCZOS)

    # Calcular posición para centrar el logo
    logo_pos = ((qr_width - logo_size[0]) // 2, (qr_height - logo_size[1]) // 2)

    # Dibujar un círculo blanco en el centro del QR
    draw = ImageDraw.Draw(qr_img)
    circle_bbox = [logo_pos[0], logo_pos[1], logo_pos[0] + logo_size[0], logo_pos[1] + logo_size[1]]
    draw.ellipse(circle_bbox, fill="white")

    # Pegar el logo con su canal alfa (transparencia)
    qr_img.paste(logo, logo_pos, mask=logo)
    return qr_img

# Crear carpeta si no existe
output_folder = 'imageQRregister'
os.makedirs(output_folder, exist_ok=True)

with open('datos_ejemplo.csv', newline='', encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nombre = row['Nombre']
        codigo = row['Código']
        cargo = row['Cargo']
        contenido_qr = f"Nombre: {nombre}, Código: {codigo}, Cargo: {cargo}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(contenido_qr)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        qr_img_con_logo = agregar_logo(qr_img, 'logoqr.png')
        qr_img_con_logo.save(os.path.join(output_folder, f"{nombre}.png"))

print("Códigos QR con logo generados correctamente en la carpeta 'imageQRregister'.")
