import MySQLdb as mdb

class Database():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'passwd': 'root',
        'db': 'gestor_gastos',
    }

    conn = mdb.connect(**db_config)
    cursor = conn.cursor()