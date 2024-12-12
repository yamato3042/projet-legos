import random
import util.gen_grille
import util.create_user_if_not_exist
from model.model_pg import execute_select_query, execute_other_query
from util.pioche import gen_pioche
import json
if POST:
    ok = True
    for i in ["pseudo", "longueur", "hauteur","tours_limitee", "nb_tours","mode"]:
        if i not in POST:
            REQUEST_VARS["err"] = "Il manque des chamsp"
            ok = False
    
    if ok:
        if not ((5 <= int(POST["longueur"][0]) <= 40) and (5 <= int(POST["hauteur"][0]) <= 40)):
            REQUEST_VARS["err"] = "Veuillez entrer une longueur ou hauteur valide (entre 5 et 40 cases)"
            ok = False
        if POST["pseudo"][0] == "":
            REQUEST_VARS["err"] = "Veuillez entrer un pseudo pour pouvoir jouer"
            ok = False
            
        if not (2 <= int(POST["nb_tours"][0]) <= 500):
            REQUEST_VARS["err"] = "Nombre de tours invalide"
            ok = False
        
        if not int(POST["tours_limitee"][0]) in [0,1]:
            ok = False
        
        if not POST["mode"][0] in ["facile", "difficile"]:
            ok = False
    if ok: 
        pourcentage_cases_remplies = [0.10,0.20] 
        longueur = int(POST["longueur"][0])
        hauteur = int(POST["hauteur"][0])
        pseudo = POST["pseudo"][0]
        tours_limitee = bool(int(POST["tours_limitee"][0]))
        nb_tours = int(POST["nb_tours"][0])
        difficulté = POST["mode"][0]
        
        
        grille = util.gen_grille.gen_grille(pourcentage_cases_remplies, longueur, hauteur)
          
        #Si l'utilisateur n'existe pas alors on le crée
        user_id = util.create_user_if_not_exist.create_user_if_not_exist(SESSION['CONNEXION'], pseudo)
        
        #On crée une nouvelle partie dans la base
        partie_id = execute_select_query(SESSION['CONNEXION'], "INSERT INTO parties (debut, grille) VALUES (NOW(), %s) RETURNING id", 
                             [json.dumps({
                                 "longueur": longueur,
                                 "hauteur": hauteur,
                                 "grille": grille
                             })])[0][0]
        
        #Les paramètres
        #Le nombre de tours
        #Si il n'y a pas de nombre de tours max alors nombre = -1
        param_nb_tours = -1
        if tours_limitee:
            param_nb_tours = nb_tours
            
        execute_other_query(SESSION['CONNEXION'], "INSERT INTO configuration (clee, valeur, parties_id) VALUES ('nb_tours', %s, %s)", [str(param_nb_tours), partie_id])
        
        #La difficulté
        execute_other_query(SESSION['CONNEXION'], "INSERT INTO configuration (clee, valeur, parties_id) VALUES ('difficulte', %s, %s)", [difficulté, partie_id])
        
        #Le joueur
        execute_other_query(SESSION['CONNEXION'], "INSERT INTO joueurs_parties (joueurs_id, parties_id) VALUES (%s,%s)", [user_id, partie_id])
        
        #La pioche
        gen_pioche(SESSION['CONNEXION'], partie_id, difficulté) 
        #La partie a été généré, on affiche donc un bouton pour y aller
        REQUEST_VARS["partie_num"] = partie_id