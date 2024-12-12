from model.model_tours import get_partie, add_tour_défausser, add_tour_placer, fin_partie
from util.pioche import get_pioche, update_pioche
#Commence par vérifier que l'on a l'id de la partie
ok = True

print("--------------")
print("session : ", SESSION)
print("request : ", REQUEST_VARS)
print("GET : ,", GET)
print("POST : ,", POST)
print("--------------")

partie = 0
    
if "partie" in GET:
    if not GET["partie"][0].isdigit():
        ok = False
    else:
        partie = int(GET["partie"][0])
elif "partie" in POST:
    if POST["partie"][0][:POST["partie"][0].find("?")].isdigit():
        print("et bah là")
        partie = int(POST["partie"][0][:POST["partie"][0].find("?")])
        #On doit réparer POST qui a un bug dans le script
        reste = POST["partie"][0][POST["partie"][0].find("?"):].split("=")
        print("reste : ", reste[0][1:])
        POST[reste[0][1:]] = [reste[1]]
        
    elif not POST["partie"][0].isdigit():
        ok = False
    else:
        partie = int(POST["partie"][0])
else:
    ok = False

print("get : ", GET)
print("post : ", POST)
print("ok : ", ok)
if ok:
    p = get_partie(SESSION['CONNEXION'], partie)
    print("partie : ", p)
    
    #On vas aller récuperer la parties ainsi que ses tours et sa dernière pioche sur le serveur
    
    
    if POST:
        #On vas analyser les trucs
        if POST["action_tour"][0] == "défausser" and "pioche" in POST:
            #On défausse et on incrémente le tour
            print("On défausse")
            print("Difficulté : [",  p.diff, "]")
            update_pioche(SESSION['CONNEXION'], partie, p.diff, int(POST["pioche"][0])-1)
            add_tour_défausser(SESSION['CONNEXION'], p)
        elif POST["action_tour"][0] == "placer" and "pioche" in POST and "grille" in POST:
            grille_x = int(POST["grille"][0].split("-")[0])
            grille_y = int(POST["grille"][0].split("-")[1])
            num_brique = int(POST["pioche"][0]) - 1
            print("position : ", grille_x, "-", grille_y)
            #On récupère la brique
            brique = get_pioche(SESSION['CONNEXION'], partie)[num_brique]
            
            #On vérifie son positionnement sur la grille
            placable = True
            for i in range(0, brique["longueur"]):
                for a in range(0, brique["largeur"]):
                    #On vérifie que la valeur soit égale à -1 sinon c'est pas possible
                    if not(0 <= grille_x+i < p.grille_longueur and 0 <= grille_y+a < p.grille_hauteur):
                        placable = False
                    elif p.grille[grille_x+i][grille_y+a] != -1:
                        placable = False
                    
            if placable:
                print("placable")
                for i in range(0, brique["longueur"]):
                    for a in range(0, brique["largeur"]):
                        p.grille[grille_x+i][grille_y+a] = brique["couleur"]
                #On enregistre le tour
                add_tour_placer(SESSION['CONNEXION'], p, brique, [grille_x, grille_y])
                #On change la pièce dans la pioche
                update_pioche(SESSION['CONNEXION'], partie, p.diff, num_brique)
                complète = True
                for i in p.grille:
                    for a in i:
                        if a == -1:
                            complète = False
                            break
                    if not complète:
                        break
                if complète:
                    fin_partie(SESSION['CONNEXION'], p, True)
            else:
                #La brique n'est pas plaçable
                REQUEST_VARS["err"] = "La brique n'est pas plaçable à cet endroit"
        #On vérifie le non dépassement du nombre de tour
        if p.tours_limités:
            if p.last_tour >= p.nb_tours:
                fin_partie(SESSION['CONNEXION'], p, False)
                        
                        
    for i in p.grille:
        print(i)
    REQUEST_VARS["partie"] = p
            
            
    
    pioche = get_pioche(SESSION['CONNEXION'], partie)
    REQUEST_VARS["pioche"] = pioche

