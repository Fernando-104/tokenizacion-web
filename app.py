
# Importa Flask para crear la aplicación web.
# request permite leer lo que escribe el usuario.
# render_template permite mostrar una página HTML.
from flask import Flask, render_template, request

# Importa re para buscar y separar texto usando patrones.
import re

# Importa unicodedata para quitar los acentos.
import unicodedata

# Importa Counter para contar cuántas veces aparece cada palabra.
from collections import Counter


# Crea la aplicación web de Flask.
app = Flask(__name__)


# Lista de palabras comunes que queremos eliminar del texto.
# Puedes agregar o quitar palabras según las necesidades del proyecto.
PALABRAS_VACIAS = {
    "a", "al", "algo", "como", "con", "de", "del", "el", "ella",
    "en", "es", "esa", "ese", "eso", "esta", "este", "esto",
    "la", "las", "lo", "los", "mi", "mis", "muy", "o", "para",
    "pero", "por", "que", "se", "sin", "su", "sus", "un", "una",
    "uno", "y", "ya"
}


# Define una función para normalizar las palabras.
def normalizar(palabra):
    # Convierte la palabra a letras minúsculas.
    palabra = palabra.lower()

    # Separa los caracteres de sus acentos.
    palabra = unicodedata.normalize("NFD", palabra)

    # Conserva únicamente los caracteres que no son marcas de acento.
    palabra = "".join(
        caracter for caracter in palabra
        if unicodedata.category(caracter) != "Mn"
    )

    # Devuelve la palabra normalizada.
    return palabra


# Define la ruta principal de la página web.
# GET muestra la página y POST procesa el formulario.
@app.route("/", methods=["GET", "POST"])
def inicio():

    # Inicializa la variable donde se guardará el texto ingresado.
    texto = ""

    # Crea listas y variables vacías para mostrar los resultados.
    oraciones = []
    tokens = []
    normalizados = []
    filtrados = []
    frecuencias = {}
    vocabulario = []
    vector = []

    # Comprueba si el usuario envió el formulario.
    if request.method == "POST":

        # Obtiene el texto del campo llamado "texto".
        # Si no se escribió nada, utiliza una cadena vacía.
        texto = request.form.get("texto", "")

        # Divide el texto en oraciones usando ., ! y ? como referencias.
        # También elimina los espacios sobrantes de cada oración.
        oraciones = [
            oracion.strip()
            for oracion in re.split(r"(?<=[.!?])\s+", texto)
            if oracion.strip()
        ]

        # Busca las palabras del texto y las guarda en una lista.
        # El patrón reconoce letras, incluidas las vocales acentuadas y la ñ.
        tokens = re.findall(
            r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+",
            texto
        )

        # Convierte cada palabra a minúsculas y elimina sus acentos.
        normalizados = [normalizar(palabra) for palabra in tokens]

        # Elimina las palabras vacías que no aportan mucho al análisis.
        filtrados = [
            palabra for palabra in normalizados
            if palabra not in PALABRAS_VACIAS
        ]

        # Cuenta cuántas veces aparece cada palabra útil.
        conteo = Counter(filtrados)

        # Ordena alfabéticamente las palabras para crear el vocabulario.
        vocabulario = sorted(conteo.keys())

        # Crea un diccionario con cada palabra y su frecuencia.
        frecuencias = {
            palabra: conteo[palabra]
            for palabra in vocabulario
        }

        # Construye el vector numérico siguiendo el orden del vocabulario.
        # Cada número representa la frecuencia de una palabra.
        vector = [conteo[palabra] for palabra in vocabulario]

    # Envía los resultados a la página HTML para mostrarlos.
    return render_template(
        "index.html",
        texto=texto,
        oraciones=oraciones,
        tokens=tokens,
        normalizados=normalizados,
        filtrados=filtrados,
        frecuencias=frecuencias,
        vocabulario=vocabulario,
        vector=vector
    )


# Comprueba si este archivo se está ejecutando directamente.
if __name__ == "__main__":

    # Inicia el servidor local en modo de depuración.
    # debug=True ayuda a detectar errores mientras desarrollas.
    app.run(debug=True)
