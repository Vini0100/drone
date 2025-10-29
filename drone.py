from djitellopy import Tello
import time


class DroneEntregaABDE:
    """
    Execução conforme o grafo:
    grafo = {
        "Base": ["A", "D"],
        "A": ["B"],
        "B": ["C", "E"],
        "C": ["F"],
        "D": ["E"],
        "E": ["C", "F"],
        "F": ["Base"]
    }

    Nesta missão: Base → A → B → E → Base
    (Respeitando o caminho direcional)
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

    # -----------------------------------
    # MOVIMENTOS CONFORME O GRAFO
    # -----------------------------------

    def base_para_a(self):
        """Base → A"""
        print("[ROTA] Base → A (esquerda diagonal)")
        self.tello.move_left(90)
        self.tello.move_forward(90)
        print("[LOCAL] Chegou em A.")
        self.tello.rotate_clockwise(360)
        time.sleep(1)

    def a_para_b(self):
        """A → B"""
        print("[ROTA] A → B (frente 100 cm)")
        self.tello.move_forward(100)
        print("[LOCAL] Chegou em B.")
        self.tello.rotate_clockwise(360)
        time.sleep(1)

    def b_para_e(self):
        """B → E"""
        print("[ROTA] B → E (gira à direita e segue 155 cm)")
        self.tello.rotate_clockwise(90)
        self.tello.move_forward(155)
        print("[LOCAL] Chegou em E.")
        self.tello.rotate_clockwise(360)
        time.sleep(1)

    def e_para_base(self):
        """E → Base (retorno direto simulado)"""
        print("[RETORNO] E → Base (gira 180° e segue 200 cm)")
        self.tello.rotate_clockwise(180)
        self.tello.move_forward(200)
        print("[LOCAL] Retornou à Base.")
        time.sleep(1)

    # -----------------------------------
    # EXECUÇÃO COMPLETA
    # -----------------------------------

    def run(self):
        """Executa a missão: Base → A → B → E → Base"""
        try:
            self.connect_drone()
            self.takeoff()

            self.base_para_a()
            self.a_para_b()
            self.b_para_e()
            self.e_para_base()

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
    mission = DroneEntregaABDE()
    mission.run()
