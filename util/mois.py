def getMois(nombre: int, capitalize=False): #Renvoie le nom du mois en fonction du nombre
    mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    nombre = int(nombre)
    if 1 <= nombre <= 12:
        if capitalize:
            return mois[nombre-1].capitalize()
        else:
            return mois[nombre-1]
    else:
        return ""
        