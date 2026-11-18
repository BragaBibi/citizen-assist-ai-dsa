"""
GS 2026.2 - Citizen Assist AI (DSA)
Sistema de gerenciamento de servicos e orientacoes ao cidadao.

Estrutura principal: lista encadeada simples implementada manualmente.
Busca: linear (por id e por atributo, com busca de substring manual).
Ordenacao: Merge Sort adaptado para lista encadeada.
"""

# ---------------------------------------------------------------------------
# Modelo de dados
# ---------------------------------------------------------------------------

class Servico:
    """Registro de um servico ou orientacao ao cidadao."""

    def __init__(self, id_, titulo, categoria, descricao, publico_alvo, canal):
        self.id = id_
        self.titulo = titulo
        self.categoria = categoria
        self.descricao = descricao
        self.publico_alvo = publico_alvo
        self.canal = canal

    def __str__(self):
        return (
            f"[ID {self.id}] {self.titulo}\n"
            f"    Categoria    : {self.categoria}\n"
            f"    Descricao    : {self.descricao}\n"
            f"    Publico-alvo : {self.publico_alvo}\n"
            f"    Canal/Local  : {self.canal}"
        )


class No:
    """No da lista encadeada: guarda um Servico e a referencia ao proximo."""

    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


# ---------------------------------------------------------------------------
# Validacao e funcoes auxiliares (sem depender de funcoes prontas de busca)
# ---------------------------------------------------------------------------

CAMPOS_TEXTO = ["titulo", "categoria", "descricao", "publico_alvo", "canal"]


def validar_id(id_):
    """O identificador deve ser um inteiro positivo."""
    if isinstance(id_, bool) or not isinstance(id_, int) or id_ <= 0:
        raise ValueError("O identificador deve ser um numero inteiro positivo.")


def validar_texto(nome_campo, valor):
    """Campos de texto sao obrigatorios (nao podem ser vazios)."""
    if not isinstance(valor, str) or valor.strip() == "":
        raise ValueError(f"O campo '{nome_campo}' e obrigatorio e nao pode ficar vazio.")


def contem(texto, termo):
    """Busca de substring implementada manualmente (sem 'in' / find).
    Ignora diferenca entre maiusculas e minusculas.
    Custo: O(n*m), com n = len(texto) e m = len(termo)."""
    texto = texto.lower()
    termo = termo.lower()
    n, m = len(texto), len(termo)
    if m == 0:
        return True
    for i in range(n - m + 1):
        j = 0
        while j < m and texto[i + j] == termo[j]:
            j += 1
        if j == m:
            return True
    return False


def _chave(servico, criterio):
    """Valor usado na comparacao durante a ordenacao."""
    if criterio == "id":
        return servico.id
    if criterio == "titulo":
        return servico.titulo.lower()
    raise ValueError("Criterio de ordenacao invalido (use 'id' ou 'titulo').")


# ---------------------------------------------------------------------------
# Lista encadeada
# ---------------------------------------------------------------------------

