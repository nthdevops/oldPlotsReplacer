import time, multiprocessing, subprocess, os, jsonConf, psutil
from tinydb import *
from sys import exit
from customLogs import CustomLog

from flask import Flask, request
app = Flask(__name__)
db = TinyDB('db.json')
conf = jsonConf.getConf('conf.json')
searchDb = Query()
totalRequest = 0
hpoolProcessName = 'hpool-miner-chia-gui.exe'
hpoolPath = "\""+conf.hpoolControl.path+"/"+hpoolProcessName+"\""

#Inicia o log
logger = CustomLog(conf, 'replacerAPI')

#Checka se o diretorio do HPOOL existe
if conf.hpoolControl.enabled:
    if not os.path.exists(conf.hpoolControl.path):
        logger.error("Nao foi possivel encontrar o diretorio do HPOLL\nVerifique se o arquivo de configuracao esta correto!")
        exit()

@app.route('/addPlotToDelete', methods=["POST"])
def addToPlotsDelete():
    global totalRequest
    totalRequest += 1
    json_data = request.json
    db.insert({"id": str(totalRequest), "deletePath": json_data["deletePath"]})
    return str(db.all())

def runApp():
    app.run(host='0.0.0.0', port=6343)

def killer(process_name):
    try:
        os.system("taskkill /im "+process_name)
    except:
        pass
    else:
        pass

def killHpool():
    if hpoolProcessName in (p.name() for p in psutil.process_iter()):
        killer(hpoolProcessName)

def hpoolStart():
    if conf.hpoolControl.enabled:
        hpoolProcess = subprocess.Popen(hpoolPath)
        return hpoolProcess

def hpoolFirstStart():
    logger.debug("Iniciando a configuracao do hpool!")
    if conf.hpoolControl.enabled:
        killHpool()
        time.sleep(2)
        hpoolProcess = hpoolStart()
        logger.debug("Validacoes do hpool finalizadas, servidor pronto para processar requisicoes!")
        return hpoolProcess
    return None

def hpoolFinish(hpoolProcess):
    if conf.hpoolControl.enabled:
        hpoolProcess.terminate()
        time.sleep(2)
        killHpool()

def getPlotFiles(plotsPath):
    plotsList = [f for f in os.listdir(plotsPath) if len(f.split('.plot')) == 2]
    return plotsList

def deleteDbItem(db, dbItem):
    db.remove(searchDb.id == dbItem["id"])

if __name__ == "__main__":
    multiprocessing.freeze_support()
    p = multiprocessing.Process(target=runApp)
    p.start()
    hpoolControl = hpoolFirstStart()

    while True:
        dbitens = db.all()
        if len(dbitens) > 0:
            logger.info("Deletando:", dbitens)
            hpoolFinish(hpoolControl)
            time.sleep(2)
            for pathItem in dbitens:
                deletePath = pathItem["deletePath"]
                if os.path.exists(deletePath):
                    plotsList = getPlotFiles(deletePath)
                    if len(plotsList) > 0:
                        fileDelete = deletePath+"/"+plotsList[0]
                        try:
                            os.remove(fileDelete)
                        except Exception as e:
                            logger.error("Nao foi possivel deletar o arquivo:", fileDelete, "\n\nA seguinte excecao aconteceu:\n", e)
                        else:
                            logger.info("Para o item:", pathItem, "\nDeletou:", fileDelete)
                    else:
                        logger.info("Para o item:", pathItem, "\nNao foi necessario deletar, diretorio nao tem plots")
                else:
                    logger.warning("Nao foi encontrado o diretorio:", deletePath, "para deletar!")
                deleteDbItem(db, pathItem)
            hpoolControl = hpoolStart()
        time.sleep(2)