"""
Testes automatizados dos cenarios exigidos (GS 2026.2 - Citizen Assist AI).
Execute:  python testes.py
Cada cenario imprime: Entrada, Esperado, Observado e o resultado (OK/FALHA).
"""
from citizen_assist import ListaEncadeada, Servico, validar_id

total = 0
aprovados = 0


def ids(lista):
    return [s.id for s in lista.percorrer()]


def cenario(numero, nome, entrada, esperado, observado):
    global total, aprovados
    total += 1
    ok = esperado == observado
    aprovados += 1 if ok else 0
    print(f"[T{numero:02d}] {nome}")
    print(f"   Entrada   : {entrada}")
    print(f"   Esperado  : {esperado}")
    print(f"   Observado : {observado}")
    print(f"   Resultado : {'OK' if ok else 'FALHA'}\n")


def erro_de(funcao):
    try:
        funcao()
        return "sem erro"
    except ValueError as e:
        return f"ValueError: {e}"


def novo(id_, titulo, categoria="Saude"):
    return Servico(id_, titulo, categoria, "Descricao", "Todos", "UBS")


# ---------------- Lista vazia ----------------
vazia = ListaEncadeada()
cenario(1, "Listar com lista vazia", "listar()", [], ids(vazia))
cenario(2, "Consultar ID em lista vazia", "buscar_por_id(1)", None, vazia.buscar_por_id(1))
cenario(3, "Excluir em lista vazia", "remover(1)", False, vazia.remover(1))
vazia.ordenar("id")
cenario(4, "Ordenar lista vazia", "ordenar('id')", [], ids(vazia))
cenario(5, "Pesquisar em lista vazia", "pesquisar('titulo','x')", [],
        ids(vazia.pesquisar("titulo", "x")))

# ---------------- Cadastro ----------------
lista = ListaEncadeada()
lista.inserir(novo(3, "Emissao de RG", "Documentos"))
lista.inserir(novo(1, "Bolsa Familia", "Assistencia Social"))
lista.inserir(novo(5, "Matricula Escolar", "Educacao"))
lista.inserir(novo(2, "Vacinacao", "Saude"))
lista.inserir(novo(4, "Mediacao de Conflitos", "Atendimento Comunitario"))
cenario(6, "Cadastrar 5 registros", "IDs 3,1,5,2,4", [3, 1, 5, 2, 4], ids(lista))

cenario(7, "Cadastro com ID duplicado", "inserir(ID 3)",
        "ValueError: Ja existe um registro com o identificador 3.",
        erro_de(lambda: lista.inserir(novo(3, "Outro"))))
cenario(8, "Cadastro com titulo vazio", "inserir(titulo='   ')",
        "ValueError: O campo 'titulo' e obrigatorio e nao pode ficar vazio.",
        erro_de(lambda: lista.inserir(novo(9, "   "))))
cenario(9, "Cadastro com ID invalido (negativo)", "inserir(ID -5)",
        "ValueError: O identificador deve ser um numero inteiro positivo.",
        erro_de(lambda: lista.inserir(novo(-5, "Teste"))))
cenario(10, "Cadastro com ID de tipo incompativel", "inserir(ID 'abc')",
        "ValueError: O identificador deve ser um numero inteiro positivo.",
        erro_de(lambda: lista.inserir(novo("abc", "Teste"))))
cenario(11, "Tamanho nao muda apos erros", "tamanho", 5, lista.tamanho)

# ---------------- Consulta ----------------
cenario(12, "Consultar ID existente", "buscar_por_id(2)", "Vacinacao",
        lista.buscar_por_id(2).titulo)
cenario(13, "Consultar ID inexistente", "buscar_por_id(99)", None, lista.buscar_por_id(99))

# ---------------- Atualizacao ----------------
lista.atualizar(2, titulo="Vacinacao Gratuita", canal="UBS / Escola")
s = lista.buscar_por_id(2)
cenario(14, "Atualizar registro existente", "atualizar(2, titulo=..., canal=...)",
        ("Vacinacao Gratuita", "UBS / Escola"), (s.titulo, s.canal))
cenario(15, "Atualizar ID inexistente", "atualizar(99, titulo='x')", False,
        lista.atualizar(99, titulo="x"))
cenario(16, "Atualizar com valor vazio", "atualizar(2, titulo='')",
        "ValueError: O campo 'titulo' e obrigatorio e nao pode ficar vazio.",
        erro_de(lambda: lista.atualizar(2, titulo="")))
cenario(17, "Registro intacto apos atualizacao invalida", "titulo do ID 2",
        "Vacinacao Gratuita", lista.buscar_por_id(2).titulo)

# ---------------- Pesquisa ----------------
cenario(18, "Pesquisar por titulo (parcial, sem diferenciar maiusculas)",
        "pesquisar('titulo','VACINA')", [2], ids(lista.pesquisar("titulo", "VACINA")))
cenario(19, "Pesquisar por categoria", "pesquisar('categoria','educ')", [5],
        ids(lista.pesquisar("categoria", "educ")))
cenario(20, "Pesquisar sem resultados", "pesquisar('titulo','zzz')", [],
        ids(lista.pesquisar("titulo", "zzz")))
cenario(21, "Pesquisar por atributo invalido", "pesquisar('canal','x')",
        "ValueError: Pesquisa disponivel apenas por 'titulo' ou 'categoria'.",
        erro_de(lambda: lista.pesquisar("canal", "x")))

# ---------------- Ordenacao ----------------
lista.ordenar("id")
cenario(22, "Ordenar por ID", "ordenar('id')", [1, 2, 3, 4, 5], ids(lista))
lista.ordenar("titulo")
titulos = [s.titulo for s in lista.percorrer()]
cenario(23, "Ordenar por titulo", "ordenar('titulo')",
        ["Bolsa Familia", "Emissao de RG", "Matricula Escolar",
         "Mediacao de Conflitos", "Vacinacao Gratuita"], titulos)
cenario(24, "Criterio de ordenacao invalido", "ordenar('canal')",
        "ValueError: Criterio de ordenacao invalido (use 'id' ou 'titulo').",
        erro_de(lambda: lista.ordenar("canal")))

# cauda correta apos ordenar: inserir deve ir ao final
lista.ordenar("id")
lista.inserir(novo(6, "Novo Servico"))
cenario(25, "Inserir apos ordenar (cauda correta)", "inserir(ID 6)",
        [1, 2, 3, 4, 5, 6], ids(lista))

# ---------------- Exclusao ----------------
r = lista.remover(1)
cenario(26, "Excluir cabeca", "remover(1)", ([2, 3, 4, 5, 6], True), (ids(lista), r))
r = lista.remover(4)
cenario(27, "Excluir no meio", "remover(4)", ([2, 3, 5, 6], True), (ids(lista), r))
r = lista.remover(6)
cenario(28, "Excluir cauda", "remover(6)", ([2, 3, 5], True), (ids(lista), r))
lista.inserir(novo(7, "Apos remover cauda"))
cenario(29, "Inserir apos remover cauda", "inserir(ID 7)", [2, 3, 5, 7], ids(lista))
cenario(30, "Excluir ID inexistente", "remover(99)", False, lista.remover(99))
cenario(31, "Tamanho apos exclusoes", "tamanho", 4, lista.tamanho)
for i in (2, 3, 5, 7):
    lista.remover(i)
cenario(32, "Esvaziar a lista por completo", "remover todos",
        ([], 0, True), (ids(lista), lista.tamanho, lista.esta_vazia()))

print("=" * 50)
print(f"Resumo: {aprovados}/{total} cenarios aprovados")
