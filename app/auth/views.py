from flask import render_template, url_for, flash, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app.model import Users
# Tentar entender o porque precisei chamar essse db
from app.model import db
from . import bp_auth
# Usar o serializer pro banco se comunicar com json e usar json pra salvar dados
# from app.serealizer import ProdutosSchema, UsersSchema

# Index como login
@bp_auth.route('/', methods=['GET', 'POST'])
@bp_auth.route('/login', methods=['GET', 'POST'])
def index():
    title = 'Login'
    
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        
        user = Users.query.filter_by(nome=nome).first()
        
        if not user or not user.verify_password(senha):
            if not user:
                flash('Seu nome de usuário não existe ou está incorreto.', 'danger')
            
            if user and not user.verify_password(senha):
                flash('Sua senha está incorreta.', 'danger')
            
            return redirect(url_for('bp_auth.index'))
        
        login_user(user)
        return  redirect(url_for('bp_produtos.sistema_produtos'))
    
    return render_template('home.html', title=title)


@bp_auth.route('/criar-conta', methods=['GET', 'POST'])
def criar_conta():
    title = 'Criar Conta'
    nome = ''
    email = ''
    senha = ''
    
    if request.method == 'POST':    
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        
        if nome != '' and email != '' and senha != '':
            conta = Users(nome, email, senha)
            db.session.add(conta)
            db.session.commit()
            
            flash('Sua conta foi criada com sucesso!', 'success')
        else:
            flash('Você precisa preencher todos os dados.', 'danger')
            
    return render_template('criar-conta.html', title=title)


# Desfazer login e retorna a page login
@bp_auth.route('/logout', methods=['GET'])
def logout():
    logout_user()    
    return redirect(url_for('bp_auth.index'))
