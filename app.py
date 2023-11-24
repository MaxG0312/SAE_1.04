from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

Saison = [
    {'saison':'Printemps'},
    {'saison':'Ete'},
    {'saison':'Automne'},
    {'saison':'Hiver'}
]


Culture = [
    {'id_culture': 1, 'libelle_culture': 'Tomates'},
    {'id_culture': 2, 'libelle_culture': 'Pommes'},
    {'id_culture': 3, 'libelle_culture': 'Poires'},
    {'id_culture': 4, 'libelle_culture': 'Maïs'},
    {'id_culture': 5, 'libelle_culture': 'Blé'},
    {'id_culture': 6, 'libelle_culture': 'Carottes'}
]


Variete = [
    {'id_variete':1, 'libelle_variete':'Carottes de Nantes', 'saison':'Ete', 'culture':6, 'prix_kg':1.5},
    {'id_variete':2, 'libelle_variete':'Tomates cerises', 'saison':'Ete', 'culture':1, 'prix_kg':5.67},
    {'id_variete':3, 'libelle_variete':'Pommes Gala', 'saison':'Hiver', 'culture':2, 'prix_kg':1.95},
    {'id_variete':4, 'libelle_variete':'Poires Williams', 'saison':'Ete', 'culture':3, 'prix_kg':3.99}
]

parcelle=[ {'id':1, 'surface':100.2,'adresse': '32 rue de la Joconde'},
{'id':1, 'surface':125.5,'adresse': '8 rue des noufats'},
{'id':1, 'surface':79.4,'adresse': '12 rue des frites'}]


collecte=[{ 'id':1,'quantite': 23.5,'produit': 'Carottes', 'date':'2023-09-27 18:21:00'},
{'id':2, 'quantite':17.5, 'produit':'Tomates', 'date':'2020-08-14 13:23:00'},
{'id':3, 'quantite':45.5, 'produit':'Pommes', 'date':'2020-10-02 15:38:00'}]
# (interface de serveur web python)
# comportements et méthodes d'un serveur web
app = Flask(__name__)    # instance de classe Flask (en paramètre le nom du module)
app.secret_key = 'caca'

def get_db():
    #mysql --user=jgenitri --password=1511 --host=serveurmysql --database=BDD_jgenitri
    if 'db' not in g:
        g.db = pymysql.connect(
            host="serveurmysql",                 # à modifier
            user="jgenitri",                     # à modifier
            password="1511",                # à modifier
            database="BDD_jgenitri",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    return render_template('layout.html')


@app.route('/')
def show_layout():
    return render_template('layout.html')

@app.route('/collecte/show')
def show_collecte():
    return render_template('collecte/show_collecte.html', collecte=collecte, parcelle=parcelle)

@app.route('/collecte/add', methods=['GET'])
def add_collecte():
    return render_template('collecte/add_collecte.html', collecte=collecte, parcelle=parcelle)

@app.route('/collecte/add', methods=['POST'])
def valid_add_collecte():
    parcelle_id = request.form.get('parcelle_id', '')
    quantite = request.form.get('quantite', '')
    produit = request.form.get('produit', '')
    date = request.form.get('date', '')
    print(u'Nouvelle collecte , quantite : ', quantite, ' | produit : ', produit, ' | date : ', date, '| parcelle_id : ' , parcelle_id)
    message = u'Nouvelle collecte , quantite : '+quantite + ' | produit : ' + produit + ' | date : ' + date+ '| parcelle_id : '+ parcelle_id
    flash(message, 'alert-success')
    return redirect('/collecte/show')

@app.route('/collecte/delete', methods=['GET'])
def delete_collecte():
    id = request.args.get('id', '')
    print ("une collecte supprimée, id : ",id)
    message=u'une collecte supprimée, id : ' + id
    flash(message, 'alert-warning')
    return redirect('/collecte/show')

@app.route('/collecte/edit', methods=['GET'])
def edit_collecte():
    id = request.args.get('id', '')
    id=int(id)
    return render_template('collecte/edit_collecte.html', collecte=collecte, parcelle=parcelle)

@app.route('/collecte/edit', methods=['POST'])
def valid_edit_collecte():
    id = request.form.get('id', '')
    quantite = request.form.get('quantite', '')
    produit = request.form.get('produit', '')
    date = request.form.get('date', '')
    parcelle_id = request.form.get('parcelle_id')
    print(u'Une collecte modifiée, quantite : ', quantite, ' | produit : ', produit, ' | date : ', date, '| parcelle_id : ', parcelle_id)
    message = u'Une collecte modifiée, quantite : '+ quantite+ ' | produit : '+ produit+ ' | date : '+ date+ '| parcelle_id : '+ parcelle_id
    flash(message, 'alert-success')
    return redirect('/collecte/show')



if __name__ == '__main__':
    app.run(debug=True, port=5000)
