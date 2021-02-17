from flask import render_template, url_for, flash, request, redirect
from sqlalchemy import exc
from . import bp_financeiro
from operator import length_hint
from flask_login import login_user, logout_user, login_required, current_user
from app.model import db
from app.model import Users, Contas, Fiado
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from datetime import date


@bp_financeiro.route('/contas-a-pagar/', methods=['GET', 'POST'])
def contas_a_pagar():
    title = 'Contas a pagar'
    hoje = date.today().strftime('%Y-%m-%d')
    
    user_id = current_user.id
    user = Users.query.filter_by(id=user_id).first()

    contas = Contas.query.filter(func.DATE(Contas.data_conta) == hoje).filter_by(user_id=user.id)
    
    if request.method == 'POST' and request.form['devedor'] != '' and request.form['data_conta'] != '' and request.form['valor'] != '':
        user_id = request.form['user']
        devedor = request.form['devedor'] 
        complemento = request.form['complemento']
        data_conta = request.form['data_conta']
        valor = request.form['valor']
        situacao = int(request.form['situacao'])
        
        try:
            conta = Contas(user_id, devedor, complemento, data_conta, valor, situacao)
            
            db.session.add(conta)
            db.session.commit()
            
            flash('Conta adicionada com sucesso', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Ocorreu algum erro ao adicionar sua conta, por favor tente novamente.')
    else:
        if request.method == 'POST':
            flash('Erro ao adicionar conta, por favor insira todos os dados corretamente.', 'danger')
    
    return render_template('contas-a-pagar.html', title=title, contas=contas, user=user, hoje=hoje)


@bp_financeiro.route('/contas-a-pagar/filtrar/', methods=['GET', 'POST'])
def contas_filtrar():
    title = 'Contas a pagar filtrar'
    hoje = date.today().strftime('%Y-%m-%d')
    
    user_id = current_user.id
    user = Users.query.filter_by(id=user_id).first()
    
    if request.method == 'POST' and request.form['data_filtro'] != '':
        data_filtro = request.form['data_filtro']
        contas = Contas.query.filter(func.DATE(Contas.data_conta) == data_filtro).filter_by(user_id=user.id)
    
    return render_template('contas-a-pagar.html', title=title, contas=contas, user=user, hoje=hoje)


@bp_financeiro.route('/contas/situacao/<int:id_conta>/<int:situacao>', methods=['GET', 'POST'])
def contas_situacao(id_conta, situacao):
    
    result = Contas.query.filter_by(id=id_conta).first()
    
    result.situacao = situacao
    db.session.commit()
    
    return redirect(url_for('bp_financeiro.contas_a_pagar'))


@bp_financeiro.route('/contas-a-receber', methods=['GET', 'POST'])
def contas_a_receber():
    title = 'Contas a receber'
    
    user_id = current_user.id
    user = Users.query.filter_by(id=user_id).first()
    
    fiado = Fiado.query.filter_by(user_id=user_id).all()
