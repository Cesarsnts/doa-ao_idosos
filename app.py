from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'minhachavesecreta'

def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        u = UserMixin()
        u.id = user['id']
        u.username = user['username']
        return u
    return None

@app.route('/')
def home():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            login_user(load_user(user['id']))
            return redirect(url_for('dashboard'))
        flash('Credenciais inválidas.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        flash('Cadastro realizado com sucesso.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/perfil')
@login_required
def perfil():
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()
    conn.close()
    return render_template('perfil.html', usuario=usuario)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM users WHERE id = ?', (current_user.id,)).fetchone()
    if request.method == 'POST':
        new_username = request.form['username']
        conn.execute('UPDATE users SET username = ? WHERE id = ?', (new_username, current_user.id))
        conn.commit()
        conn.close()
        flash('Perfil atualizado com sucesso.', 'success')
        return redirect(url_for('perfil'))
    conn.close()
    return render_template('editar_perfil.html', usuario=usuario)

@app.route('/perfil/excluir', methods=['POST'])
@login_required
def excluir_perfil():
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (current_user.id,))
    conn.commit()
    conn.close()
    logout_user()
    flash('Conta removida.', 'success')
    return redirect(url_for('register'))

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
