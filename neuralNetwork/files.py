import json
import os

pathFiles = ""


def init():
    global pathFiles
    with open("config.json") as f:
        config = json.load(f)
        pathFiles = config["path"]


def load():
    global pathFiles
    with open(pathFiles, 'r') as g:
        if g:
            reseau = json.load(g)
            return reseau[0], reseau[1]
        else:
            return None


def save(network, links):
    global pathFiles
    networkTemp = [network, links]
    with open(pathFiles, 'w+') as file:
        json.dump(networkTemp, file)


def new(name):
    os.mknod(pathFiles)
