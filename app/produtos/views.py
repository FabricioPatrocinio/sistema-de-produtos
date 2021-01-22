from flask import render_template, url_for, flash, request, redirect, session
from flask_login import login_user, logout_user, login_required, current_user
from app.model import Produtos, Referencia, Fabricante, Tipo
from random import sample
# Tentar entender o porque precisei chamar essse db
from app.model import db
from . import bp_produtos
# Usar o serializer pro banco se comunicar com json e usar json pra salvar dados
# from app.serealizer import ProdutosSchema, UsersSchema


@bp_produtos.route('/sistema-produtos')
def sistema_produtos():
    title = 'Sistema de produtos'
    
    user_id = current_user.id
    
    # Gera a lista de categorias do <select> no HTML 
    ref = Referencia.query.filter_by(user_id=user_id).all()
    fab = Fabricante.query.filter_by(user_id=user_id).all()
    tip = Tipo.query.filter_by(user_id=user_id).all()
    
    return render_template('sistema-produtos.html', title=title, ref=ref, fab=fab, tip=tip)


@bp_produtos.route('/sistema-produtos/filtro/<int:id>', methods=['GET', 'POST'])
def sistema_produtos_filtro(id):
    title = 'Sistema de produtos'
    
    user_id = current_user.id
    
    # Gera a lista de categorias do <select> no HTML 
    ref = Referencia.query.filter_by(user_id=user_id).all()
    fab = Fabricante.query.filter_by(user_id=user_id).all()
    tip = Tipo.query.filter_by(user_id=user_id).all()
    
    result = Produtos.query.filter(Produtos.referencia==id).all()
    
    return render_template('sistema-produtos.html', title=title, result=result, ref=ref, fab=fab, tip=tip, id=id)


@bp_produtos.route('/adicionar-produtos', methods=['GET', 'POST'])
def adicionar_produtos():
    title = 'Adicionar produtos'
    
    user_id = current_user.id
    
    # Gera a lista de categorias do <select> no HTML 
    ref = Referencia.query.filter_by(user_id=user_id).all()
    fab = Fabricante.query.filter_by(user_id=user_id).all()
    tip = Tipo.query.filter_by(user_id=user_id).all()   
    
    if request.method == 'POST' and request.form['cod'] != '' and request.form['referencia'] != '' and request.form['descricao'] != '' and request.form['tipo'] != '':
        user_id = request.form['user']
        cod = request.form['cod']
        descricao = request.form['descricao']
        complemento = request.form['complemento']
        referencia = request.form['referencia']
        fabricante = request.form['fabricante']
        tipo = request.form['tipo']
        quant = request.form['quant']
        custo = request.form['custo']
        preco = request.form['preco']
        
        produtos = Produtos(user_id, cod, descricao, complemento, referencia, fabricante, tipo, quant, custo, preco)
        
        db.session.add(produtos)
        db.session.commit()
        
        flash('Produto adicionado com sucesso', 'success')
    else:
        if request.method == 'POST':
            flash('Erro ao adicionar produtos, por favor insira todos os dados corretamente.', 'danger')
    
    return render_template('adicionar-produtos.html', title=title, ref=ref, fab=fab, tip=tip)


@bp_produtos.route('/deletar/produto/<int:id>', methods=['GET', 'POST'])
def deletar(id):    
    result = Produtos.query.filter_by(id=id).first()
    
    db.session.delete(result)
    db.session.commit()
    
    flash('Produto deletado com sucesso', 'success')
    
    return redirect(url_for('bp_produtos.sistema_produtos'))


@bp_produtos.route('/alterar/produto/<int:id>', methods=['GET', 'POST'])
def alterar(id):    
    result = Produtos.query.filter_by(id=id).first()
    
    result.cod = request.form['cod']
    result.descricao = request.form['descricao']
    result.complemento = request.form['complemento']
    result.referencia = request.form['referencia']
    result.fabricante = request.form['fabricante']
    result.tipo = request.form['tipo']
    result.quant = request.form['quant']
    result.custo = request.form['custo']
    result.preco = request.form['preco']
    
    db.session.commit()
    
    flash('Produto alterado com sucesso', 'success')
    
    return redirect(url_for('bp_produtos.sistema_produtos'))


