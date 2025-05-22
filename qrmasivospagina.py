import os
import csv

# Crear carpeta si no existe
output_folder_html = 'empleados_html'
os.makedirs(output_folder_html, exist_ok=True)

# Plantilla HTML básica
html_template = """
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

with open('datos_ejemplo.csv', newline='', encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        nombre = row['Nombre']
        codigo = row['Código']
        cargo = row['Cargo']

        html_content = html_template.format(nombre=nombre, codigo=codigo, cargo=cargo)

        html_filename = os.path.join(output_folder_html, f"{codigo}.html")
        with open(html_filename, 'w', encoding='utf-8') as htmlfile:
            htmlfile.write(html_content)

print("Páginas HTML generadas correctamente en la carpeta 'empleados_html'.")
