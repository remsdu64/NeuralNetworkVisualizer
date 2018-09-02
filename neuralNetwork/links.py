#!/usr/local/bin/env python3.5
# coding: utf-8

import json

pathLinkFile = 0


def init():
    global pathLinkFile
    with open("config.json") as c:
        config = json.load(c)
        pathLinkFile = config["links"]


def load():
    global pathLinkFile

    with open(pathLinkFile, 'r') as linkFile:
        if linkFile:
            links = json.load(linkFile)
            return links
        else:
            return None


def save(links):
    global pathLinkFile
    with open(pathLinkFile, 'w+') as h:
        json.dump(links, h, indent=4)