class ListaEncadeada:
    """Lista encadeada simples com ponteiros para cabeca e cauda."""

    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    def esta_vazia(self):
        return self.cabeca is None

    # -- percurso ----------------------------------------------------------
    def percorrer(self):
        """Gera os servicos na ordem da lista. O(n)."""
        atual = self.cabeca
        while atual is not None:
            yield atual.dado
            atual = atual.proximo

    # -- busca por id ------------------------------------------------------
    def buscar_por_id(self, id_):
        """Busca linear. Retorna o Servico ou None. O(n)."""
        atual = self.cabeca
        while atual is not None:
            if atual.dado.id == id_:
                return atual.dado
            atual = atual.proximo
        return None

    # -- insercao ----------------------------------------------------------
    def inserir(self, servico):
        """Insere no final. Valida campos e unicidade do id.
        Verificar duplicidade custa O(n); a insercao em si e O(1) (usa cauda)."""
        validar_id(servico.id)
        for campo in CAMPOS_TEXTO:
            validar_texto(campo, getattr(servico, campo))
        if self.buscar_por_id(servico.id) is not None:
            raise ValueError(f"Ja existe um registro com o identificador {servico.id}.")

        self._anexar(servico)

    def _anexar(self, servico):
        """Liga um novo no ao final da lista, sem validar. O(1)."""
        novo = No(servico)
        if self.cabeca is None:
            self.cabeca = novo
            self.cauda = novo
        else:
            self.cauda.proximo = novo
            self.cauda = novo
        self.tamanho += 1

    # -- atualizacao -------------------------------------------------------
    def atualizar(self, id_, **novos_valores):
        """Atualiza campos de texto de um registro existente. O(n)."""
        servico = self.buscar_por_id(id_)
        if servico is None:
            return False
        # valida tudo antes de alterar (nao deixa o registro pela metade)
        for campo, valor in novos_valores.items():
            if campo not in CAMPOS_TEXTO:
                raise ValueError(f"Campo '{campo}' nao pode ser atualizado.")
            validar_texto(campo, valor)
        for campo, valor in novos_valores.items():
            setattr(servico, campo, valor.strip())
        return True

    # -- remocao -----------------------------------------------------------
    def remover(self, id_):
        """Remove o no com o id informado. Trata cabeca, meio e cauda. O(n)."""
        anterior = None
        atual = self.cabeca
        while atual is not None and atual.dado.id != id_:
            anterior = atual
            atual = atual.proximo
        if atual is None:
            return False

        if anterior is None:                 # remove a cabeca
            self.cabeca = atual.proximo
        else:
            anterior.proximo = atual.proximo
        if atual is self.cauda:              # remove a cauda
            self.cauda = anterior
        atual.proximo = None                 # desconecta o no removido
        self.tamanho -= 1
        return True

    # -- pesquisa por atributo --------------------------------------------
    def pesquisar(self, atributo, termo):
        """Retorna uma nova ListaEncadeada com os registros cujo atributo
        contem o termo. Percorre a lista inteira: O(n * m)."""
        if atributo not in ("titulo", "categoria"):
            raise ValueError("Pesquisa disponivel apenas por 'titulo' ou 'categoria'.")
        resultado = ListaEncadeada()
        for servico in self.percorrer():
            if contem(getattr(servico, atributo), termo):
                resultado._anexar(Servico(servico.id, servico.titulo, servico.categoria,
                                          servico.descricao, servico.publico_alvo,
                                          servico.canal))
        return resultado

    # -- ordenacao (Merge Sort para lista encadeada) ----------------------
    def ordenar(self, criterio="id"):
        """Ordena a lista in-place por 'id' ou 'titulo'. O(n log n)."""
        _chave(Servico(0, "", "", "", "", ""), criterio)  # valida o criterio
        self.cabeca = self._merge_sort(self.cabeca, criterio)
        # reposiciona a cauda
        atual = self.cabeca
        self.cauda = None
        while atual is not None:
            self.cauda = atual
            atual = atual.proximo

    def _merge_sort(self, cabeca, criterio):
        if cabeca is None or cabeca.proximo is None:
            return cabeca
        meio = self._dividir(cabeca)
        esquerda = self._merge_sort(cabeca, criterio)
        direita = self._merge_sort(meio, criterio)
        return self._mesclar(esquerda, direita, criterio)

    @staticmethod
    def _dividir(cabeca):
        """Divide a lista ao meio (lento/rapido) e devolve a 2a metade."""
        lento = cabeca
        rapido = cabeca.proximo
        while rapido is not None and rapido.proximo is not None:
            lento = lento.proximo
            rapido = rapido.proximo.proximo
        segunda = lento.proximo
        lento.proximo = None
        return segunda

    @staticmethod
    def _mesclar(a, b, criterio):
        """Intercala duas listas ordenadas (estavel)."""
        sentinela = No(None)
        fim = sentinela
        while a is not None and b is not None:
            if _chave(a.dado, criterio) <= _chave(b.dado, criterio):
                fim.proximo = a
                a = a.proximo
            else:
                fim.proximo = b
                b = b.proximo
            fim = fim.proximo
        fim.proximo = a if a is not None else b
        return sentinela.proximo


# ---------------------------------------------------------------------------
# Interface: menu interativo
# ---------------------------------------------------------------------------

def ler_texto_obrigatorio(rotulo):
    while True:
        valor = input(f"{rotulo}: ").strip()
        try:
            validar_texto(rotulo, valor)
            return valor
        except ValueError as erro:
            print(f"  Erro: {erro}")


def ler_inteiro(rotulo):
    while True:
        bruto = input(f"{rotulo}: ").strip()
        try:
            numero = int(bruto)
            validar_id(numero)
            return numero
        except ValueError:
            print("  Erro: informe um numero inteiro positivo.")


def exibir_lista(lista, titulo="Registros"):
    if lista.esta_vazia():
        print("  Nenhum registro encontrado.")
        return
    print(f"--- {titulo} ({lista.tamanho}) ---")
    for servico in lista.percorrer():
        print(servico)
        print()


