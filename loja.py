# CODIGO FEIO DE PROPOSITO (TF 11). Funciona, mas viola quase todas as regras do
# Object Calisthenics. A missao e consertar SEM mudar o que ele imprime.
# Rodar no terminal: python3 loja_feia.py


class Cpf:
    def __init__(self, valor):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self.valor = valor


class Email:
    def __init__(self, valor):
        if len(valor) == 0:
            raise ValueError("email vazio")
        if "@" not in valor:
            raise ValueError("email invalido")
        self.valor = valor


class Cep:
    def __init__(self, valor):
        if len(valor) != 8:
            raise ValueError("cep invalido")
        self.valor = valor


class Dinheiro:
    def __init__(self, reais):
        self.centavos = round(reais * 100)

    def somar(self, outro):
        resultado = Dinheiro(0)
        resultado.centavos = self.centavos + outro.centavos
        return resultado

    def subtrair(self, outro):
        resultado = Dinheiro(0)
        resultado.centavos = self.centavos - outro.centavos
        return resultado

    def multiplicar(self, quantidade):
        resultado = Dinheiro(0)
        resultado.centavos = self.centavos * quantidade
        return resultado

    def percentual(self, taxa):
        resultado = Dinheiro(0)
        resultado.centavos = round(self.centavos * taxa)
        return resultado

    def __str__(self):
        reais = self.centavos // 100
        centavos = self.centavos % 100
        return "R$ %d.%02d" % (reais, centavos)


class Status:
    ABERTO = "A"
    PAGO = "P"
    CANCELADO = "C"

    def __init__(self, codigo="A"):
        self.codigo = codigo

    def descricao(self):
        if self.codigo == Status.ABERTO:
            return "aberto"
        elif self.codigo == Status.PAGO:
            return "pago"
        else:
            return "cancelado"

    def esta_aberto(self):
        return self.codigo == Status.ABERTO


class Pessoa:
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = Cpf(cpf)
        self.email = Email(email)


class Endereco:
    def __init__(self, rua, cidade, cep):
        self.rua = rua
        self.cidade = cidade
        self.cep = Cep(cep)


class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.pessoa = Pessoa(nome, cpf, email)
        self.endereco = Endereco(rua, cidade, cep)
        self.tipo = tipo          # tipo do cliente: "N" normal, "V" vip, "F" funcionario


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = Dinheiro(preco)


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade


class ItensDoPedido:
    def __init__(self):
        self._itens = []

    def adicionar(self, produto, quantidade):
        self._itens.append(ItemDoPedido(produto, quantidade))

    def esta_vazia(self):
        return len(self._itens) == 0

    def calcular_total(self):
        total_acumulado = Dinheiro(0)
        for item in self._itens:
            total_acumulado = total_acumulado.somar(item.produto.preco.multiplicar(item.quantidade))
        return total_acumulado

    def imprimir(self):
        for item in self._itens:
            print("  ", item.quantidade, "x", item.produto.nome, "=", item.produto.preco.multiplicar(item.quantidade))


class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = ItensDoPedido()
        self.status = Status()

    def get_status(self):
        return self.status

    def set_status(self, codigo):
        self.status = Status(codigo)

    def calcular_desconto(self):
        total_acumulado = self.itens.calcular_total()
        if self.cliente.tipo == "V":
            return total_acumulado.percentual(0.10)
        elif self.cliente.tipo == "F":
            return total_acumulado.percentual(0.20)
        else:
            return Dinheiro(0)

    def calcular_valor_a_pagar(self):
        return self.itens.calcular_total().subtrair(self.calcular_desconto())


def pagar(pedido):
    if pedido.get_status().esta_aberto():
        if not pedido.itens.esta_vazia():
            pedido.set_status("P")
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status().esta_aberto():
        pedido.set_status("C")
        return True
    else:
        return False


