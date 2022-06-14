import bd
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def index():
   banco = bd.SQL('root','','projeto_final')
   comando = "SELECT idt_pizza,nme_pizza,dsc_pizza,vlr_pizza FROM tb_pizza;"
   cs = banco.consultar(comando, [])
   dados = ""
   for (idt, nme, dsc, vlr) in cs:
       dados += '''
                   <h3>{}</h3>
                   <div>
                       <p>IDT Pizza: {}</p>
                       <p>Descreição da Pizza: {}</p>
                       <p>valor da Pizza: {}</p>
                   </div>
                '''.format(nme, idt, dsc, vlr)
   return render_template('home.html', dados = dados)





app.run(debug=1)