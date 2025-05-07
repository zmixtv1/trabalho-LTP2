
import firebase_db as bd
from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    pizzas = bd.buscar_dados("tb_pizza") or {}
    dados = ""
    for id_pizza, pizza in pizzas.items():
        nme = pizza.get("nme_pizza", "")
        dsc = pizza.get("dsc_pizza", "")
        vlr = pizza.get("vlr_pizza", "")
        img = pizza.get("img_pizza", "")
        dados += f"""
                <h3>{nme}</h3>
                <div>
                    <img src="static/imgs/{img}" class="img_pz" width="140px" alt=""> <br>
                    <p>Pizza -  {id_pizza}</p>
                    <p>Descrição da Pizza:  {dsc}</p>
                    <p>Valor da Pizza:  {vlr}</p>
                </div>
                """
    return render_template('home.html', dados=dados)

@app.route('/encomendar', methods=['GET', 'POST'])
def encomendar():
    msg = ''
    valEmail = ''
    valPag = '1'
    pizzas = bd.buscar_dados("tb_pizza") or {}
    pagamentos = bd.buscar_dados("tb_pagamento") or {}

    encomenda = ""
    for idt, pizza in pizzas.items():
        nme = pizza.get("nme_pizza", "")
        vlr = pizza.get("vlr_pizza", "")
        encomenda += f"""
                    <div>
                        <input type="checkbox" id="{nme}" name="sabor_{idt}" value="{idt}">
                        <label for="{nme}">{nme} - (R$ {vlr})</label>
                    </div>
                    """

    cbPag = ""
    for idt, pag in pagamentos.items():
        nome_pag = pag.get("nme_pagamento", "")
        cbPag += f'<option value="{idt}">{nome_pag}</option>\n'

    if request.method == "POST":
        email = request.form['email']
        pessoa_existente = bd.buscar_dados("tb_pessoa") or {}

        existe_email = any(p.get("email_pessoa") == email for p in pessoa_existente.values())
        if not existe_email:
            msg = """
                     <div class="msg-e">
                        <p>Usuário não cadastrado<p>
                     </div>
                  """
            valEmail = email
            valPag = request.form['pagamento']
        else:
            pedidos = []
            for idt in pizzas:
                if f"sabor_{idt}" in request.form:
                    pedidos.append({
                        "cod_pizza": idt,
                        "cod_pessoa": email,
                        "cod_pagamento": request.form["pagamento"],
                        "num_nota_fiscal": random.randint(1, 1000000)
                    })

            for pedido in pedidos:
                bd.salvar_dado("tb_pedido", pedido)

            msg = """
                     <div class="msg-c">
                        <p>Pedido Realizado com Sucesso<p>
                     </div>
                  """

    return render_template("encomendar.html", encomenda=encomenda, cbPag=cbPag, msg=msg, valEmail=valEmail, valPag=valPag)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    cadastrar = ""
    msg = ''
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        endereco = request.form['endereco']

        pessoas = bd.buscar_dados("tb_pessoa") or {}
        existe = any(p.get("email_pessoa") == email for p in pessoas.values())

        if existe:
            msg = """
                     <div class="msg-e">
                        <p>Conta já cadastrada, tente outro e-mail!<p>
                     </div>
                  """
        else:
            nova = {
                "nme_pessoa": nome,
                "email_pessoa": email,
                "telefone_pessoa": telefone,
                "endereco_pessoa": endereco
            }
            bd.salvar_dado("tb_pessoa", nova)
            msg = """
                     <div class="msg-c">
                        <p>Cadastro realizado com sucesso!<p>
                     </div>
                  """

    return render_template('cadastrar.html', cadastrar=cadastrar, MSG=msg)

if __name__ == "__main__":
    app.run(debug=True)
