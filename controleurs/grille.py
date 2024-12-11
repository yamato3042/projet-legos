from model.model_pg import execute_select_query
grille = [
    [0,0,0,0,0,0,0,0,0],
    [0,1,1,0,0,1,1,0,0],
    [0,1,0,1,0,1,0,1,0],
    [0,1,1,1,0,1,0,1,0],
    [0,1,1,1,0,1,0,1,0],
    [0,1,0,1,0,1,0,1,0],
    [0,1,1,0,0,1,1,0,0],
    [0,0,0,0,0,0,0,0,0]
]
REQUEST_VARS["grille"] = grille

#TODO: Sortir des valeurs de la base
pioche = []

pioche_raw = execute_select_query(SESSION['CONNEXION'], "SELECT id,largeur,longueur,couleur FROM briques WHERE largeur <= 2 AND longueur <= 2 ORDER BY RANDOM() LIMIT 4")

for i in pioche_raw:
    pioche.append({
        "id": i[0],
        "largeur": i[1],
        "longueur": i[2],
        "couleur": i[3]
    })

REQUEST_VARS["pioche"] = pioche