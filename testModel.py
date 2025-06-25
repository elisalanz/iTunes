from model.model import Model

mymodel = Model()
mymodel.buildGraph(60)
n, e = mymodel.getGraphDetails()
print(f"Numero di nodi: {n} Numero di archi: {e}")
