import os.path
# import sys
# import sqlite3

from flask import Flask, request, render_template, redirect

from lib.tablemodel import DatabaseModel


# This demo glues a random database and the Flask framework.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 80
FLASK_DEBUG = True

app = Flask(__name__)
# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

# Check if the database file exists.
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}.")
dbm = DatabaseModel(DATABASE_FILE)


# Main route that shows a list of tables in the database
# Note the "@app.route" decorator. This might be a new concept for you.
# It is a way to "decorate" a function with additional functionality. You
# can safely ignore this for now - or look into it as it is a really powerful
# concept in Python.


@app.route("/")
def loginscherm():
    return render_template("login.html")


database = {'Admin': 'test123'}


@app.route('/form_login', methods=['POST', 'GET'])
def login():
    tables = dbm.get_table_list()
    name1 = request.form['username']
    pwd = request.form['password']
    if name1 not in database:
        return render_template('login.html', info='Invalid User')
    else:
        if database[name1] != pwd:
            return render_template('login.html', info='Invalid Password')
        else:
            return render_template('tables.html', name=name1, table_list=tables)


@app.route('/home')
def home_screen():
    tables = dbm.get_table_list()
    return render_template('tables.html', table_list=tables)


# Routes to display vraagitems with invalid leerdoelen
@app.route("/leerdoelen_invalid")
def get_leerdoelen():
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_leerdoelen()
    return render_template("foute_leerdoelen.html", rows=rows, columns=column_names, table_list=tables)


# Route to edit the leerdoel with a dropdown
@app.route("/leerdoelen/edit/<id>")
def update_leerdoel(id=None):
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_leerdoelen()
    dropdown_leerdoel = dbm.dropdown_leerdoelen()
    vraag_id = dbm.get_vraag_id(id)
    return render_template("update_invalid_leerdoelen.html", id=id, dropdown_leerdoelen=dropdown_leerdoel, rows=rows,
                           column_names=column_names, table_list=tables, vraag_id=vraag_id)


@app.route("/leerdoelen/edit/choose/<id>", methods=["GET", "POST"])
def update_leerdoel_choose(id):
    if request.method == "POST":
        item_id = request.form['selected_id']
        new_leerdoel = request.form['update_leerdoel']
        dbm.update_leerdoelen(new_leerdoel, item_id)
        return redirect('/leerdoelen_invalid')


# Routes to display vraagitems with null leerdoelen
@app.route("/leerdoelen_null")
def get_leerdoelen_null():
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_none_leerdoelen()
    return render_template("null_leerdoelen.html", rows=rows, columns=column_names, table_list=tables)


# Route to edit the leerdoel with a dropdown
@app.route("/leerdoelen_null/edit/<id>")
def update_null_leerdoel(id=None):
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_leerdoelen()
    dropdown_leerdoel = dbm.dropdown_leerdoelen()
    vraag_id = dbm.get_vraag_id(id)
    return render_template("update_null_leerdoelen.html", id=id, dropdown_leerdoelen=dropdown_leerdoel, rows=rows,
                           column_names=column_names, table_list=tables, vraag_id=vraag_id)


@app.route("/leerdoelen_null/edit/choose/<id>", methods=["GET", "POST"])
def update_null_leerdoel_choose(id):
    if request.method == "POST":
        item_id = request.form['selected_id']
        new_leerdoel = request.form['update_leerdoel']
        dbm.update_leerdoelen(new_leerdoel, item_id)
        return redirect('/leerdoelen_null')


# Routes to display vraagitems with invalid auteurs
@app.route("/auteurs_invalid")
def get_auteurs():
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_auteurs()
    return render_template("invalid_auteur.html", rows=rows, columns=column_names, table_list=tables)


# Route to edit the auteur with a dropdown
@app.route("/auteurs/edit/<id>")
def update_auteur(id=None):
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_auteurs()
    dropdown_auteur = dbm.dropdown_auteurs()
    vraag_id = dbm.get_vraag_id(id)
    return render_template("update_invalid_auteurs.html", id=id, dropdown_auteurs=dropdown_auteur, rows=rows,
                           column_names=column_names, table_list=tables, vraag_id=vraag_id)


@app.route("/auteurs/edit/choose/<id>", methods=["GET", "POST"])
def update_auteur_choose(id):
    if request.method == "POST":
        item_id = request.form['selected_id']
        new_auteur = request.form['update_auteur']
        dbm.update_auteur(new_auteur, item_id)
        return redirect('/auteurs_invalid')


