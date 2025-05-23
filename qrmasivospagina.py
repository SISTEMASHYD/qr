import os
import csv
import qrcode
from PIL import Image, ImageDraw

# Carpeta donde se guardarán los perfiles HTML
OUTPUT_FOLDER = 'empleados_html'
QR_FOLDER = 'qrcodes'

# Plantilla HTML para cada empleado
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil de {nombre}</title>
    <link rel="stylesheet" type="text/css" href="../estilos.css">
</head>
<body>
    <div class="card credencial">
        <div class="logo-superior-container">
            <img src="../logovcard.jpg" alt="Logo de Dolphy Helados" class="logo-superior">
        </div>
        <div class="info-container">
            <h1>{nombre}</h1>
            <p><strong>Cargo:</strong> {cargo}</p>
            <p><strong>Código:</strong> {codigo}</p>
        </div>
    </div>
</body>
</html>

"""


def crear_carpeta_salida():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(QR_FOLDER, exist_ok=True)

def leer_empleados_csv(nombre_archivo):
    empleados = []
    with open(nombre_archivo, newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            empleados.append({
                'nombre': row['Nombre'],
                'codigo': row['Código'],
                'cargo': row['Cargo']
            })
    return empleados

def generar_perfiles_html(empleados):
    for emp in empleados:
        html_content = HTML_TEMPLATE.format(
            nombre=emp['nombre'],
            codigo=emp['codigo'],
            cargo=emp['cargo']
        )
        archivo_html = os.path.join(OUTPUT_FOLDER, f"{emp['nombre']}_{emp['cargo']}_{emp['codigo']}.html")
        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(html_content)

def generar_qr(empleados, base_url):
    for emp in empleados:
        url = f"{base_url}/{OUTPUT_FOLDER}/{emp['nombre']}_{emp['cargo']}_{emp['codigo']}.html"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Insertar el logo en el centro del QR
        logo = Image.open('logoqr.png')
        basewidth = 150  # Tamaño del logo
        wpercent = (basewidth / float(logo.size[0]))
        hsize = int((float(logo.size[1]) * float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)

        # Calcular la posición del círculo blanco
        logo_position = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
        circle_radius = logo.size[0] // 7  # Radio del círculo blanco (más grande)

        # Dibujar el círculo blanco
        draw = ImageDraw.Draw(img)
        draw.ellipse(
            (logo_position[0] - circle_radius, logo_position[1] - circle_radius,
             logo_position[0] + circle_radius + logo.size[0], logo_position[1] + circle_radius + logo.size[1]),
            fill='white'
        )

        # Pegar el logo encima del círculo blanco
        img.paste(logo, logo_position, logo)

        qr_filename = os.path.join(QR_FOLDER, f"{emp['nombre']}_{emp['cargo']}_{emp['codigo']}.png")
        img.save(qr_filename)

def generar_index_html(empleados):
    index_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice de Empleados</title>
    <link rel="stylesheet" type="text/css" href="estilos.css">
</head>
<body>
    <div class="index-container">
        <h1>Índice de Empleados</h1>
        <ul>
"""
    for emp in empleados:
        index_content += f'<li><a href="{OUTPUT_FOLDER}/{emp["nombre"]}_{emp["cargo"]}_{emp["codigo"]}.html">{emp["nombre"]} - {emp["cargo"]} - {emp["codigo"]}</a></li>\n'

    index_content += """
        </ul>
    </div>
</body>
</html>
"""
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_content)

def crear_archivo_css():
    css_content = """
body {
    font-family: Arial, sans-serif;
    margin: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 10px;
    max-width: 800px;
    margin: auto;
    background-color: #f0f8ff;
}

h1 {
    color: #1E90FF;
}

p {
    font-size: 18px;
    color: #333;
}

ul {
    list-style-type: none;
    padding: 0;
}

li {
    margin: 10px 0;
}

a {
    text-decoration: none;
    color: #1E90FF;
}

a:hover {
    color: #ff69b4;
}

.card {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin: 20px 0;
}

/* NUEVO: estilo tipo credencial */
.credencial {
    width: 350px;
    height: auto; /* más flexible que 500px fijos */
    border: 4px solid #1E90FF;
    border-radius: 15px;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    gap: 10px; /* Espacio uniforme entre elementos internos */
}

.logo-superior-container {
    text-align: center;
}

.logo-superior {
    max-width: 200px;
    height: auto;
    margin-bottom: 10px; /* Espacio debajo del logo */
}

.info-container {
    text-align: center;
}

h1 {
    color: #1E90FF;
    font-size: 24px;
    margin: 10px 0;
}

p {
    font-size: 18px;
    margin: 5px 0;
    color: #333;
}


"""
    with open('estilos.css', 'w', encoding='utf-8') as f:
        f.write(css_content)

def main():
    crear_carpeta_salida()
    empleados = leer_empleados_csv('datos_ejemplo.csv')
    generar_perfiles_html(empleados)
    generar_qr(empleados, 'https://sistemashyd.github.io/qr/')
    generar_index_html(empleados)
    crear_archivo_css()
    print("Perfiles HTML, códigos QR, índice y estilos generados correctamente.")

if __name__ == "__main__":
    main()
