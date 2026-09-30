import sqlite3


def criar_banco():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hospedes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                telefone TEXT,
                email TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quartos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER UNIQUE NOT NULL,
                tipo TEXT NOT NULL,
                valor_diaria REAL NOT NULL,
                status TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        ''')

        cursor.execute('''
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
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor REAL NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS consumos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_reserva INTEGER NOT NULL,
                id_servico INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                FOREIGN KEY (id_reserva) REFERENCES reservas(id),
                FOREIGN KEY (id_servico) REFERENCES servicos(id)
            )
        ''')

        conexao.commit()
        conexao.close()

        print("Banco criado com sucesso")

    except:
        print("Erro ao criar banco")


def cadastrar_hospede():
    try:
        nome = input("Digite o nome do hospede: ")
        cpf = input("Digite o CPF: ")
        telefone = input("Digite o telefone: ")
        email = input("Digite o email: ")

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO hospedes (nome, cpf, telefone, email) VALUES (?, ?, ?, ?)",
            (nome, cpf, telefone, email)
        )

        conexao.commit()
        conexao.close()

        print("Hospede cadastrado com sucesso")

    except sqlite3.IntegrityError:
        print("Esse CPF ja esta cadastrado")

    except:
        print("Erro ao cadastrar hospede")


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

    except:
        print("Erro ao listar hospedes")


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
            "UPDATE hospedes SET nome = ?, telefone = ?, email = ? WHERE id = ?",
            (nome, telefone, email, id_hospede)
        )

        conexao.commit()
        conexao.close()

        print("Hospede atualizado com sucesso")

    except ValueError:
        print("Digite um numero valido")

    except:
        print("Erro ao atualizar hospede")


def excluir_hospede():
    try:
        listar_hospedes()

        id_hospede = int(input("Digite o ID do hospede: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM hospedes WHERE id = ?",
            (id_hospede,)
        )

        conexao.commit()
        conexao.close()

        print("Hospede excluido com sucesso")

    except ValueError:
        print("Digite um numero valido")

    except:
        print("Erro ao excluir hospede")


def cadastrar_quarto():
    try:
        numero = int(input("Digite o numero do quarto: "))
        tipo = input("Digite o tipo do quarto: ")
        valor = float(input("Digite o valor da diaria: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO quartos (numero, tipo, valor_diaria, status) VALUES (?, ?, ?, ?)",
            (numero, tipo, valor, "Disponivel")
        )

        conexao.commit()
        conexao.close()

        print("Quarto cadastrado com sucesso")

    except ValueError:
        print("Digite numeros validos")

    except sqlite3.IntegrityError:
        print("Esse numero de quarto ja existe")

    except:
        print("Erro ao cadastrar quarto")


def listar_quartos():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM quartos")
        quartos = cursor.fetchall()

        conexao.close()


        for quarto in quartos:
            print("ID:", quarto[0])
            print("Numero:", quarto[1])
            print("Tipo:", quarto[2])
            print("Valor da diaria:", quarto[3])
            print("Status:", quarto[4])

    except:
        print("Erro ao listar quartos")


def listar_quartos_disponiveis():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE status = 'Disponivel'"
        )

        quartos = cursor.fetchall()

        conexao.close()


        for quarto in quartos:
            print("ID:", quarto[0])
            print("Numero:", quarto[1])
            print("Tipo:", quarto[2])
            print("Valor da diaria:", quarto[3])

    except:
        print("Erro ao listar quartos disponiveis")


def listar_quartos_indisponiveis():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE status = 'Ocupado'"
        )

        quartos = cursor.fetchall()

        conexao.close()


        for quarto in quartos:
            print("ID:", quarto[0])
            print("Numero:", quarto[1])
            print("Tipo:", quarto[2])

    except:
        print("Erro ao listar quartos indisponiveis")


def atualizar_quarto():
    try:
        listar_quartos()

        id_quarto = int(input("Digite o ID do quarto: "))
        numero = int(input("Digite o novo numero: "))
        tipo = input("Digite o novo tipo: ")
        valor = float(input("Digite o novo valor da diaria: "))
        status = input("Digite o status do quarto: ")

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "UPDATE quartos SET numero = ?, tipo = ?, valor_diaria = ?, status = ? WHERE id = ?",
            (numero, tipo, valor, status, id_quarto)
        )

        conexao.commit()
        conexao.close()

        print("Quarto atualizado com sucesso")

    except ValueError:
        print("Digite valores validos")

    except:
        print("Erro ao atualizar quarto")


def excluir_quarto():
    try:
        listar_quartos()

        id_quarto = int(input("Digite o ID do quarto: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "DELETE FROM quartos WHERE id = ?",
            (id_quarto,)
        )

        conexao.commit()
        conexao.close()

        print("Quarto excluido com sucesso")

    except ValueError:
        print("Digite um numero valido")

    except:
        print("Erro ao excluir quarto")


def cadastrar_usuario():
    try:
        nome = input("Digite o nome do usuario: ")
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")
        tipo = input("Digite o tipo do usuario: ")

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            (nome, email, senha, tipo)
        )

        conexao.commit()
        conexao.close()

        print("Usuario cadastrado com sucesso")

    except sqlite3.IntegrityError:
        print("Esse email ja esta cadastrado")

    except:
        print("Erro ao cadastrar usuario")


def listar_usuarios():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome, email, tipo FROM usuarios")
        usuarios = cursor.fetchall()

        conexao.close()


        for usuario in usuarios:
            print("ID:", usuario[0])
            print("Nome:", usuario[1])
            print("Email:", usuario[2])
            print("Tipo:", usuario[3])

    except:
        print("Erro ao listar usuarios")


def cadastrar_reserva():
    try:
        listar_hospedes()

        id_hospede = int(
            input("Digite o ID do hospede: ")
        )

        listar_quartos_disponiveis()

        id_quarto = int(
            input("Digite o ID do quarto: ")
        )

        check_in = input(
            "Digite a data de check-in: "
        )

        check_out = input(
            "Digite a data de check-out: "
        )

        if check_in == check_out:
            print("Erro: o check-out deve ser depois do check-in")
            return

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT * FROM quartos WHERE id = ?",
            (id_quarto,)
        )

        quarto = cursor.fetchone()

        if not quarto:
            print("Quarto nao encontrado")
            conexao.close()
            return

        if quarto[4] == "Ocupado":
            print("Esse quarto ja esta ocupado")
            conexao.close()
            return

        cursor.execute(
            "SELECT * FROM reservas WHERE id_quarto = ? AND status = 'Ativa'",
            (id_quarto,)
        )

        reserva = cursor.fetchone()

        if reserva:
            print("Esse quarto ja possui uma reserva")
            conexao.close()
            return

        desconto = 0

        dias = int(
            input("Digite a quantidade de dias da reserva: ")
        )

        if dias >= 7:
            desconto = 15

        cursor.execute(
            '''
            INSERT INTO reservas
            (id_hospede, id_quarto, check_in, check_out, desconto, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                id_hospede,
                id_quarto,
                check_in,
                check_out,
                desconto,
                "Ativa"
            )
        )

        cursor.execute(
            "UPDATE quartos SET status = 'Ocupado' WHERE id = ?",
            (id_quarto,)
        )

        conexao.commit()
        conexao.close()

        print("Reserva realizada com sucesso")

        if desconto == 15:
            print("Desconto de 15% aplicado")

    except ValueError:
        print("Digite os valores corretamente")

    except:
        print("Erro ao cadastrar reserva")


