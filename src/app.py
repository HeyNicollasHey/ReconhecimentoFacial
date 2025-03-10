from flask import Flask, render_template, request
import DAO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reconhecimento', methods=['POST'])
def enviar_foto():

    file = request.files['imagem']
    DAO.reconhecerRosto(file)


if __name__ == '__main__':
    app.run(debug=True)