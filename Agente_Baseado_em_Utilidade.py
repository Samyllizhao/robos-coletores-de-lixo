import random
import time
import os

class Ambiente:
    def __init__(self):
        self.tamanho = 20
        self.matriz = [[None for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.lixos_restantes = 15
        self._distribuir_lixos()
        
    def _distribuir_lixos(self):
        lixos = ['O'] * 10 + ['R'] * 5
        for lixo in lixos:
            while True:
                x, y = random.randint(1, 20), random.randint(1, 20)
                if (x, y) not in [(1, 1), (20, 20)] and self.matriz[x-1][y-1] is None:
                    self.matriz[x-1][y-1] = lixo
                    break

    def get_conteudo(self, x, y):
        return self.matriz[x-1][y-1]

    def remover_lixo(self, x, y):
        self.matriz[x-1][y-1] = None
        self.lixos_restantes -= 1

    def get_vizinhos(self, x, y):
        vizinhos = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = x + dx, y + dy
                if 1 <= nx <= 20 and 1 <= ny <= 20:
                    conteudo = self.get_conteudo(nx, ny)
                    if conteudo in ['O', 'R']:
                        vizinhos.append({'x': nx, 'y': ny, 'tipo': conteudo})
        return vizinhos

    def imprimir_mapa(self, agente_x, agente_y):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=== Simulador: Agente Baseado em Utilidade ===")
        print("Legenda: [A] Agente | [O] Orgânico | [R] Reciclável | [X] Lixeira | [.] Vazio\n")
        
        for i in range(self.tamanho):
            linha = ""
            for j in range(self.tamanho):
                x, y = j + 1, i + 1
                
                if x == agente_x and y == agente_y:
                    linha += "[A]"
                elif x == 20 and y == 20:
                    linha += "[X]"
                elif self.matriz[x-1][y-1] == 'O':
                    linha += "[O]"
                elif self.matriz[x-1][y-1] == 'R':
                    linha += "[R]"
                else:
                    linha += "[.]"
            print(linha)
        print("==============================================")

class AgenteBaseadoEmUtilidade:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.carga = None 
        self.pontuacao = 0
        self.passos = 0
        self.acao_atual = "Iniciando..."
        
        # Memórias do agente
        self.visitados = [[0 for _ in range(20)] for _ in range(20)]
        self.lixos_conhecidos = {} 
        self.objetivo_atual = None 

    def atualizar_crencas(self, ambiente):
        self.visitados[self.x - 1][self.y - 1] += 1
        vizinhos = ambiente.get_vizinhos(self.x, self.y)
        for v in vizinhos:
            self.lixos_conhecidos[(v['x'], v['y'])] = v['tipo']

    def calcular_utilidade(self, alvo_x, alvo_y, tipo):
        # Recompensa: +5 para Reciclável, +1 para Orgânico[cite: 1]
        recompensa = 5.0 if tipo == 'R' else 1.0
        
        # Distância de Manhattan: passos do agente até o lixo + do lixo até a lixeira (20,20)
        dist_ate_lixo = abs(alvo_x - self.x) + abs(alvo_y - self.y)
        dist_ate_lixeira = abs(20 - alvo_x) + abs(20 - alvo_y)
        
        custo_total = dist_ate_lixo + dist_ate_lixeira
        
        # Evita divisão por zero caso o agente já esteja sobre o lixo (o que seria utilidade máxima)
        if custo_total == 0:
            return float('inf')
            
        return recompensa / custo_total

    def deliberar(self):
        if self.carga is not None:
            self.objetivo_atual = (20, 20)
            return

        # Avalia a utilidade de todos os lixos na memória para escolher o melhor
        if self.lixos_conhecidos:
            melhor_utilidade = -1
            melhor_alvo = None
            
            for (lx, ly), tipo in self.lixos_conhecidos.items():
                utilidade = self.calcular_utilidade(lx, ly, tipo)
                if utilidade > melhor_utilidade:
                    melhor_utilidade = utilidade
                    melhor_alvo = (lx, ly)
            
            self.objetivo_atual = melhor_alvo
            return
            
        self.objetivo_atual = None

    def agir(self, ambiente):
        self.passos += 1
        self.atualizar_crencas(ambiente)
        conteudo_atual = ambiente.get_conteudo(self.x, self.y)

        # Regra de Coleta
        if conteudo_atual in ['O', 'R'] and self.carga is None:
            self.carga = conteudo_atual
            ambiente.remover_lixo(self.x, self.y)
            if (self.x, self.y) in self.lixos_conhecidos:
                del self.lixos_conhecidos[(self.x, self.y)]
            self.objetivo_atual = None 
            self.acao_atual = f"Pegou lixo '{self.carga}' (Decisão baseada em Utilidade máxima)"
            return

        # Regra de Descarte
        if self.carga is not None and self.x == 20 and self.y == 20:
            if self.carga == 'R': self.pontuacao += 5
            elif self.carga == 'O': self.pontuacao += 1
            self.acao_atual = f"Soltou lixo '{self.carga}' na Lixeira!"
            self.carga = None
            self.objetivo_atual = None
            return

        self.deliberar()
        
        if self.objetivo_atual is not None:
            self.mover_para(self.objetivo_atual[0], self.objetivo_atual[1])
            if self.carga:
                self.acao_atual = f"Indo para a Lixeira (Custo minimizado)"
            else:
                tipo_alvo = self.lixos_conhecidos.get(self.objetivo_atual, '?')
                self.acao_atual = f"Calculou utilidade: Indo buscar lixo '{tipo_alvo}' em {self.objetivo_atual}"
        else:
            self.mover_inteligentemente()
            self.acao_atual = "Mapeando área desconhecida para encontrar recursos."

    def mover_para(self, destino_x, destino_y):
        if self.x < destino_x: self.x += 1
        elif self.x > destino_x: self.x -= 1
        
        if self.y < destino_y: self.y += 1
        elif self.y > destino_y: self.y -= 1

    def mover_inteligentemente(self):
        opcoes = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = self.x + dx, self.y + dy
                if 1 <= nx <= 20 and 1 <= ny <= 20:
                    visitas = self.visitados[nx-1][ny-1]
                    opcoes.append({'x': nx, 'y': ny, 'visitas': visitas})
        
        min_visitas = min(opcao['visitas'] for opcao in opcoes)
        melhores_opcoes = [opc for opc in opcoes if opc['visitas'] == min_visitas]
        escolha = random.choice(melhores_opcoes)
        
        self.x = escolha['x']
        self.y = escolha['y']

# --- Execução do Simulador ---
if __name__ == "__main__":
    MOSTRAR_ANIMACAO = True
    
    amb = Ambiente()
    robo = AgenteBaseadoEmUtilidade()
    
    inicio_tempo = time.perf_counter()
    
    while amb.lixos_restantes > 0:
        robo.agir(amb)
        
        if MOSTRAR_ANIMACAO:
            amb.imprimir_mapa(robo.x, robo.y)
            print(f"Passos: {robo.passos} | Lixos Restantes: {amb.lixos_restantes}")
            print(f"Carga Atual: {robo.carga if robo.carga else 'Vazia'} | Pontuação: {robo.pontuacao}")
            print(f"Ação: {robo.acao_atual}")
            time.sleep(0.05) 
            
    fim_tempo = time.perf_counter()
    tempo_execucao_ms = (fim_tempo - inicio_tempo) * 1000

    if not MOSTRAR_ANIMACAO:
        amb.imprimir_mapa(robo.x, robo.y)
        
    print("\n" + "="*40)
    print("           FIM DA SIMULAÇÃO")
    print("="*40)
    print(f"Lixos Restantes: {amb.lixos_restantes}")
    print(f"Pontuação Total: {robo.pontuacao}")
    print(f"Número de Passos: {robo.passos}")
    print(f"Tempo de Execução: {tempo_execucao_ms:.2f} ms")
    print("="*40)
