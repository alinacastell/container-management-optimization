"""
Template file for simple.py module.
"""


import sys
import curses

from store import *


class Strategy:

    """Implementation of the simple strategy."""
    """Logistic management of a store of containers"""

    _store: Store   # atribut privat _store de tipus de dades Store
    _time: int      #current time
    _logger: Logger #utilitzat per registrar cada moviment cada vegada que es faci
    _pila1: List[int]
    _pila1: List[int]


    def __init__(self, width: int, log_path: str):
        """ """
        self._store = Store(width) #width es un parametre d'entrada
        self._time = 0
        self._logger = Logger(log_path, "Simple", width)
        self._pila1 = [-1,0,2,6,12]
        self._pila2 = [-1,1,4,9,16]

    def cash(self) -> int:
        """Returns accumulated profit earned from removing containers on time"""
        return self._store.cash()

#preguntar store.c.size o c.size
    def insert_container(self,c: Container) -> None:
        """For every size of the container, place it at the top of the stack of said size"""
        #comentar
        self._store.add(c,self._pila1[c.size])
        """
        if(c.size == 1):
            self._store.add(c,0)
        elif(c.size == 2):
            self._store.add(c,2)
        elif(c.size == 3):
            self._store.add(c,6)
        elif(c.size == 4):
            self._store.add(c,12)
        """

    def rellocate_containers(self,c: Container) -> None:
        """Rellocate containers from first stack to the second of the same size and rellocate from the second to the first"""
        #auxiliar variable for size
        size = self._store.c.size
        #make sure the timestamp of the container is not overpassed
        stack = self._store.location(c).second
        i = 0
        while self._time < self._store.c.arrival.end and not self._store[[0][stack]].empty() :
            #move every container of the stack
            cont = self._store[[i][stack]]
            update_stack(cont, size*size)
            i += 1
        j = 0
        while self._time < self._store.c.arrival.end and not self._store[[0][stack]].empty() :
            #move every container of the stack
            cont = self._store[[j][size*size]]
            update_store(cont,stack)
            j += 1
        i = 0

    def update_stack(self, c: Container, p: Position) -> None:
        """ """
        #auxiliar variable for size
        size = self._store.c.size
        #check if container is expired
        if self._store.c.expired(self._time) :
            self._store.remove(c)
        elif self._store.c.delivery(self._time) :
            self._store.add_cash(c.value)
            self._store.remove(c)
        else :
            self._store.move(c,size*size)
            self._time += 1


    def exec(self, c: Container): ...
    #executar cada vegada que arriba nou contenidors
    #tantes accions de la grua com temps que tingui dins l'interval
    """ que fa l'exec"""
    """First action is to insert the received container to the store"""
    self.insert_container(c)

    """Rellocate all containers of the first stack to the second"""
    self.rellocate_container(c)





def init_curses():
    """Initializes the curses library to get fancy colors and whatnots."""

    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, curses.COLOR_WHITE, i)


def execute_strategy(containers_path: str, log_path: str, width: int):
    """Execute the strategy on an empty store of a certain width reading containers from containers_path and logging to log_path."""

    containers = read_containers(containers_path)
    strategy = Strategy(width, log_path)
    for container in containers:
        strategy.exec(container)


def main(stdscr: curses.window):
    """main script"""

    init_curses()

    #name of the container's file
    containers_path = sys.argv[1]
    #name of the register's file
    log_path = sys.argv[2]
    #width of the store
    width = int(sys.argv[3])

    #reads the containers that arrive to the store and places them into the store
    execute_strategy(containers_path, log_path, width)
    #checks and shows the store
    check_and_show(containers_path, log_path, stdscr)


# start main script when program executed
if __name__ == '__main__':
    curses.wrapper(main)
