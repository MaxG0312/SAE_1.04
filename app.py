from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

import pymysql.cursors

# (interface de serveur web python)
# comportements et méthodes d'un serveur web
app = Flask(__name__)    # instance de classe Flask (en paramètre le nom du module)
app.secret_key = 'secreeet'

def get_db():
    #mysql --user=jgenitri --password=1511 --host=serveurmysql --database=BDD_jgenitri
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",                 # à modifier
            user="jbfroehl",                     # à modifier
            password="motdepassehehe",                # à modifier
            database="BDD_jbfroehl",        # à modifier
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

@app.route('/ticket/show')
def show_ticket():
    mycursor = get_db().cursor()
    sql = '''
    SELECT ticket_incident.id_ticket AS id,
    ticket_incident.description_incident AS description,
    ticket_incident.date_incident AS date,
    ticket_incident.statut_incident AS statut,
    ticket_incident.parcelle_concernee AS parcelle,
    parcelle.adresse AS adresse FROM ticket_incident LEFT JOIN parcelle ON parcelle.id_parcelle = ticket_incident.parcelle_concernee;
    '''
    mycursor.execute(sql)
    ticket_incident = mycursor.fetchall()

    return render_template('tickets/show_ticket.html', ticket_incident=ticket_incident)

@app.route('/ticket/add', methods=['GET'])
def add_ticket():
    mycursor = get_db().cursor()
    sql='''
    SELECT ticket_incident.id_ticket AS id FROM ticket_incident;
    '''
    mycursor.execute(sql)
    ticket = mycursor.fetchall()
    sql = '''
    SELECT parcelle.id_parcelle AS id, parcelle.adresse AS adresse FROM parcelle;
    '''
    mycursor.execute(sql)
    parcelle = mycursor.fetchall()
    return render_template('tickets/add_ticket.html', ticket=ticket, parcelle=parcelle)

@app.route('/ticket/add', methods=['POST'])
def valid_add_ticket():
    mycursor = get_db().cursor()

    description_ticket = request.form.get('description_ticket', '')
    date = request.form.get('date', '')
    statut_incident = request.form.get('statut', '')
    parcelle_concernee = request.form.get('parcelle', '')
    tuple_insert = (description_ticket, date, statut_incident, parcelle_concernee)
    sql = '''
    INSERT INTO ticket_incident(description_incident, date_incident, statut_incident, parcelle_concernee)
    VALUES (%s, %s, %s, %s);
    '''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()

    message = u'Nouveau ticket , description : '+description_ticket + ' | date : ' + date + \
                ' | statut : ' + statut_incident+ '| parcelle_concernee : '+ parcelle_concernee
    flash(message, 'alert-success')

    return redirect('/ticket/show')

@app.route('/ticket/delete', methods=['GET'])
def delete_ticket():
    mycursor = get_db().cursor()
    id_ticket = request.args.get('id', '')
    tuple_delete = (id_ticket)
    sql = '''
    DELETE FROM ticket_incident WHERE id_ticket = %s;
    '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    message=u'Un ticket supprimé ! id : ' + id_ticket
    flash(message, 'alert-warning')
    return redirect('/ticket/show')

@app.route('/ticket/edit', methods=['GET'])
def edit_ticket():
    mycursor = get_db().cursor()

    id = request.args.get('id', '')
    sql = '''
        SELECT ticket_incident.id_ticket AS id,
        ticket_incident.description_incident AS description,
        ticket_incident.date_incident AS date,
        ticket_incident.statut_incident AS statut,
        ticket_incident.parcelle_concernee AS parcelle FROM ticket_incident WHERE ticket_incident.id_ticket=%s;
        '''
    mycursor.execute(sql, (id))

    ticket = mycursor.fetchone()
    sql = '''
        SELECT parcelle.id_parcelle AS id, parcelle.adresse AS adresse FROM parcelle;
        '''
    mycursor.execute(sql)
    parcelle = mycursor.fetchall()
    
    return render_template('tickets/edit_ticket.html', ticket=ticket, parcelle=parcelle)

@app.route('/ticket/edit', methods=['POST'])
def valid_edit_ticket():
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    description = request.form.get('description', '')
    date_incident = request.form.get('date_incident', '')
    statut = request.form.get('statut', '')
    parcelle = request.form.get('parcelle_id', '')
    parcelle_adresse = request.form.get('parcelle_adresse', '')
    tuple_update = (description, date_incident, statut, parcelle, id)
    sql = '''
    UPDATE ticket_incident SET description_incident = %s, date_incident = %s, statut_incident = %s,
        parcelle_concernee = %s WHERE id_ticket = %s;'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()

    message = u'Un ticket modifié, id : '+ id + ' | description : '+ description + \
                ' | date : '+ date_incident + ' | statut : '+ statut + \
                ' | parcelle_concernee : ' + parcelle
    flash(message, 'alert-success')
    return redirect('/ticket/show')