def acao_cadastrar(lista):
    print("--- Cadastrar servico ---")
    while True:
        id_ = ler_inteiro("ID")
        if lista.buscar_por_id(id_) is not None:
            print(f"  Erro: ja existe um registro com o ID {id_}. Escolha outro.")
        else:
            break
    servico = Servico(
        id_,
        ler_texto_obrigatorio("Titulo"),
        ler_texto_obrigatorio("Categoria"),
        ler_texto_obrigatorio("Descricao"),
        ler_texto_obrigatorio("Publico-alvo"),
        ler_texto_obrigatorio("Canal/Local de atendimento"),
    )
    lista.inserir(servico)
    print("  Servico cadastrado com sucesso.")


def acao_consultar(lista):
    id_ = ler_inteiro("ID para consulta")
    servico = lista.buscar_por_id(id_)
    if servico is None:
        print(f"  Registro com ID {id_} nao encontrado.")
    else:
        print(servico)


def acao_atualizar(lista):
    id_ = ler_inteiro("ID do registro a atualizar")
    servico = lista.buscar_por_id(id_)
    if servico is None:
        print(f"  Registro com ID {id_} nao encontrado.")
        return
    print(servico)
    print("Deixe em branco para manter o valor atual.")
    novos = {}
    for campo in CAMPOS_TEXTO:
        valor = input(f"Novo {campo} [{getattr(servico, campo)}]: ").strip()
        if valor != "":
            novos[campo] = valor
    if not novos:
        print("  Nada foi alterado.")
        return
    lista.atualizar(id_, **novos)
    print("  Registro atualizado com sucesso.")


def acao_excluir(lista):
    id_ = ler_inteiro("ID do registro a excluir")
    if lista.remover(id_):
        print("  Registro excluido com sucesso.")
    else:
        print(f"  Registro com ID {id_} nao encontrado.")


def acao_pesquisar(lista):
    print("Pesquisar por: 1) Titulo  2) Categoria")
    opcao = input("Opcao: ").strip()
    if opcao not in ("1", "2"):
        print("  Opcao invalida.")
        return
    atributo = "titulo" if opcao == "1" else "categoria"
    termo = ler_texto_obrigatorio("Termo de pesquisa")
    exibir_lista(lista.pesquisar(atributo, termo), f"Resultado ({atributo})")


def acao_ordenar(lista):
    print("Ordenar por: 1) ID  2) Titulo")
    opcao = input("Opcao: ").strip()
    if opcao not in ("1", "2"):
        print("  Opcao invalida.")
        return
    if lista.esta_vazia():
        print("  A lista esta vazia; nada para ordenar.")
        return
    lista.ordenar("id" if opcao == "1" else "titulo")
    print("  Lista ordenada com sucesso.")


DADOS_EXEMPLO = [
    (3, "Emissao de RG", "Documentos", "Emissao da 1a e 2a via do RG.",
     "Todos os cidadaos", "Poupatempo / agendamento online"),
    (1, "Bolsa Familia - Cadastro", "Assistencia Social", "Inscricao no CadUnico.",
     "Familias de baixa renda", "CRAS do bairro"),
    (5, "Matricula Escolar", "Educacao", "Matricula na rede publica de ensino.",
     "Responsaveis por estudantes", "Secretaria de Educacao"),
    (2, "Vacinacao", "Saude", "Calendario de vacinas gratuitas.",
     "Todas as idades", "UBS mais proxima"),
    (4, "Mediacao de Conflitos", "Atendimento Comunitario", "Orientacao e mediacao.",
     "Moradores da comunidade", "Centro Comunitario"),
]


def carregar_exemplos(lista):
    novos = 0
    for dados in DADOS_EXEMPLO:
        try:
            lista.inserir(Servico(*dados))
            novos += 1
        except ValueError:
            pass  # ja existe: ignora
    print(f"  {novos} registro(s) de exemplo carregado(s).")


MENU = """
===== Citizen Assist AI =====
1 - Cadastrar servico
2 - Consultar por ID
3 - Listar todos
4 - Atualizar
5 - Excluir
6 - Pesquisar (titulo/categoria)
7 - Ordenar (id/titulo)
8 - Carregar dados de exemplo
0 - Sair
"""


def main():
    lista = ListaEncadeada()
    while True:
        print(MENU)
        opcao = input("Escolha uma opcao: ").strip()
        if opcao == "1":
            acao_cadastrar(lista)
        elif opcao == "2":
            acao_consultar(lista)
        elif opcao == "3":
            exibir_lista(lista, "Todos os registros")
        elif opcao == "4":
            acao_atualizar(lista)
        elif opcao == "5":
            acao_excluir(lista)
        elif opcao == "6":
            acao_pesquisar(lista)
        elif opcao == "7":
            acao_ordenar(lista)
        elif opcao == "8":
            carregar_exemplos(lista)
        elif opcao == "0":
            print("Encerrando o sistema. Ate logo!")
            break
        else:
            print("  Opcao invalida. Escolha um numero do menu.")


if __name__ == "__main__":
    main()
