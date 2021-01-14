from flask import render_template, url_for, flash, request, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app.model import Produtos, Referencia, Fabricante, Tipo
# Tentar entender o porque precisei chamar essse db
from app.model import db
from . import bp_produtos
# Usar o serializer pro banco se comunicar com json e usar json pra salvar dados
# from app.serealizer import ProdutosSchema, UsersSchema


@bp_produtos.route('/sistema-produtos')
def sistema_produtos():
    title = 'Sistema de produtos'
    
    # Gera a lista de categorias do <select> no HTML    
    ref = Referencia.query.all()
    fab = Fabricante.query.all()
    tip = Tipo.query.all()
    
    return render_template('sistema-produtos.html', title=title, ref=ref, fab=fab, tip=tip)


@bp_produtos.route('/sistema-produtos/filtro/<filtro>', methods=['GET', 'POST'])
def sistema_produtos_filtro(filtro):
    title = 'Sistema de produtos'
    
    # Gera a lista de categorias do <select> no HTML    
    ref = Referencia.query.all()
    fab = Fabricante.query.all()
    tip = Tipo.query.all()
    
    result = Produtos.query.filter(Produtos.referencia==filtro).all()
    
    return render_template('sistema-produtos.html', title=title, result=result, ref=ref, fab=fab, tip=tip, filtro=filtro)


@bp_produtos.route('/adicionar-produtos', methods=['GET', 'POST'])
def adicionar_produtos():
    title = 'Adicionar produtos'
    
    # Gera a lista de categorias do <select> no HTML    
    ref = Referencia.query.all()
    fab = Fabricante.query.all()
    tip = Tipo.query.all()
    
    
    if request.method == 'POST' and request.form['cod'] != '' and request.form['referencia'] != '' and request.form['descricao'] != '' and request.form['tipo'] != '':
        cod = request.form['cod']
        descricao = request.form['descricao']
        complemento = request.form['complemento']
        referencia = request.form['referencia']
        fabricante = request.form['fabricante']
        tipo = request.form['tipo']
        quant = request.form['quant']
        custo = request.form['custo']
        preco = request.form['preco']
        
        produtos = Produtos(cod, descricao, complemento, referencia, fabricante, tipo, quant, custo, preco)
        
        db.session.add(produtos)
        db.session.commit()
        
        flash('Produto adicionado com sucesso', 'success')
    else:
        if request.method == 'POST':
            flash('Erro ao adicionar produtos, por favor insira todos os dados corretamente.', 'danger')
    
    return render_template('adicionar-produtos.html', title=title, ref=ref, fab=fab, tip=tip)


@bp_produtos.route('/deletar/produto/<int:id>', methods=['GET', 'POST'])
def deletar(id):
    title = 'Delete'
    
    result = Produtos.query.filter_by(id=id).first()
    
    db.session.delete(result)
    db.session.commit()
    
    flash('Produto deletado com sucesso', 'success')
    
    return redirect(url_for('bp_produtos.sistema_produtos'))


@bp_produtos.route('/alterar/produto/<int:id>', methods=['GET', 'POST'])
def alterar(id):
    title = 'Alterar'
    
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


@bp_produtos.route('/adicionar-categorias', methods=['GET', 'POST'])
def adicionar_categorias():
    # title = 'Adicionar categorias'
    
    if request.method == 'POST' and request.form['referencia'] != '':
        referencia = request.form['referencia']
        ref = Referencia(referencia)
        
        db.session.add(ref)
        db.session.commit()
        flash('Categoria(s) adicionada(s) com sucesso!', 'success')

    elif request.method == 'POST' and request.form['fabricante'] != '':
        fabricante = request.form['fabricante']
        fab = Fabricante(fabricante)
        
        db.session.add(fab)
        db.session.commit()
        flash('Categoria(s) adicionada(s) com sucesso!', 'success')

    elif request.method == 'POST' and request.form['tipo'] != '':
        tipo = request.form['tipo']
        tip = Tipo(tipo)
        
        db.session.add(tip)
        db.session.commit()
        flash('Categoria(s) adicionada(s) com sucesso!', 'success')
    
    else:
        if request.method == 'POST':
            flash('Erro ao adicionar categorias', 'danger')

    return redirect(url_for('bp_produtos.adicionar_produtos'))


@bp_produtos.route('/produtos-em-falta', methods=['GET', 'POST'])
def produtos_em_falta():
    title = 'Produtos em falta'
    # Pega produtos com quantidade igual a ZERO
    result = Produtos.query.filter(db.or_((Produtos.quant <= 2))).all()
    
    return render_template('produtos-em-falta.html', title=title, result=result)
