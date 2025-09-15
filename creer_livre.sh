# 1️⃣ Activer l'environnement virtuel (si nécessaire)
# conda activate jupyter-env
# ou
# source jupyter-env/bin/activate

# 2️⃣ Installer Jupyter Book et ghp-import si ce n'est pas déjà fait
pip install -U jupyter-book ghp-import

# 3️⃣ Ajouter tous les fichiers au dépôt Git (si changements)
git add .
git commit -m "Mise à jour du Jupyter Book"

# 4️⃣ Pousser les sources sur GitHub (branche main)
git push -u origin main

# 5️⃣ Construire le livre localement
jupyter-book clean .
jupyter-book build .

# 5️⃣b Générer le PDF via LaTeX
jupyter-book build . --builder pdflatex

# Copie du PDF avec un nom stable
cp _build/latex/Spikes-Data-Sciences.pdf _build/html/Spikes-Data-Sciences.pdf

# 6️⃣ Publier le site sur GitHub Pages (branche gh-pages)
ghp-import -n -p -f _build/html


# 1️⃣ Activer l'environnement virtuel (si nécessaire)
# conda activate jupyter-env
# ou
# source jupyter-env/bin/activate

# 2️⃣ Installer Jupyter Book et ghp-import si ce n'est pas déjà fait
# pip install -U jupyter-book ghp-import

# 3️⃣ Ajouter tous les fichiers au dépôt Git (si changements)
# git add .
# git commit -m "Mise à jour du Jupyter Book"

# 4️⃣ Pousser les sources sur GitHub (branche main)
# git push -u origin main

# 5️⃣ Construire le livre localement
# jupyter-book clean . # je préfère cleaner
# jupyter-book build .

# 5️⃣b Générer le PDF via LaTeX
# Cette commande va créer _build/latex/nom_du_livre.tex puis compiler en PDF
# jupyter-book build . --builder pdfhtml
# ou si tu veux compiler via LaTeX directement :
# jupyter-book build . --builder pdflatex
# cp _build/latex/projectnamenotset.pdf _build/latex/Spikes-Data-Sciences.pdf

# 6️⃣ Publier le site sur GitHub Pages (branche gh-pages)
# ghp-import -n -p -f _build/html

