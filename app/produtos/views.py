from flask import render_template, url_for, flash, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app.model import Produtos, Users, Referencia, Fabricante, Tipo
# Tentar entender o porque precisei chamar essse db
from app.model import db
from . import bp_produtos
# Usar o serializer pro banco se comunicar com json e usar json pra salvar dados
# from app.serealizer import ProdutosSchema, UsersSchema

# Index como login
@bp_produtos.route('/', methods=['GET', 'POST'])
def index():
    title = 'Login'
    erro = ''
    
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        
        user = Users.query.filter_by(nome=nome).first()
        
        if not user or not user.verify_password(senha):
            if not user:
                flash('Seu nome de usuário não existe ou está incorreto.')
            
            if user and not user.verify_password(senha):
                flash('Sua senha está incorreta.')
            
            return redirect(url_for('bp_produtos.index'))
        
        login_user(user)
        return  redirect(url_for('bp_produtos.sistema_produtos'))
    
    return render_template('home.html', title=title)


@bp_produtos.route('/criar-conta', methods=['GET', 'POST'])
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
            
            flash('Sua conta foi criada com sucesso!', 'sucess')
        else:
            flash('Você precisa preencher todos os dados.', 'error')
            
    return render_template('criar-conta.html', title=title)


# Desfazer login e retorna a page login
@bp_produtos.route('/logout', methods=['GET'])
def logout():
    logout_user()    
    return redirect(url_for('bp_produtos.index'))


@bp_produtos.route('/admin/')
def admin():
    return '<h1>Admin</h1>'


@bp_produtos.route('/sistema-produtos', methods=['GET', 'POST'])
def sistema_produtos():
    title = 'Sistema de produtos'
    result = Produtos.query.all()
    
    return render_template('sistema-produtos.html', title=title, result=result)


@bp_produtos.route('/adicionar-produtos', methods=['GET', 'POST'])
def adicionar_produtos():
    title = 'Adicionar produtos'
    erro = ''
    msg = ''
    
    # Isso gera a lista de categorias do <select> no HTML    
    ref = Referencia.query.all()
    fab = Fabricante.query.all()
    tip = Tipo.query.all()
    
    
    if request.method == 'POST':
        cod = request.form['cod']
        referencia = request.form['referencia']
        descricao = request.form['descricao']
        complemento = request.form['complemento']
        fabricante = request.form['fabricante']
        tipo = request.form['tipo']
        quant = request.form['quant']
        custo = request.form['custo']
        preco = request.form['preco']
        
        produtos = Produtos(cod, referencia, descricao, complemento, fabricante, tipo, quant, custo, preco)
        
        db.session.add(produtos)
        db.session.commit()
        
        msg = 'Produto adicionado com sucesso'
    else:
        if request.method == 'POST':
            erro = 'Erro ao adicionar produtos, por favor insira todos os dados corretamente.'
    
    return render_template('adicionar-produtos.html', title=title, msg=msg, erro=erro, ref=ref, fab=fab, tip=tip)


@bp_produtos.route('/adicionar-categorias', methods=['GET', 'POST'])
def adicionar_categorias():
    title = 'Adicionar categorias'
    erro = ''
    msg = ('')
    
    if request.method == 'POST' and request.form['referencia'] != '':
        referencia = request.form['referencia']
        ref = Referencia(referencia)
        
        db.session.add(ref)
        db.session.commit()
        msg = 'Categoria(s) adicionada(s) com sucesso!'

    if request.method == 'POST' and request.form['fabricante'] != '':
        fabricante = request.form['fabricante']
        fab = Fabricante(fabricante)
        
        db.session.add(fab)
        db.session.commit()
        msg = 'Categoria(s) adicionada(s) com sucesso!'

    if request.method == 'POST' and request.form['tipo'] != '':
        tipo = request.form['tipo']
        tip = Tipo(tipo)
        
        db.session.add(tip)
        db.session.commit()
        msg = 'Categoria(s) adicionada(s) com sucesso!'

    return render_template('adicionar-categorias.html', title=title, erro=erro, msg=msg)


@bp_produtos.route('/produtos-em-falta', methods=['GET', 'POST'])
def produtos_em_falta():
    title = 'Produtos em falta'
    
    # Pega produtos com quantidade igual a ZERO
    result = Produtos.query.filter(db.or_((Produtos.quant <= 2))).all()
    
    return render_template('produtos-em-falta.html', title=title, result=result)
