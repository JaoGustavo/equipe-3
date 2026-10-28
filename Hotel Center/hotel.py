import sqlite3

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
    except sqlite3.Error as erro:
        print("Erro ao cadastrar quarto:", erro)

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
            print("--------------------")

    except sqlite3.Error as erro:
        print("Erro ao listar quartos:", erro)

def listar_quartos_disponiveis():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM quartos WHERE status = 'Disponivel'")
        quartos = cursor.fetchall()
        conexao.close()

        if not quartos:
            print("Nao existem quartos disponiveis")

        for quarto in quartos:
            print("ID:", quarto[0])
            print("Numero:", quarto[1])
            print("Tipo:", quarto[2])
            print("Valor da diaria:", quarto[3])

    except sqlite3.Error as erro:
        print("Erro ao listar quartos disponiveis:", erro)

def listar_quartos_indisponiveis():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM quartos WHERE status = 'Ocupado'")
        quartos = cursor.fetchall()
        conexao.close()

        for quarto in quartos:
            print("ID:", quarto[0])
            print("Numero:", quarto[1])
            print("Tipo:", quarto[2])

    except sqlite3.Error as erro:
        print("Erro ao listar quartos indisponiveis:", erro)

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
    except sqlite3.IntegrityError:
        print("Esse numero de quarto ja existe")
    except sqlite3.Error as erro:
        print("Erro ao atualizar quarto:", erro)

