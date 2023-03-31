from bs4 import BeautifulSoup
import requests
import pandas
tout_les_sites={
    'jumia':'https://www.jumia.sn/',
    'expatdakar':''
}

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


# ************************************ EXPAT ****************************************

reponse_expat = requests.get("https://www.expat-dakar.com/mode-beaute")
web_expat=reponse_expat.text
soup_expat = BeautifulSoup(web_expat, "html.parser")
produits_expats=soup_expat.find_all(name="div", class_="listing-card")
# teste pour voir la disposition des balises
# print(soup_expat.body.div.find_all(name="a", class_="listing-card__inner")[0])
category_produit_expat=[soup_expat.body.find_all(name="a", class_="listing-card__inner")[i].get("data-t-listing_category_title") for i in range (len(produits_expats))]
prix_produit_expat=[soup_expat.body.find_all(name="a", class_="listing-card__inner")[i].get("data-t-listing_price") for i in range (len(produits_expats))]
nom_produit_expat=[soup_expat.body.find_all(name="a", class_="listing-card__inner")[i].get("data-t-listing_title") for i in range (len(produits_expats))]
frame_expat=pandas.DataFrame({
    'Nom':nom_produit_expat,
     'Prix Produit':prix_produit_expat,
     'Prix Promo':''
    })

with pandas.ExcelWriter('data/data.xlsx') as writer:
    frame_expat.to_excel(writer, sheet_name="produit Expat")
    Tab_produits_jumia.to_excel(writer, sheet_name="ProduitJumia", index=False)
