# Documentação — Escalonador de CPU (SO 2026.2)

Esta pasta reúne a documentação do projeto de **Algoritmos de Escalonamento** da disciplina de
Sistemas Operacionais (UFPB / CI / DSC), feito em dupla e em Python.

| Arquivo | Conteúdo |
|---|---|
| [`especificacao.md`](especificacao.md) | Resumo fiel da especificação oficial (PDF): entrada, saída, casos de teste, entrega |
| [`planejamento.md`](planejamento.md) | O que precisamos fazer, divisão de tarefas e checklist até o prazo |
| `README.md` | Este arquivo: visão geral e explicação dos algoritmos e métricas |

**Prazo de entrega:** 13/11/2026 às 23:59, pelo SIGAA (um `.zip` com todo o código-fonte).

---

## O que o programa faz

1. Lê da **entrada padrão** pares de inteiros `chegada duração`, um processo por linha, até o fim do arquivo.
2. Simula três algoritmos de escalonamento sobre esses processos: **FCFS**, **SJF** e **RR (quantum = 2)**.
3. Imprime, para cada algoritmo, uma linha com a sigla e as médias de **retorno**, **resposta** e
   **espera**, com uma casa decimal e **vírgula** como separador decimal.

```bash
python3 escalonador.py < testes/entrada1.txt
```

```
FCFS 30,5 19,5 19,5
SJF 21,5 10,5 10,5
RR 31,5 2,0 20,5
```

A correção é automática: qualquer caractere a mais (cabeçalho, espaço extra, ponto no lugar de vírgula)
faz a saída ser considerada errada.

---

## Métricas

Para cada processo *i* com tempo de chegada `chegada`, duração `duração`, instante em que roda pela
primeira vez `início` e instante em que termina `fim`:

| Métrica | Fórmula | Significado |
|---|---|---|
| Tempo de retorno (*turnaround*) | `fim − chegada` | Tempo total no sistema |
| Tempo de resposta | `início − chegada` | Quanto esperou até usar a CPU pela 1ª vez |
| Tempo de espera | `fim − chegada − duração` | Tempo total parado na fila de prontos |

O programa imprime a **média** de cada métrica sobre todos os processos.

> Observação: em algoritmos não preemptivos (FCFS e SJF) o processo nunca volta para a fila, então
> **resposta = espera**. No RR elas diferem, porque o processo pode ser interrompido várias vezes.

---

## Algoritmos

### FCFS — First-Come, First-Served
Não preemptivo. Os processos são atendidos na ordem de chegada; empates são resolvidos pela ordem em
que aparecem no arquivo. Se a CPU fica ociosa, o relógio avança até a próxima chegada.

### SJF — Shortest Job First
Não preemptivo. Sempre que a CPU fica livre, escolhe, **entre os processos que já chegaram**, o de
menor duração. Desempate: quem chegou primeiro; depois, ordem no arquivo. Uma vez iniciado, o processo
roda até o fim.

### RR — Round Robin (quantum = 2)
Preemptivo. Fila circular de prontos; cada processo roda por no máximo 2 unidades de tempo e, se não
terminou, volta para o **final** da fila.

Regra importante (e que faz os casos de teste baterem): processos que **chegam durante** uma fatia de
tempo entram na fila **antes** do processo que acabou de ser preemptado.

---

## Exemplo passo a passo

Entrada (exemplo 1 da especificação):

```
0 20   -> P0
0 10   -> P1
4 6    -> P2
4 8    -> P3
```

**FCFS:** P0 [0–20], P1 [20–30], P2 [30–36], P3 [36–44]

| | retorno | resposta | espera |
|---|---|---|---|
| P0 | 20 | 0 | 0 |
| P1 | 30 | 20 | 20 |
| P2 | 32 | 26 | 26 |
| P3 | 40 | 32 | 32 |
| **média** | **30,5** | **19,5** | **19,5** |

**SJF:** em t=0 só P0 e P1 chegaram → P1 (10) [0–10]; depois P2 (6) [10–16], P3 (8) [16–24],
P0 (20) [24–44] → médias **21,5 10,5 10,5**.

**RR (q=2):** todos começam rapidamente (resposta média **2,0**), mas os processos longos terminam
tarde → médias **31,5 2,0 20,5**.

---

## Estrutura atual do código (`escalonador.py`)

| Função | Responsabilidade |
|---|---|
| `ler_processos()` | Lê `stdin`, devolve lista de `(índice, chegada, duração)` |
| `fcfs()`, `sjf()`, `rr()` | Simulam o algoritmo e devolvem dicionários `início` e `fim` por processo |
| `metricas()` | Calcula as três médias a partir de `início`/`fim` |
| `formatar()` | Arredonda para 1 casa (meio para cima, via `Decimal`) e troca `.` por `,` |
| `main()` | Executa os três algoritmos na ordem FCFS, SJF, RR e imprime |

Usa apenas a biblioteca padrão (`sys`, `collections`, `decimal`), então é auto-contido.
