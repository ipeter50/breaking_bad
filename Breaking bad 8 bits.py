import sys, pygame, random, time, os, math
from pygame.locals import *


def main(): # Initialisation et appel de la fonction titre
    global screen

    pygame.init()
    screen= pygame.display.set_mode((770,421)) # Definition de l'écran de facon standard
    pygame.mouse.set_visible(0) # On rend la souris invisible dans la fenêtre du jeu
    
    main_load() # Appel fonction LOAD
    titre() # Appel fonction TITRE
    return

def titre(): # Affichage de l'écran titre
    global sonTitre
    sonTitre.play()
    x,y=titre1.get_size()
    screen= pygame.display.set_mode((x,y),FULLSCREEN) # Adaptation de l'ecran à la taille du background (bg) et mise en plein écran
    

    while True:
    
        event=interactions() # Récupération des interactions
        
        if event==0: # Pression sur Entrée --> Appel de la fonction MENU
            
            menu() 
            
        screen.blit(titre1,(0,0)) # Alternance entre les images avec ou sans le message "PRESS ENTER"
        pygame.display.flip()
        pygame.time.delay(900)
        screen.blit(titre2,(0,0))
        pygame.display.flip()
        pygame.time.delay(1800)
    return

def menu(): # Affichage du menu et selection d'un mode (JEU/INSTRUCTIONS/HISTOIRE/OPTIONS)
    
    pygame.key.set_repeat(100000,100000) # Key repeat mis a de grande valeur puisqu'il est indispensable lors de la phase de jeu mais pas dans le menu
    reinit()
    screen= pygame.display.set_mode((664,388),FULLSCREEN)
    n=0 # Index de l'image à afficher

    while True:
        event=interactions() # Récupération des interactions
        
        if event==1: # Flèche du haut --> on charge une autre image un rang plus haut
            n=n-1
            if n==-1: n=4 # Si on monte trop haut, retour au dernier choix possible
            
        if event==2: # Flèche du bas --> on charge une autre image un rang plus bas
            
            n=n+1
            if n==5: n=0 # Si on descend trop bas, retour au premier choix
            
        if event==0: # Si on appuie sur Entrée, on regarde quelle valeur de n on a, c'est à dire le choix selectionné
            
            if n==0:
                choixDifficulte()
            elif n==1:
                instructions()
            elif n==2:
                Histoire()
            elif n==3:
                Highscores()
            elif n==4:
                pygame.font.quit()
                pygame.quit()
                sys.exit()
                    
        screen.blit(menuFond[n],(0,0)) # Affichage de l'image d'indice n
        pygame.display.flip() # Update de l'écran
        
    return

def jeu(): # Fonction principale du jeu
    
    
    pygame.key.set_repeat(5,19)
    x,y=background[0].get_size()
    screen= pygame.display.set_mode((x,y),FULLSCREEN) # Adaptation de l'ecran à la taille du background (bg) et mise en plein écran
    
    
    while True:
        personnageSprite.mouvementPerso()
        tortueSprite.mouvementTortue()
        affichage()

def interactions(): # Récupère les interactions avec le clavier et renvoie une valeur pour chaque interaction possible
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: # Sortie du programme
            pygame.quit()
            sys.exit()
        if event.type==KEYDOWN and event.key==K_ESCAPE: # Sortie du programme après pression de ECHAP
            screen.fill(0)
            pygame.mixer.stop()
            menu()
        if event.type == KEYDOWN and event.key== K_RETURN: # Pression boutton Entrée, on renvoie la valeur 0
            return 0
        if event.type == KEYDOWN and event.key== K_UP: # Pression flèche du haut, on renvoie la valeur 1
            return 1
        if event.type == KEYDOWN and event.key== K_DOWN: # Pression flèche du bas, on renvoie la valeur 2
            return 2
        if event.type == KEYDOWN and event.key== K_RIGHT: # Pression flèche de droite, on renvoie la valeur 3
            return 3
        if event.type == KEYDOWN and event.key== K_LEFT: # Pression flèche de gauche, on renvoie la valeur 4
            return 4
        if event.type == KEYUP and event.key==K_RIGHT:
            return 50
        if event.type == KEYUP and event.key==K_LEFT:
            return 50
        
    
    
            
    return None # Si il n'y a eu aucun évènement on renvoie la valeur None

def instructions(): # Affiche les intructions du jeu
    pygame.key.set_repeat(100000,100000)
    n=0 # Index de l'image à afficher
    while True:
        event=interactions() # Récupération des interactions
        if event==0:
            n+=1
            if n==3:
                n=0
        screen.fill(0)
        screen.blit(instruction[n],(0,0)) # Affichage de l'image d'indice n
        pygame.display.flip()

def Histoire():# Affiche l'histoire pour ceux qui ne connaissent pas la série
    pygame.key.set_repeat(100000,100000)
    n=0 # Index de l'image à afficher
    while True:
        event=interactions() # Récupération des interactions
        if event==0:
            n+=1
            if n==2:
                n=0
        screen.fill(0)
        screen.blit(histoire[n],(0,0)) # Affichage de l'image d'indice n
        pygame.display.flip()

def Highscores(): #Affichage des scores
    while True:
        event=interactions() # Récupération des interactions
        screen.blit(scoresImage,(0,0))
        fichier=open("scores.txt", "r") #ouverture du fichier texte contenant les meilleurs scores enregistrés
        liste=fichier.readlines() #récupération de chaque ligne du document dans une variable de la liste
        for i in range (0,10):
            liste[i]=liste[i].strip('\n') #suppression du retour à la ligne "/n" au bout de chaque variable
        i=0
        afficheF=5*['']
        while i<10:
            afficheF[i/2]=font.render(str((i/2)+1)+". "+str(liste[i])+": "+str(liste[i+1]),1,(255,255,255)) # remplissage le la liste "affiche" par les chaines de caractères qu'elle va contenir: Rang de 1 à 5+" ."+nom du joueur+score
            i+=2
        for i in range (0,5):
            screen.blit(afficheF[i], (150,150+(i*50))) # disposition des éléments de la liste sur l'écran
        pygame.display.flip() #rafraichissement de l'écran
        fichier.close()

