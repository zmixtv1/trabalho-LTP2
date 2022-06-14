import bd
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
   banco = bd.SQL('root','uniceub','projeto_final')
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





app.run(debug=1)