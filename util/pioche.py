from model.model_pg import execute_select_query, execute_other_query
#Génère une pioche
def gen_pioche(connexion, partie, mode):
    #Récupère 4 briques
    briques_raw = ()
    
    if "facile" in mode:
        briques_raw = execute_select_query(connexion, """SELECT id FROM briques 
                                                        WHERE longueur <= 2 AND largeur <= 2
                                                        ORDER BY RANDOM() LIMIT 4""")
    elif "difficile" in mode:
        briques_raw = execute_select_query(connexion, """SELECT id FROM briques 
                                                        ORDER BY RANDOM() LIMIT 4""")
    
    for i in range(0,4):
        execute_other_query(connexion, "INSERT INTO pioche VALUES (%s,%s,%s)", [briques_raw[i][0], i, partie])

#Update pioche
def update_pioche(connexion, partie, mode, num):
    brique_raw = ()
    if "facile" in mode:
        brique_raw = execute_select_query(connexion, """SELECT id FROM briques 
                                                        WHERE longueur <= 2 AND largeur <= 2
                                                        ORDER BY RANDOM() LIMIT 1""")
    elif "difficile" in mode:
        brique_raw = execute_select_query(connexion, """SELECT id FROM briques 
                                                        ORDER BY RANDOM() LIMIT 1""")
        
    execute_other_query(connexion, "UPDATE pioche SET briques_id = %s WHERE partie_id = %s AND num = %s", [brique_raw[0][0], partie, num])
    
    
def get_pioche(connexion, partie):
    pioche_raw = execute_select_query(connexion, """SELECT briques_id, largeur, longueur, couleur FROM pioche
                                    LEFT JOIN briques on id = briques_id
                                    WHERE partie_id = %s ORDER BY num""", [partie])
    pioche = []
    for i in pioche_raw:
        pioche.append({
            "id": i[0],
            "largeur": i[1],
            "longueur": i[2],
            "couleur": i[3]
        })
    return pioche