def choixDifficulte():
    global difficulte,tempsLimite, difficile
    n=0
    difficile=0
    while True:
        event=interactions() # Récupération des interactions
        
        if event==1: # Flèche du haut --> on charge une autre image un rang plus haut
            n=n-1
            if n==-1: n=2 # Si on monte trop haut, retour au dernier choix possible
            
        if event==2: # Flèche du bas --> on charge une autre image un rang plus bas
            
            n=n+1
            if n==3: n=0 # Si on descend trop bas, retour au premier choix
            
        if event==0:
            
            if n==0:
                tempsLimite=100 #application de 100 s comme temps maximal pour tous les niveaux
                selectionPerso()
            elif n==1:
                tempsLimite=50 #application de 50 s comme temps maximal pour tous les niveaux
                selectionPerso()
            elif n==2:
                difficile=True #activation du mode difficile --> temps adapté selon le niveau
                selectionPerso()
        screen.blit(difficulte[n],(0,0)) # Affichage de l'image d'indice n
        pygame.display.flip() # Update de l'écran
    

def selectionPerso():# Selection personnage 
    global persochoisi,sonJeu
    
    pygame.mixer.stop()
    sonJeu.play(-1)
    
    pygame.key.set_repeat(100000,100000)
    
    n=0 # Index de l'image à afficher
    while True:
        event=interactions() # Récupération des interactions
        
        if event==1: # Flèche du haut --> on charge une autre image celle avec surbrillance un rang plus haut
            n=n-1
            if n==-1: n=4 # Si on monte trop haut, retour au dernier choix possible
            
        if event==2: # Flèche du bas --> on charge une autre image celle avec surbrillance un rang plus bas
            
            n=n+1
            if n==5: n=0 # Si on descend trop bas, retour au premier choix
            
        if event==0: # Si on appuie sur Entrée, on regarde quelle valeur de n on a
            
            if n==0: #si on est sur l'image associé à l'index 0 
                load_walter() #envoi vers la fonction de chargement du personnage choisi 
                interNiveau(1) #envoi vers la fonction qui affiche l'écran "level 1"
                levelInit() #envoi vers la fonction qui charge le jeu

            
            elif n==1:
                load_junior()
                interNiveau(1)
                levelInit()
                
            elif n==2:
                load_jesse()
                interNiveau(1)
                levelInit()

            elif n==3:
                load_gustavo()
                interNiveau(1)
                levelInit()
                
            elif n==4:
                load_hector()
                interNiveau(1)
                levelInit()
                
        screen.blit(selection[n],(0,0)) # Affichage de l'image d'indice n
        pygame.display.flip() # Update de l'écran
    
    return


def levelInit(): # Initialise le niveau
    global personnageSprite, score, tortueSprite, plateformeBasSprite1,plateformeBasSpriteR,level,sachetGroup,flaconGroup,tortueCollision,explosion,start,vie,coeurs, c, saut,memoire,fall,compteurSaut

    saut=False #initialisation des variables de jeu
    fall=True
    compteurSaut=0
    memoire=3
    personnageSprite=Personnage()# création des sprites personnage, tortue et plateforme du bas
    tortueSprite=Tortue()
    plateformeBasSprite1=PlateformeBas()
    plateformeBasSprite1.position()
    
    
    plate=load_level(level,'plateforme') # appel de la fonction "load_level" pour charger les plateformes, sachets et flacons
    sachet=load_level(level,'sachet')
    flacon=load_level(level,'flacon')
    
    
    plateformeBasSpriteR=pygame.sprite.RenderPlain(plateformeBasSprite1,plate) # création d'un groupe de sprites: plateformes et plateforme du bas
    plateformeBasSpriteR.update()

    
    sachetGroup=pygame.sprite.Group(sachet) # création d'un groupe de sprites: sachet
    flaconGroup=pygame.sprite.Group(flacon) # création d'un groupe de sprites: flacon
    tortueCollision=False
    
    start=time.clock() #enregistrement de la date de début de la partie(heures/secondes)
    
    j=0 
    c=3*[0] #création d'une liste contenant 3 variables égales à 0
    coeurs=pygame.sprite.Group() #création d'un groupe de sprites: "coeurs" (=nombre de vies affiché à l'écran)
    while j<vie: # pour chaques vies restantes:
        c[j]=Coeur() #on crée un nouveau sprite "Coeur"
        c[j].pos(765-(j*18)) #décalage des coordonnées pour ne pas que les coeurs se superposent à l'écran
        coeurs.add(c[j]) #ajout du sprite "Coeur numéro j" au groupe de sprites "coeurs"
        j+=1
        
    
    jeu() 



def affichage(): # Affichage à l'écran de différent objet (argument liste d'objet et une liste de position)
 
    global start,s,tempsLimite,difficile,tempsLim,level
    
    screen.blit(background[levelIndex], (0,0)) #affichage le l'arrière plan correspondant au groupe de niveaux(1-4, 5-9, 10-15)
    rectPersonnage=personnageSprite.position() #récupération de la position du personnage
    rectTortue=tortueRect #récupération de la position de la tortue
    plateformeBasSpriteR.draw(screen) #affichage de la plateforme du bas, des sachets et flacons
    sachetGroup.draw(screen) 
    flaconGroup.draw(screen)
    screen.blit(persochoisi[index],personnageRect) #affichage aux coordonnées de l'image correspondant au mouvement du personnage
    screen.blit(tortue[indexTortue],rectTortue) #affichage aux coordonnées de l'image correspondant au mouvement de la tortue
    coeurs.draw(screen) # affichage des coeurs
    
    s="Score: " +str(score) # création d'une chaîne de caractères "Score:"+ le score
    scoreS=font.render(s,1,(0,0,0)) #crée une surface qui contient le texte de cette chaîne
    screen.blit(scoreS,(0,0)) #affichage de cette surface

    if difficile==True: # en mode difficile (voir "choisDifficulte")
        tempsLimite=tempsLim[level-1] # le temps limite est récupéré depuis la liste "tempsLim" qui contient les temps adaptés à chaque niveau
    
    ecoule=( time.clock()- start) # variable qui contient le temps écoulé ===> différence entre la date de départ(voir LevelInit) et la date actuelle
    temps=int(tempsLimite-ecoule+1) #decompte tempsLimite - temps écoulé + 1 (à cause d'un décalage)

    timer=str(temps) #meme principe que pour le score
    timerS=font.render(timer,1,(0,0,0))#idem
    screen.blit(timerS,(365,0))#idem
    
    pygame.display.flip()# Update de l'écran
    
    if temps==0:
        game_over()


def animation(increment,direction): # Renvoie l'index de l'image du personnage correspondant à sa direction et à l'index du mouvement
    numeroInd=0
    
    if direction==3:#si le personnage va vers la droite:
        if increment==1:
            numeroInd=1
        elif increment<=3:
            numeroInd=2
        elif increment<=5:
            numeroInd=3
        
    if direction==4:#si le personnage va vers la gauche:
        if increment==1: 
            numeroInd=6    
        elif increment<=3:
            numeroInd=7
        elif increment<=5:
            numeroInd=8
        
    return numeroInd
    

