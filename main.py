import ply.lex

from flask import Flask, render_template, request
from ply import lex
from textblob import TextBlob

app = Flask(__name__)

def procesarCadena(entrada):
    # Implement your logic to process the input string
    # For demonstration purposes, let's assume the processing is converting the string to uppercase
    cadenaProcesada = entrada.upper()
    return cadenaProcesada


def procesarEntradaSemantica(entrada):
    # Implement your logic to process the semantic input string
    # For demonstration purposes, let's assume the processing is checking if the input is a valid Python expression
    if not isinstance(entrada, str):
        return "Error de sintaxis"

    try:
        eval(entrada)
    except SyntaxError:
        return "Error de sintaxis"

    return "Entrada semánticamente correcta"


tokens = (
    'NUMERO',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
)

t_SUMA = r'\+'
t_RESTA = r'\-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_ignore = '\t\n'

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f'Caracter errroneo: {t.value[0]}')
    t.lexer.skip(1)

# construyendo el lexer
lexer = lex.lex()

def analizadorLexico(codigoFuente):
    lexer.input(codigoFuente)
    for token in lexer:
        if token == list['']:
            return False
        else:
            return True
#-----------------------------------------------------
#Analizador semantico


def analyze_sentiment(text):
    blob= TextBlob(text)

    polarity= blob.sentiment.polarity

    if polarity>0:
        sentiment='positivo'
    elif polarity<0:
        sentiment= 'negativo'
    else:
        sentiment='neutro'

    print(f'Text: {text}')
    print(f'Sentimiento: {sentiment}')
    return sentiment


@app.route("/", methods=["GET", "POST"])
def homepage():
    cadenaProcesada = None
    if request.method == "POST":
        entrada = request.form.get("entrada")
    return render_template("index.html", title="Automatas II", cadenaProcesada=cadenaProcesada)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/Semantico.html", methods=["GET", "POST"])
def semantico():
    mensajeError = None
    if request.method == "POST":
        cadena = request.form['cadena']
        sentimiento= analyze_sentiment(cadena)
        return render_template("Semantico.html", feeling= sentimiento)
    else:
        return render_template("Semantico.html")


@app.route("/Sintactico.html")
def sintactico():
    mensajeError = None
    if request.method == "POST":
        entrada = request.form.get("entrada")
        mensajeError = procesarEntradaSemantica(entrada)

    return render_template("Sintactico.html", mensajeError=mensajeError)


@app.route("/lexico.html")
def lexico():
    mensajeError = None

    if request.method == "POST":
        entrada = request.form.get("entrada")
        mensajeError = procesarEntradaSemantica(entrada)

    return render_template("lexico.html", mensajeError=mensajeError)



if __name__ == "main":
    app.run(debug=True)


