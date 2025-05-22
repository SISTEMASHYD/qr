import os
import csv
import qrcode

# Carpeta donde se guardarán los perfiles HTML
OUTPUT_FOLDER = 'empleados_html'
# Carpeta donde se guardarán los códigos QR
QR_FOLDER = 'qrcodes'

# Plantilla HTML para cada empleado
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil de {nombre}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            max-width: 600px;
            margin: auto;
        }}
        h1 {{
            color: #333;
        }}
        p {{
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <h1>Perfil de {nombre}</h1>
    <p><strong>Código:</strong> {codigo}</p>
    <p><strong>Cargo:</strong> {cargo}</p>
</body>
</html>
"""

def crear_carpetas_salida():
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
        archivo_html = os.path.join(OUTPUT_FOLDER, f"{emp['nombre']}.html")
        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(html_content)

def generar_qr_codes(empleados, base_url):
    for emp in empleados:
        url = f"{base_url}/{OUTPUT_FOLDER}/{emp['nombre']}.html"
        qr = qrcode.make(url)
        archivo_qr = os.path.join(QR_FOLDER, f"{emp['nombre']}.png")
        qr.save(archivo_qr)

def main():
    base_url = "https://tu-usuario.github.io/mi-proyecto"  # Cambia esto por la URL de tu GitHub Pages
    crear_carpetas_salida()
    empleados = leer_empleados_csv('datos_ejemplo.csv')
    generar_perfiles_html(empleados)
    generar_qr_codes(empleados, base_url)
    print("Perfiles HTML y códigos QR generados correctamente.")

if __name__ == "__main__":
    main()