def main_load(): # Lancement des fonctions de chargement des images, son et autres  
   
    pygame.font.init()
    pygame.time.Clock()
    load_level_time()
    load_score_image()
    load_difficulte()
    load_histoire()
    load_instruction()
    load_objet_image()
    load_police()
    load_background()
    load_tortue()
    load_selection()
    load_fin()
    load_menu()
    load_titre()
    load_son()

#Chargement des images pour divers menu et autres:

def load_score_image(): #tableau de scores
    global scoresImage
    scoresImage=pygame.image.load('image/scores.png').convert()
    
def load_difficulte():  #menu de choix de difficulté
    global difficulte
    difficulte1=pygame.image.load('image/difficulte1.png').convert()
    difficulte2=pygame.image.load('image/difficulte2.png').convert()
    difficulte3=pygame.image.load('image/difficulte3.png').convert()
    difficulte=[difficulte1,difficulte2,difficulte3]
    
def load_histoire():
    global histoire
    histoire1=pygame.image.load('image/histoire1.png').convert()
    histoire2=pygame.image.load('image/histoire2.png').convert()

    histoire=[histoire1,histoire2]
    
def load_instruction(): 
    global instruction
    instruction1=pygame.image.load('image/instruction1.png').convert()
    instruction2=pygame.image.load('image/instruction2.png').convert()
    instruction3=pygame.image.load('image/instruction3.png').convert()

    instruction=[instruction1,instruction2,instruction3]
    
def load_objet_image():
    global plateformeBas,plateforme,sachet,flacon,coeur
    plateformeBas=pygame.image.load('Plateformes/PlateformeBas.png').convert()
    plateformeBas.set_colorkey((0,0,0),RLEACCEL)

    plateforme=pygame.image.load('Plateformes/plate2.png').convert()
    plateforme.set_colorkey((0,0,0),RLEACCEL)

    sachet=pygame.image.load('image/sachet.png').convert()
    sachet.set_colorkey((255,255,255),RLEACCEL)

    flacon=pygame.image.load('image/flacon.png').convert()
    flacon.set_colorkey((127,127,127),RLEACCEL)
    
    coeur=pygame.image.load('image/coeur.png')
    coeur.set_colorkey((127,127,127),RLEACCEL)
    
def load_police(): #chargement de la police
    global font
    font=pygame.font.Font('FreeSansBold.ttf',16)

#chargement des images   
def load_background():
    global background
    background1=pygame.image.load('image/background1.png').convert()
    background2=pygame.image.load('image/background2.png').convert()
    background3=pygame.image.load('image/background3.png').convert()
    background=[background1,background2,background3]

def load_tortue():
    global tortue
    tortue1=pygame.image.load('image/tortue/tortue1.png').convert()
    colorkey=tortue1.get_at((0,0))
    tortue1.set_colorkey(colorkey,RLEACCEL)
    tortue2=pygame.image.load('image/tortue/tortue2.png').convert()
    tortue2.set_colorkey(colorkey,RLEACCEL)
    tortue3=pygame.image.load('image/tortue/tortue3.png').convert()
    tortue3.set_colorkey(colorkey,RLEACCEL)
    tortue4=pygame.image.load('image/tortue/tortue4.png').convert()
    tortue4.set_colorkey(colorkey,RLEACCEL)
    tortue5=pygame.image.load('image/tortue/tortue5.png').convert()
    tortue5.set_colorkey(colorkey,RLEACCEL)
    tortue6=pygame.image.load('image/tortue/tortue6.png').convert()
    tortue6.set_colorkey(colorkey,RLEACCEL)
    tortue7=pygame.image.load('image/tortue/tortue7.png').convert()
    tortue7.set_colorkey(colorkey,RLEACCEL)
    tortue8=pygame.image.load('image/tortue/tortue8.png').convert()
    tortue8.set_colorkey(colorkey,RLEACCEL)
    tortue9=pygame.image.load('image/tortue/tortue9.png').convert()
    tortue9.set_colorkey(colorkey,RLEACCEL)
    tortue10=pygame.image.load('image/tortue/tortue10.png').convert()
    tortue10.set_colorkey(colorkey,RLEACCEL)
    tortue11=pygame.image.load('image/tortue/tortue11.png').convert()
    tortue11.set_colorkey(colorkey,RLEACCEL)
    tortue12=pygame.image.load('image/tortue/tortue12.png').convert()
    tortue12.set_colorkey(colorkey,RLEACCEL)
    tortue13=pygame.image.load('image/tortue/tortue13.png').convert()
    tortue13.set_colorkey(colorkey,RLEACCEL)
    tortue14=pygame.image.load('image/tortue/tortue14.png').convert()
    tortue14.set_colorkey(colorkey,RLEACCEL)
    tortue15=pygame.image.load('image/tortue/tortue15.png').convert()
    tortue15.set_colorkey(colorkey,RLEACCEL)

    tortue=[tortue1,tortue2,tortue3,tortue4,tortue5,tortue6,tortue7,tortue8,tortue9,tortue10,tortue11,tortue12,tortue13,tortue14,tortue15]

def load_selection():
    global selection
    sel1=pygame.image.load('image/selectionww.png').convert() #chargement image selection du personnage
    sel2=pygame.image.load('image/selectionwjr.png').convert()
    sel3=pygame.image.load('image/selectionjp.png').convert()
    sel4=pygame.image.load('image/selectiongf.png').convert()
    sel5=pygame.image.load('image/selectionhs.png').convert()
    selection=[sel1,sel2,sel3,sel4,sel5]


def load_fin(): #chargement des éléments pour l'animation de fin
    global fin,fin2,car,fin3,gameover
    gameover=pygame.image.load('image/gameover.png').convert()
    fin=pygame.image.load('image/fin.png').convert()
    fin2=pygame.image.load('image/fin2.png').convert()
    fin3=pygame.image.load('image/fin3.png').convert()
    car1=pygame.image.load('image/car1.png').convert()
    car1.set_colorkey((255,255,255),RLEACCEL)
    car2=pygame.image.load('image/car2.png').convert()
    car2.set_colorkey((255,255,255),RLEACCEL)
    car3=pygame.image.load('image/car3.png').convert()
    car3.set_colorkey((255,255,255),RLEACCEL)
    car4=pygame.image.load('image/car4.png').convert()
    car4.set_colorkey((255,255,255),RLEACCEL)
    car5=pygame.image.load('image/car5.png').convert()
    car5.set_colorkey((255,255,255),RLEACCEL)
    car6=pygame.image.load('image/car6.png').convert()
    car6.set_colorkey((255,255,255),RLEACCEL)
    
    car=[car1,car2,car3,car4,car5,car6]

    
