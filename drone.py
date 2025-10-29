from djitellopy import Tello
import time

class DroneEntregaCidade:
    """
    Simulação de voo conforme o grafo direcional:
    grafo = {
        "Base": ["A", "D"],
        "A": ["B"],
        "B": ["C", "E"],
        "C": ["F"],
        "D": ["E"],
        "E": ["C", "F"],
        "F": ["Base"]
    }

    Layout:
    - A, B, C ficam à esquerda
    - D, E, F ficam à direita
    - Distância entre colunas: 155 cm
    - Distância entre linhas (mesma coluna): 100 cm
    """

    def __init__(self):
        self.tello = Tello()

    def connect_drone(self):
        print("[DRONE] Conectando...")
        self.tello.connect()
        print(f"[DRONE] Conectado! Bateria: {self.tello.get_battery()}%")

    def takeoff(self):
        print("[DRONE] Decolando...")
        self.tello.takeoff()
        print("[DRONE] Subindo 45 cm...")
        self.tello.move_up(45)
        time.sleep(2)

    def land(self):
        print("[DRONE] Pousando...")
        self.tello.land()
        time.sleep(2)

    # ===================================================
    # MOVIMENTOS ENTRE PONTOS (distâncias reais)
    # ===================================================

    def base_para_a(self):
        """Base → A (diagonal esquerda)"""
        print("[ROTA] Base → A")
        self.tello.move_left(90)
        self.tello.move_forward(90)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em A.")
        time.sleep(1)

    def base_para_d(self):
        """Base → D (diagonal direita)"""
        print("[ROTA] Base → D")
        self.tello.move_right(90)
        self.tello.move_forward(90)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em D.")
        time.sleep(1)

    def a_para_b(self):
        """A → B (mesma coluna esquerda, desce 100 cm)"""
        print("[ROTA] A → B")
        self.tello.move_back(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em B.")
        time.sleep(1)

    def b_para_c(self):
        """B → C (mesma coluna esquerda, desce 100 cm)"""
        print("[ROTA] B → C")
        self.tello.move_back(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em C.")
        time.sleep(1)

    def b_para_e(self):
        """B → E (gira à direita e segue 155 cm)"""
        print("[ROTA] B → E")
        self.tello.rotate_clockwise(90)
        self.tello.move_forward(155)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em E.")
        time.sleep(1)

    def d_para_e(self):
        """D → E (desce 100 cm na mesma coluna direita)"""
        print("[ROTA] D → E")
        self.tello.move_back(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em E.")
        time.sleep(1)

    def e_para_f(self):
        """E → F (desce 100 cm)"""
        print("[ROTA] E → F")
        self.tello.move_back(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em F.")
        time.sleep(1)

    def f_para_base(self):
        """F → Base (volta 155 cm e sobe 200 cm para alinhar à Base)"""
        print("[RETORNO] F → Base")
        self.tello.rotate_clockwise(90)  # vira para a esquerda (coluna da Base)
        self.tello.move_forward(155)
        self.tello.rotate_counter_clockwise(90)
        self.tello.move_up(200)
        print("[LOCAL] Retornou à Base.")
        time.sleep(1)

    # ===================================================
    # EXECUÇÃO DE UMA ROTA COMPLETA (EXEMPLO)
    # ===================================================

    def run(self):
        try:
            self.connect_drone()
            self.takeoff()

            # Exemplo de entrega: Base → A → B → E → F → Base
            self.base_para_a()
            self.a_para_b()
            self.b_para_e()
            self.e_para_f()
            self.f_para_base()

            self.land()
            print("[MISSÃO] Entregas concluídas com sucesso!")

        except Exception as e:
            print(f"[ERRO] {e}")
            print("[DRONE] Pousando por segurança...")
            self.tello.land()


# =====================================================
# EXECUÇÃO PRINCIPAL
# =====================================================
if __name__ == "__main__":
    mission = DroneEntregaCidade()
    mission.run()
