from bs4 import BeautifulSoup
import requests
import pandas

response = requests.get("https://www.jumia.sn/fashion-mode/")
web=response.text
soup = BeautifulSoup(web, "html.parser")

produits=soup.find_all(name="article", class_=["prd","_fb", "col", "c-prd"])
# nom_produits=[produits[i]['data-name'] for i in range(len(produits)) ]

# ---------------           MANIPULATION
# produits[0].contents
# ----------------recuperation du nom d'un produit
# produits[1].contents[0].get("data-name")
# ici faut noter que contet[0] contient les balise et attribut qui nous interessse
nom_produits=[produits[i].contents[0].get("data-name") for i in range(len(produits)) ]

# ----------------- recuperation du prix si y'a promo
prix_hors_promo=[produits[i].contents[0].find(name="div", class_="prc").getText() for i in range(len(produits))]

# print(produits[0].contents[0].find(name="div", class_="prc").getText())
# ---------------- recuperation du prix si y'a  promo
prix_en_promo=[produits[i].contents[0].find(name="div", class_="prc").get("data-oprc") for i in range(len(produits))]

# print(produits[0].contents[0].find(name="div", class_="prc").get("data-oprc"))
# ---------------- Recuperation pourcentage
#produits[0].contents[0].find(name="div", class_="bdg _dsct").getText()
# pourcentage=[produits[i].contents[0].find(name="div", class_="bdg _dsct").getText() for i in range(len(produits))]

Tab_produits_jumia = pandas.DataFrame(
    {'Nom': nom_produits,
     'Prix Hors Promo': prix_en_promo,
     'Prix Promo': prix_hors_promo
    })
# affichage
print(Tab_produits_jumia)
# creation d'un fichier excel
Tab_produits_jumia.to_excel("data/data.xlsx", sheet_name="ProduitJumia", index=False)





