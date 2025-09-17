#!/usr/bin/env bash

# 1️⃣ Activer l'environnement virtuel (si nécessaire)
# conda activate jupyter-env
# ou
# source jupyter-env/bin/activate

# 2️⃣ Installer Jupyter Book et ghp-import si ce n'est pas déjà fait
pip install -U jupyter-book ghp-import

# 3️⃣ Construire le livre localement
jupyter-book clean .
jupyter-book build .

# 4️⃣ Générer le PDF seulement si demandé avec "-pdf"
if [[ "$1" == "-pdf" ]]; then
    echo "📄 Génération du PDF..."
    jupyter-book build . --builder latex

    # adding a title page and a blank page (difficult to do it with sphinx)
    #gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=pdf/Spikes-Data-Sciences_temp.pdf pdf/blank_page.pdf _build/latex/Spikes-Data-Sciences.pdf 
    #gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=pdf/Spikes-Data-Sciences.pdf      pdf/title_page.pdf pdf/Spikes-Data-Sciences_temp.pdf 
    #rm pdf/Spikes-Data-Sciences_temp.pdf

    # 4️⃣a Renommer et copier le PDF (par défaut: projectnamenotset.pdf)
    cp _build/latex/Spikes-Data-Sciences.pdf pdf/Spikes-Data-Sciences.pdf

    # 4️⃣b Copier aussi dans le HTML pour le rendre accessible en ligne
    cp pdf/Spikes-Data-Sciences.pdf _build/html/Spikes-Data-Sciences.pdf

fi

# 5️⃣ Ajouter tous les fichiers au dépôt Git (incluant le PDF si généré)
git add .
git commit -m "Mise à jour du Jupyter Book"

# 6️⃣ Pousser les sources sur GitHub (branche main)
git push -u origin main

# 7️⃣ Publier le site sur GitHub Pages (branche gh-pages)
ghp-import -n -p -f _build/html

