from djitellopy import Tello
import time

class DroneEntregaMapaFinal:
    """
    Grafo Direcional:
    grafo = {
        "Base": ["A", "D"],
        "A": ["B"],
        "B": ["C", "E"],
        "C": ["F"],
        "D": ["E"],
        "E": ["C", "F"],
        "F": ["Base"]
    }

    Layout físico:
        ESQUERDA             DIREITA
        C (0, 200)     ↔     F (155, 200)
        B (0, 100)     ↔     E (155, 100)
        A (0,   0)     ↔     D (155,   0)
                     ↑
                   Base (entre A e D)

    Distâncias:
    - Entre colunas: 155 cm
    - Entre linhas: 100 cm
    """

    def __init__(self):
        self.tello = Tello()

    def connect_drone(self):
        print("[DRONE] Conectando ao Tello...")
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
    # MOVIMENTOS ENTRE PONTOS (com base no layout)
    # ===================================================

    def base_para_a(self):
        """Base → A (vai ligeiramente à esquerda e para frente ~70 cm)"""
        print("[ROTA] Base → A")
        self.tello.move_left(70)
        self.tello.move_forward(70)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em A.")
        time.sleep(1)

    def base_para_d(self):
        """Base → D (vai ligeiramente à direita e para frente ~70 cm)"""
        print("[ROTA] Base → D")
        self.tello.move_right(70)
        self.tello.move_forward(70)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em D.")
        time.sleep(1)

    def a_para_b(self):
        """A → B (mesma coluna esquerda, sobe 100 cm)"""
        print("[ROTA] A → B")
        self.tello.move_up(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em B.")
        time.sleep(1)

    def b_para_c(self):
        """B → C (mesma coluna esquerda, sobe 100 cm)"""
        print("[ROTA] B → C")
        self.tello.move_up(100)
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
        """D → E (sobe 100 cm na coluna direita)"""
        print("[ROTA] D → E")
        self.tello.move_up(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em E.")
        time.sleep(1)

    def e_para_f(self):
        """E → F (sobe 100 cm na coluna direita)"""
        print("[ROTA] E → F")
        self.tello.move_up(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em F.")
        time.sleep(1)

    def f_para_base(self):
        """F → Base (gira à esquerda, anda 155 cm e desce 200 cm)"""
        print("[RETORNO] F → Base")
        self.tello.rotate_counter_clockwise(90)
        self.tello.move_forward(155)
        self.tello.move_down(200)
        print("[LOCAL] Retornou à Base.")
        time.sleep(1)

    # ===================================================
    # EXECUÇÃO DA MISSÃO EXEMPLO
    # ===================================================

    def run(self):
        try:
            self.connect_drone()
            self.takeoff()

            # Exemplo de missão: Base → A → B → E → Base
            self.base_para_a()
            self.a_para_b()
            self.b_para_e()
            self.f_para_base()  # simulando retorno direto por cima de F/Base

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
    mission = DroneEntregaMapaFinal()
    mission.run()
