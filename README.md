## Exécution
1. Installez les dépendances avec la commande : `pip install -r requirements.txt`.
2. Placez les fichiers de données (`sales_data.csv`, `customer_feedback.csv`, `geographic_data.csv`) dans le dossier racine.
3. Lancez l’application avec la commande : `bokeh serve --show main.py`.


## Fonctionnalités
- **Tendance des Ventes :** Visualisation de la tendance des ventes quotidiennes avec des infobulles interactives.
- **Ventes par Catégorie :** Graphique en barres montrant la répartition des ventes par catégorie de produits.
- **Carte de Chaleur des Ventes :** Carte de chaleur illustrant l’intensité des ventes selon les jours de la semaine et les catégories.
- **Ventes Géographiques :** Carte interactive avec des marqueurs proportionnels au volume des ventes.
- **Graphique Circulaire des Ventes :** Répartition des ventes en pourcentage par catégorie.
- **Distribution des Avis Clients :** Nombre d’avis par catégorie de produits.
- **Sentiment Moyen :** Score moyen des sentiments pour les avis clients par catégorie.


## Fonctionnalités Supplémentaires
- Visualisations avec des couleurs adaptées pour une meilleure lisibilité.
- Infobulles améliorées pour des visualisations interactives.
- Effets au survol pour afficher des détails sur les points de données.
- Organisation en onglets pour regrouper plusieurs visualisations dans un seul tableau de bord.


## Réflexion
- **Quels ont été les principaux défis dans l’implémentation du tableau de bord ?**  
  Les principaux défis incluent la gestion des visualisations interactives, la compatibilité des différents jeux de données, et la coordination des entrées multiples tout en maintenant une interface claire.

- **Comment avez-vous géré le prétraitement des données pour les différentes visualisations ?**  
  Le prétraitement a été réalisé dans le fichier `data_preprocessing.py`, en standardisant le nettoyage des données (conversion des types, gestion des valeurs manquantes) pour garantir leur compatibilité avec les visualisations.

- **Quelles fonctionnalités supplémentaires ajouteriez-vous avec plus de temps ?**  
  - Mises à jour des données en temps réel pour un tableau de bord dynamique.
  - Filtres utilisateurs pour personnaliser les plages de dates ou les catégories spécifiques.
  - Options d’exportation pour les visualisations et les résumés des données.