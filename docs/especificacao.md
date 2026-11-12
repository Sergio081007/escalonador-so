# Especificação do projeto (resumo do PDF oficial)

Fonte: *Especificação do projeto de Algoritmos de Escalonamento (Semestre 2026.2)* —
UFPB, Centro de Informática, Departamento de Sistemas de Computação, disciplina Sistemas Operacionais.

## Objetivo

Em dupla, implementar algoritmos de escalonamento de CPU e um programa que calcula estatísticas
sobre eles.

Algoritmos obrigatórios:

- **FCFS** — First-Come, First-Served
- **SJF** — Shortest Job First
- **RR** — Round Robin, com **quantum = 2**

Métricas obrigatórias (médias):

- Tempo de retorno médio
- Tempo de resposta médio
- Tempo de espera médio

## Entrada

- Série de pares de inteiros separados por um espaço: `tempo_de_chegada duração`.
- Um processo por par; a entrada termina no **fim do arquivo** (EOF).

```
0 20
0 10
4 6
4 8
```

## Saída

- Uma linha por algoritmo, na ordem **FCFS, SJF, RR**.
- Cada linha: `SIGLA retorno resposta espera`, separados por **um espaço**.
- Valores médios com **uma casa decimal** e **vírgula** como separador decimal.

```
FCFS 30,5 19,5 19,5
SJF 21,5 10,5 10,5
RR 31,5 2,0 20,5
```

## Casos de teste oficiais

| # | Entrada | Saída esperada |
|---|---|---|
| 1 | `0 20` / `0 10` / `4 6` / `4 8` | `FCFS 30,5 19,5 19,5` / `SJF 21,5 10,5 10,5` / `RR 31,5 2,0 20,5` |
| 2 | `0 10` / `4 4` / `8 6` / `21 8` | `FCFS 10,0 3,0 3,0` / `SJF 10,0 3,0 3,0` / `RR 11,0 0,5 4,0` |
| 3 | `0 10` / `0 4` / `0 6` / `0 8` | `FCFS 18,0 11,0 11,0` / `SJF 15,0 8,0 8,0` / `RR 21,5 3,0 14,5` |

(`/` separa as linhas.)

## Corretude

- Testada **automaticamente**: o formato deve ser **exatamente** o especificado.
- Qualquer caractere extra ou dado fora de ordem torna a saída incorreta.
- Outras entradas serão testadas **durante a apresentação** do projeto.

## Entrega

- Um(a) representante da dupla submete pelo **SIGAA**.
- Todo o código-fonte em **Python**, em um arquivo **.ZIP**.
- Os arquivos devem rodar e ser **auto-contidos** (sem dependências externas).
- **Prazo: 13/11/2026, 23:59.**
