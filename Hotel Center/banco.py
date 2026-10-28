import sqlite3


def criar_banco():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS hospedes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT,
                email TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quartos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                valor_diaria REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_hospede INTEGER NOT NULL,
                id_quarto INTEGER NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT NOT NULL,
                desconto REAL DEFAULT 0,
                status TEXT NOT NULL,
                FOREIGN KEY (id_hospede) REFERENCES hospedes(id),
                FOREIGN KEY (id_quarto) REFERENCES quartos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor REAL NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consumos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_reserva INTEGER NOT NULL,
                id_servico INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                FOREIGN KEY (id_reserva) REFERENCES reservas(id),
                FOREIGN KEY (id_servico) REFERENCES servicos(id)
            )
        """)

        conexao.commit()
        conexao.close()

    except sqlite3.Error as erro:
        print("Erro ao criar banco:", erro)


def criar_usuarios_padrao():
    conexao = sqlite3.connect("hotel_center.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (nome, email, senha, tipo)
        VALUES (?, ?, ?, ?)
    """, ("Recepcionista", "adm@hotel.com",
          "hc456", "Recepcionista"))

    cursor.execute("""
        INSERT OR IGNORE INTO usuarios (nome, email, senha, tipo)
        VALUES (?, ?, ?, ?)
    """, ("Cliente", "cliente@hotel.com",
          "1234", "Cliente"))

    conexao.commit()
    conexao.close()