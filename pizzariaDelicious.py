import bd
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
   banco = bd.SQL('root','','projeto_final')
   comando = "SELECT * FROM tb_pizza;"
   cs = banco.consultar(comando, [])
   dados = ""
   for (idt, nme, dsc, vlr, img) in cs:
       dados += '''
                   <h3>{}</h3>
                   <div>
                       <img src="{}" width="140px"alt=""> <br>
                       <p>IDT Pizza: {}</p>
                       <p>Descreição da Pizza: {}</p>
                       <p>valor da Pizza: {}</p>
                   </div>
                '''.format(nme, img, idt, dsc, vlr)
   return render_template('home.html', dados = dados)


@app.route('/encomendar')
def encomendar():
   banco = bd.SQL('root', '', 'projeto_final')
   comando = "SELECT nme_pizza FROM tb_pizza;"
   cs = banco.consultar(comando, [])
   encomenda = ""
   for (nme) in cs:
      encomenda += '''
                      <div>
                          <input type="checkbox" id="{}" name="sabor" value="{}" >
                          <label for="{}">{}</label>
                      </div>
                   '''.format(nme, nme, nme, nme)
      encomenda = encomenda.replace("(", "").replace(")", "").replace("'", "").replace(",","")
   return render_template('encomendar.html', encomenda=encomenda)



@app.route('/cadastrar')
def cadastrar():
   return render_template('cadastrar.html', cadastrar=cadastrar)

app.run(debug=1)