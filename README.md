# GS 2026.2 — Citizen Assist AI (DSA)

## 1. Objetivo
Protótipo em **Python** para gerenciar e consultar registros (fictícios) de serviços e orientações ao cidadão (documentos, assistência social, educação, saúde, atendimento comunitário), usando uma **lista encadeada implementada pela equipe**, busca e ordenação próprias e menu interativo.

## 2. Como executar
Requisito: Python 3.8+ (sem bibliotecas externas).

```
python citizen_assist.py    # menu interativo
python testes.py            # cenários de teste (entrada / esperado / observado)
```
Dica: no menu, use a opção **8** para carregar 5 registros de exemplo.

## 3. Campos do registro (`Servico`)
| Campo | Tipo | Regra |
|---|---|---|
| id | int | obrigatório, positivo, **único** |
| titulo | str | obrigatório |
| categoria | str | obrigatório |
| descricao | str | obrigatório |
| publico_alvo | str | obrigatório |
| canal | str | obrigatório (canal ou local de atendimento) |

## 4. Lista encadeada
- `No`: guarda `dado` (um `Servico`) e `proximo` (referência explícita ao próximo nó).
- `ListaEncadeada`: lista simples com `cabeca`, `cauda` e `tamanho`. Nenhuma `list` nativa é usada como armazenamento.
- Operações: `inserir` (no fim), `percorrer`, `buscar_por_id`, `atualizar`, `remover` (cabeça, meio e cauda), `pesquisar`, `ordenar`.
- A remoção reajusta `cabeca`/`cauda` e desconecta o nó removido.

## 5. Organização do código
| Arquivo | Conteúdo |
|---|---|
| `citizen_assist.py` | modelo (`Servico`, `No`), validações, `ListaEncadeada`, menu |
| `testes.py` | 32 cenários automatizados |
| `saida_testes.txt` | saída da execução dos testes (evidência) |

## 6. Algoritmos
**Busca por id:** busca linear, percorre nó a nó até achar o id.

**Pesquisa por título/categoria:** percorre a lista e usa uma busca de substring escrita à mão (`contem`), sem diferenciar maiúsculas de minúsculas.

**Ordenação (por id ou título):** *Merge Sort* para lista encadeada: (1) divide a lista ao meio com ponteiros lento/rápido, (2) ordena cada metade recursivamente, (3) intercala as duas metades ordenadas religando os nós (estável). Não precisa de acesso por índice, por isso é adequado a listas encadeadas.

## 7. Análise Big-O
Hipóteses: *n* = número de registros na lista; *m* = tamanho do termo pesquisado; comparações e atribuições custam O(1).

| Operação | Custo | Justificativa |
|---|---|---|
| Inserção | **O(n)** | a inserção em si é O(1) (usa `cauda`), mas é preciso checar id duplicado percorrendo a lista |
| Busca por id | **O(n)** (melhor caso O(1)) | busca linear |
| Pesquisa por atributo | **O(n·m)** | percorre os n nós e compara substring de tamanho m; os resultados são anexados em O(1) cada |
| Atualização | **O(n)** | localiza o registro por busca linear; a alteração é O(1) |
| Exclusão | **O(n)** | localiza o nó (e o anterior); religar ponteiros é O(1) |
| Ordenação (Merge Sort) | **O(n log n)** em todos os casos | log n níveis de divisão, cada um com custo O(n) para dividir e mesclar |
| Listagem | **O(n)** | percorre toda a lista |

Espaço extra da ordenação: O(log n) pela pilha de recursão (os nós são religados, não copiados).

## 8. Tratamento de erros
Opção de menu inexistente, ID não numérico/negativo, ID duplicado, campos vazios, registro não encontrado, lista vazia e critério de ordenação/pesquisa inválido geram mensagens claras sem encerrar o programa.

## 9. Testes e evidências
`python testes.py` executa 32 cenários (lista vazia, cadastro, duplicado, vazio, consulta, atualização, pesquisa, ordenação, exclusão de cabeça/meio/cauda e esvaziamento). Cada um mostra **Entrada, Esperado, Observado e Resultado**. A saída está em `saida_testes.txt`. Para as capturas de tela, rode o menu e tire prints das telas de cada operação.