def excluir_quarto():
    try:
        listar_quartos()
        id_quarto = int(input("Digite o ID do quarto: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM quartos WHERE id = ?", (id_quarto,))
        conexao.commit()
        conexao.close()

        print("Quarto excluido com sucesso")

    except ValueError:
        print("Digite um numero valido")
    except sqlite3.IntegrityError:
        print("Nao e possivel excluir um quarto vinculado a uma reserva")
    except sqlite3.Error as erro:
        print("Erro ao excluir quarto:", erro)

def cadastrar_usuario():
    try:
        nome = input("Digite o nome do usuario: ")
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")
        tipo = input("Digite o tipo do usuario (Recepcionista / Cliente): ")

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
    except sqlite3.Error as erro:
        print("Erro ao cadastrar usuario:", erro)

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

    except sqlite3.Error as erro:
        print("Erro ao listar usuarios:", erro)

def cadastrar_reserva():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome FROM hospedes")
        hospedes = cursor.fetchall()

        for hospede in hospedes:
            print("ID:", hospede[0], "- Nome:", hospede[1])

        id_hospede = int(input("Digite o ID do hospede: "))

        cursor.execute("SELECT id FROM hospedes WHERE id = ?", (id_hospede,))
        if not cursor.fetchone():
            print("Hospede nao encontrado")
            conexao.close()
            return

        conexao.close()
        listar_quartos_disponiveis()

        id_quarto = int(input("Digite o ID do quarto: "))
        check_in = input("Digite a data de check-in (AAAA-MM-DD): ")
        check_out = input("Digite a data de check-out (AAAA-MM-DD): ")

        if check_out <= check_in:
            print("Erro: o check-out deve ser depois do check-in")
            return

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("SELECT status FROM quartos WHERE id = ?", (id_quarto,))
        quarto = cursor.fetchone()

        if not quarto:
            print("Quarto nao encontrado")
            conexao.close()
            return

        if quarto[0] == "Ocupado":
            print("Esse quarto ja esta ocupado")
            conexao.close()
            return

        cursor.execute(
            "SELECT id FROM reservas WHERE id_quarto = ? AND status = 'Ativa'",
            (id_quarto,)
        )

        if cursor.fetchone():
            print("Esse quarto ja possui uma reserva")
            conexao.close()
            return

        dias = int(input("Digite a quantidade de dias da reserva: "))

        if dias <= 0:
            print("Digite uma quantidade de dias valida")
            conexao.close()
            return

        desconto = 15 if dias >= 7 else 0

        cursor.execute(
            """
            INSERT INTO reservas
            (id_hospede, id_quarto, check_in, check_out, desconto, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (id_hospede, id_quarto, check_in, check_out, desconto, "Ativa")
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
    except sqlite3.Error as erro:
        print("Erro ao cadastrar reserva:", erro)

def listar_reservas():
    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT reservas.id, hospedes.nome, quartos.numero,
                   reservas.check_in, reservas.check_out,
                   reservas.desconto, reservas.status
            FROM reservas
            JOIN hospedes ON reservas.id_hospede = hospedes.id
            JOIN quartos ON reservas.id_quarto = quartos.id
        """)

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
            print("--------------------")

    except sqlite3.Error as erro:
        print("Erro ao listar reservas:", erro)

def cancelar_reserva():
    try:
        listar_reservas()
        id_reserva = int(input("Digite o ID da reserva: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id_quarto FROM reservas WHERE id = ? AND status = 'Ativa'",
            (id_reserva,)
        )
        reserva = cursor.fetchone()

        if not reserva:
            print("Reserva ativa nao encontrada")
            conexao.close()
            return

        cursor.execute(
            "UPDATE reservas SET status = 'Cancelada' WHERE id = ?",
            (id_reserva,)
        )
        cursor.execute(
            "UPDATE quartos SET status = 'Disponivel' WHERE id = ?",
            (reserva[0],)
        )

        conexao.commit()
        conexao.close()
        print("Reserva cancelada com sucesso")

    except ValueError:
        print("Digite um numero valido")
    except sqlite3.Error as erro:
        print("Erro ao cancelar reserva:", erro)

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
    except sqlite3.Error as erro:
        print("Erro ao cadastrar servico:", erro)

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

    except sqlite3.Error as erro:
        print("Erro ao listar servicos:", erro)

def lancar_consumo():
    try:
        listar_reservas()
        id_reserva = int(input("Digite o ID da reserva: "))

        listar_servicos()
        id_servico = int(input("Digite o ID do servico: "))
        quantidade = int(input("Digite a quantidade: "))

        if quantidade <= 0:
            print("A quantidade deve ser maior que zero")
            return

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id FROM reservas WHERE id = ? AND status = 'Ativa'",
            (id_reserva,)
        )
        if not cursor.fetchone():
            print("Reserva ativa nao encontrada")
            conexao.close()
            return

        cursor.execute("SELECT id FROM servicos WHERE id = ?", (id_servico,))
        if not cursor.fetchone():
            print("Servico nao encontrado")
            conexao.close()
            return

        cursor.execute(
            """
            INSERT INTO consumos (id_reserva, id_servico, quantidade)
            VALUES (?, ?, ?)
            """,
            (id_reserva, id_servico, quantidade)
        )

        conexao.commit()
        conexao.close()
        print("Consumo cadastrado com sucesso")

    except ValueError:
        print("Digite numeros validos")
    except sqlite3.Error as erro:
        print("Erro ao cadastrar consumo:", erro)

def gerar_conta():
    try:
        listar_reservas()
        id_reserva = int(input("Digite o ID da reserva: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT hospedes.nome, quartos.numero,
                   quartos.valor_diaria, reservas.desconto
            FROM reservas
            JOIN hospedes ON reservas.id_hospede = hospedes.id
            JOIN quartos ON reservas.id_quarto = quartos.id
            WHERE reservas.id = ?
        """, (id_reserva,))

        reserva = cursor.fetchone()

        if not reserva:
            print("Reserva nao encontrada")
            conexao.close()
            return

        nome = reserva[0]
        numero_quarto = reserva[1]
        valor_diaria = reserva[2]
        desconto = reserva[3]

        dias = int(input("Digite a quantidade de dias: "))

        if dias <= 0:
            print("Digite uma quantidade de dias valida")
            conexao.close()
            return

        valor_diarias = valor_diaria * dias
        valor_desconto = valor_diarias * desconto / 100
        valor_diarias -= valor_desconto

        cursor.execute("""
            SELECT servicos.nome, servicos.valor, consumos.quantidade
            FROM consumos
            JOIN servicos ON consumos.id_servico = servicos.id
            WHERE consumos.id_reserva = ?
        """, (id_reserva,))

        consumos = cursor.fetchall()
        conexao.close()

        total_servicos = 0

        print("Hospede:", nome)
        print("Quarto:", numero_quarto)
        print("Dias:", dias)
        print("Valor das diarias:", round(valor_diarias, 2))
        print("Desconto:", desconto, "%")

        for consumo in consumos:
            nome_servico = consumo[0]
            valor_servico = consumo[1]
            quantidade = consumo[2]
            subtotal = valor_servico * quantidade
            total_servicos += subtotal

            print(
                nome_servico,
                "Quantidade:", quantidade,
                "Valor:", round(subtotal, 2)
            )

        valor_final = valor_diarias + total_servicos

        print("Total dos servicos:", round(total_servicos, 2))
        print("Valor final:", round(valor_final, 2))

    except ValueError:
        print("Digite numeros validos")
    except sqlite3.Error as erro:
        print("Erro ao gerar conta:", erro)

def forma_pagamento():
    try:
        listar_reservas()
        id_reserva = int(input("Digite o ID da reserva: "))

        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()
        cursor.execute("SELECT id FROM reservas WHERE id = ?", (id_reserva,))
        reserva = cursor.fetchone()
        conexao.close()

        if not reserva:
            print("Reserva nao encontrada")
            return

        print("1 - Pix")
        print("2 - Cartao de credito")
        print("3 - Cartao de debito")
        print("4 - Dinheiro")

        opcao = int(input("Escolha a forma de pagamento: "))

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
    except sqlite3.Error as erro:
        print("Erro na forma de pagamento:", erro)
