from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

# (interface de serveur web python)
# comportements et méthodes d'un serveur web
app = Flask(__name__)    # instance de classe Flask (en paramètre le nom du module)
app.secret_key = ''

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
def show_layout():
    return render_template('layout.html')
    
@app.route('/variete/show')
def show_variete():
    mycursor = get_db().cursor()
    sql = '''
    SELECT variete.id_variete AS id,
    variete.libelle_variete AS nom,
    variete.saison AS saison,
    culture.libelle_culture AS type_culture,
    variete.prix_kg AS prix,
    variete.stock AS stock
    FROM variete, culture
    WHERE culture.id_culture = variete.culture;
    '''
    mycursor.execute(sql)
    variete = mycursor.fetchall()
    print(variete)
    return render_template('variete/show_variete.html', variete=variete)


@app.route('/variete/add', methods=['GET'])
def add_variete():
    mycursor = get_db().cursor()
    sql='''
    SELECT culture.id_culture AS id_culture, culture.libelle_culture AS nom FROM culture;
    '''
    mycursor.execute(sql)
    culture = mycursor.fetchall()
    sql = '''
    SELECT saison.saison AS saison FROM saison;
    '''
    mycursor.execute(sql)
    saison = mycursor.fetchall()
    return render_template('variete/add_variete.html', culture=culture, saison=saison)


@app.route('/variete/add', methods=['POST'])
def valid_add_variete():
    mycursor = get_db().cursor()

    libelle_variete = request.form.get('libelle_variete', '')
    saison = request.form.get('saison', '')
    culture = request.form.get('culture', '')
    prix_kg = request.form.get('prix_kg', '')
    stock = request.form.get('stock', '')
    tuple_insert = (libelle_variete, saison, culture, prix_kg, stock)

    sql = '''
    INSERT INTO variete(libelle_variete, saison, culture, prix_kg, stock)
    VALUES (%s, %s, %s, %s, %s);
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    message = u'Nouvelle variété , nom : '+libelle_variete + ' | saison : ' + saison + \
              ' | culture : ' + culture+ '| prix/kg : '+ prix_kg + ' | stock : ' + stock
    flash(message, 'alert-success')
    return redirect('/variete/show')


@app.route('/variete/delete', methods=['GET'])
def delete_variete():
    mycursor = get_db().cursor()
    id_variete = request.args.get('id', '')
    tuple_delete = (id_variete)
    sql = '''
    DELETE FROM variete WHERE id_variete = %s;
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'une variété supprimée, id : ' + id_variete
    flash(message, 'alert-warning')
    return redirect('/variete/show')


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
