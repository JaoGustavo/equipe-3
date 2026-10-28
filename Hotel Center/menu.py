import sqlite3

from banco import criar_banco, criar_usuarios_padrao

from hospede import (
    cadastrar_hospede,
    listar_hospedes,
    atualizar_hospede,
    excluir_hospede,
    relatorio_hospedes
)

from hotel import (
    cadastrar_quarto,
    listar_quartos,
    listar_quartos_disponiveis,
    listar_quartos_indisponiveis,
    atualizar_quarto,
    excluir_quarto,
    cadastrar_usuario,
    listar_usuarios,
    cadastrar_reserva,
    listar_reservas,
    cancelar_reserva,
    cadastrar_servico,
    listar_servicos,
    lancar_consumo,
    gerar_conta,
    forma_pagamento
)


def login():
    print("\n===== LOGIN HOTEL CENTER =====")

    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    try:
        conexao = sqlite3.connect("hotel_center.db")
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT nome, tipo
            FROM usuarios
            WHERE email = ? AND senha = ?
        """, (email, senha))

        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            print("Bem-vindo", usuario[0])
            return usuario[1]

        print("Email ou senha incorretos!")
        return None

    except sqlite3.Error as erro:
        print("Erro ao realizar login:", erro)
        return None


def menu():
    criar_banco()
    criar_usuarios_padrao()

    tipo_usuario = login()

    if tipo_usuario is None:
        print("Login invalido!")
        return

    while True:
        try:
            print("\n       HOTEL CENTER")

            if tipo_usuario == "Cliente":
                print("1 - Listar quartos disponiveis")
                print("2 - Cadastrar hospede")
                print("3 - Fazer reserva")
                print("4 - Listar servicos")
                print("5 - Cancelar reserva")
                print("6 - Sair")

                opcao = int(input("Escolha uma opcao: "))

                if opcao == 1:
                    listar_quartos_disponiveis()

                elif opcao == 2:
                    cadastrar_hospede()

                elif opcao == 3:
                    cadastrar_reserva()

                elif opcao == 4:
                    listar_servicos()

                elif opcao == 5:
                    cancelar_reserva()

                elif opcao == 6:
                    print("Saindo do Hotel Center...")
                    break

                else:
                    print("Opcao invalida")

            else:
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
                    print("Saindo do Hotel Center...")
                    break

                else:
                    print("Opcao invalida")

        except ValueError:
            print("Digite apenas numeros")

    menu()