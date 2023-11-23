import MySQLdb as mdb

class Database():
    db_config = {
        'host': 'localhost',
        'user': 'admin',
        'passwd': '13298jona',
        'db': 'gestor_gastos',
        'port': 33096
    }

    conn = mdb.connect(**db_config)
    cursor = conn.cursor()