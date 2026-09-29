import sqlite3

conexao = sqlite3.connect("hotel.db")
cursor = conexao.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS hospedes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    cpf TEXT UNIQUE,
    telefone TEXT,
    email TEXT)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS quartos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero TEXT UNIQUE,
    tipo TEXT,
    capacidade INTEGER,
    diaria REAL,
    status TEXT DEFAULT 'disponivel')""")

cursor.execute("""CREATE TABLE IF NOT EXISTS reservas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_hospede INTEGER,
    id_quarto INTEGER,
    checkin TEXT,
    checkout TEXT)""")

conexao.commit()




def cadastrar_hospede():
    print("--- Cadastrar hospede ---")
    nome = input("Nome: ")
    cpf = input("CPF (so numeros): ")
    telefone = input("Telefone: ")
    email = input("Email: ")


    numeros = "0123456789"
    so_numeros = True
    for letra in cpf:
        if letra not in numeros:
            so_numeros = False

    if nome == "" or cpf == "":
        print("Preencha o nome e o CPF!")
    elif len(cpf) != 11 or so_numeros == False:
        print("O CPF precisa ter 11 numeros!")
    else:
        cursor.execute("SELECT * FROM hospedes WHERE cpf = ?", (cpf,))
        achou = cursor.fetchone()

        if achou != None:
            print("Ja existe um hospede com esse CPF!")
        else:
            cursor.execute("INSERT INTO hospedes (nome, cpf, telefone, email) VALUES (?, ?, ?, ?)",
                           (nome, cpf, telefone, email))
            conexao.commit()
            print("Hospede cadastrado!")


def listar_hospedes():
    print("--- Lista de hospedes ---")
    cursor.execute("SELECT * FROM hospedes")
    lista = cursor.fetchall()

    if len(lista) == 0:
        print("Nenhum hospede cadastrado.")
    else:
        for h in lista:
            print("ID:", h[0], "| Nome:", h[1], "| CPF:", h[2], "| Tel:", h[3], "| Email:", h[4])


def excluir_hospede():
    print("--- Excluir hospede ---")
    cpf = input("CPF do hospede: ")

    cursor.execute("SELECT * FROM hospedes WHERE cpf = ?", (cpf,))
    achou = cursor.fetchone()

    if achou == None:
        print("Hospede nao encontrado!")
    else:
        cursor.execute("DELETE FROM hospedes WHERE cpf = ?", (cpf,))
        conexao.commit()
        print("Hospede excluido!")




