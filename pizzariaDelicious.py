import bd
from flask import Flask, render_template, request
import random


app = Flask(__name__)


@app.route('/')
def index():
    banco = bd.SQL('root','Teste','projeto_final')
    comando = "SELECT * FROM tb_pizza;"
    cs = banco.consultar(comando, [])
    dados = ""
    for (idt, nme, dsc, vlr, img) in cs:
        dados += '''
                    <h3>{}</h3>
                    <div>
                        <img src="static/imgs/{}" class="img_pz" width="140px"alt=""> <br>
                        <p>Pizza -  {}</p>
                        <p>Descrição da Pizza:  {}</p>
                        <p>Valor da Pizza:  {}</p>
                    </div>
                 '''.format(nme, img, idt, dsc, vlr)
    return render_template('home.html', dados = dados)


@app.route('/encomendar',  methods=['GET', 'POST'])
def encomendar():
    banco = bd.SQL('root', 'Teste', 'projeto_final')
    msg = ''
    valEmail = ''
    valPag = '1'
    comando = "SELECT id_pizza, nme_pizza,vlr_pizza FROM tb_pizza;"
    cs = banco.consultar(comando, [])
    encomenda = ""
    for (idt, nme, vlr) in cs:
        encomenda += '''
                       <div>
                           <input type="checkbox" id="{}" name="sabor_{}" value="{}" >
                           <label for="{}">{} - (R$ {})</label>
                       </div>
                    '''.format(nme, idt, idt, nme, nme, vlr)
        encomenda = encomenda.replace("(", "").replace(")", "").replace("'", "").replace(",","")

    cmdPag = "SELECT * FROM tb_pagamento"
    csPag = banco.consultar(cmdPag, [])
    cbPag = ""
    for (idt, nme) in csPag:
        cbPag += '<option value="{}">{}</option>\n'.format(idt, nme)

    if request.method == "POST":
        comando = "INSERT INTO tb_pedido (cod_pizza, cod_pessoa, cod_pagamento, num_nota_fiscal) VALUES (%s, %s, %s, %s);"

        cmdTeste = "SELECT COUNT(id_pessoa) as qtd FROM tb_pessoa WHERE email_pessoa = %s;"
        if banco.consultar(cmdTeste, [request.form['email']]).fetchone()[0] == 0:
            msg = '''
                        <div class="msg-e">
                           <p>Usuario não cadastrado<p>
                        </div>
                  '''
            valEmail = request.form['email']
            valPag = request.form['pagamento']
        else:
            cmdEmail = "SELECT id_pessoa FROM tb_pessoa WHERE email_pessoa = %s;"
            idPessoa = banco.consultar(cmdEmail, [request.form['email']]).fetchone()[0]

            nf = random.randrange(1, 1000000)
            print(nf, idPessoa, request.form['pagamento'])

            for val in request.form:
                if val[0:5] == 'sabor':
                    print(val)
                    banco.executar(comando, [request.form[val], idPessoa, request.form['pagamento'], nf])

            # cs = banco.consultar(comando, [])
            msg = '''
                        <div class="msg-c">
                           <p>Pedido Realizado com Sucesso<p>
                        </div>
                  '''

    return render_template('encomendar.html', encomenda=encomenda, cbPag=cbPag, MSG=msg, valEmail=valEmail)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    banco = bd.SQL('root', 'Teste', 'projeto_final')
    cadastrar = ""
    msg = ''
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']
        cmdTeste = "SELECT COUNT(id_pessoa) as qtd FROM tb_pessoa WHERE email_pessoa = %s;"

        if banco.consultar(cmdTeste, [request.form['email']]).fetchone()[0] == 1:
            msg = '''
                     <div class="msg-e">
                        <p>Conta ja cadastrada, tente outro e-mail!<p>
                     </div>
                  '''
        else:
            comando = "INSERT INTO tb_pessoa (nm_pessoa, email_pessoa, telefone_pessoa, endereco_pessoa) VALUES (%s, %s, %s, %s);"
            banco.executar(comando, [nome, email, telefone, endereco])

            msg = '''
                     <div class="msg-c">
                        <p>Cadastro realizado com sucesso!<p>
                     </div>
                  '''

    return render_template('cadastrar.html', cadastrar=cadastrar, MSG=msg)


app.run(debug=1)
