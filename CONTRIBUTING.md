## CONTRIBUTING

### Notizen
* Wir haben uns darauf geeinigt [Markdown-Dateien](https://docs.gitlab.com/ee/user/markdown.html) zu verwenden, und **keine Jupyter-Notebooks**, da *GitLab flavored Markdown* ebenfalls eine `LaTeX`-Unterstützung anbietet
* `LaTeX`-Snippets werden wiefolgt in GitLab unterstützt: [Docs](https://docs.gitlab.com/ee/user/markdown.html#math)  
    Beispiel (inline):  $`a^2+b^2=c^2`$ 

### Workflow
* **Beispiel**: Angenommen, du willst deine Notizen zu Aufgabe 1, A-4 hochladen:  
    1. `git clone https://r-n-d.informatik.hs-augsburg.de:8080/mozartus/cassiopeia.git`
    2. `cd cassiopeia`
    3. `git checkout -b teil1_a4`  *erstellt neue branch ausgehend von master*
    4. `cp /home/patrick/a-4_gravitation.md notes/teil_1/`  *fügt die datei hinzu*
    5. `git add notes/teil_1/a-4_gravitation.md`  *staging (vormerken) deiner #nderungen*
    6. `git commit -m "Added aufgabe 1, A4"`
    7. `git push origin teil1_a4`
    8. *Merge request* erstellen in dem du uns deine Änderungen erklärst
* Unsere `master-branch` enthält nur sogenannten *production-ready*-Code, also Code 
der funktioniert und nicht grob fehlerhaft ist.  
* Das erreichen wir durch den sogenannten *Git-Flow* Workflow, der oben exemplarisch beschrieben wurde
* Für kleinere Änderungen, wie zum Beispiel an der `README` kann auch direct auf `master` gepushed werden