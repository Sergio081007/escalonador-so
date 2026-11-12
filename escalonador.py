import sys
from collections import deque
from decimal import Decimal, ROUND_HALF_UP

QUANTUM = 2


def ler_processos():
    numeros = [int(x) for x in sys.stdin.read().split()]
    # cada processo: (indice, chegada, duracao)
    return [(i, numeros[2 * i], numeros[2 * i + 1]) for i in range(len(numeros) // 2)]


def metricas(processos, inicio, fim):
    """Calcula as medias de retorno, resposta e espera."""
    n = len(processos)
    retorno = resposta = espera = 0
    for i, chegada, duracao in processos:
        retorno += fim[i] - chegada
        resposta += inicio[i] - chegada
        espera += fim[i] - chegada - duracao
    return retorno / n, resposta / n, espera / n


def fcfs(processos):
    inicio, fim = {}, {}
    tempo = 0
    for i, chegada, duracao in sorted(processos, key=lambda p: (p[1], p[0])):
        tempo = max(tempo, chegada)
        inicio[i] = tempo
        tempo += duracao
        fim[i] = tempo
    return inicio, fim


def sjf(processos):
    """SJF nao preemptivo."""
    inicio, fim = {}, {}
    pendentes = sorted(processos, key=lambda p: (p[1], p[0]))
    tempo = 0
    while pendentes:
        prontos = [p for p in pendentes if p[1] <= tempo]
        if not prontos:
            tempo = pendentes[0][1]
            continue
        # menor duracao; empate -> chegou primeiro; depois ordem de entrada
        escolhido = min(prontos, key=lambda p: (p[2], p[1], p[0]))
        pendentes.remove(escolhido)
        i, _, duracao = escolhido
        inicio[i] = tempo
        tempo += duracao
        fim[i] = tempo
    return inicio, fim


def rr(processos, quantum=QUANTUM):
    inicio, fim = {}, {}
    chegadas = deque(sorted(processos, key=lambda p: (p[1], p[0])))
    restante = {i: d for i, _, d in processos}
    fila = deque()
    tempo = 0

    def admitir():
        while chegadas and chegadas[0][1] <= tempo:
            fila.append(chegadas.popleft()[0])

    while chegadas or fila:
        admitir()
        if not fila:
            tempo = chegadas[0][1]
            continue
        i = fila.popleft()
        if i not in inicio:
            inicio[i] = tempo
        fatia = min(quantum, restante[i])
        tempo += fatia
        restante[i] -= fatia
        # processos que chegaram durante a fatia entram antes do preemptado
        admitir()
        if restante[i] > 0:
            fila.append(i)
        else:
            fim[i] = tempo
    return inicio, fim


def formatar(valor):
    arred = Decimal(str(valor)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return str(arred).replace(".", ",")


def main():
    processos = ler_processos()
    if not processos:
        return
    for nome, algoritmo in (("FCFS", fcfs), ("SJF", sjf), ("RR", rr)):
        inicio, fim = algoritmo(processos)
        valores = metricas(processos, inicio, fim)
        print(nome, " ".join(formatar(v) for v in valores))


if __name__ == "__main__":
    main()
