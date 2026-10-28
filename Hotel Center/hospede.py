import sqlite3


def cadastrar_hospede():
    try:
        nome = input("Digite o nome do hospede: ")
        cpf = input("Digite o CPF: ")
        telefone = input("Digite o telefone: ")
        email = input("Digite o email: ")

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("""INSERT INTO hospedes(nome, cpf, telefone, email) VALUES (?, ?, ?, ?)""",(nome, cpf, telefone, email))

        conexao.commit()
        conexao.close()

        print("Hospede cadastrado com sucesso")

    except sqlite3.IntegrityError:
        print("Esse CPF ja esta cadastrado")

    except sqlite3.Error as erro:
        print("Erro ao cadastrar hospede:", erro)


def listar_hospedes():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM hospedes")
        hospedes = cursor.fetchall()

        conexao.close()

        for hospede in hospedes:
            print("ID:", hospede[0])
            print("Nome:", hospede[1])
            print("CPF:", hospede[2])
            print("Telefone:", hospede[3])
            print("Email:", hospede[4])


    except sqlite3.Error as erro:
        print("Erro ao listar hospedes:", erro)


def atualizar_hospede():
    try:
        listar_hospedes()

        id_hospede = int(input("Digite o ID do hospede: "))
        nome = input("Digite o novo nome: ")
        telefone = input("Digite o novo telefone: ")
        email = input("Digite o novo email: ")

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            """UPDATE hospedes
            SET nome = ?, telefone = ?, email = ?
            WHERE id = ?""",
            (nome, telefone, email, id_hospede)
        )

        conexao.commit()

        if cursor.rowcount == 0:
            print("Hospede nao encontrado")
        else:
            print("Hospede atualizado com sucesso")

        conexao.close()

    except ValueError:
        print("Digite um numero valido")

    except sqlite3.Error as erro:
        print("Erro ao atualizar hospede:", erro)


def excluir_hospede():
    try:
        listar_hospedes()

        id_hospede = int(input("Digite o ID do hospede: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM hospedes WHERE id = ?",(id_hospede,))

        conexao.commit()

        if cursor.rowcount == 0:
            print("Hospede nao encontrado")
        else:
            print("Hospede excluido com sucesso")

        conexao.close()

    except ValueError:
        print("Digite um numero valido")

    except sqlite3.Error as erro:
        print("Erro ao excluir hospede:", erro)


def relatorio_hospedes():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT
                hospedes.nome,
                hospedes.cpf,
                hospedes.telefone,
                COUNT(reservas.id)
            FROM hospedes
            LEFT JOIN reservas
            ON hospedes.id = reservas.id_hospede
            GROUP BY hospedes.id
        """)

        hospedes = cursor.fetchall()
        conexao.close()

        for hospede in hospedes:
            print("Nome:", hospede[0])
            print("CPF:", hospede[1])
            print("Telefone:", hospede[2])
            print("Quantidade de reservas:", hospede[3])
           
    except sqlite3.Error as erro:
        print("Erro ao gerar relatorio:", erro)