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

# Lista para almacenar los datos de los empleados
empleados = []

# Leer el archivo CSV y generar los archivos HTML individuales
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
        
        # Agregar los datos del empleado a la lista
        empleados.append((nombre, codigo))

# Generar el archivo index.html con enlaces a los perfiles
index_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice de Perfiles</title>
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
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            margin: 10px 0;
        }}
        a {{
            text-decoration: none;
            color: #0066cc;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>Índice de Perfiles</h1>
    <ul>
"""

# Agregar los enlaces a los perfiles
for nombre, codigo in empleados:
    index_content += f'<li><a href="{output_folder_html}/{codigo}.html">{nombre}</a></li>\n'

index_content += """
    </ul>
</body>
</html>
"""

# Guardar el archivo index.html
with open('index.html', 'w', encoding='utf-8') as index_file:
    index_file.write(index_content)

print("Páginas HTML generadas correctamente en la carpeta 'empleados_html'.")
print("Archivo 'index.html' generado correctamente con enlaces a los perfiles.")