def listar_reservas():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute('''
            SELECT
                reservas.id,
                hospedes.nome,
                quartos.numero,
                reservas.check_in,
                reservas.check_out,
                reservas.desconto,
                reservas.status
            FROM reservas
            JOIN hospedes
            ON reservas.id_hospede = hospedes.id
            JOIN quartos
            ON reservas.id_quarto = quartos.id
        ''')

        reservas = cursor.fetchall()

        conexao.close()

        for reserva in reservas:
            print("ID:", reserva[0])
            print("Hospede:", reserva[1])
            print("Quarto:", reserva[2])
            print("Check-in:", reserva[3])
            print("Check-out:", reserva[4])
            print("Desconto:", reserva[5], "%")
            print("Status:", reserva[6])

    except:
        print("Erro ao listar reservas")


def cancelar_reserva():
    try:
        listar_reservas()

        id_reserva = int(
            input("Digite o ID da reserva: ")
        )

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id_quarto FROM reservas WHERE id = ?",
            (id_reserva,)
        )

        reserva = cursor.fetchone()

        if not reserva:
            print("Reserva nao encontrada")
            conexao.close()
            return

        id_quarto = reserva[0]

        cursor.execute(
            "UPDATE reservas SET status = 'Cancelada' WHERE id = ?",
            (id_reserva,)
        )

        cursor.execute(
            "UPDATE quartos SET status = 'Disponivel' WHERE id = ?",
            (id_quarto,)
        )

        conexao.commit()
        conexao.close()

        print("Reserva cancelada com sucesso")

    except ValueError:
        print("Digite um numero valido")

    except:
        print("Erro ao cancelar reserva")


