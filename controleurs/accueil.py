from model.model_pg import count_instances, execute_select_query

#Demande 1 :
REQUEST_VARS["nb_briques"] = count_instances(SESSION['CONNEXION'], 'briques')[0][0]
REQUEST_VARS["nb_constructions"] = count_instances(SESSION['CONNEXION'], 'constructions')[0][0]
REQUEST_VARS["nb_parties"] = count_instances(SESSION['CONNEXION'], 'parties')[0][0]

#Demande 2 :
couleurs_raw = execute_select_query(SESSION['CONNEXION'], "SELECT couleur FROM briques GROUP BY couleur ORDER BY COUNT(*) DESC LIMIT 5")
couleurs = []
for i in couleurs_raw:
    couleurs.append(i[0])

REQUEST_VARS["top_couleurs"] = couleurs #TODO: Faut voir si la base est bonne avant

#Demande 3 :
joueurs_raw = execute_select_query(SESSION['CONNEXION'], """SELECT prenom, COALESCE(MIN(score),0), COALESCE(MAX(score),0) FROM joueurs_parties 
                                                LEFT JOIN joueurs ON joueurs.id = joueurs_id
                                                GROUP BY joueurs_id, prenom
                                                ORDER BY MAX(score) DESC
                                                LIMIT 15""")

#TODO: TEMP
joueurs_raw = list(joueurs_raw)
joueurs_raw.append(["Jacques", "25", "250"])
joueurs_raw.append(["Louis", "38", "400"])
joueurs_raw.append(["Paul", "12", "1000"])

joueurs = []
for i in joueurs_raw:
    joueurs.append({
        "nom": i[0],
        "min": i[1],
        "max": i[2]
    })

#Demande 4
#TODO: Refaire
REQUEST_VARS["joueurs"] = joueurs
defaussé_raw = execute_select_query(SESSION['CONNEXION'], """SELECT COUNT(*), debut, fin FROM tours
                                                LEFT JOIN parties ON parties.id = parties_id 
                                                GROUP BY parties.id, debut, fin, action
                                                HAVING action LIKE 'défaussée'""")

#TODO: TEMP
defaussé_raw = list(defaussé_raw)
defaussé_raw.append([50, "11/02/1992", "13/02/1992"])
defaussé_raw.append([1585, "25/12/2009", "25/12/2010"])


defaussé = []
for i in defaussé_raw:
    defaussé.append({
        "nb": i[0],
        "debut": i[1],
        "fin": i[2]
    })
defaussé.sort(key=lambda x: x["nb"])

if len(defaussé) > 10:
    # Sinon, extraire les 5 premiers et 5 derniers éléments
    premiers_cinq = defaussé[:5]
    derniers_cinq = defaussé[-5:]
    defaussé = premiers_cinq + derniers_cinq

REQUEST_VARS["defaussé"] = defaussé

#Demande 5:
#TODO:

#Demande 6:
#TODO: