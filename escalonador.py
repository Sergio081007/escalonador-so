import sys
from collections import deque
import heapq

# quantum do round robin, o pdf manda ser 2
QUANTUM = 2

# a ideia aqui e que cada algoritmo nn calcula metrica nenhuma, ele so
# devolve o gantt, que e uma lista de fatias (indice, inicio, fim) de quando
# cada processo ficou na cpu. as metricas saem todas dessa lista numa
# funcao so, la embaixo. assim nn precisa repetir a conta 3x


def ler_entrada():
    # se passar arquivo como argumento le dele, senao le do stdin
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as arquivo:
            texto = arquivo.read()
    else:
        texto = sys.stdin.read()

    numeros = [int(x) for x in texto.split()]

    # agrupa de 2 em 2 (chegada, duracao). se sobrar 1 numero solto
    # no final ele eh ignorado msm, nn tem par pra ele
    return list(zip(numeros[0::2], numeros[1::2]))


def ordenar_por_chegada(processos):
    # devolve os indices dos processos ordenados pela chegada, e no
    # empate vale a ordem do arquivo
    return sorted(range(len(processos)), key=lambda i: (processos[i][0], i))


def gantt_fcfs(processos):
    # processos eh a lista de (chegada, duracao) e o indice dela serve de id
    gantt = []
    tempo = 0
    for i in ordenar_por_chegada(processos):
        chegada, duracao = processos[i]
        tempo = max(tempo, chegada)  # cpu ociosa, espera o processo chegar
        gantt.append((i, tempo, tempo + duracao))
        tempo += duracao
    return gantt


def gantt_sjf(processos):
    # sjf sem preempcao. uso um heap de (duracao, indice) pq o topo eh
    # sempre o menor job, e se empatar na duracao sai quem veio antes
    por_chegada = ordenar_por_chegada(processos)
    proximo = 0  # posicao em por_chegada do proximo que ainda nao entrou no heap
    prontos = []
    gantt = []
    tempo = 0

    while proximo < len(por_chegada) or prontos:
        # joga no heap todo mundo que ja chegou ate agora
        while proximo < len(por_chegada) and processos[por_chegada[proximo]][0] <= tempo:
            i = por_chegada[proximo]
            heapq.heappush(prontos, (processos[i][1], i))
            proximo += 1

        if not prontos:
            # ngm pronto, a cpu fica parada ate o proximo chegar
            tempo = processos[por_chegada[proximo]][0]
            continue

        duracao, i = heapq.heappop(prontos)
        gantt.append((i, tempo, tempo + duracao))
        tempo += duracao
    return gantt


def gantt_rr(processos):
    por_chegada = ordenar_por_chegada(processos)
    proximo = 0
    restante = [duracao for _, duracao in processos]  # quanto cada um ainda precisa de cpu
    fila = deque()
    gantt = []
    tempo = 0

    def colocar_na_fila():
        # bota na fila quem ja chegou. fiz funcao interna pq uso isso
        # em 2 lugares e nn queria copiar o codigo
        nonlocal proximo
        while proximo < len(por_chegada) and processos[por_chegada[proximo]][0] <= tempo:
            fila.append(por_chegada[proximo])
            proximo += 1

    while proximo < len(por_chegada) or fila:
        colocar_na_fila()

        if not fila:
            tempo = processos[por_chegada[proximo]][0]  # pula o tempo ocioso
            continue

        i = fila.popleft()
        fatia = min(QUANTUM, restante[i])
        gantt.append((i, tempo, tempo + fatia))
        tempo += fatia
        restante[i] -= fatia

        # importante, quem chegou enquanto o processo rodava entra na
        # fila ANTES dele voltar pro final. se inverter essa ordem os
        # casos de teste do pdf dao errado (ja testei kkk)
        colocar_na_fila()
        if restante[i] > 0:
            fila.append(i)
    return gantt


def calcular_somas(processos, gantt):
    # tira as somas de retorno, resposta e espera a partir do gantt
    primeira_vez = {}  # quando cada processo comecou a rodar pela 1a vez
    termino = {}       # quando cada processo terminou (fim da ultima fatia)
    for i, inicio, fim in gantt:
        primeira_vez.setdefault(i, inicio)
        termino[i] = fim

    soma_retorno = soma_resposta = soma_espera = 0
    for i, (chegada, duracao) in enumerate(processos):
        retorno = termino[i] - chegada        # do momento que chegou ate terminar
        resposta = primeira_vez[i] - chegada  # da chegada ate a 1a vez na cpu
        espera = retorno - duracao            # todo o tempo que ficou parado
        soma_retorno += retorno
        soma_resposta += resposta
        soma_espera += espera
    return soma_retorno, soma_resposta, soma_espera


def formatar_media(soma, quantidade):
    # media com 1 casa e VIRGULA. fiz so com inteiros pra fugir do round()
    # do python, que arredonda o .5 pro par e ai 1.25 virava 1.2 quando
    # o certo eh 1,3. a conta eh a media em decimos, arredondada pra cima no .5
    decimos = (soma * 20 + quantidade) // (2 * quantidade)
    return f"{decimos // 10},{decimos % 10}"


def main():
    processos = ler_entrada()
    quantidade = len(processos)
    if quantidade == 0:  # arquivo vazio, nn tem o que imprimir
        return

    algoritmos = (
        ("FCFS", gantt_fcfs),
        ("SJF", gantt_sjf),
        ("RR", gantt_rr),
    )
    for nome, gerar_gantt in algoritmos:
        somas = calcular_somas(processos, gerar_gantt(processos))
        medias = " ".join(formatar_media(soma, quantidade) for soma in somas)
        print(f"{nome} {medias}")


if __name__ == "__main__":
    main()
