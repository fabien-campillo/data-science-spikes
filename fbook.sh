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

# 4️⃣ Générer le PDF par défaut, sauf si "-nopdf" est passé
if [[ "$1" != "-nopdf" ]]; then
    echo "📄 Génération du PDF..."
    jupyter-book build . --builder pdflatex

    # Ajout page blanche + page de titre (plus simple via ghostscript qu’avec Sphinx)
    gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
       -sOutputFile=pdf/Spikes-Data-Sciences_temp.pdf \
       pdf/blank_page.pdf _build/latex/Spikes-Data-Sciences.pdf 

    gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite \
       -sOutputFile=pdf/Spikes-Data-Sciences.pdf \
       pdf/title_page.pdf pdf/Spikes-Data-Sciences_temp.pdf 

    rm pdf/Spikes-Data-Sciences_temp.pdf

    # Copier aussi le PDF dans le HTML pour le rendre accessible en ligne
    cp pdf/Spikes-Data-Sciences.pdf _build/html/Spikes-Data-Sciences.pdf
else
    echo "ℹ️ PDF skipped (option -nopdf)"
fi