# Routes to display vraagitems with null auteurs
@app.route("/auteurs_null")
def get_auteurs_null():
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_none_auteurs()
    return render_template("null_auteurs.html", rows=rows, columns=column_names, table_list=tables)


# Route to edit the auteur with a dropdown
@app.route("/auteurs_null/edit/<id>")
def update_null_auteur(id=None):
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_auteurs()
    dropdown_auteur = dbm.dropdown_auteurs()
    vraag_id = dbm.get_vraag_id(id)
    return render_template("update_null_auteurs.html", id=id, dropdown_auteurs=dropdown_auteur, rows=rows,
                           column_names=column_names, table_list=tables, vraag_id=vraag_id)


@app.route("/auteurs_null/edit/choose/<id>", methods=["GET", "POST"])
def update_null_auteur_choose(id):
    if request.method == "POST":
        item_id = request.form['selected_id']
        new_auteur = request.form['update_auteur']
        dbm.update_auteur(new_auteur, item_id)
        return redirect('/auteurs_null')


# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    tables = dbm.get_table_list()
    columns = dbm.get_columns(table_name)
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=columns, table_name=table_name, table_list=tables)


@app.route("/table_details/<table_name>/filtered", methods=["GET", "POST"])
def get_select_values(table_name=None):
    tables = dbm.get_table_list()
    columns = dbm.get_columns(table_name)
    if request.method == "POST":
        result = request.form
        columnname = (result.get('Value_1'))
        start_value = (result.get('Value_2'))
        stop_value = (result.get('Value_3'))
        rows, column_names = dbm.get_selected_content(table_name, columnname, start_value, stop_value)
        return render_template('table_details.html',
                               column_names=column_names,
                               rows=rows,
                               columns=columns,
                               table_name=table_name,
                               table_list=tables,
                               columnnames=columnname,
                               Start_values=start_value,
                               Stop_values=stop_value)


@app.route("/table_details/<table_name>", methods=["GET", "POST"])
def get_one_row(table_name=None):
    tables = dbm.get_table_list()
    columns = dbm.get_columns(table_name)
    if request.method == "POST":
        result = request.form
        rowid = (result.get('rowid'))
        rij, naam = dbm.get_one_row(table_name, rowid)
        rows, column_names = dbm.get_table_content(table_name)
    return render_template('table_details.html',
                           rij=rij,
                           naam=naam,
                           table_list=tables,
                           column_names=column_names,
                           rows=rows,
                           table_name=table_name,
                           rowid=rowid,
                           columns=columns)


@app.route("/table_details/<table_name>/update", methods=["GET", "POST"])
def update_to_database(table_name=None):
    tables = dbm.get_table_list()
    columns = dbm.get_columns(table_name)
    update_values = []
    if request.method == "POST":
        result = request.form
        update_values = (result.getlist('Update_values'))
        row_id = (result.get('id'))
        rows, column_names = dbm.get_table_content(table_name)
        dbm.update_row(table_name, update_values, columns, row_id)
    return render_template('table_details.html',
                           table_list=tables,
                           rows=rows,
                           table_name=table_name,
                           Update_values=update_values,
                           column_names=column_names,
                           columns=columns,
                           row_id=row_id)


@app.route("/allHTML_error")
def get_allhtml_error():
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_allhtmlcodes()
    return render_template("ALLHTML_errors.html", rows=rows, columns=column_names, table_list=tables)


@app.route("/update_web/<id>")
def update_html_errors(id=None):
    vraag = dbm.get_vraag_id(id)
    tables = dbm.get_table_list()
    rows, column_names = dbm.get_allhtmlcodes()
    return render_template("HTML_edit.html", id=id, rows=rows,
                           column_names=column_names, table_list=tables, vraag=vraag)


@app.route("/update_vraag/<id>", methods=["POST"])
def update_de_vragen(id):
    vraag = dbm.get_vraag_id(id)
    if request.method == "POST":
        id_item = request.form['id']
        vragen = request.form['vraag']
        dbm.update_vragen(id_item, vragen)
        return redirect("/allHTML_error")


@app.route("/auteur_text")
def get_auteur_text():
    tables = dbm.get_table_list()
    rows, columns = dbm.get_auteur_string()
    return render_template("auteur_strings.html", table_list=tables, rows=rows, columns=columns)


if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
