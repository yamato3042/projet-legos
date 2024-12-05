import random

if POST:
    pourcentage_cases_remplies = [0.10,0.20] 
    longueur = int(POST["longueur"][0])
    hauteur = int(POST["hauteur"][0])
    nb_cases = longueur*hauteur
    
    if not (5 <= longueur <= 40 and 5 <= hauteur <= 40):
        REQUEST_VARS["err"] = "Veuillez entrer une longueur ou hauteur valide (entre 5 et 40 cases)"
    else:
        grille = []
        for i in range(0, longueur):
            c = []
            for a in range(0,hauteur):
                c.append(0)
            grille.append(c)
            
        #Remplissage des cases
        min_perc = nb_cases * pourcentage_cases_remplies[0]
        max_perc = nb_cases * pourcentage_cases_remplies[1]
        
        nb_cases_remplies = int(random.uniform(min_perc, max_perc))

        
        last_case = [-1,-1]
        for i in range(0, nb_cases_remplies):
            if last_case == [-1,-1]:
                #On remplit une case au hasard
                case_x = random.randint(0, longueur-1)
                case_y = random.randint(0, hauteur-1)
                grille[case_x][case_y] = 1
                last_case = [case_x, case_y]
            else:
                over = False
                iterCount = 0 #Au bout de cinq itération, ça veux dire que la valeur est bloqué, donc on vas essayer d'en trouver une autre ailleurs
                while not over:
                    #On essaie de placer une case
                    direction = random.choice([[-1,0],[1,0],[0,-1],[0,1]])
                    new_case = [-1,-1]
                    new_case = [last_case[0] + direction[0], last_case[1] + direction[1]]
                    if iterCount >= 5:
                        case_x = random.randint(0, longueur-1)
                        case_y = random.randint(0, hauteur-1)
                        #On vas venir appliquer la fonction sur une case aléatoire du tableau
                        new_case = [case_x + direction[0], case_y + direction[1]]
                        #Faire en sorte que la case soit à proximité d'une autre
                        if grille[case_x][case_y] == 0:
                            #On ne fait rien car nous ne serions pas à côté d'une case existante
                            iterCount += 1
                            continue
                        
                    
                    #Maintenant on vérifie que les valeurs soit possibles
                    if 0 <= new_case[0] <= longueur-1 and 0 <= new_case[1] <= hauteur-1:
                        #Maintenant on vérifie que la valeur ne soit pas déjà prise
                        if grille[new_case[0]][new_case[1]] == 0:
                            grille[new_case[0]][new_case[1]] = 1
                            last_case = new_case
                            over = True
                    iterCount += 1
                        
                
        
        print("-----")
        for i in grille:
            print(i)
        print("-----")