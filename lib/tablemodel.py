import os
import sqlite3


class DatabaseModel:
    """This class is a wrapper around the sqlite3 database. It provides a simple interface that maps methods
    to database queries. The only required parameter is the database file."""

    def __init__(self, database_file):
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    def run_query(self, sql_query):
        conn = sqlite3.connect(self.database_file)
        c = conn.cursor()
        c.execute(sql_query)
        tables = c.fetchall()
        conn.close()
        return tables

    # Using the built-in sqlite3 system table, return a list of all tables in the database
    def get_table_list(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        return tables

    # Given a table name, return the rows and column names
    def get_table_content(self, table_name):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()
        # Note that this method returns 2 variables!
        return table_content, table_headers

    def get_selected_content(self, table_name, columnnames, start_values, stop_values):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * from {table_name} Where  {columnnames} "
                       f"BETWEEN {start_values} AND {stop_values} ORDER BY {columnnames} ASC")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        selected_headers = [column_name[0] for column_name in cursor.description]
        selected_content = cursor.fetchall()
        # Note that this method returns 2 variables!
        return selected_content, selected_headers

    def get_one_row(self, table_name, rowid):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * from {table_name} Where id={rowid}")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        selected_onerow_headers = [column_name[0] for column_name in cursor.description]
        selected_onerow_content = cursor.fetchall()
        # Note that this method returns 2 variables!
        return selected_onerow_content, selected_onerow_headers

    def update_row(self, table_name, update_values, columns, row_id):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        if len(columns) == len(update_values):
            set_clause = ""
            for column, value in zip(columns, update_values):
                set_clause += f"{column} = '{value}', "
            set_clause = set_clause[:-2]  # Remove last comma
            cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = {row_id}")
            connection.commit()

    # Patronen > Leerdoelen

    def get_leerdoelen(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        # Creates a new table from the sql query
        cursor.execute(f"SELECT * FROM vragen WHERE leerdoel NOT IN(SELECT id FROM leerdoelen)")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        leerdoelen_table_headers = [column_name[0] for column_name in cursor.description]
        leerdoelen_table_content = cursor.fetchall()
        # Note that this method returns 2 variables!
        return leerdoelen_table_content, leerdoelen_table_headers

    def dropdown_leerdoelen(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        # Creates a new table from the sql query
        cursor.execute(f"SELECT * FROM leerdoelen")
        leerdoelen_list = cursor.fetchall()
        return leerdoelen_list

    def dropdown_auteurs(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        # Creates a new table from the sql query
        cursor.execute(f"SELECT * FROM auteurs")
        auteurs_list = cursor.fetchall()
        return auteurs_list

    # Function partially inspired by
    # https://flask.palletsprojects.com/en/2.2.x/tutorial/blog/
    # https://www.tutorialspoint.com/what-is-python-commit-method-in-mysql
    def update_leerdoelen(self, new_leerdoel, selected_id):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        # Creates a new table from the sql query
        cursor.execute(f"UPDATE vragen SET leerdoel = {new_leerdoel} WHERE id = {selected_id}")
        # Commits changes to database
        connection.commit()

    def update_auteur(self, new_auteur, selected_id):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        # Creates a new table from the sql query
        cursor.execute(f"UPDATE vragen SET auteur = {new_auteur} WHERE id = {selected_id}")
        # Commits changes to database
        connection.commit()

    def get_columns(self, table):
        sql_query = f"PRAGMA table_info({table})"
        result = self.run_query(sql_query)
        table_list = ["\"{}\"".format(val[1]) for val in result]
        return table_list

    # Patronen > Auteurs
    def get_auteurs(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT * FROM vragen WHERE auteur NOT IN(SELECT id FROM auteurs)")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        auteurs_table_headers = [column_name[0] for column_name in cursor.description]
        auteurs_table_content = cursor.fetchall()
        return auteurs_table_content, auteurs_table_headers

    # Data kwaliteit > Vragen tabel
    def get_none_leerdoelen(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT * FROM vragen WHERE leerdoel IS NULL")
        leerdoel_headers = [column_name[0] for column_name in cursor.description]
        leerdoel_content = cursor.fetchall()
        return leerdoel_content, leerdoel_headers

    def get_none_auteurs(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT * FROM vragen WHERE auteur IS NULL")
        auteur_headers = [column_name[0] for column_name in cursor.description]
        auteur_content = cursor.fetchall()
        return auteur_content, auteur_headers

    # Data kwaliteit > HTML_errors
    def get_allhtmlcodes(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT id,vraag FROM vragen WHERE vraag LIKE '%&%' "
                       "OR vraag LIKE '%<%' OR vraag LIKE '%>%' OR vraag LIKE '%nbsp%';")
        allhtml_error_header = [column_name[0] for column_name in cursor.description]
        all_error_content = cursor.fetchall()
        return all_error_content, allhtml_error_header

    def get_vraag_id(self, id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT vraag FROM vragen WHERE id = ?;", (id,))
        vraag = cursor.fetchone()[0]
        return vraag

    def update_vragen(self, id, vraag):
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()
        # Creates a new table from the sql query
        cursor.execute("UPDATE vragen SET vraag = ? WHERE id = ?", (vraag, id))
        # Commits changes to database
        connection.commit()

    # Auteurs table with invalid datatypes in column medewerkers
    def get_auteur_string(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        # Creates a new table from the sql query
        cursor.execute(f"SELECT * FROM auteurs WHERE medewerker != 0 AND medewerker != 1")
        auteur_headers = [column_name[0] for column_name in cursor.description]
        auteur_content = cursor.fetchall()
        return auteur_content, auteur_headers
