#  Robôs Coletores de Lixo - Inteligência Artificial

Atividade de Inteligência Artificial, ministrada pelo Prof. Me. Nerval de Jesus Santos Junior. 

Este repositório contém a implementação em Python de um simulador de ambiente (Matriz 20x20) e quatro diferentes arquiteturas de agentes autônomos projetados para coletar lixos orgânicos e recicláveis, otimizando pontuação e tempo.

##  Arquiteturas Implementadas

1. **Agente Reativo Simples (`Agente_Reativo_Simples.py`):** Toma decisões baseadas puramente na percepção atual imediata (posição atual e 8 vizinhos), sem estado interno.
2. **Agente Reativo Baseado em Modelos (`Agente_Reativo_Baseado_em_Modelos.py`):** Utiliza uma matriz de estado interno (memória) para registrar células visitadas e evitar loops e redundâncias na navegação.
3. **Agente Baseado em Objetivos - BDI (`Agente_Baseado_em_Objetivos.py`):** Prioriza ativamente a coleta de lixos recicláveis (+5 pontos) utilizando uma memória temporal dos lixos avistados (crenças) para guiar suas intenções.
4. **Agente Baseado em Utilidade (`Agente_Baseado_em_Utilidade.py`):** Utiliza o cálculo da Distância de Manhattan para avaliar dinamicamente a relação custo-benefício entre a recompensa do lixo e a distância total até ele e, em seguida, até a lixeira, tomando a decisão mais racional possível.

# ALUNOS:
* `João Marcus Prazeres Carvalho`
* `Murilo Gandra de Carvalho Martins`
* `Pedro Lucas Monteiro`
* `Samylli Kalei Silva Zhao`
