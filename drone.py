from djitellopy import Tello
import time

class SimpleDroneDelivery:
    """
    Simulação simples de entregas com o drone Tello.
    Cenário: apenas 3 pontos — Base, A (esquerda diagonal) e D (direita diagonal)
    """

    def __init__(self):
        self.tello = Tello()

    def connect_drone(self):
        """Conecta ao drone Tello e verifica a bateria."""
        print("[DRONE] Conectando ao Tello...")
        self.tello.connect()
        print(f"[DRONE] Conectado! Bateria: {self.tello.get_battery()}%")

    def takeoff(self):
        """Decola o drone."""
        print("[DRONE] Decolando...")
        self.tello.takeoff()
        time.sleep(2)

    def land(self):
        """Pousa o drone."""
        print("[DRONE] Pousando...")
        self.tello.land()
        time.sleep(2)

    def go_to_A(self):
        """
        Voa da Base até o ponto A.
        A está na diagonal esquerda (90cm para esquerda e 90cm à frente).
        """
        print("[ROTA] Indo para A (esquerda diagonal)")
        self.tello.move_left(90)
        self.tello.move_forward(90)
        print("[LOCAL] Chegou em A.")
        self.tello.rotate_clockwise(360)  # Simula entrega
        time.sleep(1)

    def go_to_D(self):
        """
        Voa da Base até o ponto D.
        D está na diagonal direita (90cm para direita e 90cm à frente).
        """
        print("[ROTA] Indo para D (direita diagonal)")
        self.tello.move_right(90)
        self.tello.move_forward(90)
        print("[LOCAL] Chegou em D.")
        self.tello.rotate_clockwise(360)  # Simula entrega
        time.sleep(1)

    def return_to_base_from_A(self):
        """Volta da posição A até a Base."""
        print("[RETORNO] Voltando da A para Base...")
        self.tello.move_back(90)
        self.tello.move_right(90)
        print("[LOCAL] Retornou à Base.")

    def return_to_base_from_D(self):
        """Volta da posição D até a Base."""
        print("[RETORNO] Voltando da D para Base...")
        self.tello.move_back(90)
        self.tello.move_left(90)
        print("[LOCAL] Retornou à Base.")

    def run(self):
        """Executa o voo completo: Base → A → Base → D → Base."""
        try:
            self.connect_drone()
            self.takeoff()

            # Entrega na A
            self.go_to_A()
            self.return_to_base_from_A()

            # Entrega na D
            self.go_to_D()
            self.return_to_base_from_D()

            self.land()
            print("[MISSÃO] Todas as entregas concluídas!")

        except Exception as e:
            print(f"[ERRO] {e}")
            print("[DRONE] Pousando por segurança...")
            self.tello.land()

# =====================================================
# PONTO DE ENTRADA PRINCIPAL
# =====================================================
if __name__ == "__main__":
    mission = SimpleDroneDelivery()
    mission.run()
