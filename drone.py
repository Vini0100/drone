import time
from collections import deque
import itertools

# --- SIMULAÇÃO DO DRONE (MockTello) ---
# Para usar um drone real:
# 1. Instale: pip install djitellopy
# 2. Comente esta classe "MockTello"
# 3. Descomente a linha: from djitellopy import Tello

class MockTello:
    """
    Classe de simulação do drone Tello.
    Imprime as ações no console em vez de voar.
    """
    def connect(self):
        print("[DRONE] Conectando ao Tello...")
        time.sleep(1)
        print("[DRONE] Conexão estabelecida.")

    def takeoff(self):
        print("[DRONE] Decolando...")
        time.sleep(1)

    def land(self):
        print("[DRONE] Pousando...")
        time.sleep(1)

    def move_forward(self, cm):
        # Simula o tempo de voo
        print(f"[DRONE] Voando para frente {cm}cm...")
        time.sleep(1)

    def rotate_clockwise(self, deg):
        print(f"[DRONE] Girando {deg} graus no sentido horário...")
        time.sleep(1)

    def get_battery(self):
        return 100

# Se for usar o drone real, descomente a linha abaixo e comente a classe MockTello
# from djitellopy import Tello

# -----------------------------------------------

class DroneDeliverySimulator:
    
    def __init__(self, graph, tello):
        self.graph = graph
        self.tello = tello
        self.order_queue = deque()
        self.undelivered_orders = []
        print("Simulador de Entrega com Drone iniciado.")

    def load_orders(self, orders):
        """Carrega uma lista de pedidos na fila."""
        self.order_queue.extend(orders)
        print(f"Pedidos carregados na fila: {list(self.order_queue)}")

    def find_path(self, start, end):
        """
        Encontra o caminho mais curto entre 'start' e 'end' usando BFS.
        Retorna a lista do caminho (ex: ['A', 'B', 'C']) ou None se não houver caminho.
        """
        if start not in self.graph or end not in self.graph:
            return None

        # Fila do BFS armazena tuplas: (nó_atual, caminho_até_aqui)
        queue = deque([(start, [start])])
        visited = {start}

        while queue:
            current_node, path = queue.popleft()

            if current_node == end:
                return path  # Caminho encontrado

            # Pega os vizinhos do nó atual. Usa .get() para evitar erros se um nó não tiver saídas.
            for neighbor in self.graph.get(current_node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append((neighbor, new_path))
        
        return None  # Nenhum caminho encontrado

    def optimize_route(self, start_node, destinations):
        """
        Encontra a ordem de visitação ideal (menor custo) para uma lista de destinos,
        garantindo que um caminho completo (incluindo retorno à Base) exista.
        """
        best_permutation = None
        min_cost = float('inf')

        # Testa todas as permutações possíveis dos destinos
        for perm in itertools.permutations(destinations):
            current_cost = 0
            current_node = start_node
            is_valid_permutation = True

            # 1. Calcula o custo da permutação (ex: Base -> C -> E)
            for stop in perm:
                path = self.find_path(current_node, stop)
                if path:
                    current_cost += len(path) - 1  # Custo é o número de arestas
                    current_node = stop # Atualiza a localização atual
                else:
                    is_valid_permutation = False
                    break # Esta permutação é impossível
            
            if not is_valid_permutation:
                continue

            # 2. Verifica se é possível voltar para a Base
            path_to_base = self.find_path(current_node, "Base")
            if path_to_base:
                current_cost += len(path_to_base) - 1
            else:
                is_valid_permutation = False # Não pode voltar para a base
            
            # 3. Se for uma rota válida e de menor custo, armazena
            if is_valid_permutation and current_cost < min_cost:
                min_cost = current_cost
                best_permutation = perm

        return list(best_permutation) if best_permutation else None

    def collect_valid_batch(self):
        """
        Retira até 4 pedidos da fila principal e os valida (Base -> Destino).
        Pedidos inválidos são descartados. Tenta preencher os 4 slots.
        """
        valid_batch = []
        print("\n[COLETA] Verificando novos pedidos na fila...")
        
        while len(valid_batch) < 4 and self.order_queue:
            order = self.order_queue.popleft()
            
            # Validação: Existe *pelo menos um* caminho da Base até o destino?
            if self.find_path("Base", order):
                print(f"[COLETA] Pedido '{order}' é válido. Adicionando ao lote.")
                valid_batch.append(order)
            else:
                print(f"[COLETA] Pedido '{order}' não tem rota da Base. Descartando.")
                self.undelivered_orders.append(order)
                # O loop continua automaticamente, puxando o próximo item da fila
                # para tentar preencher o slot.
        
        if not valid_batch:
            print("[COLETA] Nenhum pedido válido encontrado neste lote.")
        else:
            print(f"[COLETA] Lote de entrega pronto: {valid_batch}")
            
        return valid_batch

    def fly_delivery_route(self, batch):
        """
        Executa a otimização e o voo para um lote de pedidos válidos.
        """
        print(f"[ROTA] Otimizando a rota para o lote: {batch}")
        current_location = "Base"
        
        optimized_destinations = self.optimize_route(current_location, batch)
        
        if not optimized_destinations:
            print(f"[ERRO ROTA] Não foi encontrada uma permutação de rota válida para {batch}.")
            print(f"[ERRO ROTA] Isso pode significar que não há caminho entre os pontos de entrega ou de volta à Base.")
            print(f"[ERRO ROTA] Descartando todos os pedidos deste lote.")
            self.undelivered_orders.extend(batch)
            # Retorna à base (simbolicamente)
            self.fly_path(["Base", "Base"]) # Apenas para log
            return

        print(f"[ROTA] Rota otimizada definida: {' -> '.join(optimized_destinations)}")

        # Executa o voo seguindo a rota otimizada
        for destination in optimized_destinations:
            path = self.find_path(current_location, destination)
            
            print(f"\n[VIAGEM] Próximo destino: {destination}")
            self.fly_path(path)
            self.perform_delivery(destination)
            current_location = destination # Atualiza a localização do drone

        # Após a última entrega, retorna à Base
        print(f"\n[VIAGEM] Entregas do lote concluídas. Retornando à Base a partir de {current_location}.")
        path_to_base = self.find_path(current_location, "Base")
        
        if path_to_base:
            self.fly_path(path_to_base)
            current_location = "Base"
            print("[VIAGEM] Pousado sobre a Base. Verificando novos pedidos.")
        else:
            # Esta situação não deve ocorrer se o otimizador funcionou
            print(f"[ERRO CRÍTICO] Não foi possível encontrar caminho de {current_location} para a Base. Pouso de emergência!")
            self.tello.land()
            # Força a parada da simulação
            self.order_queue.clear() 

    def fly_path(self, path):
        """Simula o voo ao longo de um caminho nó-a-nó."""
        if not path or len(path) < 2:
            print("[VOO] Caminho inválido ou já está no destino.")
            return

        for i in range(len(path) - 1):
            start = path[i]
            end = path[i+1]
            print(f"[VOO] Voando de '{start}' para '{end}'...")
            # Em um drone real, aqui você teria comandos como
            # tello.go_xyz_speed(x, y, z, speed) ou move_forward()
            # baseado em um mapa de coordenadas pré-definido.
            # Para simulação, apenas avançamos simbolicamente.
            self.tello.move_forward(100) # Distância simbólica de 100cm
        
        print(f"[VOO] Chegou em '{path[-1]}'.")

    def perform_delivery(self, area):
        """Simula a conclusão da entrega."""
        print(f"[ENTREGA] Chegou na Área {area}. Realizando giro de 360° para confirmar.")
        self.tello.rotate_clockwise(360)
        print(f"[ENTREGA] Entrega em '{area}' concluída.")

    def run_simulation(self):
        """
        Método principal que executa todo o ciclo de vida da simulação.
        """
        try:
            self.tello.connect()
            # print(f"Bateria: {self.tello.get_battery()}%") # Útil para drone real
            self.tello.takeoff()

            # Loop principal: continua enquanto houver pedidos na fila
            while self.order_queue:
                print(f"\n--- INICIANDO NOVO LOTE DE ENTREGAS ---")
                print(f"Pedidos restantes na fila: {len(self.order_queue)}")
                
                # 1. Coleta e valida um lote de até 4 pedidos
                valid_batch = self.collect_valid_batch()
                
                # Se o lote não estiver vazio, voa para entregá-lo
                if valid_batch:
                    # 2. Otimiza e voa a rota de entrega
                    self.fly_delivery_route(valid_batch)
                else:
                    # Se a fila principal ainda tem pedidos, mas nenhum é válido,
                    # o loop 'while self.order_queue' continuará até esvaziá-la.
                    print("Nenhum pedido válido encontrado. A fila principal está sendo esvaziada.")

            # Fim do loop principal (fila vazia)
            print("\n--- SIMULAÇÃO CONCLUÍDA ---")
            print("Fila de pedidos vazia.")
            self.tello.land()
            
            print("\n--- RELATÓRIO FINAL ---")
            if self.undelivered_orders:
                print(f"Pedidos não entregues (sem rota): {self.undelivered_orders}")
            else:
                print("Todos os pedidos foram entregues com sucesso!")

        except Exception as e:
            print(f"\n[ERRO GERAL] Ocorreu um erro: {e}")
            print("Iniciando pouso de emergência.")
            self.tello.land()

# --- FIM DAS CLASSES ---


def get_user_inputs():
    """Função para coletar os dados da competição."""
    
    # Exemplo de grafo (pode ser substituído por input() se necessário)
    grafo_competicao = {
        "Base": ["A", "D"],
        "A": ["B"],
        "B": ["C", "E"],
        "C": ["F"],
        "D": ["E"],
        "E": ["C", "F"],
        "F": ["Base"]
    }
    
    # Exemplo de pedidos
    # "C", "E", "A", "F", "B" (Todos são alcançáveis)
    # Adicionando 'G' (inalcançável) e um 'C' repetido para testar
    pedidos_competicao = ["C", "E", "A", "F", "B", "G", "C"]
    
    print("--- DADOS DA COMPETIÇÃO ---")
    print(f"Grafo do Mapa: {grafo_competicao}")
    print(f"Lista de Pedidos: {pedidos_competicao}")
    print("-----------------------------\n")
    
    return grafo_competicao, pedidos_competicao

# --- PONTO DE ENTRADA PRINCIPAL ---
if __name__ == "__main__":
    
    # 1. Obter os dados da competição
    grafo, pedidos = get_user_inputs()
    
    # 2. Inicializar o Tello (Mock ou Real)
    # Use MockTello() para simulação segura
    tello_drone = MockTello()
    
    # Para voo real (CUIDADO: requer espaço e configuração):
    # tello_drone = Tello() 
    
    # 3. Inicializar o Simulador
    simulator = DroneDeliverySimulator(grafo, tello_drone)
    
    # 4. Carregar os pedidos
    simulator.load_orders(pedidos)
    
    # 5. Rodar a simulação
    simulator.run_simulation()