def load_menu():
    global menuFond
    bgm1=pygame.image.load('image/menu1.png').convert() # Chargement des images du menu principal
    bgm2=pygame.image.load('image/menu2.png').convert()
    bgm3=pygame.image.load('image/menu3.png').convert()
    bgm4=pygame.image.load('image/menu4.png').convert()
    bgm5=pygame.image.load('image/menu5.png').convert()
    
    menuFond=[bgm1,bgm2,bgm3,bgm4,bgm5] # Regroupement dans une liste

def load_titre():
    global titre1,titre2
    titre1=pygame.image.load('image/title.png').convert() # Chargement de l'écran titre
    
    titre2=pygame.image.load('image/title-enter.png').convert() # CHargement de l'écran titre avec le message


#chargement des sons
def load_son():
    global sonJeu, sonExplosion,sonFlacon, sonVictoire, sonOver,sonTitre,sonSnif
    sonJeu=pygame.mixer.Sound('sound/Tamacun.wav')
    sonJeu.set_volume(0.05)

    sonSnif=pygame.mixer.Sound('sound/snif.wav')
    sonSnif.set_volume(0.3)

    sonOver=pygame.mixer.Sound('sound/over.wav')
    sonOver.set_volume(0.2)
    
    sonExplosion=pygame.mixer.Sound('sound/explosion.wav')
    sonExplosion.set_volume(0.4)

    sonFlacon=pygame.mixer.Sound('sound/flacon.wav')
    sonFlacon.set_volume(0.2)

    sonVictoire=pygame.mixer.Sound('sound/won.wav')
    sonVictoire.set_volume(0.2)

    sonTitre=pygame.mixer.Sound("sound/BBgenerique.wav")
    
    sonTitre.set_volume(0.1)
    sonTitre.fadeout(500)
    
def load_level_time(): #récupération des temps dans le fichier texte pour le mode difficile
    global tempsLim
    tempsLim=15*[0]
    fichier=open('levels/tempsLevels.txt',"r")
    liste=fichier.readlines()
    i=0
    while i < 15:
        tempsLim[i]=int(liste[i])
        i+=1
        


#load des images des différents perso
def load_walter(): 

    global persochoisi
    
    walter1=pygame.image.load('image/ww/1.png').convert() 
    colorkey=walter1.get_at((0,0))
    walter1.set_colorkey(colorkey,RLEACCEL)
    walter2=pygame.image.load('image/ww/2.png').convert()
    walter2.set_colorkey(colorkey,RLEACCEL)
    walter3=pygame.image.load('image/ww/3.png').convert()
    walter3.set_colorkey(colorkey,RLEACCEL)
    walter4=pygame.image.load('image/ww/4.png').convert()
    walter4.set_colorkey(colorkey,RLEACCEL)
    walter5=pygame.image.load('image/ww/5.png').convert()
    walter5.set_colorkey(colorkey,RLEACCEL)
    walter6=pygame.image.load('image/ww/6.png').convert()
    walter6.set_colorkey(colorkey,RLEACCEL)
    walter7=pygame.image.load('image/ww/7.png').convert()    
    walter7.set_colorkey(colorkey,RLEACCEL)
    walter8=pygame.image.load('image/ww/8.png').convert()    
    walter8.set_colorkey(colorkey,RLEACCEL)
    walter9=pygame.image.load('image/ww/9.png').convert()    
    walter9.set_colorkey(colorkey,RLEACCEL)
    walter10=pygame.image.load('image/ww/10.png').convert()    
    walter10.set_colorkey(colorkey,RLEACCEL)
    walter11=pygame.image.load('image/ww/11.png').convert()    
    walter11.set_colorkey(colorkey,RLEACCEL)
    
    persochoisi=[walter1,walter2,walter3,walter4,walter5,walter6,walter7,walter8,walter9,walter10,walter11]
   


def load_junior():
    global persochoisi
    
    junior1=pygame.image.load('image/wjr/1.png').convert()
    colorkey=junior1.get_at((0,0))    
    junior1.set_colorkey(colorkey,RLEACCEL)    
    junior2=pygame.image.load('image/wjr/2.png').convert()    
    junior2.set_colorkey(colorkey,RLEACCEL)    
    junior3=pygame.image.load('image/wjr/3.png').convert()    
    junior3.set_colorkey(colorkey,RLEACCEL)    
    junior4=pygame.image.load('image/wjr/4.png').convert()    
    junior4.set_colorkey(colorkey,RLEACCEL)
    junior5=pygame.image.load('image/wjr/5.png').convert()    
    junior5.set_colorkey(colorkey,RLEACCEL)
    junior6=pygame.image.load('image/wjr/6.png').convert()    
    junior6.set_colorkey(colorkey,RLEACCEL)
    junior7=pygame.image.load('image/wjr/7.png').convert()    
    junior7.set_colorkey(colorkey,RLEACCEL)
    junior8=pygame.image.load('image/wjr/8.png').convert()    
    junior8.set_colorkey(colorkey,RLEACCEL)
    junior9=pygame.image.load('image/wjr/9.png').convert()    
    junior9.set_colorkey(colorkey,RLEACCEL)
    junior10=pygame.image.load('image/wjr/10.png').convert()    
    junior10.set_colorkey(colorkey,RLEACCEL)
    junior11=pygame.image.load('image/wjr/11.png').convert()    
    junior11.set_colorkey(colorkey,RLEACCEL)
    
    persochoisi=[junior1,junior2,junior3,junior4,junior5,junior6,junior7,junior8,junior9,junior10,junior11]


    
