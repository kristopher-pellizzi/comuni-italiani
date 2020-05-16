import json

path = "/Users/krijojo/Desktop/"

oldJson = open(path + "comuni-italiani.json", "r")

newJson = open(path + "comuni-italiani-short.json", "w")

dct = json.load(oldJson)

newJson.write("[")

for i in range(len(dct)):
    val = dct[i].get("Denominazione regione")
    newTuple = {"Regione": val}
    val = dct[i].get("Denominazione in italiano")
    newTuple["Comune"] = val
    val = dct[i].get("Denominazione dell'Unità territoriale sovracomunale \n(valida a fini statistici)")
    newTuple["Provincia"] = val
    print(newTuple)
    json.dump(newTuple, newJson, ensure_ascii=False)
    if i == len(dct) - 1:
        newJson.write("]")
    else:
        newJson.write(",\n")

oldJson.close()
newJson.close()