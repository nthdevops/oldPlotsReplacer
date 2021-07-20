import time, multiprocessing, subprocess, os, jsonConf, psutil
from sys import exit
from customLogs import CustomLog

conf = jsonConf.getConf('conf.json')
processControlEnabled = conf.processShutControl.enabled
executableName = conf.processShutControl.executableName
processControlPath = conf.processShutControl.path+executableName
controlPaths = conf.controlPaths

#Inicia o log
logger = CustomLog(conf, 'plotsReplacer')

def killer(process_name):
    try:
        os.system("taskkill /im "+process_name)
    except Exception as e:
        logger.debug("Nao foi possivel matar o processo", process_name, "| Exception:\n", e)

def killProcess():
    if executableName in (p.name() for p in psutil.process_iter()):
        logger.debug("Matando processo pelo sistema!")
        killer(executableName)

def processStart():
    if processControlEnabled:
        logger.info("Iniciando processo!")
        try:
            processStarted = subprocess.Popen(processControlPath)
        except Exception as e:
            logger.info("Nao foi possivel iniciar o processo! | Exception:\n", e)
            exit()
        else:
            return processStarted

def processFinish(processExecution):
    if processControlEnabled and processExecution != None:
        logger.info("Fechando processo!")
        try:
            processExecution.terminate()
        except Exception as e:
            logger.info("Nao foi possivel finalizar o processo pelo controlador padrao! | Exception:\n", e)
        time.sleep(2)
        killProcess()

def processFirstStart():
    logger.debug("Inicio do controle de processos!")
    if processControlEnabled:
        killProcess()
        time.sleep(2)
        processExecution = processStart()
        logger.debug("Validacoes de processo finalizadas!")
        return processExecution
    return None

def getPlotFiles(plotsPath):
    plotsList = []
    if os.path.exists(plotsPath):
        for f in os.listdir(plotsPath):
            if len(f.split('.plot')) == 2:
                if not len(f.split('.tmp')) == 2:
                    plotsList.append(f)
    else:
        logger.error("A contagem de plots falhou pois o diretorio", plotsPath, "nao existe!! A execucao sera abortada!")
        exit()
    return plotsList

def getPlotAndTmpPlot(plotsPath):
    plotsList = []
    if os.path.exists(plotsPath):
        for f in os.listdir(plotsPath):
            if len(f.split('.plot')) == 2:
                plotsList.append(f)
    else:
        logger.error("A contagem de plots falhou pois o diretorio", plotsPath, "nao existe!! A execucao sera abortada!")
        exit()
    return plotsList

def pathExists(path):
    return os.path.exists(path)

def pathErrorExit(path):
    logger.error("Nao foi possivel encontrar o caminho inidicado!\nVerifique se o arquivo de configuracao esta correto!\nCaminho configurado:", path)
    exit()

#Valida se todos os diretorios da configuracao sao validos
def checkAllConfPaths():
    logger.info("Validando diretorios da configuracao!")
    if processControlEnabled:
        if not os.path.isfile(processControlPath):
            pathErrorExit(processControlPath)
    
    for controlPath in controlPaths:
        for key in controlPath:
            if key != "maxPlots":
                path = controlPath[key]
                if not pathExists(path):
                    pathErrorExit(path)
    logger.info("Diretorios validados!")

#Antes de iniciar a execucao valida diretorios
checkAllConfPaths()
#Habilita o freeze_support para execucao de binarios
multiprocessing.freeze_support()
#Toma o controle da execucao do processo configurado
processExecution = processFirstStart()

logger.info("Tudo certo! Script validando plots..")

#Inicia o loop infinito para validacao de plots
while True:
    if len(controlPaths) > 0:
        #Variavel para validar se o processo foi finalizado e se sera necessario inicia-lo novamente
        startProcessAgain = False
        for controlPath in controlPaths:
            nftPlotsPath = controlPath["nftPlotsPath"]
            oldPlotsPath = controlPath["oldPlotsPath"]
            maxPlots = controlPath["maxPlots"]
            nftPlotsList = getPlotAndTmpPlot(nftPlotsPath)
            oldPlotsList = getPlotFiles(oldPlotsPath)
            #Se todos os plots comparados ao maximo forem NFT e nao existirem plots antigos, remove o elemento de configuracao
            if len(nftPlotsList) == maxPlots and len(oldPlotsList) == 0:
                logger.debug("Todos os plots sao NFT para o controlPath:\n", controlPath)
                controlPaths.remove(controlPath)
                logger.info("Tudo certo! Script validando plots..")
                continue
            #A partir da lista de plots nft e antigos, soma os valor e subtrai do maximo para validar se passou o total de plots
            difPlotsToMax = (len(nftPlotsList) + len(oldPlotsList)) - maxPlots
            #Se o total estiver acima do esperado, deleta a quantidade plots antigos necessaria
            if difPlotsToMax > 0:
                logger.info("Novos plots foram detectados, ira deletar plots antigos!")
                #Finaliza a execucao do processo configurado
                if not startProcessAgain:
                    processFinish(processExecution)
                    startProcessAgain = True
                    time.sleep(3)
                #Itera sobre a quantidade de plots que estao a mais do maximo
                for idx in range(difPlotsToMax):
                    #Atribui a variavel plotToRemove o path de delecao de um plot antigo
                    plotToRemove = oldPlotsPath+oldPlotsList[idx]
                    logger.info("Deletando plot:", plotToRemove)
                    try:
                        #Deleta o plot antigo configurado
                        os.remove(plotToRemove)
                    except Exception as e:
                        logger.error("Nao foi possivel deletar o plot:", plotToRemove, "\nA seguinte excecao aconteceu:\n", e)
                    else:
                        logger.info("Deletou o plot:", plotToRemove)
        #Inicia novamente a execucao do processo se necessario
        if startProcessAgain:
            processExecution = processStart()
            logger.info("Tudo certo! Script validando plots..")
    else:
        logger.info("Todos os diretorios foram validados e so existem plots NFT")
        exit()
    time.sleep(1)