def load_jesse():
    global persochoisi

    
    jesse1=pygame.image.load('image/jp/1.png').convert()
    colorkey=jesse1.get_at((0,0))
    jesse1.set_colorkey(colorkey,RLEACCEL)
    jesse2=pygame.image.load('image/jp/2.png').convert()
    jesse2.set_colorkey(colorkey,RLEACCEL)
    jesse3=pygame.image.load('image/jp/3.png').convert()
    jesse3.set_colorkey(colorkey,RLEACCEL)
    jesse4=pygame.image.load('image/jp/4.png').convert()
    jesse4.set_colorkey(colorkey,RLEACCEL)
    jesse5=pygame.image.load('image/jp/5.png').convert()
    jesse5.set_colorkey(colorkey,RLEACCEL)
    jesse6=pygame.image.load('image/jp/6.png').convert()
    jesse6.set_colorkey(colorkey,RLEACCEL)
    jesse7=pygame.image.load('image/jp/7.png').convert()
    jesse7.set_colorkey(colorkey,RLEACCEL)
    jesse8=pygame.image.load('image/jp/8.png').convert()
    jesse8.set_colorkey(colorkey,RLEACCEL)
    jesse9=pygame.image.load('image/jp/9.png').convert()    
    jesse9.set_colorkey(colorkey,RLEACCEL)
    jesse10=pygame.image.load('image/jp/10.png').convert()    
    jesse10.set_colorkey(colorkey,RLEACCEL)
    jesse11=pygame.image.load('image/jp/11.png').convert()    
    jesse11.set_colorkey(colorkey,RLEACCEL)
    
    persochoisi=[jesse1,jesse2,jesse3,jesse4,jesse5,jesse6,jesse7,jesse8,jesse9,jesse10,jesse11]

def load_gustavo():
    global persochoisi

    
    gustavo1=pygame.image.load('image/gf/1.png').convert()
    colorkey=gustavo1.get_at((0,0))
    gustavo1.set_colorkey(colorkey,RLEACCEL)  
    gustavo2=pygame.image.load('image/gf/2.png').convert()    
    gustavo2.set_colorkey(colorkey,RLEACCEL)    
    gustavo3=pygame.image.load('image/gf/3.png').convert()    
    gustavo3.set_colorkey(colorkey,RLEACCEL)    
    gustavo4=pygame.image.load('image/gf/4.png').convert()    
    gustavo4.set_colorkey(colorkey,RLEACCEL)
    gustavo5=pygame.image.load('image/gf/5.png').convert()   
    gustavo5.set_colorkey(colorkey,RLEACCEL)
    gustavo6=pygame.image.load('image/gf/6.png').convert()    
    gustavo6.set_colorkey(colorkey,RLEACCEL)
    gustavo7=pygame.image.load('image/gf/7.png').convert()    
    gustavo7.set_colorkey(colorkey,RLEACCEL)
    gustavo8=pygame.image.load('image/gf/8.png').convert()    
    gustavo8.set_colorkey(colorkey,RLEACCEL)
    gustavo9=pygame.image.load('image/gf/9.png').convert()    
    gustavo9.set_colorkey(colorkey,RLEACCEL)
    gustavo10=pygame.image.load('image/gf/10.png').convert()    
    gustavo10.set_colorkey(colorkey,RLEACCEL)
    gustavo11=pygame.image.load('image/gf/11.png').convert()    
    gustavo11.set_colorkey(colorkey,RLEACCEL)
    
    persochoisi=[gustavo1,gustavo2,gustavo3,gustavo4,gustavo5,gustavo6,gustavo7,gustavo8,gustavo9,gustavo10,gustavo11]

def load_hector():
    global persochoisi

    
    hector1=pygame.image.load('image/hs/1.png').convert()
    colorkey=hector1.get_at((0,0))
    hector1.set_colorkey(colorkey,RLEACCEL)    
    hector2=pygame.image.load('image/hs/2.png').convert()    
    hector2.set_colorkey(colorkey,RLEACCEL)    
    hector3=pygame.image.load('image/hs/3.png').convert()    
    hector3.set_colorkey(colorkey,RLEACCEL)    
    hector4=pygame.image.load('image/hs/4.png').convert()    
    hector4.set_colorkey(colorkey,RLEACCEL)
    hector5=pygame.image.load('image/hs/5.png').convert()    
    hector5.set_colorkey(colorkey,RLEACCEL)
    hector6=pygame.image.load('image/hs/6.png').convert()    
    hector6.set_colorkey(colorkey,RLEACCEL)
    hector7=pygame.image.load('image/hs/7.png').convert()    
    hector7.set_colorkey(colorkey,RLEACCEL)
    hector8=pygame.image.load('image/hs/8.png').convert()    
    hector8.set_colorkey(colorkey,RLEACCEL)
    hector9=pygame.image.load('image/hs/9.png').convert()    
    hector9.set_colorkey(colorkey,RLEACCEL)
    hector10=pygame.image.load('image/hs/10.png').convert()    
    hector10.set_colorkey(colorkey,RLEACCEL)
    hector11=pygame.image.load('image/hs/11.png').convert()    
    hector11.set_colorkey(colorkey,RLEACCEL)
    
    persochoisi=[hector1,hector2,hector3,hector4,hector5,hector6,hector7,hector8,hector9,hector10,hector11]


def load_level(level,objet):# Permet de charger le niveau en créant les objets aux bonnes coordonnées
    fichier=open('levels/level_%s/%s.txt'%(level,objet),"r")#Ouverture du fichier

    liste=fichier.readlines()#Lecture
    
    lon=len(liste)
    l=lon/2
    x=l*[0]
    y=l*[0]
    
    caractere=''
    typeL=0
    b=0
    n=0
    i=0
    inti=0
    while i<lon: #Boucle parcourant le fichier et récuperant les abscisses et ordonnées des objets
        caractere=liste[i]
        
        inti=int(i/2)
        if inti==i/2.0:
            if typeL==0:
                 
                x[n]=int(caractere)
                
            
        elif inti!=i/2.0:
            if typeL==0: 
                y[n]=int(caractere)
                n=n+1
                
            
        i=i+1          
    objetListe=[]
    
    for j in range(0,l):#selon l'objet choisi, on appelle des class différentes.
        
        if objet=='plateforme':
            p=Plateforme()
        elif objet=='sachet':
            p=Sachet()
        elif objet=='flacon':
            p=Flacon()
        objetListe.append(p)
        objetListe[j].position(x[j],y[j])
    
    return objetListe #on renvoie l'objet créer
    




def mouvement(direction,rectPerso): # Fait bouger le personnage prend en argument le type de mouvement haut, bas, gauche, droite
    global collisionSens,index,fall,saut,memoire,persochoisi
    
    interpretationCollision(collisionSens,rectPerso)#Selon la direction du personnage, on modifie ses coordonnées(rectPerso)
    personnageSprite.image=persochoisi[index]
    if direction==1:
        rectPerso.left=rectPerso.left+2
    elif direction==2 :
        rectPerso.left=rectPerso.left-2
    elif direction==3:
        rectPerso.bottom=rectPerso.bottom-1
        pygame.time.delay(10)
    elif direction==4:
        
        rectPerso.bottom=rectPerso.bottom+1
        pygame.time.delay(10)
        if fall==False:
            index=0
    
    return rectPerso



