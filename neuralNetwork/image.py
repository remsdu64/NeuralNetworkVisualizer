from PIL import Image
from imutils import paths
from matplotlib import pyplot as plt

def getImgs(noms, Long, larg):
    samples = []
    sortie = []
    for truc in noms:
        chemin = "images/"+str(truc)
        #print(chemin)
        for imagePath in paths.list_images(chemin):
            sortie = []
            #print(imagePath)
            i = Image.open(imagePath)
            t = i.resize((Long, larg), Image.ANTIALIAS)
            (l, h) = t.size
            pixels = []
            for y in range(h):
                for x in range(l):
                    c = Image.Image.getpixel(t, (x, y))
                    luminosite = (c[0] * 0.299) + (c[1] * 0.587) + (c[2] * 0.114)
                    pixels.append(luminosite/255)
            ajout = []
            ajout.append(pixels)
            for j in noms:
                if j == truc:
                    sortie.append(1)
                else:
                    sortie.append(0)
            ajout.append(sortie)
            samples.append(ajout)
    return samples

def getImg(noms, Long, larg, sortie):
    import cv2
    samples = []
    chemin = "images/"+str(noms)+"/1.jpg"
    #print(chemin)
    sortie = []
    #print(imagePath)
    i = Image.open(chemin)
    i = i.resize((Long, larg), Image.ANTIALIAS)
    (l, h) = i.size
    pixels = []
    for y in range(h):
        for x in range(l):
            c = Image.Image.getpixel(i, (x, y))
            luminosite = (c[0] * 0.299) + (c[1] * 0.587) + (c[2] * 0.114)
            pixels.append(luminosite/255)
    ajout = []
    ajout.append(pixels)
    ajout.append(sortie)
    samples.append(ajout)
    cv2.imshow("Base", cv2.imread(chemin))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return samples

#print(getImg("voiture", 10, 10, [1, 0]))
