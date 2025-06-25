import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceDD = None

    def handleCreaGrafo(self, e):
        dMinTxt = self._view._txtInDurata.value
        if dMinTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, valore minimo di durata non isnerito.", color="red"))
            self._view.update_page()
            return
        try:
            dMin = int(dMinTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, valore inserito non valido.", color="red"))
            self._view.update_page()
            return
        self._model.buildGraph(dMin)
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo è costituito di {n} nodi e {a} archi."))
        self.fillDD(self._model.getAllNodes())
        self._view.update_page()

    def fillDD(self, listOfNodes):
        listOfNodes.sort(key = lambda x: x.Title)
        listOfOptions = map(lambda x: ft.dropdown.Option(data = x, text = x.Title, on_click = self._readDDValue), listOfNodes)
        # for n in listOfNodes:
        #     listOfOptions.append(ft.dropdown.Option(data = x, text = x.Title, on_click = self._readDDValue))
        self._view._ddAlbum.options = list(listOfOptions)

    def _readDDValue(self, e):
        if e.control.data is None:
            print("error in reading DD")
            self._choiceDD = None
        self._choiceDD = e.control.data

    # def getSelectedAlbum(self, e):
    #     pass

    def handleAnalisiComp(self, e):
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, album non selezionato.", color="red"))
            self._view.update_page()
            return
        size, dTotCC = self._model.getInfoConnessa(self._choiceDD)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene {self._choiceDD.Title} ha {size} nodi e una durata totale di {dTotCC} minuti."))
        self._view.update_page()

    def handleGetSetAlbum(self, e):
        sogliaTxt = self._view._txtInSoglia.value
        if sogliaTxt == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, soglia massima di durata non inserita.", color="red"))
            self._view.update_page()
            return
        try:
            soglia = int(sogliaTxt)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, il valore di soglia inserito non è un intero", color="red"))
            self._view.update_page()
            return
        if self._choiceDD is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare una voce dal menu.", color="red"))
            self._view.update_page()
            return
        setOfNodes, sumDurate = self._model.getSetOfNodes(self._choiceDD, soglia)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Ho trovato un set di album che soddisfa le specifiche, dimensione = {len(setOfNodes)}, durata totale: {sumDurate}."))
        self._view.txt_result.controls.append(ft.Text("Di seguito gli album che fanno parte della soluzione trovata:"))
        for n in setOfNodes:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()