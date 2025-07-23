from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'minhachavesecreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users_db = {}

class User(UserMixin):
    def __init__(self, id, email, password_hash):
        self.id = id
        self.email = email
        self.password_hash = password_hash

    def get_id(self):
        return self.id

@login_manager.user_loader
def load_user(user_id):
    for email, user_data in users_db.items():
        if user_data['id'] == user_id:
            return User(user_data['id'], email, user_data['password_hash'])
    return None

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = users_db.get(email)
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], email, user_data['password_hash'])
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
        elif email in users_db:
            flash('Este e-mail já está cadastrado.', 'danger')
        else:
            user_id = str(len(users_db) + 1)
            password_hash = generate_password_hash(password)
            users_db[email] = {'id': user_id, 'password_hash': password_hash}
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Bem-vindo, {current_user.email}!Você está logado."

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('login'))
@app.route('/usuarios')
@login_required
def listar_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)
