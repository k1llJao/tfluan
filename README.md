# TF-11 — Refatoração da Loja Feia

## 1. Normalização

Normalizar significa guardar cada informação em um lugar só, em vez de copiar ela em vários objetos. Na loja feia, os dados da Ana (nome, CPF, endereço) eram repetidos dentro do pedido 1 e do pedido 3. Se o e-mail dela mudasse, era preciso atualizar os dois. Depois da refatoração, existe um único objeto `Cliente` para a Ana, e os dois pedidos apontam para ele — mudar uma vez muda para todos.

## 2. Obsessão por tipos primitivos

Uma string qualquer aceita `"abc"` como CPF sem reclamar. Ao criar a classe `Cpf`, a validação fica no construtor: qualquer CPF inválido levanta `ValueError` na hora em que é criado, antes de chegar a qualquer outra parte do sistema. O programa ganhou uma garantia: se um `Cpf` existe, ele é válido. O `Dinheiro` guarda centavos como `int` porque `float` não representa dinheiro com precisão — `0.1 + 0.2` em float dá `0.30000000000000004`, o que causaria erros de arredondamento em totais e descontos.

## 3. Diga, não pergunte

Antes, o código de fora perguntava o status do pedido (`get_status()`) e então decidia o que fazer. Depois, basta chamar `pedido.pagar()` e o próprio pedido aplica as regras: só paga se estiver aberto e tiver itens. A regra ficou melhor dentro do `Pedido` porque é ele quem conhece seu estado — nenhum código externo precisa saber os detalhes de quando um pagamento é possível ou não.

## 4. Fail first

O hadouken era a função `valida()` com quatro `if`s aninhados, cada um dentro do anterior, em forma de pirâmide. Ele foi eliminado de duas formas: nas validações de `Cpf`, `Email` e `Cep`, cada regra faz uma verificação e retorna o erro imediatamente se falhar, sem entrar em outro `if`. No desconto por tipo de cliente, o `if/elif/else` foi substituído por polimorfismo — cada tipo (`TipoNormal`, `TipoVip`, `TipoFuncionario`) sabe calcular seu próprio desconto, sem precisar de condicionais.

## 5. Modularização — classes criadas

| Classe | Responsabilidade |
|---|---|
| `Cpf` | Guardar e validar um CPF de 11 dígitos. |
| `Email` | Guardar e validar um e-mail com `@` e não vazio. |
| `Cep` | Guardar e validar um CEP de 8 dígitos. |
| `Dinheiro` | Guardar um valor monetário em centavos inteiros e operar sobre ele. |
| `Status` | Guardar o estado de um pedido (aberto, pago, cancelado) e descrevê-lo. |
| `TipoNormal` | Representar o tipo de cliente normal, com desconto zero. |
| `TipoVip` | Representar o tipo de cliente VIP, com desconto de 10%. |
| `TipoFuncionario` | Representar o tipo de cliente funcionário, com desconto de 20%. |
| `Pessoa` | Guardar nome, CPF e e-mail de uma pessoa. |
| `Endereco` | Guardar rua, cidade e CEP de um endereço. |
| `Cliente` | Associar uma pessoa, um endereço e um tipo de desconto. |
| `Produto` | Guardar nome e preço de um produto. |
| `ItemDoPedido` | Guardar produto e quantidade de uma linha do pedido e calcular seu subtotal. |
| `ItensDoPedido` | Encapsular a lista de itens de um pedido e operar sobre ela. |
| `Pedido` | Associar cliente e itens, controlar o status e calcular totais. |
| `Pedidos` | Encapsular o dicionário de todos os pedidos da loja e gerar relatórios. |

## 6. Dívida técnica

Não ficou nenhuma regra sem aplicar. A mais difícil foi o **polimorfismo para o desconto** (passo 8). Substituir um `if/elif/else` por três classes parece exagero para três casos simples, mas é o que garante que adicionar um novo tipo de cliente no futuro não exige tocar em nenhum código existente — só criar uma nova classe. Entender isso como vantagem, e não como complicação, foi o que levou mais tempo.
