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
        # Limpa o terminal (funciona no Windows e Linux/Mac)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=== Simulador: Agente Reativo Simples ===")
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
        print("=========================================")

class AgenteReativoSimples:
    def __init__(self):
        self.x = 1
        self.y = 1
        self.carga = None 
        self.pontuacao = 0
        self.passos = 0
        self.acao_atual = "Iniciando..."

    def agir(self, ambiente):
        self.passos += 1
        conteudo_atual = ambiente.get_conteudo(self.x, self.y)

        # Regra 1: Pegar Lixo
        if conteudo_atual in ['O', 'R'] and self.carga is None:
            self.carga = conteudo_atual
            ambiente.remover_lixo(self.x, self.y)
            self.acao_atual = f"Pegou lixo '{self.carga}'"
            return

        # Regra 2: Soltar Lixo na Lixeira[cite: 1]
        if self.carga is not None and self.x == 20 and self.y == 20:
            if self.carga == 'R':
                self.pontuacao += 5
            elif self.carga == 'O':
                self.pontuacao += 1
            self.acao_atual = f"Soltou lixo '{self.carga}' na Lixeira!"
            self.carga = None
            return

        # Regra 3: Mover para lixo vizinho[cite: 1]
        if self.carga is None:
            vizinhos = ambiente.get_vizinhos(self.x, self.y)
            if vizinhos:
                alvo = vizinhos[0] 
                self.mover_para(alvo['x'], alvo['y'])
                self.acao_atual = "Viu lixo vizinho. Movendo para coletar."
                return
            else:
                self.mover_aleatoriamente()
                self.acao_atual = "Explorando aleatoriamente..."
                return

        # Fallback: Se tem carga, vai pra lixeira
        if self.carga is not None:
            self.mover_para(20, 20)
            self.acao_atual = "Carregando lixo. Indo para a lixeira."
            return

    def mover_para(self, destino_x, destino_y):
        if self.x < destino_x: self.x += 1
        elif self.x > destino_x: self.x -= 1
        
        if self.y < destino_y: self.y += 1
        elif self.y > destino_y: self.y -= 1

    def mover_aleatoriamente(self):
        dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
        self.x = max(1, min(20, self.x + dx))
        self.y = max(1, min(20, self.y + dy))


# --- Execução do Simulador ---
if __name__ == "__main__":
    MOSTRAR_ANIMACAO = True # Mude para False quando for medir o tempo real para a tabela!
    
    amb = Ambiente()
    robo = AgenteReativoSimples()
    
    # Inicia a contagem de tempo
    inicio_tempo = time.perf_counter()
    
    while amb.lixos_restantes > 0:
        robo.agir(amb)
        
        if MOSTRAR_ANIMACAO:
            amb.imprimir_mapa(robo.x, robo.y)
            print(f"Passos: {robo.passos} | Lixos Restantes: {amb.lixos_restantes}")
            print(f"Carga Atual: {robo.carga if robo.carga else 'Vazia'} | Pontuação: {robo.pontuacao}")
            print(f"Ação: {robo.acao_atual}")
            time.sleep(0.05) # Pausa de 50ms para você conseguir enxergar o movimento
            
    # Finaliza a contagem de tempo
    fim_tempo = time.perf_counter()
    tempo_execucao_ms = (fim_tempo - inicio_tempo) * 1000

    # Imprime os resultados finais
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