def interpretationCollision(sens,rectPerso):#Cette fonction interprete les résultats du test de collision
    global collisionSens,fall,index,compteurSaut
   
    if sens!=0:  
            
        if sens==3:
            compteurSaut=0
            saut=False
        elif sens==4 and compteurSaut==0:
            
            fall=False
            index=0
            
    
    
class Personnage(pygame.sprite.Sprite):#Permet de créer un personnage, de la faire se déplacer, et de tester les collisions avec les différents objets
    
    def __init__(self):#Initialisation de la classe (coordonnées de départ, image)
        global personnageRect
        pygame.sprite.Sprite.__init__(self)        
        self.image=persochoisi[0]
        self.rect=persochoisi[0].get_rect()#création d'une surface contenant le personnage avec les dimensions de la première image
        
        self.rect.top=350
        self.rect.left=10
        
        personnageRect=self.rect
    

    def mouvementPerso(self):#Fonction permettant le mouvement du personnage, réalisant les tests pour savoir si un mouvement est possible ou non
        global saut, memoire, index, i, fall,collisionSens,sol

        
        evenement=interactions()#Récupération des interractions
        collisionSens=personnageSprite.collision()#Test de collision avec les plateformes
        personnageSprite.collisionSachets()#Test de collision avec les sachets
        personnageSprite.collisionFlacons()#Test de collision avec les Flacons
        personnageSprite.collisionTortue()#Test de collision avec la tortue
        
        if evenement ==3 and collisionSens!=1 and self.rect.right<770: #On test si le personnage peut aller vers la droite à condition qu'il ne soit pas contre une plateforme ou contre le bord du niveau
            i=i+1
            self.rect=mouvement(1,self.rect)#On appelle alors la fonction mouvement
            index=animation(i,evenement)#Ainsi que la fonction animation pour modifier ou non l'image du personnage à afficher
            if i==5:#i est la variable qui permet de tester si il faut changer ou non l'image à afficher
                i=0
                    
        elif evenement ==4 and collisionSens!=2 and self.rect.left>0:#On test si le personnage peut aller vers la gauche à condition qu'il ne soit pas contre une plateforme ou contre le bord du niveau
            i=i+1
            self.rect=mouvement(2,self.rect)
            index=animation(i,evenement)
            if i==5:
                i=0
                
        elif evenement ==50:#Lorsque que l'on relache les touches de mouvement latéral, la fonction interraction renvoie la valeur 50 afin que l'on affiche l'image 0 du personnage
            
            index=0
            
        elif evenement==1 and collisionSens!=0 and collisionSens!=3 and sol==True:#Si le personnage est dans les bonnes conditions ( pas de plateforme au dessus, qu'il touche le sol) on change le booléen saut
            
            saut=True
            sol=False
            
            
        self.saut(memoire)
        
        self.fall()
            
        if evenement == 3 or evenement ==4:# On prend en mémoire la direction dans laquelle se déplacer le personnage, pour l'animation pendant les sauts
            memoire=evenement

        

        
    def saut(self,memoire):#Fonciton qui permet de réaliser un saut
        global saut,fall,index,compteurSaut,collisionSens
        
        
        if compteurSaut==0 and saut==True and collisionSens!=3:# Si on vient de sauter, on active le compteur de saut pour que le personnage monte petit à petit et que l'on puisse toujours interagir avec lui
            compteurSaut=100
            

            
        if compteurSaut>0:
            compteurSaut=compteurSaut-1
            if memoire==3: #selon le sens de déplacement on donne un index différent pour l'animation
                index=4
                
            elif memoire==4:
                index=9
                
            
                
            self.rect=mouvement(3,self.rect)#on appelle la fonction mouvement en lui donnant la valeur 3 qui correspond à une diminution de l'ordonnée du personnage
        if compteurSaut==0 or collisionSens==3:#Lorsque le compteur saut arrive à 0, on active la chute et le personnage commence à descendre
                saut=False
                fall=True
                
                

    def fall(self):#Fonction permettant la chute
        global saut, fall,index,collisionSens,memoire,sol
        
        if collisionSens==4:#Si on touche le sol, on arrete la chute et on remet le booléen sol à True
            fall=False
            sol=True
             
        
            
        if fall==True:# Selon le sens de déplacement, on change l'image du personnage
            sol=False
            if memoire==3:
                index=5
            elif memoire==4:
                index=10
        if saut==False and collisionSens!=4:
            
            if fall==False:
                fall=True
            self.rect=mouvement(4,self.rect)#on appelle la fonction mouvement en lui donnant la valeur 4 qui correspond à une augmentation de l'ordonnée du personnage
                
    def collision(self):#Fonction qui teste les collisions avec les plateformes
        
        global plateformeBasSpriteR,memoireMouvement,personnageSprite,collisionSens,index
        
        plateformeCollision=pygame.sprite.spritecollideany(personnageSprite,plateformeBasSpriteR)#On met dans une variable, l'objet avec lequel le personnage est en collision (lorsqu'il y a contact)
        
        if plateformeCollision != None:#Si il n'y a pas de collision, la variable plateformeCollision prend comme valeur None
            
            if personnageSprite.rect.bottom==plateformeCollision.rect.top+1 and collisionSens!=4:#Selon les coordonnées du personnage, par rapport à celles de la plateforme, on modifie la variable sensCollision
                sensCollision=4
                index=0
                return sensCollision
            elif personnageSprite.rect.top==plateformeCollision.rect.bottom-1 and collisionSens!=3:
                sensCollision=3
                return sensCollision
            elif personnageSprite.rect.right==plateformeCollision.rect.left+1 and collisionSens!=1:
                
                sensCollision=1
                return sensCollision
            elif personnageSprite.rect.left==plateformeCollision.rect.right-1 and collisionSens!=2:
                
                sensCollision=2
                return sensCollision
            #Il y a deux variables différentes, collisionSens et sensCollision, elles sont différentes et permettent de déterminer le sens de la collision si il est différent du sens de la dernière collision
            return collisionSens
        return 0#Si il n'y a pas de collision, on renvoie la valeur 0


    def collisionSachets(self):#Fonction qui gère le collision avec les sachets
        global sachetGroup,personnageSprite,sonSnif,score
        objetCollision=pygame.sprite.spritecollideany(personnageSprite,sachetGroup)#En cas de collision, on met l'objet qui est en collision dans une variable.
        if objetCollision!= None:
            sonSnif.play()#On joue le son de récupération d'un sachet
            sachetGroup.remove(objetCollision)#On enlève l'objet du groupe d'objet pour qu'il ne soit plus afficher
            liste=sachetGroup.sprites()#on met tous les objets restants dans une liste
            score+=100#On augmente le score
            if liste==[]:#Si la liste est vide, il n'y a plus de sachet à ramasser, on passe donc au niveau suivant
                
                levelChange()

                
    def collisionFlacons(self):#Fonction qui gère les collisions avec les flacons
        global flaconGroup,personnageSprite,sonFlacon,score
        flaconCollision=pygame.sprite.spritecollideany(personnageSprite,flaconGroup)
        if flaconCollision!= None:
            sonFlacon.play()
            score+=25
            flaconGroup.remove(flaconCollision)
            
    def collisionTortue(self):#Fonction qui gère les collisions avec la torute
        global personnageSprite, tortueSprite, explosion, tortueCollision, level
        tortueCollision=pygame.sprite.collide_rect(personnageSprite,tortueSprite)#Test de la collision avec la tortue
        if tortueCollision != False: # En cas de collision, on lance l'animation
            
            tortueSprite.rect.bottom=339
            tortueSprite.rect.left=tortueSprite.rect.left-55
            sonExplosion.play()
            for i in range (4,15):#Animation de l'explosion
                screen.blit(background[levelIndex], (0,0))
                plateformeBasSpriteR.draw(screen)
                sachetGroup.draw(screen)
                flaconGroup.draw(screen)
                explosionRect=tortueSprite.rect
                screen.blit(tortue[i],explosionRect)
                pygame.display.flip()
                pygame.time.delay(100)
            pygame.time.delay(600)
            gestionVie()#On appelle la fonction gestion de vie pour retirer une vie au joueur
            
    
    def position(self):#renvoie la position de la tortue
        return self.rect




