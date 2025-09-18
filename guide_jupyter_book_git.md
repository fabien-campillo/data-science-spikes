# Guide Jupyter Book + Git

Ce guide explique comment travailler avec Jupyter Book, Git et PDF/notebooks générés de manière sûre pour éviter les conflits et garder un dépôt stable.

## 1️⃣ Structure et fichiers à versionner

À versionner dans Git :

- Notebooks source : `*.ipynb`
- `_toc.yml`, `_config.yml`
- Scripts ou fichiers `.py` si besoin
- PDF généré si tu veux le versionner

À ignorer (.gitignore) :

- `.virtual_documents/`
- `_build/`
- `jupyter-env/`
- `pdf/`  si tu veux régénérer automatiquement et éviter conflits

**Remarque :** tu peux versionner le PDF si tu le souhaites, mais il faudra gérer les merges avec .gitattributes.

## 2️⃣ Configurer Git pour les PDFs versionnés

Dans `.gitattributes` :

```
pdf/Spikes-Data-Sciences.pdf binary merge=ours
```

Puis configurer le driver :

```
git config merge.ours.driver true
```

Cela évite les conflits Git pour les fichiers PDF générés automatiquement.

## 3️⃣ Installer et configurer nbdime pour les notebooks

```
pip install nbdime
nbdime config-git --enable
```

`nbdime` permet de voir et fusionner les notebooks cellule par cellule.
Les merges et pulls ne corrompent plus les notebooks.

## 4️⃣ Workflow quotidien

1. Mettre à jour la branche : git pull --no-rebase
   - Si conflits sur un notebook : nbdime s’ouvre pour fusionner proprement.
2. Travailler sur les notebooks normalement.
3. Régénérer le Jupyter Book / PDF : ./build_jb.sh -pdf
4. Commit et push : git add . ; git commit -m "Update notebooks / Jupyter Book / PDF" ; git push origin main

## 5️⃣ Astuces pour éviter les problèmes

- Ne jamais versionner .virtual_documents/ ni l’environnement virtuel (jupyter-env/)
- Si tu versionnes le PDF, toujours utiliser .gitattributes pour merge=ours
- Toujours faire git pull avant de commencer à travailler
- Pour fusionner des notebooks, utiliser nbdime (nbdiff-web) plutôt que Git classique

## ✅ Résultat attendu

- Merge et pull sont sûrs
- Les notebooks restent intacts
- PDF et fichiers générés ne posent plus de conflits
- Dépôt propre et collaboratif
