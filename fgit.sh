#!/usr/bin/env bash

# Usage:
#   ./fgit.sh -m "Commit message"

# 1️⃣ Vérifier les changements locaux
if [[ -n $(git status --porcelain) ]]; then
    echo "⚠️  Changements locaux détectés, commit automatique avec message par défaut."
    
    # Vérifier si un message a été fourni
    if [[ "$1" == "-m" && -n "$2" ]]; then
        COMMIT_MSG="$2"
    else
        COMMIT_MSG="Mise à jour du Jupyter Book (commit automatique)"
    fi

    git add .
    git commit -m "$COMMIT_MSG" || { echo "❌ git commit failed"; exit 1; }
else
    echo "✅ Aucun changement local, pas de commit nécessaire."
fi

# 2️⃣ Pull avec rebase pour récupérer les dernières modifications
git pull --rebase origin main || { echo "❌ git pull failed"; exit 1; }

# 3️⃣ Push vers GitHub
git push -u origin main || { echo "❌ git push failed"; exit 1; }

# 4️⃣ Publier le site sur GitHub Pages
ghp-import -n -p -f _build/html || { echo "❌ ghp-import failed"; exit 1; }