class PlateformeBas(pygame.sprite.Sprite):#Classe de la plateforme du bas

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= plateformeBas
        self.rect=plateformeBas.get_rect()
        
    def position(self):
        
        self.rect.bottom=421
        self.rect.left=0
        

class Plateforme(pygame.sprite.Sprite):#Classe des autres plateformes

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= plateforme
        self.rect=plateforme.get_rect()
        
        

    def position(self,x,y):
        self.rect.top=y
        self.rect.left=x
        


class Sachet(pygame.sprite.Sprite): #Classe de création des sachets

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= sachet
        self.rect=sachet.get_rect()
        
    def position(self,x,y):
        self.rect.bottom=y
        self.rect.left=x

class Flacon(pygame.sprite.Sprite):#Classe de création des flacons
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= flacon
        self.rect=flacon.get_rect()
        
    def position(self,x,y):
        self.rect.bottom=y
        self.rect.left=x

class Tortue(pygame.sprite.Sprite):#Classe de la tortue
    def __init__(self):#Initialisation de la tortue (position, image,...)
        global tortueRect,directionTortue,indexTortue
        pygame.sprite.Sprite.__init__(self)        
        self.image=tortue[0]
        self.rect=tortue[0].get_rect()
        directionTortue=1
        self.rect.top=380
        self.rect.left=750
        directionTortue=1
        indexTortue=0
        tortueRect=self.rect

    def mouvementTortue(self):#Fonction faisant bouger la tortue
        global tortueRect,directionTortue, indexTortue, index2

        
        if self.rect.left>1 and directionTortue==1:#Mouvement dans une direction en fonction des coordonnées de la tortue (tant qu'elle reste au bon endroit)
            if fall==False and saut==False :
                pygame.time.delay(10)
                self.rect.left=self.rect.left-1
            else:
                self.rect.left=self.rect.left-1
            index2+=1
            #Modification des indexs pour l'animation
            if index2==3:
                indexTortue=1
            elif index2==6:
                indexTortue=0
            if index2==6:
                index2=0
        elif self.rect.left<750 and directionTortue==2:#Mouvement dans une direction en fonction des coordonnées de la tortue (tant qu'elle reste au bon endroit)
            if fall==False and saut==False:
                pygame.time.delay(10)
                self.rect.left=self.rect.left+1
            else:
                self.rect.left=self.rect.left+1
            index2+=1
            #Modification des indexs pour l'animation
            if index2==3:
                indexTortue=3
            elif index2==6:
                indexTortue=2
            if index2==6:
                index2=0   
        if self.rect.left<=1:#Si la& tortue arrive au bord de l'écran, elle change de sens
            directionTortue=2
            indexTortue=2
        if self.rect.left>=750:
            directionTortue=1
            indexTortue=0
        tortueRect=self.rect



class Coeur(pygame.sprite.Sprite):#Création des coeurs (uniquement pour affichage)
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect=coeur.get_rect()
        self.image=coeur
        
    def pos(self,x):
        self.rect.top=5
        self.rect.right=x


def interNiveau(niveau):#Fonction affichant le numero du niveau, juste avant de le commencer
    screen= pygame.display.set_mode((770,421),FULLSCREEN) 
    policeL=pygame.font.Font('FreeSansBold.ttf', 22)
    screen.fill(0)#on affiche un ecran noir
    numero="Level "+str(niveau)
    levelNum=policeL.render(numero,1,(255,255,255))#on affiche 
    screen.blit(levelNum,(350,150))
    pygame.display.flip()
    pygame.time.delay(2500)


        
def levelChange(): # Changement de level 
        global level,screen,plateformeBasSpriteR,sachetGroup,levelIndex
        if level==15:#Si on termine le dernier niveau, on lance l'ecran de fin
            Fin()
        
        plateformeBasSpriteR.empty()#On vide les groupes d'objets
        sachetGroup.empty()
        tortueSprite.__init__()#On initialise la tortue pour le niveau suivant
        level=level+1
        screen.fill((0,0,0))
        interNiveau(level)
        if level/5.0==int(level/5.0) and level!=15:#Tous les 5 niveaux, on change le fond d'ecran
            levelIndex=levelIndex+1
        levelInit()#On initialise ensuite le niveau

def Fin():#Affichage de l'ecran de fin et appel de la fonction récupérant le nom du joueur
    screen.fill(0)
    pygame.mixer.stop()
    pygame.display.flip()
    pygame.time.delay(1000)
    ecranFin()
    screen.fill(0)
    reinit()
    nom(fin3)
    
    menu()


