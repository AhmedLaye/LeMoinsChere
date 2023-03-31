from bs4 import BeautifulSoup
import requests
import pandas
# TODO: Recuperer les données des autres autres
response = requests.get("https://www.jumia.sn/fashion-mode/")
web=response.text
soup = BeautifulSoup(web, "html.parser")
produits=soup.find_all(name="article", class_=["prd","_fb", "col", "c-prd"])
nom_produits=[produits[i].contents[0].get("data-name") for i in range(len(produits)) ]
prix_hors_promo = [produits[i].contents[0].find(name="div", class_="prc").getText() for i in range(len(produits))]
prix_en_promo = [produits[i].contents[0].find(name="div", class_="prc").get("data-oprc") for i in range(len(produits))]
Tab_produits_jumia = pandas.DataFrame(
    {'Nom': nom_produits,
     'Prix Hors Promo': prix_en_promo,
     'Prix Promo': prix_hors_promo
    })

# todo: Ajouter plus de données pour EXPAT DAKAR
reponse_expat = requests.get("https://www.expat-dakar.com/mode-beaute")
web_expat=reponse_expat.text
soup_expat = BeautifulSoup(web_expat, "html.parser")
produits_expats=soup_expat.find_all(name="div", class_="listing-card")
category_produit_expat=[soup_expat.body.find_all(name="a", class_="listing-card__inner")[i].get("data-t-listing_category_title") for i in range (len(produits_expats))]
prix_produit_expat=[soup_expat.body.find_all(name="a", class_="listing-card__inner")[i].get("data-t-listing_price") for i in range (len(produits_expats))]
nom_produit_expat=[soup_expat.body.find_all(name="a", class_="listing-card__inner")[i].get("data-t-listing_title") for i in range (len(produits_expats))]
frame_expat=pandas.DataFrame({
    'Nom':nom_produit_expat,
     'Prix Produit':prix_produit_expat,
     'Prix Promo':''
    })

# todo: Ajouter plus de données et de pour SOUMARI
reponse_soumari = requests.get("https://www.soumari.com/categorie-produit/informatique/")
web_soumari=reponse_soumari.text
soup_soumari = BeautifulSoup(web_soumari, "html.parser")
produit_soumari=soup_soumari.find_all( name="li", class_=["type-product","product","type-product"])
nom_produit_soumari=[produit_soumari[i].find(name="h2", class_="woo-loop-product__title").getText() for i in range(len(produit_soumari))]

prix_produit_soumari=[produit_soumari[i].find(name="span", class_="woocommerce-Price-amount amount").getText()[0:-4] for i in range(len(produit_soumari))]
frame_soumari = pandas.DataFrame({
    'Nom': nom_produit_soumari,
    'Prix Produit': prix_produit_soumari,
})

#TOdo: ICI ON CREER LES SHEETS POUR CHAQUE SITE
with pandas.ExcelWriter('data/data.xlsx') as writer:
    frame_expat.to_excel(writer, sheet_name="produit Expat", index=False)
    Tab_produits_jumia.to_excel(writer, sheet_name="ProduitJumia", index=False)
    frame_soumari.to_excel(writer, sheet_name="Produit Soumari",index=False)