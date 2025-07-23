from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'minhachavesecreta'

def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM auth_users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if usuario:
        return User(usuario['id'], usuario['email'], usuario['password_hash'])
    return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM auth_users WHERE email = ?', (email,)).fetchone()
        conn.close()
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['email'], user_data['password_hash'])
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha incorretos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
        else:
            conn = get_db_connection()
            existing = conn.execute('SELECT * FROM auth_users WHERE email = ?', (email,)).fetchone()
            if existing:
                flash('Este e-mail já está cadastrado.', 'danger')
            else:
                password_hash = generate_password_hash(password)
                conn.execute('INSERT INTO auth_users (email, password_hash) VALUES (?, ?)', (email, password_hash))
                conn.commit()
                flash('Conta criada com sucesso! Faça login.', 'success')
            conn.close()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Bem-vindo, {current_user.email}! Você está logado."

@app.route('/usuarios')
@login_required
def listar_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/novo', methods=['GET', 'POST'])
@login_required
def criar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (nome) VALUES (?)', (nome,))
        conn.commit()
        conn.close()
        flash('Usuário criado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))
    return render_template('criar_usuario.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    if not usuario:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('listar_usuarios'))
    if request.method == 'POST':
        novo_nome = request.form['nome']
        conn.execute('UPDATE users SET nome = ? WHERE id = ?', (novo_nome, id))
        conn.commit()
        conn.close()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))
    conn.close()
    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/usuarios/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_usuario(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Usuário excluído com sucesso.', 'success')
    return redirect(url_for('listar_usuarios'))

if __name__ == '__main__':
    app.run(debug=True)
