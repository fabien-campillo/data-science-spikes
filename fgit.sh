#!/usr/bin/env bash

# 0️⃣ Récupérer les dernières modifications distantes
git pull --rebase origin main

# 1️⃣ Ajouter tous les fichiers au dépôt Git (incluant PDF si généré)
git add .
git commit -m "Mise à jour du Jupyter Book"

# 2️⃣ Pousser les sources sur GitHub (branche main)
git push -u origin main

# 3️⃣ Publier le site sur GitHub Pages (branche gh-pages)
ghp-import -n -p -f _build/html
