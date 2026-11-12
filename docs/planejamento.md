# Planejamento

Prazo: **13/11/2026 às 23:59** (SIGAA). Hoje: 12/11/2026 — falta ~1 dia.

## Situação atual

- [x] Especificação lida e resumida em [`especificacao.md`](especificacao.md)
- [x] Protótipo `escalonador.py` com FCFS, SJF (não preemptivo) e RR (q=2)
- [x] Três casos de teste em `testes/` (`entradaN.txt` / `saidaN.txt`) — **todos passando**
- [x] Código e testes dentro do repositório

## O que precisamos fazer

### 1. Organizar o repositório
- [x] Mover `escalonador.py` e a pasta `testes/` para dentro do repositório
- [ ] Atualizar o `README.md` da raiz com descrição curta e link para `docs/`
- [ ] Adicionar `.gitignore` (`__pycache__/`, `*.pyc`, `*.zip`)

### 2. Testes
- [ ] Script `testes/rodar_testes.sh` (ou `.py`) que roda todas as entradas e compara com `diff`
- [ ] Casos extras (o professor testará outras entradas na apresentação):
  - [ ] Um único processo
  - [ ] CPU ociosa entre processos (chegada depois do término do anterior)
  - [ ] Processos com duração menor que o quantum (1) e igual ao quantum (2)
  - [ ] Empates de duração no SJF e de chegada no FCFS
  - [ ] Entrada fora de ordem de chegada
  - [ ] Médias que caem em `,x5` para conferir o arredondamento
  - [ ] Linha em branco / espaços extras no fim do arquivo
- [ ] Conferir à mão (diagrama de Gantt) pelo menos um caso novo por algoritmo

### 3. Revisar decisões de implementação
- [ ] Confirmar que o SJF esperado é **não preemptivo** (os casos oficiais batem assim)
- [ ] Confirmar a regra do RR: quem chega durante a fatia entra na fila antes do preemptado
- [ ] Decidir comportamento para entrada vazia (hoje: não imprime nada)
- [ ] Garantir que nenhuma saída extra (prints de debug, cabeçalho) vai para `stdout`

### 4. Entrega
- [ ] Gerar o `.zip` só com o código-fonte (`escalonador.py` + o que for necessário)
- [ ] Testar o `.zip` em pasta limpa: descompactar e rodar `python3 escalonador.py < entrada`
- [ ] Submeter no SIGAA antes de 13/11 23:59 (definir quem da dupla envia)

### 5. Apresentação
- [ ] Os dois sabem explicar cada algoritmo e as fórmulas das métricas (ver [`README.md`](README.md))
- [ ] Saber rodar um caso novo ao vivo e justificar o resultado

## Divisão sugerida

| Tarefa | Responsável |
|---|---|
| Organizar repositório + `.gitignore` | _a definir_ |
| Script de testes + casos extras | _a definir_ |
| Revisão dos algoritmos (Gantt à mão) | _a definir_ |
| Gerar `.zip` e submeter | _a definir_ |
