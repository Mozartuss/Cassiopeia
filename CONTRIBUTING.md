Unsere `master-branch` enthält nur sogenannten *production-ready*-Code, also Code 
der funktioniert und nicht grob fehlerhaft ist.  
Das erreichen wir durch den sogenannten *Git-Flow* Workflow:  

Die Entwicklung einzelner Features (wie z.B. Teilaufgabe `teil1-a2` findet in eigenen `branches` statt, da wir so  
unsere `master-branch` *"sauber"* halten:  
Um eine neue `branch`, ausgehend von `master` zu erstellen: `git checkout -b <branch-name>`.  
Nun befindet man sich innerhalb dieser Branch, in der man sich austoben kann.  
Wenn man seinen fertigen Code auf das GitLab-Repository pushen will  
(nachdem man den Code *commited* hat), muss man folgendes Kommando eingeben:  
`git push origin <branch-name>`.  
Damit der Code letztendlich zusammen mit `master` *zusammengefügt* wird, muss man einen sog.  
*Merge-Request* auf GitLab erstellen.
