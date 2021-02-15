# Trustpilot scrapper

Petit projet pour apprendre le web scraping avec python et beautifoul soup.

Le programme extrait les informations suivantes :

|     | username | date                 | comment   | rating | nb_review_user | is_verified | company    |
| --- | -------- | -------------------- | --------- | ------ | -------------- | ----------- | ---------- |
| 0   | id1      | 2020-12-23T19:17:11Z | Essentiel | 5      | 1              | True        | adidas.com |

J'ai ajouté quelques contraintes :

- faire appel à des proxies. Pour chaque page requêtée, un proxy est choisit aléatoirement dans une liste préablemment construite.
- Un user-agent est aussi envoyé aléatoirement en suivant le même principe.

Prochaines améliorations :

- mieux structurer le script
- sauvegarder au fur et à mesure les données pour ne pas tout perdre si le script explose en cours de route
- scrapper directement une liste de plusieurs entreprise
- ajout d'une fonction pour completer les données avec les nouveaux commentaires
- scrapper le commentaire plein en plus de la preview
