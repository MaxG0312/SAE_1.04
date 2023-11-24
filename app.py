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


if __name__ == '__main__':
    app.run(debug=True, port=5000)