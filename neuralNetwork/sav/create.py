def createReseau(infos, classe):
    reseau = []
    n = 0
    for couche in infos:
        reseau.append([])
        for neurone in infos:
            reseau[n].append(classe)
        n+=1
