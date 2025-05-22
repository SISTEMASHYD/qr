import os
import csv

# Carpeta donde se guardarán los perfiles HTML
OUTPUT_FOLDER = 'empleados_html'

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

# Plantilla HTML para el índice
INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Índice de Empleados</title>
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
    <h1>Índice de Empleados</h1>
    <ul>
        {empleados_list}
    </ul>
</body>
</html>
"""

def crear_carpeta_salida():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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
        archivo_html = os.path.join(OUTPUT_FOLDER, f"{emp['codigo']}.html")
        with open(archivo_html, 'w', encoding='utf-8') as f:
            f.write(html_content)

def generar_indice_html(empleados):
    empleados_list = ""
    for emp in empleados:
        empleados_list += f'<li><a href="{emp["codigo"]}.html">{emp["nombre"]}</a></li>\n'
    
    index_content = INDEX_TEMPLATE.format(empleados_list=empleados_list)
    archivo_index = os.path.join(OUTPUT_FOLDER, "index.html")
    with open(archivo_index, 'w', encoding='utf-8') as f:
        f.write(index_content)

def main():
    crear_carpeta_salida()
    empleados = leer_empleados_csv('datos_ejemplo.csv')
    generar_perfiles_html(empleados)
    generar_indice_html(empleados)
    print("Perfiles HTML e índice generados correctamente.")

if __name__ == "__main__":
    main()

