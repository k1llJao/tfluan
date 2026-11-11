# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py

pedidos = []                      # todos os pedidos da loja: lista solta, global


class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo          # tipo do cliente: "N" normal, "V" vip, "F" funcionario


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []           # lista de ItemDoPedido
        self.status = "A"         # A = aberto, P = pago, C = cancelado

    def get_status(self):
        return self.status

    def set_status(self, valor):
        self.status = valor


def valida(cliente):
    if len(cliente.email) > 0:
        if "@" in cliente.email:
            if len(cliente.cpf) == 11:
                if len(cliente.cep) == 8:
                    return "ok"
                else:
                    return "cep invalido"
            else:
                return "cpf invalido"
        else:
            return "email invalido"
    else:
        return "email vazio"


def novo_pedido(numero, cliente):
    resultado = valida(cliente)
    if resultado != "ok":
        print("pedido", numero, "recusado:", resultado)
        return None
    else:
        pedido = Pedido(numero, cliente)
        pedidos.append(pedido)
        return pedido


def add_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def total(pedido):
    total_acumulado = 0
    for item in pedido.itens:
        total_acumulado = total_acumulado + item.quantidade * item.produto.preco
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
    return total(pedido) - calcular_desconto(pedido.cliente.tipo, total(pedido))


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
        print("Pedido", pedido.numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
        print("  status:", descrever_status(pedido.get_status()))
        for item in pedido.itens:
            print("  ", item.quantidade, "x", item.produto.nome, "= R$ %.2f" % (item.quantidade * item.produto.preco))
        if len(pedido.itens) > 0:
            print("  total: R$ %.2f | desconto: R$ %.2f | a pagar: R$ %.2f" % (total(pedido), calcular_desconto(pedido.cliente.tipo, total(pedido)), calcular_valor_a_pagar(pedido)))


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
ana = Cliente("Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
bruno = Cliente("Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")
carla = Cliente("Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")
diego = Cliente("Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")
eva = Cliente("Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
fabio = Cliente("Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")
gil = Cliente("Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")

caderno = Produto("Caderno", 15.5)
caneta = Produto("Caneta", 2.5)
livro = Produto("Livro", 89.5)
fone = Produto("Fone", 60.0)

pedido_da_ana = novo_pedido(1, ana)
add_item(pedido_da_ana, caderno, 2)
add_item(pedido_da_ana, caneta, 5)

novo_pedido(2, bruno)

pedido_da_ana_2 = novo_pedido(3, ana)
add_item(pedido_da_ana_2, livro, 1)

novo_pedido(4, carla)

pedido_do_diego = novo_pedido(5, diego)

pedido_da_eva = novo_pedido(6, eva)
add_item(pedido_da_eva, fone, 1)

novo_pedido(7, fabio)

pedido_do_gil = novo_pedido(8, gil)
add_item(pedido_do_gil, fone, 2)

print("pagar 1:", pagar(pedido_da_ana))
print("pagar 3:", pagar(pedido_da_ana_2))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(pedido_da_ana))

relatorio()
print("arrecadado: R$ %.2f" % arrecadado())
print("abertos:", qtd_abertos())