@app.route('/ticket/all')
def show_all_ticket():
    mycursor = get_db().cursor()
    sql = '''
    SELECT COUNT(ticket_incident.id_ticket) AS nombre_ticket,
    SUM(ticket_incident.statut_incident = 'En cours') AS nombre_ticket_en_cours,
    SUM(ticket_incident.statut_incident = 'Résolu') AS nombre_ticket_resolu,
    SUM(ticket_incident.statut_incident = 'A traiter') AS nombre_ticket_en_attente
    FROM ticket_incident LEFT JOIN parcelle ON parcelle.id_parcelle = ticket_incident.parcelle_concernee
    ORDER BY ticket_incident.parcelle_concernee;
    '''
    mycursor.execute(sql)
    ticket_counter = mycursor.fetchall()

    sql = '''
    SELECT ticket_incident.id_ticket AS id,
    ticket_incident.description_incident AS description,
    ticket_incident.date_incident AS date,
    ticket_incident.statut_incident AS statut,
    ticket_incident.parcelle_concernee AS parcelle,
    parcelle.adresse AS adresse FROM ticket_incident LEFT JOIN parcelle ON parcelle.id_parcelle = ticket_incident.parcelle_concernee;
    '''
    mycursor.execute(sql)
    ticket_incident = mycursor.fetchall()

    sql = '''
    SELECT parcelle.id_parcelle AS id,
    parcelle.adresse AS adresse,
    COUNT(ticket_incident.id_ticket) AS nombre_ticket,
    SUM(ticket_incident.statut_incident = 'En cours') AS nombre_ticket_en_cours,
    SUM(ticket_incident.statut_incident = 'Résolu') AS nombre_ticket_resolu,
    SUM(ticket_incident.statut_incident = 'A traiter') AS nombre_ticket_en_attente
    FROM ticket_incident LEFT JOIN parcelle ON parcelle.id_parcelle = ticket_incident.parcelle_concernee
    GROUP BY ticket_incident.parcelle_concernee
    ORDER BY ticket_incident.parcelle_concernee;
    '''
    mycursor.execute(sql)
    ticket_parcelle = mycursor.fetchall()

    max = 0
    for row in ticket_parcelle:
        if row['nombre_ticket'] > max:
            max = row['nombre_ticket']
            parcelle_max = row['id']

    min = 10000000
    for row in ticket_parcelle:
        if row['nombre_ticket'] < min:
            min = row['nombre_ticket']
            parcelle_min = row['id'] 

    return render_template('tickets/show_all_tickets.html', ticket_counter=ticket_counter, ticket_incident=ticket_incident, ticket_parcelle=ticket_parcelle, parcelle_max=parcelle_max, parcelle_min=parcelle_min)

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

@app.route('/variete/etat_show')
def show_etat_variete():
    mycursor = get_db().cursor()
    sql = '''
    SELECT 
    culture.libelle_culture AS nom,
    SUM(variete.stock) AS stock,
    SUM(variete.prix_kg*variete.stock) AS prix
    FROM variete
    LEFT JOIN culture ON variete.culture = culture.id_culture
    GROUP BY culture.id_culture
    ORDER BY culture.id_culture;
    '''
    mycursor.execute(sql)
    stock = mycursor.fetchall()

    sql ='''
    SELECT  culture.libelle_culture AS culture
    FROM culture
    LEFT JOIN variete ON culture.id_culture = variete.culture
    GROUP BY culture.id_culture
    ORDER BY culture.id_culture;
    '''
    mycursor.execute(sql)
    variete = mycursor.fetchall()

    labels = [str(row['culture']) for row in variete]
    return render_template('variete/etat_variete.html', stock=stock, variete=variete,
                           labels=labels)


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
    VALUES (%s, %s, %s, %s);
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

@app.route('/variete/edit', methods=['GET'])
def edit_variete():
    mycursor = get_db().cursor()

    sql = '''
            SELECT culture.id_culture AS id_culture, culture.libelle_culture AS nom FROM culture;
            '''
    mycursor.execute(sql)
    culture = mycursor.fetchall()

    sql = '''
        SELECT saison.saison AS saison FROM saison;
        '''
    mycursor.execute(sql)
    saison = mycursor.fetchall()

    id = request.args.get('id', '')
    sql = '''
        SELECT variete.id_variete AS id,
        variete.libelle_variete AS nom,
        variete.saison AS saison,
        variete.culture AS culture,
        variete.prix_kg AS prix,
        variete.stock AS stock
        FROM variete, culture
        WHERE variete.id_variete=%s AND culture.id_culture = variete.culture;
        '''
    mycursor.execute(sql, (id))
    variete = mycursor.fetchone()
    return render_template('variete/edit_variete.html', variete=variete, culture=culture, saison=saison)



@app.route('/variete/edit', methods=['POST'])
def valid_edit_collecte():
    mycursor = get_db().cursor()
    id = request.form.get('id', '')
    nom = request.form.get('nom', '')
    saison = request.form.get('saison', '')
    culture = request.form.get('culture', '')
    prix = request.form.get('prix_kg', '')
    stock = request.form.get('stock', '')
    tuple_update = (nom, saison, culture, prix, stock, id)
    sql = '''
    UPDATE variete SET libelle_variete = %s, saison = %s, culture = %s,
     prix_kg = %s, stock = %s WHERE id_variete = %s;'''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    message = u'Une variété modifiée, id : '+ id + ' | nom : '+ nom + \
              ' | saison : '+ saison + ' | type_culture : '+ culture + \
              ' | prix : ' + prix  + ' | stock : ' + stock
    flash(message, 'alert-success')
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

# @app.route('/collecte/edit', methods=['GET'])
# def edit_collecte():
#     id = request.args.get('id', '')
#     id=int(id)
#     return render_template('collecte/edit_collecte.html', collecte=collecte, parcelle=parcelle)

# @app.route('/collecte/edit', methods=['POST'])
# def valid_edit_collecte():
#     id = request.form.get('id', '')
#     quantite = request.form.get('quantite', '')
#     produit = request.form.get('produit', '')
#     date = request.form.get('date', '')
#     parcelle_id = request.form.get('parcelle_id')
#     print(u'Une collecte modifiée, quantite : ', quantite, ' | produit : ', produit, ' | date : ', date, '| parcelle_id : ', parcelle_id)
#     message = u'Une collecte modifiée, quantite : '+ quantite+ ' | produit : '+ produit+ ' | date : '+ date+ '| parcelle_id : '+ parcelle_id
#     flash(message, 'alert-success')
#     return redirect('/collecte/show')



if __name__ == '__main__':
    app.run(debug=True, port=5000)
