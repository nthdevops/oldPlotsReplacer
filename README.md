# Old Plots Replacer
#
#
## Descrição do Projeto
##### A execução do script irá deletar plots antigos quando detectar novos plots a partir da configuração definida. Caso esteja usando hpool ou outro software que trave os plots antigos, o programa irá fechar o software antes de deletar plots.
#
#
### Pré-requisitos

##### Antes de começar, você vai precisar renomear o arquivo conf.json.example para conf.json e realizar a configuração:
#
#
##### O arquivo .example estará no seguinte formato:
#
```javascript
{
    "logsPath": "Caminho para o log terminando com / ou \\",
    "loglevel": "info" ou "debug",
    "processShutControl": {
        "enabled": true,
        "path": "Caminho para o executavel do processo terminado com / ou \\",
        "executableName": "hpool-miner-chia-gui.exe" ou o nome do executavel que precisar ser fechado antes de deletar os plots
    },
    "controlPaths": [
        {
            "nftPlotsPath": "Path dos plots NFT terminado com / ou \\",
            "oldPlotsPath": "Path dos plots antigos terminado com / ou \\",
            "maxPlots": Numero maximo de plots que podem existir, somando os plots antigos com os NFT, sera o numero usado para validar se um plot antigo precisa ser deletado (Colocar o numero sem aspas, exemplo: 10)
        }
    ]
}
```

##### Exemplo de arquivo de configuração final com diretórios de rede e locais configurados, também com o gerenciamento ativo para o HPOOL:
#
```javascript
{
    "logsPath": "C:/Users/USER/Chia/logs/",
    "loglevel": "info",
    "processShutControl": {
        "enabled": true,
        "path": "C:/Users/USER/Chia/programs/windows/",
        "executableName": "hpool-miner-chia-gui.exe"
    },
    "controlPaths": [
        {
            "nftPlotsPath": "C:/Users/USER/Chia/ChiaNFTPlots/",
            "oldPlotsPath": "C:/Users/USER/Chia//ChiaPlots/",
            "maxPlots": 10
        },
        {
            "nftPlotsPath": "\\\\DESKTOP-NETWORKNAME\\Folder\\ChiaNFTPlots\\",
            "oldPlotsPath": "\\\\DESKTOP-NETWORKNAME\\Folder\\ChiaPlots\\",
            "maxPlots": 15
        }
    ]
}
```

##### Exemplo de arquivo de configuração final com diretórios de rede e locais configurados, com gerenciamento de programa desativado:
#
```javascript
{
    "logsPath": "C:/Users/USER/Chia/logs/",
    "loglevel": "info",
    "processShutControl": {
        "enabled": false,
        "path": "",
        "executableName": ""
    },
    "controlPaths": [
        {
            "nftPlotsPath": "C:/Users/USER/Chia/ChiaNFTPlots/",
            "oldPlotsPath": "C:/Users/USER/Chia//ChiaPlots/",
            "maxPlots": 10
        },
        {
            "nftPlotsPath": "\\\\DESKTOP-NETWORKNAME\\Folder\\ChiaNFTPlots\\",
            "oldPlotsPath": "\\\\DESKTOP-NETWORKNAME\\Folder\\ChiaPlots\\",
            "maxPlots": 15
        }
    ]
}
```


##### Adicione quantos elementos forem necessários em controlPaths!
#
##### Agora basta iniciar o executável "runPlotManager.exe".
#
##### Caso ele for fechar um programa como o hpool que necessita de acesso ADMIN, inicie o script como administrador!
#
#
### Veja também:
- [Gerenciador customizado do plotter madMax](https://github.com/nthdevops/ChiaMadMaxPlotterPy)