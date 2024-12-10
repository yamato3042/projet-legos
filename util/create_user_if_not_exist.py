from model.model_pg import execute_select_query, execute_other_query

def create_user_if_not_exist(connexion, user : str) -> int:
    #Cette fonction créé l'utilisateur s'il n'existe pas et retourne un id
    val = execute_select_query(connexion, "SELECT id FROM joueurs WHERE prenom LIKE %s", [user])
    if len(val) == 1:
        #Le joueur existe
        return val[0][0]
    else:
        #On créé le joueur
        v = execute_select_query(connexion, "INSERT INTO joueurs (prenom, date_inscription) VALUES (%s, NOW()) RETURNING id", [user])
        return v[0][0]