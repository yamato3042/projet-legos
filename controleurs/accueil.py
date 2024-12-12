from model.model_pg import count_instances, execute_select_query
from util.mois import getMois
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
joueurs_raw = execute_select_query(SESSION['CONNEXION'], """SELECT prenom, COALESCE(MIN(score),0), COALESCE(MAX(score),0) as score_max FROM joueurs_parties 
                                                LEFT JOIN joueurs ON joueurs.id = joueurs_id
                                                GROUP BY joueurs_id, prenom
                                                ORDER BY score_max DESC
                                                LIMIT 15""")

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
defaussé_raw = execute_select_query(SESSION['CONNEXION'], """WITH counts AS (
  SELECT 
    COUNT(*) AS nb, 
    parties_id 
  FROM tours
  LEFT JOIN parties ON parties_id = parties.id AND fin IS NOT NULL
  WHERE action = 'défausser'
  GROUP BY parties_id
),
max_min AS (
  SELECT 
    MAX(nb) AS max_nb, 
    MIN(nb) AS min_nb
  FROM counts
)
SELECT 
  c.parties_id, 
  c.nb 
FROM counts c
JOIN max_min mm
ON c.nb = mm.max_nb OR c.nb = mm.min_nb;""")

defaussé = []
for i in defaussé_raw:
    defaussé.append({
        "id": i[0],
        "nb": i[1]
    })

REQUEST_VARS["defaussé"] = defaussé

#Demande 5:
moyen_tour_raw = execute_select_query(SESSION['CONNEXION'], """SELECT 
    EXTRACT(YEAR FROM p.debut) AS annee,
    EXTRACT(MONTH FROM p.debut) AS mois,
    AVG(t.nb_tours) AS moyenne_tours
FROM (
    SELECT 
        parties_id, 
        COUNT(*) AS nb_tours
    FROM jeu.tours
    GROUP BY parties_id
) t
JOIN jeu.parties p ON t.parties_id = p.id
GROUP BY annee, mois
ORDER BY annee, mois;""")

moyen_tour = []
for i in moyen_tour_raw:
    moyen_tour.append({"periode": f"{getMois(i[1], True)} {i[0]}", "moyenne": round(i[2], 2)})
REQUEST_VARS["moyen_tour"] = moyen_tour

#Demande 6:
top_3_grandes_pieces_raw = execute_select_query(SESSION['CONNEXION'], """SELECT FLOOR(AVG(longueur * largeur)), COUNT(*), parties_id
                                                                        FROM tours
                                                                        LEFT JOIN briques ON briques.id = tours.brique_id
                                                                        WHERE action = 'placer'
                                                                        GROUP BY parties_id
                                                                        ORDER BY AVG(longueur * largeur) DESC
                                                                        LIMIT 3""")

top_3_grandes_pieces = []
for i in top_3_grandes_pieces_raw:
    top_3_grandes_pieces.append({
        "moy": i[0],
        "nb_briques": i[1],
        "id": i[2]
    })
#On trie en fonction du nombre de briques utilises
top_3_grandes_pieces = sorted(top_3_grandes_pieces, key=lambda x: x["nb_briques"], reverse=True)
REQUEST_VARS["top_3_grandes_pièces"] = top_3_grandes_pieces