@bp_produtos.route('/produtos-em-falta', methods=['GET', 'POST'])
def produtos_em_falta():
    title = 'Produtos em falta'
    # Pega produtos com quantidade igual a ZERO
    result = Produtos.query.filter(db.or_((Produtos.quant <= 2))).all()
    
    return render_template('produtos-em-falta.html', title=title, result=result)


@bp_produtos.route('/adicionar-categorias', methods=['GET', 'POST'])
def adicionar_categorias():
    
    if request.method == 'POST' and request.form['referencia'] != '':
        referencia = request.form['referencia']
        user_id = request.form['user']
        
        ref = Referencia(referencia, user_id)
        
        db.session.add(ref)
        db.session.commit()
        flash('Categoria(s) adicionada(s) com sucesso!', 'success')

    elif request.method == 'POST' and request.form['fabricante'] != '':
        fabricante = request.form['fabricante']
        user_id = request.form['user']
        
        fab = Fabricante(fabricante, user_id)
        
        db.session.add(fab)
        db.session.commit()
        flash('Categoria(s) adicionada(s) com sucesso!', 'success')

    elif request.method == 'POST' and request.form['tipo'] != '':
        tipo = request.form['tipo']
        user_id = request.form['user']
        
        tip = Tipo(tipo, user_id)
        
        db.session.add(tip)
        db.session.commit()
        flash('Categoria(s) adicionada(s) com sucesso!', 'success')
    
    else:
        if request.method == 'POST':
            flash('Erro ao adicionar categorias', 'danger')

    return redirect(url_for('bp_produtos.adicionar_produtos'))


@bp_produtos.route('/editar-categorias/', methods=['GET', 'POST'])
def editar_categorias():
    title = 'Editar categorias'
    
    user_id = current_user.id
    
    # Gera a lista de categorias do <select> no HTML 
    db_ref = Referencia.query.filter_by(user_id=user_id).all()
    db_fab = Fabricante.query.filter_by(user_id=user_id).all()
    db_tip = Tipo.query.filter_by(user_id=user_id).all()
    
    return render_template('editar-categorias.html', title=title, db_ref=db_ref, db_fab=db_fab, db_tip=db_tip)

@bp_produtos.route('/deletar-categoria/<categoria>/<int:id>', methods=['GET', 'POST'])
def deletar_categoria(categoria, id):
    cat_nome = ''
    
    if categoria == 'Referencia':
        db_ref = Referencia.query.filter_by(id=id).first()
    
        db.session.delete(db_ref)
        db.session.commit()
        cat_nome = 'Referencia'
    
    if categoria == 'Fabricante':
        db_fab = Fabricante.query.filter_by(id=id).first()
    
        db.session.delete(db_fab)
        db.session.commit()
        cat_nome = 'Fabricante'
    
    if categoria == 'Tipo':
        db_tip = Tipo.query.filter_by(id=id).first()
    
        db.session.delete(db_tip)
        db.session.commit()
        cat_nome = 'Tipo'
    
    flash(cat_nome + ' deletado com sucesso', 'success')
    
    return redirect(url_for('bp_produtos.editar_categorias'))


@bp_produtos.route('/alterar/<categoria>/<int:id>', methods=['GET', 'POST'])
def alterar_categoria(categoria, id):
    nome_cat = ''
    
    if categoria == 'Referencia':
        db_ref = Referencia.query.filter_by(id=id).first()
        db_ref.nome = request.form['referencia']
        
        db.session.commit()
        nome_cat = 'Referencia'
    
    if categoria == 'Fabricante':
        db_fab = Fabricante.query.filter_by(id=id).first()
        db_fab.nome = request.form['fabricante']
        
        db.session.commit()
        nome_cat = 'Fabricante'
    
    if categoria == 'Tipo':
        db_tip = Tipo.query.filter_by(id=id).first()
        db_tip.nome = request.form['tipo']
        
        db.session.commit()
        nome_cat = 'Tipo'
    
    flash('Categoria '+ nome_cat + ' alterada com sucesso!', 'success')
    
    return redirect(url_for('bp_produtos.editar_categorias'))