def ecranFin():#Affiche le "générique" de fin en faisant bouger la voiture le long de la route
    global screen
    screen.blit(fin2,(53,10))
    pygame.display.flip()
    pygame.time.delay(6000)
    screen.fill(0)
    
    sonVictoire.play()
    x=-100
    n=0
    m=2
    y=322
    i=0
    p=0
    moveCar=True
    screen= pygame.display.set_mode((679,421),FULLSCREEN)
    while True:
        pygame.display.flip()
        screen.fill(0)
        screen.blit(fin,(0,0))
        pygame.time.delay(10)
        if moveCar==True:
            x=x+1
            screen.blit(car[n],(x,y))
            if int((x/20.0)/2.0)==((x/20.0)/2.0):
                n=1
                y=y+2
            elif int(x/20.0)==x/20.0:
                n=0
                y=y-2
            if x>=450 and x<475:
                y=y-2
            if x==500:
                moveCar=False
        if moveCar==False:
            
            screen.blit(car[m],(x,y))
            i=i+1
            if i==5:
                m=m+1
            elif i==10:
                m=m+1
            elif i==15:
                m=m+1
            elif i==20:
                i=0
                m=2
            
            p=p+1
            if p==400:
                return
    

   
def game_over():#Si le joueur perd toutes ses vies ou dépasse le temps imparti, on appelle la fonction Game Over
    
    screen.blit(gameover,(0,0))
    reinit()
    pygame.display.flip()
    pygame.time.delay(500)
    sonOver.play()
    pygame.time.delay(1000)
    pygame.mixer.stop()
    nom(gameover)
    
    
def reinit():#Réinitialisation des variables
    global vie,score,level,levelIndex
    level=1
    
    vie=3
    levelIndex=0

    
def nom(fond):#Récupération du nom du joueur
    global screen,score
    screen= pygame.display.set_mode((770,421),FULLSCREEN)
    screen.blit(fond,(0,0))
    name = ''
    boucle=True
    entrer="Entrez votre nom: "
    scoreAffiche="Score: "+str(score)
    pygame.font.init()
    police = pygame.font.Font('FreeSansBold.ttf', 16)#Création d'une surface contenant le texte 
    
    scoreN=police.render(scoreAffiche,1,(255,255,255))
    enter = police.render(entrer,1,(255,255,255))
    pygame.key.set_repeat(100000,100000)#
    pygame.display.flip()
    while boucle==True:
        scoreN=police.render(s,1,(255,255,255))
        enter = police.render(entrer,1,(255,255,255))
        screen.blit(enter,(100,400))
        screen.blit(scoreN,(100,350))
        
        for evt in pygame.event.get():#On utilise une autre fonction que la fonction interaction car elle ne s'occupe pas des lettres sur le clavier
            
            if evt.type == KEYDOWN:
                
                if evt.unicode.isalpha():#Si une interaction correspond à la pression d'une lettre on l'ajoute à la liste entrer
                    name = evt.unicode                    
                    entrer=entrer+name
                    name=''
                elif evt.key == K_BACKSPACE:#Si on appuie sur la touche retour, on efface la dernière lettre et le dernier élément de la liste entrer
                    entrer=entrer[:-1]
                    screen.blit(fond,(0,0))
                    
                    
                elif evt.key == K_RETURN:#Si on appuie sur Entrée, on appelle la fonction triScore
                    screen.fill((0,0,0))
                    boucle=False
                    triScore(entrer)
            pygame.display.flip()
            
def triScore(nomJ):#Fonction qui tri les scores, si le score que l'on vient d'entrer est plus grand que l'un des scores déjà réalisés, on décale les score plus faibles vers le bas et il prend sa place
    global score
    
    longeur=len(nomJ)
    nomJ=nomJ[18:longeur]
    
    fichier=open('scores.txt' ,"r")#ouverture du fichier score
    liste=fichier.readlines()#on met tout le contenu du fichier dans une liste
    i=0
    j=1
    k=0
    otherScore=5*[0]
    otherName=5*[0]
    while j<10:
        inter=liste[j]
        inter=inter.strip("\n")#On enlève le retour à la ligne à la fin de chaque élément de la liste
        otherScore[i]=int(inter)#on recupère uniquement les scores dans une liste
        j=j+2
        i+=1
    i=0
    while k<10:
        otherName[i]=liste[k]#On recupère les noms dans une autre liste
        
        k=k+2
        i+=1
    otherScore.sort(None,None,1)
    
    l=0
    if score > int(otherScore[4]):
        
        while l<5:# ON teste ensuite si le score réalisé est plus grand qu'un de ceux qui se trouve dans le fichier score
            if score>int(otherScore[l]):
                
                otherScore=decalage(otherScore,l)# Si oui, on décale les scores et les noms à partir du rang du nouveau score, vers le bas
                otherName=decalage(otherName,l)
                otherScore[l]=score#On inscrit ensuite le nouveau score et le nouveau nom dans les listes
                otherName[l]=str(nomJ+'\n')
                
                l=10
            l+=1
        fichier.close()
        os.remove("scores.txt")#On ferme et on efface l'ancien fichier score
        file("scores.txt","w")#On crée un nouveau fichier ayant le même nom
        fichier=open("scores.txt","a")
        contenu=[]
        i=0
        ligne=''
        for i in range(0,5):#On écrit dans ce nouveau fichier le contenu des listes nom et score modifiées
        
            ligne= str(otherName[i])+ str(otherScore[i])+'\n'
            contenu.append(ligne)
        i=0
        for i in range(0,5):
            fichier.write(str(contenu[i]))
        fichier.close()
    score=0
    menu()
               
    
def decalage(liste,index):#Cette fonction permet de décaler les scores vers le bas
    i=0
    index=4-index
    while i< index:
        liste[4-i]=liste[4-(i+1)]
        i+=1
    return liste
    
def gestionVie():#Si on appelle cette on fonction on perd une vie et si il n'y a plus de vie on appelle la focntion game over
    global coeurs,vie
    
    coeurs.remove(c[3-vie])
    vie-=1
    if vie==0:
        game_over()
    levelInit()

#Détermination des variables globales, en dehors de toutes fonctions pour ne pas avoir de problème
global saut,compteurSaut,index,memoire,i,fall,collisionSens,memoireMouvement,level,sol,levelIndex,indexTortue, index2, score,vie
saut=False
compteurSaut=0
index=0
indexTortue=0
memoire=3
i=0
fall=False
collisionSens=0
level=1
sol=True
levelIndex=0
index2=0
score=0
vie=3
main()