def cadastrar_servico():
    try:
        nome = input("Digite o nome do servico: ")
        valor = float(input("Digite o valor do servico: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO servicos (nome, valor) VALUES (?, ?)",
            (nome, valor)
        )

        conexao.commit()
        conexao.close()

        print("Servico cadastrado com sucesso")

    except ValueError:
        print("Digite um valor valido")

    except:
        print("Erro ao cadastrar servico")


def listar_servicos():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM servicos")
        servicos = cursor.fetchall()

        conexao.close()


        for servico in servicos:
            print("ID:", servico[0])
            print("Nome:", servico[1])
            print("Valor:", servico[2])

    except:
        print("Erro ao listar servicos")


def lancar_consumo():
    try:
        listar_reservas()

        id_reserva = int(
            input("Digite o ID da reserva: ")
        )

        listar_servicos()

        id_servico = int(
            input("Digite o ID do servico: ")
        )

        quantidade = int(
            input("Digite a quantidade: ")
        )

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            '''
            INSERT INTO consumos
            (id_reserva, id_servico, quantidade)
            VALUES (?, ?, ?)
            ''',
            (id_reserva, id_servico, quantidade)
        )

        conexao.commit()
        conexao.close()

        print("Consumo cadastrado com sucesso")

    except ValueError:
        print("Digite numeros validos")

    except:
        print("Erro ao cadastrar consumo")


def gerar_conta():
    try:
        listar_reservas()

        id_reserva = int(
            input("Digite o ID da reserva: ")
        )

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute('''
            SELECT
                hospedes.nome,
                quartos.numero,
                quartos.valor_diaria,
                reservas.desconto
            FROM reservas
            JOIN hospedes
            ON reservas.id_hospede = hospedes.id
            JOIN quartos
            ON reservas.id_quarto = quartos.id
            WHERE reservas.id = ?
        ''', (id_reserva,))

        reserva = cursor.fetchone()

        if not reserva:
            print("Reserva nao encontrada")
            conexao.close()
            return

        nome = reserva[0]
        numero_quarto = reserva[1]
        valor_diaria = reserva[2]
        desconto = reserva[3]

        dias = int(
            input("Digite a quantidade de dias: ")
        )

        valor_diarias = valor_diaria * dias

        valor_desconto = valor_diarias * desconto / 100

        valor_diarias = valor_diarias - valor_desconto

        cursor.execute('''
            SELECT
                servicos.nome,
                servicos.valor,
                consumos.quantidade
            FROM consumos
            JOIN servicos
            ON consumos.id_servico = servicos.id
            WHERE consumos.id_reserva = ?
        ''', (id_reserva,))

        consumos = cursor.fetchall()

        total_servicos = 0

        print("Hospede:", nome)
        print("Quarto:", numero_quarto)
        print("Dias:", dias)
        print("Valor das diarias:", valor_diarias)
        print("Desconto:", desconto, "%")

        for consumo in consumos:
            nome_servico = consumo[0]
            valor_servico = consumo[1]
            quantidade = consumo[2]

            subtotal = valor_servico * quantidade

            total_servicos = total_servicos + subtotal

            print(
                nome_servico,
                "Quantidade:",
                quantidade,
                "Valor:",
                subtotal
            )

        valor_final = valor_diarias + total_servicos

        print("Total dos servicos:", total_servicos)
        print("Valor final:", valor_final)

        conexao.close()

    except ValueError:
        print("Digite numeros validos")

    except:
        print("Erro ao gerar conta")


