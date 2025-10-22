from djitellopy import Tello
import time

class SimpleDroneDelivery:
    """
    Simulação de voo com 3 pontos:
    Base → A (esquerda diagonal) e Base → D (direita diagonal).
    - Sobe 45 cm após decolar.
    - Gira 360° ao chegar em cada destino (A e D).
    """

    def __init__(self):
        self.tello = Tello()

    def connect_drone(self):
        """Conecta ao drone Tello e mostra o nível da bateria."""
        print("[DRONE] Conectando ao Tello...")
        self.tello.connect()
        print(f"[DRONE] Conectado! Bateria: {self.tello.get_battery()}%")

    def takeoff(self):
        """Decola e sobe 45 cm."""
        print("[DRONE] Decolando...")
        self.tello.takeoff()
        print("[DRONE] Subindo 45 cm...")
        self.tello.move_up(45)
        time.sleep(2)

    def land(self):
        """Pousa o drone."""
        print("[DRONE] Pousando...")
        self.tello.land()
        time.sleep(2)

    # -----------------------------
    # MOVIMENTOS PARA A E D
    # -----------------------------

    def go_to_A(self):
        """
        Vai da Base até o ponto A:
        - Move 90 cm à esquerda
        - Move 90 cm à frente
        - Gira 360° (simula entrega)
        """
        print("[ROTA] Indo para A (diagonal esquerda)")
        self.tello.move_left(90)
        self.tello.move_forward(90)
        print("[LOCAL] Chegou em A.")
        self.tello.rotate_clockwise(360)
        time.sleep(1)

    def go_to_D(self):
        """
        Vai da Base até o ponto D:
        - Move 90 cm à direita
        - Move 90 cm à frente
        - Gira 360° (simula entrega)
        """
        print("[ROTA] Indo para D (diagonal direita)")
        self.tello.move_right(90)
        self.tello.move_forward(90)
        print("[LOCAL] Chegou em D.")
        self.tello.rotate_clockwise(360)
        time.sleep(1)

    # -----------------------------
    # RETORNOS À BASE
    # -----------------------------

    def return_from_A(self):
        """Retorna da A até a Base (movimentos inversos)."""
        print("[RETORNO] Voltando de A para Base...")
        self.tello.move_back(90)
        self.tello.move_right(90)
        print("[LOCAL] Retornou à Base.")

    def return_from_D(self):
        """Retorna da D até a Base (movimentos inversos)."""
        print("[RETORNO] Voltando de D para Base...")
        self.tello.move_back(90)
        self.tello.move_left(90)
        print("[LOCAL] Retornou à Base.")

    # -----------------------------
    # EXECUÇÃO PRINCIPAL
    # -----------------------------

    def run(self):
        """Executa o ciclo completo: Base → A → Base → D → Base."""
        try:
            self.connect_drone()
            self.takeoff()

            # Entrega A
            self.go_to_A()
            self.return_from_A()

            # Entrega D
            self.go_to_D()
            self.return_from_D()

            # Pouso final
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
    mission = SimpleDroneDelivery()
    mission.run()
