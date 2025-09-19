Ce qui ne marche pas:


- **cross-ref** :
```
{ref}`chap-pyabf` marche ainsi que [link](chap-pyabf)
```


- changer la page titre du PDF (on tourne en rond)

- les [content-blocks](https://jupyterbook.org/en/stable/content/content-blocks.html) sont parfait pour le jupyter-book mais disparaissent dans le PDF

Grater du coté de sphynx ?

en dessous les latex_elements ne fonctionnent pas
```
# ----------------------------
# LaTeX / PDF Configuration
# les "  latex_elements:" ne marchent pas
# ----------------------------
latex:
  latex_engine: xelatex
  latex_documents:
    targetname: "Spikes-Data-Sciences.tex"
  latex_elements:
    # Packages
    preamble: |
      \usepackage{graphicx}  % needed for including images
      \usepackage{xcolor}
      \usepackage{tcolorbox}
      % Define LaTeX boxes for callouts
      \newtcolorbox{notebox}{colback=blue!10!white,colframe=blue!50!black,title=Note}
      \newtcolorbox{tipbox}{colback=green!10!white,colframe=green!50!black,title=Tip}
      \newtcolorbox{warningbox}{colback=yellow!10!white,colframe=orange!50!black,title=Warning}
      \newtcolorbox{importantbox}{colback=red!10!white,colframe=red!50!black,title=Important}          # Custom title page
    maketitle: |
      \begin{titlepage}
        \centering
        \vspace*{2cm}
        \includegraphics[width=0.4\textwidth]{pics/Spikes-Data-Sciences.pdf} % PDF logo for LaTeX
        \vspace{2cm}
        {\Huge \textbf{\@title}} \\[1cm]
        {\Large \@author} \\[1cm]
        \@date
      \end{titlepage}

```
