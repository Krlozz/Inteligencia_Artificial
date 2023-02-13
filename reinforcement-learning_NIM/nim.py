import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        """
             Inicializa el tablero de juego.
          Cada tablero de juego tiene
              - `pilas`: una lista de cuántos elementos quedan en cada pila
              - `jugador`: 0 o 1 para indicar el turno de qué jugador
              - `ganador`: Ninguno, 0 o 1 para indicar quién es el ganador
              

        """
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        """
        Nim.available_actions(piles) toma una lista de `pilas` como entrada
         y devuelve todas las acciones disponibles `(i, j)` en ese estado.

         La acción `(i, j)` representa la acción de eliminar elementos `j`
         de la pila `i` (donde las pilas están indexadas en 0).


        """
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, piles[i] + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        """
        Nim.other_player(jugador) devuelve el jugador que no es
         `jugador`. Asume que `jugador` es 0 o 1.

        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Nim.other_player(self.player)

    def move(self, action):
        """
       Haz el movimiento `acción` para el jugador actual.
         `acción` debe ser una tupla `(i, j)`.

        """
        pile, count = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        elif pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        elif count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")

        # Update pile
        self.piles[pile] -= count
        self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        """
        Inicializar AI con un diccionario Q-learning vacío,
        una tasa alfa (aprendizaje) y una tasa épsilon.

        El diccionario Q-learning mapea `(estado, acción)`
        se empareja con un valor Q (un número).
         - `estado` es una tupla de las pilas restantes, p. (1, 1, 4, 4)
         - `acción` es una tupla `(i, j)` para una acción

        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Actualizar el modelo de Q-learning, dado un estado anterior, una acción realizada
        en ese estado, un nuevo estado resultante, y la recompensa recibida
        de tomar esa acción.

        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Devuelve el valor Q para el estado `estado` y la acción `acción`.
        Si todavía no existe un valor Q en `self.q`, devuelve 0.

        """
        return self.q[(tuple(state), action)] if (tuple(state), action) in self.q else 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Actualice el valor Q para el estado `estado` y la acción `acción`
        dado el valor Q anterior `old_q`, una recompensa actual `recompensa`,
        y una estimación de las recompensas futuras `future_rewards`.

        Usa la fórmula:

        Q(s, a) <- estimación del valor antiguo
                   + alfa * (valor estimado nuevo - valor estimado antiguo)

        donde `estimación del valor antiguo` es el valor Q anterior,
        `alfa` es la tasa de aprendizaje, y `nuevo valor estimado`
        es la suma de la recompensa actual y las recompensas futuras estimadas.

        """
        self.q[(tuple(state), action)] = old_q + self.alpha * (reward + future_rewards - old_q)

    def best_future_reward(self, state):
        """
        Dado un estado 'estado', considere todos los posibles '(estado, acción)'
        pares disponibles en ese estado y devolver el máximo de todos
        de sus valores Q.

        Use 0 como el valor Q si un par `(estado, acción)` no tiene
        Valor Q en `self.q`. Si no hay acciones disponibles en
        `estado`, devuelve 0.

        """
        best_reward = 0

        for action in Nim.available_actions(list(state)):
            best_reward = max(self.get_q_value(state, action), best_reward)

        return best_reward

    def choose_action(self, state, epsilon=True):
        """
        Dado un estado `estado`, devuelve una acción `(i, j)` para realizar.

        Si `epsilon` es `False`, devuelve la mejor acción
        disponibles en el estado (el que tiene el valor Q más alto,
        usando 0 para pares que no tienen valores Q).

        Si `epsilon` es `Verdadero`, entonces con probabilidad
        `self.epsilon` elige una acción aleatoria disponible,
        de lo contrario, elija la mejor acción disponible.

        Si múltiples acciones tienen el mismo valor Q, cualquiera de esas
        options es un valor de retorno aceptable.

        """
        best_action = None
        best_reward = 0
        actions = list(Nim.available_actions(list(state)))

        for action in actions:
            if best_action is None or self.get_q_value(state, action) > best_reward:
                best_reward = self.get_q_value(state, action)
                best_action = action

        if epsilon:
            # Distribute probability weights:
            #   (1 - epsilon) --> best_action
            #   epsilon       --> among all the other actions
            weights = [(1 - self.epsilon) if action == best_action else
                       (self.epsilon / (len(actions) - 1)) for action in actions]

            best_action = random.choices(actions, weights=weights, k=1)[0]

        return best_action


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = NimAI()

    # Play n games
    for i in range(n):
        print(f"Jugando para entrenar {i + 1}")
        game = Nim()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.piles.copy()
            action = player.choose_action(game.piles)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.piles.copy()

            # When game is over, update Q values with rewards
            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Entrenamiento terminado")

    # Return the trained AI
    return player


def play(ai, human_player=None):
    """
    Juega un juego humano contra la IA.
    `human_player` se puede establecer en 0 o 1 para especificar si
    el jugador humano se mueve primero o segundo.
.
    """

    # If no player order set, choose human's order randomly
    if human_player is None:
        human_player = random.randint(0, 1)

    # Create new game
    game = Nim()

    # Game loop
    while True:

        # Print contents of piles
        print()
        print("Pilas:")
        for i, pile in enumerate(game.piles):
            print(f"Pila {i}: {pile}")
        print()

        # Compute available actions
        available_actions = Nim.available_actions(game.piles)
        time.sleep(1)

        # Let human make a move
        if game.player == human_player:
            print("Tu turno")
            while True:
                pile = int(input("Eleji la fila: "))
                count = int(input("Cuantos: "))
                if (pile, count) in available_actions:
                    break
                print("Movimiento no válido.")

        # Have AI make a move
        else:
            print("Es turno de la AI")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI toma {count} de la pila {pile}.")

        # Make move
        game.move((pile, count))

        # Check for winner
        if game.winner is not None:
            print()
            print("Final de juego")
            winner = "Humano" if game.winner == human_player else "AI"
            print(f"El ganador es {winner}")
            return
