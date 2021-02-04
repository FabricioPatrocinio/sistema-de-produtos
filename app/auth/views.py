from flask import render_template, url_for, flash, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from app.model import Users
# Tentar entender o porque precisei chamar essse db
from app.model import db
from . import bp_auth
import os
# Usar o serializer pro banco se comunicar com json e usar json pra salvar dados
# from app.serealizer import ProdutosSchema, UsersSchema

# Caminho para o updload da imagem
IMAGE_UPLOADS = '/home/f/my-dev-py/sys-pro/app/static/uploads/imagens/perfil/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Index como login
@bp_auth.route('/', methods=['GET', 'POST'])
@bp_auth.route('/login', methods=['GET', 'POST'])
def index():
    title = 'Login'
    
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        
        try:
            user = Users.query.filter_by(nome=nome).first()
            
            if not user or not user.verify_password(senha):
                if not user:
                    flash('Seu nome de usuário não existe ou está incorreto.', 'danger')
                
                if user and not user.verify_password(senha):
                    flash('Sua senha está incorreta.', 'danger')
                
                return redirect(url_for('bp_auth.index'))
            
            login_user(user)
            return  redirect(url_for('bp_produtos.sistema_produtos'))
        except IntegrityError:
            db.session.rollback()
            flash('Erro no base de dados.', 'danger')
    
    return render_template('home.html', title=title)


# Função que verifica se é do tipo imagem
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        confirmar_senha = request.form['confirmar-senha']
        
        try:
            if nome != '' and email != '' and senha != '':
                
                if request.files:
                    image = request.files['img-perfil']
                    
                    if image.filename != '':
                        
                        if not allowed_file(image.filename):
                            flash('O arquivo precisa ser imagem do tipo PNG, JPG, JPEG ou GIF','danger')
                            
                        image.save(os.path.join(IMAGE_UPLOADS, image.filename))
                        img_perfil = image.filename
                        
                        if confirmar_senha == senha:
                            conta = Users(nome, email, senha, img_perfil)
                            db.session.add(conta)
                            db.session.commit()
                            
                            flash('Sua conta foi criada com sucesso. Faça login!', 'success')
                        else:
                            flash('Suas senhas não coincidem, por favor crie sua senha e confirme-a.', 'danger')
            else:
                flash('Você precisa preencher todos os dados.', 'danger')
        except IntegrityError:
            db.session.rollback()
            flash('Usuário ou email já estão cadastrado, por favor use outros.', 'danger')
        
    return render_template('criar-conta.html', title=title)


# Desfazer login e retorna a page login
@bp_auth.route('/logout', methods=['GET'])
def logout():
    logout_user()    
    return redirect(url_for('bp_auth.index'))


@bp_auth.route('/perfil', methods=['GET', 'POST'])
def perfil():
    title = 'Perfil'
    
    user_id = current_user.id
    
    result = Users.query.filter_by(id=user_id)
    
    return render_template('perfil.html', title=title, result=result)


@bp_auth.route('/alterar-perfil', methods=['GET', 'POST'])
def alterar_perfil():
    user_id = current_user.id
    
    user = Users.query.filter_by(id=user_id).first()
    senha = request.form['senha']
    
    if user and not user.verify_password(senha):
        flash('Sua senha está incorreta, tente novamente.', 'danger')
        
        return redirect(url_for('bp_auth.perfil'))
    
    user.nome = request.form['nome']
    user.email = request.form['email']
    
    if request.files:
        image = request.files['img-perfil']
        
        if image.filename != '':
            
            if not allowed_file(image.filename):
                flash('O arquivo precisa ser imagem do tipo PNG, JPG, JPEG ou GIF','danger')
                
            image.save(os.path.join(IMAGE_UPLOADS, image.filename))
            img_perfil = image.filename
            
            user.img_perfil = img_perfil

    db.session.commit()
    
    flash('Perfil atualizado com sucesso', 'success')
    
    return redirect(url_for('bp_auth.perfil'))
    