def forma_pagamento():
    try:
        listar_reservas()

        id_reserva = int(
            input("Digite o ID da reserva: ")
        )

        print("1 - Pix")
        print("2 - Cartao de credito")
        print("3 - Cartao de debito")
        print("4 - Dinheiro")

        opcao = int(
            input("Escolha a forma de pagamento: ")
        )

        if opcao == 1:
            pagamento = "Pix"

        elif opcao == 2:
            pagamento = "Cartao de credito"

        elif opcao == 3:
            pagamento = "Cartao de debito"

        elif opcao == 4:
            pagamento = "Dinheiro"

        else:
            print("Opcao invalida")
            return

        print("Reserva:", id_reserva)
        print("Forma de pagamento:", pagamento)

    except ValueError:
        print("Digite um numero valido")

    except:
        print("Erro na forma de pagamento")


def relatorio_hospedes():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute('''
            SELECT
                hospedes.nome,
                hospedes.cpf,
                hospedes.telefone,
                COUNT(reservas.id)
            FROM hospedes
            LEFT JOIN reservas
            ON hospedes.id = reservas.id_hospede
            GROUP BY hospedes.id
        ''')

        hospedes = cursor.fetchall()

        conexao.close()

        for hospede in hospedes:
            print("Nome:", hospede[0])
            print("CPF:", hospede[1])
            print("Telefone:", hospede[2])
            print("Quantidade de reservas:", hospede[3])

    except:
        print("Erro ao gerar relatorio")


def menu():
    criar_banco()

    while True:
        try:
 
            print("       HOTEL CENTER")

            print("1 - Cadastrar hospede")
            print("2 - Listar hospedes")
            print("3 - Atualizar hospede")
            print("4 - Excluir hospede")
            print("5 - Cadastrar quarto")
            print("6 - Listar quartos")
            print("7 - Quartos disponiveis")
            print("8 - Quartos indisponiveis")
            print("9 - Atualizar quarto")
            print("10 - Excluir quarto")
            print("11 - Cadastrar usuario")
            print("12 - Listar usuarios")
            print("13 - Fazer reserva")
            print("14 - Listar reservas")
            print("15 - Cancelar reserva")
            print("16 - Cadastrar servico")
            print("17 - Listar servicos")
            print("18 - Lancar consumo")
            print("19 - Gerar conta final")
            print("20 - Forma de pagamento")
            print("21 - Relatorio de hospedes")
            print("22 - Sair")

            opcao = int(input("Escolha uma opcao: "))

            if opcao == 1:
                cadastrar_hospede()

            elif opcao == 2:
                listar_hospedes()

            elif opcao == 3:
                atualizar_hospede()

            elif opcao == 4:
                excluir_hospede()

            elif opcao == 5:
                cadastrar_quarto()

            elif opcao == 6:
                listar_quartos()

            elif opcao == 7:
                listar_quartos_disponiveis()

            elif opcao == 8:
                listar_quartos_indisponiveis()

            elif opcao == 9:
                atualizar_quarto()

            elif opcao == 10:
                excluir_quarto()

            elif opcao == 11:
                cadastrar_usuario()

            elif opcao == 12:
                listar_usuarios()

            elif opcao == 13:
                cadastrar_reserva()

            elif opcao == 14:
                listar_reservas()

            elif opcao == 15:
                cancelar_reserva()

            elif opcao == 16:
                cadastrar_servico()

            elif opcao == 17:
                listar_servicos()

            elif opcao == 18:
                lancar_consumo()

            elif opcao == 19:
                gerar_conta()

            elif opcao == 20:
                forma_pagamento()

            elif opcao == 21:
                relatorio_hospedes()

            elif opcao == 22:
                print("Saindo do sistema...")
                break

            else:
                print("Opcao invalida")

        except ValueError:
            print("Digite apenas numeros")

        except:
            print("Erro no menu")


menu()