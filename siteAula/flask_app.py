from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'
db = SQLAlchemy(app)
UPLOAD_FOLDER = '/home/NathanBatista/mysite/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.app_context().push()
app.secret_key = 'Nathan123'

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))

    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

@app.route("/")
def index():
    usuarios = Usuario.query.all()
    return render_template('index.html', usuarios=usuarios)

@app.route('/usuario', methods=['POST', 'GET'])
def addUsuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        usuario = Usuario(nome, senha)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('index'))
    return render_template('usuario.html')

@app.route('/delete/<int:id>')
def delete(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['arquivo']
        if file:
            filename = file.filename
            savePath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(savePath)
            return 'upload feito com sucesso'
    return render_template('upload.html')

@app.route('/area_vip')
def area_vip():
    if 'username' in session:
        return render_template('area_vip.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['username']
        senha = request.form['password']
        usuario = Usuario.query.filter_by(nome=nome, senha=senha).first()
        if usuario:
            session['username'] = nome
            return redirect(url_for('area_vip'))
        else:
            flash('Usuário ou senha incorretos. Tente novamente.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
