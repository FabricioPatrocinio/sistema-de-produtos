# Sistema de produtos
Link: http://fabriciopatrocinio.pythonanywhere.com/
Criado por mim mesmo **Fabricio Patrocinio**
Usando Python com Flask

## Ideia
Bem a idéia consiste em um sistema de cadastro de produtos com uma interface fácil de usar e totalmente funcional. Que possa ser usado em diferentes areas de trabalho. Estou fazendo atrelado aos estudos de **python** com **flask**, então o processo vai ser lento.

## Dependências usadas
As dependências que usei se encontram no **_requirements.txt_**.
Para instalar use o comando:
```
pip install -r requirements.txt
```

## Banco de dados
No banco de dados estou usando SQLAlchemy com Migrate. E todos os dados do banco se encotra na pasta _migrations_.
Crie um banco de dados com nome **sys_pro** e rode no terminal esse comando:
```
flask db upgrade
```
Caso não consiga criar o banco de dados, apague a pasta migrations e use:
```
flask db init
flask db migrate
```
Feito isso ele irá criar todas as tabelas no seu banco.

## Rodar o projeto
Dentro da pasta raiz rode esse comando:
```
flask run (Para rodar o servidor)
```

## Rotas ou endpoints
Estou usando o Blueprint para criar os endpoints.
Para ver todas as rotas rode o comando:
```
flask routes
```
Aqui estão alguns dos principais:
- [x] /criar-conta
- [x] /login (index)
- [x] /logout
- [x] /sistema-de-produtos
- [x] /adicionar-produtos
- [x] /alterar/produto/<id>
- [x] /deletar/produto/<id>
- [x] /adicionar-categorias
- [x] /editar/categorias/
- [x] /alterar/<categoria>/<id>
- [x] /deletar-categoria/<categoria>/<id>
- [x] /produtos-em-falta
- [x] /sistema-produtos/filtro/<filtro>
- [x] /buscar
- [ ] Brevemente mais

### Erros a resolver (pessoal)
Estou usando isso para lista os erros que pretedo lidar mais na frente

### Alterar cores bootstrap 4 usando SASS (pessoal)
Comando:
```
sass app/static/css/style.scss app/static/css/style.css (normal) 
node-sass --watch app/static/css/style.scss app/static/css/style.css --output-style compressed (compreessado) 
``` 
Cores pra usar
80ffdb
72efdd
64dfdf
56cfe1
48bfe3
4ea8de
5390d9
5e60ce
6930c3
7400b8
