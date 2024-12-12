from model.model_pg import execute_select_query, execute_other_query
import datetime

class Partie:
    def __init__(self, id : int, debut : datetime, fin : datetime, grille_longueur : int, grille_hauteur : int, grille : list):
        self.id = id
        self.debut = debut
        self.fin = fin
        self.grille_hauteur = grille_hauteur
        self.grille_longueur = grille_longueur
        self.grille = grille
    
        self.last_tour = 0
    def set_nb_tours(self, nb_tours):
        if nb_tours == -1:
            self.tours_limités = False
        else:
            self.tours_limités = True
            self.nb_tours : int = nb_tours
    def set_difficulté(self, diff):
        self.diff : str = diff
    def set_joueur(self, id : int, prenom : str):
        self.joueur_id = id
        self.joueur_prenom = prenom
    def transformer_grille(self):
        #La grille vas passer les 1 et 0 à -1 et -2 pour pouvoir apprès ammener les couleurs
        for i in range(0, self.grille_longueur):
            for a in range(0, self.grille_hauteur):
                if self.grille[i][a] == 1:
                    self.grille[i][a] = -1
                elif self.grille[i][a] == 0:
                    self.grille[i][a] = -2
    def compiler_tour(self, tour_raw):
        numero = tour_raw[1]
        action = tour_raw[2]
        self.last_tour = numero
        
        if action == "placer":
            #SELECT tours.id, numero, action, position_x, position_y, brique_id, largeur, longueur, couleur
            position_x = tour_raw[3]
            position_y = tour_raw[4]
            largeur = tour_raw[6]
            longueur = tour_raw[7]
            couleur = tour_raw[8]
            #On viens placer sur le tableau
            for i in range(0, longueur):
                for a in range(0, largeur):
                    self.grille[position_x + i][position_y + a] = couleur
            
    
def get_partie(connexion, partie_id: int):
    #Cette fonction retourne la table de la partie
    partie_raw = execute_select_query(connexion, "SELECT * FROM parties WHERE id = %s", [partie_id])
    if len(partie_raw) != 1:
        return None
    
    partie = Partie(partie_raw[0][0], partie_raw[0][1], partie_raw[0][2], partie_raw[0][3]["longueur"], partie_raw[0][3]["hauteur"], partie_raw[0][3]["grille"])
    #On récupère les paramètres
    paramètres_raw = execute_select_query(connexion, "SELECT clee, valeur FROM configuration WHERE parties_id = %s", [partie_id])
    for i in paramètres_raw:
        if i[0] == "nb_tours":
            partie.set_nb_tours(int(i[1]))
        elif i[0] == "difficulte":
            partie.set_difficulté(i[1])
    
    #On récupère le joueurs (dans cette version il n'y en a qu'un)
    joueurs_raw = execute_select_query(connexion, "SELECT id, prenom FROM joueurs_parties LEFT JOIN joueurs ON id = joueurs_id WHERE parties_id = %s", [partie_id])
    partie.set_joueur(joueurs_raw[0][0], joueurs_raw[0][1])
    
    #Transformation de la grille
    partie.transformer_grille()
    
    #Compilation des tours
    tours_raw = execute_select_query(connexion, """SELECT tours.id, numero, action, position_x, position_y, brique_id, largeur, longueur, couleur 
                                                    FROM tours 
                                                    LEFT JOIN briques ON briques.id = tours.brique_id
                                                    WHERE parties_id = %s
                                                    ORDER BY numero""", [partie_id])
    for i in tours_raw:
        partie.compiler_tour(i)
        
    #Récupère la pioche
    
        
    return partie


def add_tour_défausser(connexion, partie : Partie):
    partie.last_tour += 1
    execute_other_query(connexion, "INSERT INTO tours (joueurs_id, parties_id,	numero, action) VALUES (%s, %s, %s, 'défausser')", [partie.joueur_id, partie.id, partie.last_tour])
    
def add_tour_placer(connexion, partie: Partie, brique, position):
    partie.last_tour += 1
    execute_other_query(connexion, """INSERT INTO tours (joueurs_id, parties_id, numero, brique_id, action, position_x, position_y)
                                    VALUES (%s,%s,%s,%s, 'placer', %s,%s)""",
                                    [partie.joueur_id, partie.id, partie.last_tour, brique["id"], position[0], position[1]])
    
def add_tour_pénalité(connexion, partie: Partie):
    partie.last_tour += 1
    execute_other_query(connexion, "INSERT INTO tours (joueurs_id, parties_id,	numero, action) VALUES (%s, %s, %s, 'pénalité')", [partie.joueur_id, partie.id, partie.last_tour])
    
def fin_partie(connexion, partie: Partie, gagné : bool):
    execute_other_query(connexion, "UPDATE parties SET fin = now() WHERE id = %s", [partie.id])
    score = 0
    if gagné:
        score = partie.last_tour
    execute_other_query(connexion, "UPDATE joueurs_parties SET score = %s, gagnant = %s WHERE joueurs_id = %s AND parties_id = %s",
                        [score, gagné, partie.joueur_id, partie.id])
    partie.fin = datetime.datetime.now()
