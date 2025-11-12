from djitellopy import Tello
import time

class DroneEntregaMapaFinal:
    """
    Grafo e layout conforme definido:
        C (0, 200)  ↔  F (155, 200)
        B (0, 100)  ↔  E (155, 100)
        A (0,   0)  ↔  D (155,   0)
                    ↑
                  Base

    - 155 cm entre colunas
    - 100 cm entre linhas (frente/trás)
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
    # MOVIMENTOS ENTRE PONTOS (distâncias reais)
    # ===================================================

    def base_para_a(self):
        """Base → A (diagonal esquerda)"""
        print("[ROTA] Base → A")
        self.tello.move_left(70)
        self.tello.move_forward(70)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em A.")
        time.sleep(1)

    def base_para_d(self):
        """Base → D (diagonal direita)"""
        print("[ROTA] Base → D")
        self.tello.move_right(70)
        self.tello.move_forward(70)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em D.")
        time.sleep(1)

    def a_para_b(self):
        """A → B (frente 100 cm na mesma coluna esquerda)"""
        print("[ROTA] A → B")
        self.tello.move_forward(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em B.")
        time.sleep(1)

    def b_para_e(self):
        """B → E (gira à direita e segue 155 cm)"""
        print("[ROTA] B → E")
        self.tello.rotate_clockwise(90)
        self.tello.move_forward(155)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em E.")
        time.sleep(1)

    def e_para_f(self):
        """E → F (frente 100 cm na mesma coluna direita)"""
        print("[ROTA] E → F")
        self.tello.move_forward(100)
        self.tello.rotate_clockwise(360)
        print("[LOCAL] Chegou em F.")
        time.sleep(1)

    def f_para_base(self):
        """F → Base (volta 155 cm à esquerda e retorna à altura da base)"""
        print("[RETORNO] F → Base")
        self.tello.rotate_counter_clockwise(90)
        self.tello.move_forward(155)
        self.tello.move_down(45)  # volta para altura da base
        print("[LOCAL] Retornou à Base.")
        time.sleep(1)

    # ===================================================
    # EXECUÇÃO DE UMA ROTA EXEMPLO
    # ===================================================

    def run(self):
        try:
            self.connect_drone()
            self.takeoff()

            # Exemplo de rota: Base → A → B → E → F → Base
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