class Pedidos:
    def __init__(self):
        self._pedidos = {}

    def criar(self, numero, cliente):
        pedido = Pedido(cliente)
        self._pedidos[numero] = pedido
        return pedido

    def relatorio(self):
        for numero, pedido in self._pedidos.items():
            print("Pedido", numero, "-", pedido.cliente.pessoa.nome, "-", pedido.cliente.endereco.cidade)
            print("  status:", pedido.get_status().descricao())
            pedido.itens.imprimir()
            if not pedido.itens.esta_vazia():
                print("  total:", pedido.itens.calcular_total(), "| desconto:", pedido.calcular_desconto(), "| a pagar:", pedido.calcular_valor_a_pagar())

    def arrecadado(self):
        total_arrecadado = Dinheiro(0)
        for pedido in self._pedidos.values():
            if pedido.get_status().codigo == Status.PAGO:
                total_arrecadado = total_arrecadado.somar(pedido.calcular_valor_a_pagar())
        return total_arrecadado

    def qtd_abertos(self):
        quantidade = 0
        for pedido in self._pedidos.values():
            if pedido.get_status().esta_aberto():
                quantidade = quantidade + 1
        return quantidade


# --- o roteiro da loja (o TF mantem esta saida identica) -----------------------
loja = Pedidos()

caderno = Produto("Caderno", 15.5)
caneta = Produto("Caneta", 2.5)
livro = Produto("Livro", 89.5)
fone = Produto("Fone", 60.0)

try:
    ana = Cliente("Ana Souza", "12345678901", "ana@mail.com", "Rua das Flores, 10", "Sorocaba", "18010000", "V")
    pedido_da_ana = loja.criar(1, ana)
    pedido_da_ana.itens.adicionar(caderno, 2)
    pedido_da_ana.itens.adicionar(caneta, 5)
except ValueError as erro:
    print("pedido 1 recusado:", erro)
    pedido_da_ana = None

try:
    bruno = Cliente("Bruno Lima", "123", "bruno@mail.com", "Av. Central, 200", "Votorantim", "18110000", "N")
    loja.criar(2, bruno)
except ValueError as erro:
    print("pedido 2 recusado:", erro)

try:
    pedido_da_ana_2 = loja.criar(3, ana)
    pedido_da_ana_2.itens.adicionar(livro, 1)
except ValueError as erro:
    print("pedido 3 recusado:", erro)
    pedido_da_ana_2 = None

try:
    carla = Cliente("Carla Dias", "98765432100", "carla.mail.com", "Rua do Sol, 55", "Sorocaba", "18020000", "F")
    loja.criar(4, carla)
except ValueError as erro:
    print("pedido 4 recusado:", erro)

try:
    diego = Cliente("Diego Rocha", "11122233344", "diego@mail.com", "Rua Nova, 7", "Itu", "13300000", "N")
    pedido_do_diego = loja.criar(5, diego)
except ValueError as erro:
    print("pedido 5 recusado:", erro)
    pedido_do_diego = None

try:
    eva = Cliente("Eva Nunes", "55566677788", "eva@mail.com", "Alameda Azul, 1", "Itu", "13300001", "F")
    pedido_da_eva = loja.criar(6, eva)
    pedido_da_eva.itens.adicionar(fone, 1)
except ValueError as erro:
    print("pedido 6 recusado:", erro)
    pedido_da_eva = None

try:
    fabio = Cliente("Fabio Costa", "99988877766", "fabio@mail.com", "Rua Velha, 3", "Itu", "123", "N")
    loja.criar(7, fabio)
except ValueError as erro:
    print("pedido 7 recusado:", erro)

try:
    gil = Cliente("Gil Alves", "44455566677", "gil@mail.com", "Rua do Meio, 9", "Sorocaba", "18030000", "N")
    pedido_do_gil = loja.criar(8, gil)
    pedido_do_gil.itens.adicionar(fone, 2)
except ValueError as erro:
    print("pedido 8 recusado:", erro)
    pedido_do_gil = None

print("pagar 1:", pagar(pedido_da_ana))
print("pagar 3:", pagar(pedido_da_ana_2))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(pedido_da_ana))

loja.relatorio()
print("arrecadado:", loja.arrecadado())
print("abertos:", loja.qtd_abertos())
