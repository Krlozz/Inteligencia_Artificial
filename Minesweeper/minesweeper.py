

import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count



    def won(self):
        """
        Checks if all mines have been flagged.
        """

        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        #Returns the set of all cells in self.cells known to be mines.
        if len(self.cells) == self.count:
            return self.cells
        return set()


    def known_safes(self):
        #Returns the set of all cells in self.cells known to be safe.

        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """


    def mark_safe(self, cell):
        self.cells.discard(cell)
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
                Se llama cuando el tablero del Buscaminas nos lo indica, para un determinado
         celda segura, cuántas celdas vecinas tienen minas en ellas.

         Esta función debería:
             1) marcar la celda como un movimiento que se ha realizado
             2) marcar la celda como segura
             3) agregar una nueva oración a la base de conocimientos de la IA
                basado en el valor de `cell` y `count`
             4) marcar cualquier celda adicional como segura o como mina
                si se puede concluir en base a la base de conocimientos de la IA
             5) agregue cualquier oración nueva a la base de conocimiento de AI
                si se pueden inferir del conocimiento existente
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        neighbours = set()

        # obyiene todos los vecinos seguros al rededor
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                #ifnora su propia celda
                if (i, j) == cell:
                    continue

                # si las celdas son ya seguras, las ignora
                if (i, j) in self.safes:
                    continue

                #Si se sabe que las celdas son minas, reduzca el conteo en 1 e ignórelas:
                if (i, j) in self.mines:
                    count = count - 1
                    continue

                # De lo contrario, agréguelos a la sentencia si están en el tablero de juego:
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours.add((i, j))

        print(f'Given Cell: {cell} has these neighbouring cells {neighbours} = {count}')
        self.knowledge.append(Sentence(neighbours, count)) #Agregue los vecinos y el conteo como una oración. Luego agregue esa oración al conocimiento.


        # Verifique la oración recién agregada para cajas fuertes y minas y márquelas en consecuencia:
        knowledge_inferred = True

        while knowledge_inferred:
            knowledge_inferred = False

            safes = set()
            mines = set()


            for sentence in self.knowledge:
                safes = safes.union(sentence.known_safes())
                mines = mines.union(sentence.known_mines())


            if safes:
                knowledge_changed = True
                for safe in safes:
                    self.mark_safe(safe)
            if mines:
                knowledge_changed = True
                for mine in mines:
                    self.mark_mine(mine)

            # Elimina las oraciones vacías de la base de conocimientos:
            empty = Sentence(set(), 0)

            self.knowledge[:] = [x for x in self.knowledge if x != empty]

            # Comprueba si 2 oraciones son subconjuntos entre sí
            for sentence_1 in self.knowledge:
                for sentence_2 in self.knowledge:

                    # ignora cuando las sentencias son iguales
                    if sentence_1.cells == sentence_2.cells:
                        continue

                    if sentence_1.cells == set() and sentence_1.count > 0:
                        print('Error - sentence with no cells and count created')
                        raise ValueError

                    # Crea una nueva oración si 1 es un subconjunto de 2 y no en KB:
                    if sentence_1.cells.issubset(sentence_2.cells):
                        new_sentence_cells = sentence_2.cells - sentence_1.cells
                        new_sentence_count = sentence_2.count - sentence_1.count

                        new_sentence = Sentence(new_sentence_cells, new_sentence_count)

                        # Agrega al conocimiento si aún no está en KB:
                        if new_sentence not in self.knowledge:
                            knowledge_changed = True

                            self.knowledge.append(new_sentence)


        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #raise NotImplementedError

    def make_safe_move(self):
        """
         Devuelve una celda segura para elegir en el tablero Buscaminas.
         Se debe saber que el movimiento es seguro, y no ya un movimiento.
         que se ha hecho.

         Esta función puede usar el conocimiento en self.mines, self.safes
         y self.moves_made, pero no debe modificar ninguno de esos valores.
         """
        safe_moves = self.safes - self.moves_made
        if safe_moves:

            return random.choice(list(safe_moves))

        # De lo contrario, no se pueden realizar movimientos seguros garantizados.
        return None
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
    

    def make_random_move(self):
        """
         Devuelve un movimiento para hacer en el tablero Buscaminas.
         Debe elegir aleatoriamente entre celdas que:
             1) aún no han sido elegidos, y
             2) no se sabe que sean minas
         """
        
        all_moves = {(i, j) for i in range(0, self.height) for j in range(0, self.width)}
        moves = all_moves - (self.mines | self.moves_made)
        if moves:
            return random.choice(tuple(moves))
        return None
