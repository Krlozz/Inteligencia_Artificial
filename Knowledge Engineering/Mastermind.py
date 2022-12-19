import random
import os
 
def clear():
    print("------------------");
 
# Imprime el tablero
def print_mastermind_tablero(colores_objetivo, adivinar_codigo, adivinar_banderas):
 
 
    print("-----------------------------------------")
    print("\t      MASTERMIND")
    print("-----------------------------------------")
 
    print("    |", end="")
    for x in colores_objetivo:
        print("\t" + x[:3], end="")
    print() 
 
    for i in reversed(range(len(adivinar_codigo))):
        print("-----------------------------------------")
        print(adivinar_banderas[i][0], adivinar_banderas[i][1], "|")
         
 
        print(adivinar_banderas[i][2], adivinar_banderas[i][3], end=" |")
        for x in adivinar_codigo[i]:
            print("\t" + x[:3], end="")
 
        print() 
    print("-----------------------------------------")
 

if __name__ == '__main__':
 
    # Colores
    colors = ["ROJO", "VERDE", "AMARILLO", "AZUL", "NEGRO", "NARANJA"]
 
    # Mapping de colores a numeros
    colors_map = {1:"ROJO", 2:"VERDE", 3:"AMARILLO", 4:"AZUL", 5:"NEGRO", 6:"NARANJA"}
 
    # Selección aleatoria de un código de acceso
    random.shuffle(colors)
    colores_objetivo = colors[:4]
    print(colores_objetivo , " codigo")
    # Numero de oportunidades
    chances = 12
 
    # Los colores a encontrar
    mostrar_colores = ['?', '?', '?', '?']
 
    # The codes guessed by the player each turn
    adivinar_codigo = [['-', '-', '-', '-'] for x in range(chances)]
 
    # The clues provided to the player each turn
    adivinar_banderas = [['-', '-', '-', '-'] for x in range(chances)]
     
    clear()
 
    # Turno actual
    turn = 0

    # bucle del juego
    while turn < chances:
         
        print("-----------------------------------------")
        print("\t Indicaciones")
        print("-----------------------------------------")
        print("Ingresa los numeros.")
        print("1 - ROJO, 2 - VERDE, 3 - AMARILLO, 4 - AZUL, 5 - NEGRO, 6 - NARANJA")
        print("Ejemplo: 1 3 6 5")
        print("-----------------------------------------")
        print_mastermind_tablero(mostrar_colores, adivinar_codigo, adivinar_banderas)
 
        # Aceptar la entrada del jugador
        try:    
            #code = list(map(int, input("Escribe la secuncia aquí = ").split())   ### forma manual
            code = random.sample(range(1,7),4)
        except ValueError:
            clear()
            print("\tWrong choice!! Try again!!")
            continue   
 
        # Verfica el numero de colores
        if len(code) != 4:
            clear()
            print("\tWrong choice!! Try again!!")
            continue
 
        # Verifica si corresponde a un numero entero
        flag = 0
        for x in code:
            if x > 6 or x < 1:
                flag = 1
 
        if flag == 1:           
            clear()
            print("\tWrong choice!! Try again!!")
            continue   
 
        # Almacenamiento de la entrada del jugador
        for i in range(4):
            adivinar_codigo[turn][i] = colors_map[code[i]]  
 
        # Proceso para aplicar pistas según la entrada del jugador  
        dummy_colores_objetivo = [x for x in colores_objetivo]  
 
        pos = 0
 
        # Bucle para configurar pistas para el movimiento del jugador.
        for x in code:
            if colors_map[x] in dummy_colores_objetivo:
                if code.index(x) == colores_objetivo.index(colors_map[x]):
                    adivinar_banderas[turn][pos] = 'o'
                    #print(pos)
                else:
                    adivinar_banderas[turn][pos] = 'x'
                    #print(pos)
                pos += 1
                dummy_colores_objetivo.remove(colors_map[x])
 
        random.shuffle(adivinar_banderas[turn])               
 
 
        # Verifica si gana
        if adivinar_codigo[turn] == colores_objetivo:
            clear()
            print_mastermind_tablero(colores_objetivo, adivinar_codigo, adivinar_banderas)
            print("Felicidades!! Ganaste!!!!")
            break
 
        # actualiza el turno
        turn += 1          
        clear()
 
# Verifica si pierde 
if turn == chances:
    clear()
    print_mastermind_tablero(colores_objetivo, adivinar_codigo, adivinar_banderas)
    print("Perdiste...")