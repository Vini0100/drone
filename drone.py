from djitellopy import Tello
import time

class DroneEntregaMapaFinal:
    """
    Grafo e layout conforme definido:
        C (0, 220)  ↔  F (155, 220)
        B (0, 110)  ↔  E (155, 110)
        A (0,   0)  ↔  D (155,   0)
                    ↑
                  Base

    - 155 cm entre colunas (E ↔ D)
    - 110 cm entre linhas (frente/trás)
    - Da Base até A/D: 100 cm lateral + 110 cm frente
    - De F para a Base: mover para trás 220 cm e para a esquerda 100 cm
    - Deixe comentados os 360°
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
        print("[DRONE] Subindo 45 cm para altitude de cruzeiro...")
        self.tello.move_up(45)
        time.sleep(2)

    def land(self):
        print("[DRONE] Pousando...")
        self.tello.land()
        time.sleep(2)

    # ===================================================
    # MOVIMENTOS ENTRE PONTOS (com base no layout real)
    # ===================================================

    def base_para_a(self):
        """Base → A (100 cm à esquerda + 110 cm à frente)"""
        print("[ROTA] Base → A (diagonal esquerda)")
        self.tello.move_left(100)
        self.tello.move_forward(110)
        # self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em A.")
        time.sleep(1)

    def base_para_d(self):
        """Base → D (100 cm à direita + 110 cm à frente)"""
        print("[ROTA] Base → D (diagonal direita)")
        self.tello.move_right(100)
        self.tello.move_forward(110)
        # self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em D.")
        time.sleep(1)

    def a_para_b(self):
        """A → B (110 cm à frente, mesma coluna esquerda)"""
        print("[ROTA] A → B")
        self.tello.move_forward(110)
        # self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em B.")
        time.sleep(1)

    def b_para_e(self):
        """B → E (155 cm à direita, mesma linha)"""
        print("[ROTA] B → E")
        self.tello.move_right(155)
        # self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em E.")
        time.sleep(1)

    def e_para_f(self):
        """E → F (110 cm à frente, mesma coluna direita)"""
        print("[ROTA] E → F")
        self.tello.move_forward(110)
        # self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em F.")
        time.sleep(1)

    def f_para_base(self):
        """F → Base (move para trás 220 cm e para a esquerda 100 cm)"""
        print("[RETORNO] F → Base")
        self.tello.move_back(220)
        self.tello.move_left(100)
        self.tello.move_down(45)  # volta à altura base
        # self.tello.rotate_clockwise(360)
        print("[LOCAL] Retornou à Base.")
        time.sleep(1)

    # ===================================================
    # EXECUÇÃO DE ROTA EXEMPLO
    # ===================================================

    def run(self):
        try:
            self.connect_drone()
            self.takeoff()

            # Exemplo de missão: Base → A → B → E → F → Base
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
    mission = DroneEntregaMapaFinal()
    mission.run()
