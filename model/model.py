import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._allNodi = []
        self._allEdges = []
        self._idMapAlbum = {}
        self._bestSet = {}
        self._maxLen = 0

    def buildGraph(self, durataMin):
        self._grafo.clear()
        self._allNodi = DAO.getAlbums(durataMin)
        self._grafo.add_nodes_from(self._allNodi)
        self._idMapAlbum = {n.AlbumId: n for n in self._allNodi}
        self._allEdges = DAO.getAllEdges(self._idMapAlbum)
        self._grafo.add_edges_from(self._allEdges)

    def getGraphDetails(self):
        return self._grafo.number_of_nodes(), self._grafo.number_of_edges()

    def getAllNodes(self):
        return list(self._grafo.nodes())

    def getInfoConnessa(self, a1):
        cc = nx.node_connected_component(self._grafo, a1)
        return len(cc), self._getDurataTot(cc)

    def _getDurataTot(self, listOfNodes):
        # return sum([n.dTot for n in listOfNodes])
        sumDurata = 0
        for n in listOfNodes:
            sumDurata += n.dTot
        return sumDurata



    def getSetOfNodes(self, a1, soglia):
        self._bestSet = {}
        self._maxLen = 0
        parziale = {a1}
        cc = nx.node_connected_component(self._grafo, a1)
        cc.remove(a1)
        for n in cc:
            # richiamo la mia ricorsione
            parziale.add(n) # add perché è un set
            cc.remove(n)
            self._ricorsione(parziale, cc, soglia)
            cc.add(n)
            parziale.remove(n)
        return self._bestSet, self._getDurataTot(self._bestSet)

    def _ricorsione(self, parziale, rimanenti, soglia):
        # 1) verifico che parziale sia una soluzione ammissibile, ovvero se viola i vincoli
        if self._getDurataTot(parziale) > soglia:
            return # evito di continuare l'esplorazione (inutile)
        # 2) se parziale soffisfa i criteri, allora verifico se è migliore di bestSet
        if len(parziale) > self._maxLen:
            self._maxLen = len(parziale)
            self._bestSet = copy.deepcopy(parziale) # COPIA
        # 3) aggiungo e faccio ricorsione
        for n in rimanenti:
            parziale.add(n)
            rimanenti.remove(n)
            self._ricorsione(parziale, rimanenti, soglia)
            parziale.remove(n)
            rimanenti.add(n)