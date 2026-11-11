# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                      # todos os pedidos da loja: lista solta, global


class Pedido:
    def __init__(self, numero, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua, cidade, cep, tipo):
        self.numero = numero            # numero do pedido
        self.nome_do_cliente = nome_do_cliente    # os dados do cliente se repetem em CADA pedido dele
        self.cpf_do_cliente = cpf_do_cliente
        self.email_do_cliente = email_do_cliente
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo          # tipo do cliente: "N" normal, "V" vip, "F" funcionario
        self.itens = []       # cada item e uma lista: [produto, quantidade, preco]
        self.status = "A"         # A = aberto, P = pago, C = cancelado

    def get_status(self):
        return self.status

    def set_status(self, valor):
        self.status = valor


def valida(email_do_cliente, cpf_do_cliente, cep):
    if len(email_do_cliente) > 0:
        if "@" in email_do_cliente:
            if len(cpf_do_cliente) == 11:
                if len(cep) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def novo_pedido(numero, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua, cidade, cep, tipo):
    resultado = valida(email_do_cliente, cpf_do_cliente, cep)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)
        return None
    else:
        pedido = Pedido(numero, nome_do_cliente, cpf_do_cliente, email_do_cliente, rua, cidade, cep, tipo)
        pedidos.append(pedido)
        return pedido


def add_item(pedido, produto, quantidade, preco):
    pedido.itens.append([produto, quantidade, preco])


def total(pedido):
    total_acumulado = 0
    for item in pedido.itens:
        total_acumulado = total_acumulado + item[1] * item[2]
    return total_acumulado


def calcular_desconto(tipo, total_acumulado):
    if tipo == "V":
        desconto = total_acumulado * 0.10
    elif tipo == "F":
        desconto = total_acumulado * 0.20
    else:
        desconto = 0
    return desconto


def calcular_valor_a_pagar(pedido):
    return total(pedido) - calcular_desconto(pedido.tipo, total(pedido))


def pagar(pedido):
    if pedido.get_status() == "A":
        if len(pedido.itens) > 0:
            pedido.set_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status() == "A":
        pedido.set_status("C")
        return True
    else:
        return False


def descrever_status(status):
    if status == "A":
        return "aberto"
    elif status == "P":
        return "pago"
    else:
        return "cancelado"


def relatorio():
    for pedido in pedidos:
        print("Pedido", pedido.numero, "-", pedido.nome_do_cliente, "-", pedido.cidade)
        print("  status:", descrever_status(pedido.get_status()))
        for item in pedido.itens:
            print("  ", item[1], "x", item[0], "= R$ %.2f" % (item[1] * item[2]))
        if len(pedido.itens) > 0:
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (total(pedido), calcular_desconto(pedido.tipo, total(pedido)), calcular_valor_a_pagar(pedido)))


def arrecadado():
    total_arrecadado = 0
    for pedido in pedidos:
        if pedido.get_status() == "P":
            total_arrecadado = total_arrecadado + calcular_valor_a_pagar(pedido)
    return total_arrecadado


def qtd_abertos():
    quantidade = 0
    for pedido in pedidos:
        if pedido.get_status() == "A":
            quantidade = quantidade + 1
    return quantidade


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
pedido_da_ana = novo_pedido(1, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
add_item(pedido_da_ana, "Caderno", 2, 15.5)
add_item(pedido_da_ana, "Caneta", 5, 2.5)

novo_pedido(2, "Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")

pedido_da_ana_2 = novo_pedido(3, "Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
add_item(pedido_da_ana_2, "Livro", 1, 89.5)

novo_pedido(4, "Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")

pedido_do_diego = novo_pedido(5, "Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")

pedido_da_eva = novo_pedido(6, "Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
add_item(pedido_da_eva, "Fone", 1, 60.0)

novo_pedido(7, "Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")

pedido_do_gil = novo_pedido(8, "Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
add_item(pedido_do_gil, "Fone", 2, 60.0)

print("pagar 1:", pagar(pedido_da_ana))
print("pagar 3:", pagar(pedido_da_ana_2))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(pedido_da_ana))

relatorio()
print("arrecadado: R$ %.2f" % arrecadado())
print("abertos:", qtd_abertos())
