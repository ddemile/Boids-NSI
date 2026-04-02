# Boid's Night
## Présentation globale
Lorsque nous avons découvert le thème *Nature & Informatique*, nous nous sommes souvenus de quelque chose dont notre professeur de NSI nous avait parlé : les Boids.
C'est donc ainsi que **Boid's Night** est né.
C'est une simulation de boids (contraction de bird-oid : qui a la forme d'un oiseau) interactive qui a pour but de permettre à l'utilisateur de simuler le comportement d'une nuée d'oiseaux en vol, tout en permettant de modifier différents paramètres.

## Présentation de l'équipe
Notre équipe est composée de 4 élèves de première au Lycée Moulin Joli à La Possession. Voici comment la répartition des tâches s'est effectuée :
- **HOARAU Emilien** - Logique de déplacement des boids (`update`, `apply_rules`) / Gestion et initialisation de `pyxel` (`init_boids`)
- **DAROUECHI Ashima** - Logique de l'interface (`update_ui`) / Création et affichage de l'arrière-plan (`draw`)
- **DIOT Eloïse** - Affichage de l'interface et des boids (`draw`, `draw_boids`, `draw_ui`)
- **WATANABE Romain** - Gestion des bords (`warp`, `bounce`, `bound`)

## Étapes du projet
1. Découverte du thème puis choix de faire une simulation de boids
2. Recherches sur le fonctionnement des boids (articles, blogs, pseudo-code, ...)
3. Première version du projet très minimaliste avec des pixels blancs (boids) sur fond noir
4. Ajout de l'interface (sliders, boutons, ...)
5. Choix de la palette de couleurs et création de l'arrière-plan
6. Intégration de l'arrière-plan dans le projet
7. Équilibrage afin de trouver de bonnes valeurs de départ

## Validation de l'opérationnalité et du fonctionnement
### État au moment du dépôt
Dans son état actuel, le projet est totalement fonctionnel ; nous avons pu implémenter tout ce qui était prévu à la base.

### Approches mises en œuvre pour vérifier l'absence de bugs
Notre projet étant une simulation, l'ajout de tests automatiques aurait été assez difficile. Pour pallier à ce manque, nous avons testé toutes les fonctionnalités du projet avant de le rendre pour nous assurer qu'il n'y ait pas de bugs (ou presque pas).

### Difficultés rencontrées
Durant la phase de développement, un problème majeur est apparu : l'optimisation. En effet, les premières versions du projet étaient presque inutilisables à cause d'un nombre d'images par seconde très faible. N'arrivant pas à trouver de solution, nous avons demandé de l'aide à ChatGPT, qui nous a proposé d'implémenter un système de grille à l'aide d'une fonction : `build_grid`. Nous avons par la suite modifié cette fonction pour qu'elle puisse s'adapter à notre projet.

## Ouverture
### HOARAU Emilien
Le projet **Boid's Night** m'a permis d'en apprendre davantage sur le module pyxel. J'aurais aimé pouvoir simuler un nombre plus important de boids, mais nous n'avons pas réussi à optimiser le projet au-delà de son état actuel.
Ce projet m'a apporté beaucoup de choses : j'ai pu apprendre à mieux travailler en équipe, approfondir mes connaissances en Python et apprendre à créer un projet en respectant un thème donné.
En regardant le projet après coup, je trouve que nous avons réalisé un projet concret et abouti. Cependant, je pense que nous aurions pu ajouter d'autres fonctionnalités, comme la possibilité de faire suivre le curseur aux boids, ou même de pouvoir choisir entre différents thèmes.

### DAROUECHI Ashima
Pour le projet **Boid's Night**, j'avais au départ énormément d'idées. Par exemple, j'avais envisagé d'ajouter une seconde interface avec une simulation de poissons que nous aurions appelée *"Pesca-Droïde"*. Cependant, je n'ai pas pu la mettre en place par manque de temps. Malgré tout, je trouve que le projet a très bien abouti et je suis très satisfait du résultat. J'ai par ailleurs eu l'occasion d'améliorer mes compétences en organisation, étant principalement en charge de la coordination des différents rendez-vous au sein du groupe et de la répartition des différentes parties du travail à effectuer.

### DIOT Eloïse
La réalisation de notre projet Boid's Night a été une expérience très enrichissante !
En dehors du fait que cela m'a permis de renforcer les liens avec mes coéquipiers, cela m'a permis de développer plusieurs compétences personnelles :
J'ai pu progresser en codage, améliorer ma capacité à travailler en équipe et à m'auto-organiser.
Au niveau du projet, d'autres améliorations ont été évoquées ; j'aurais par exemple aimé pouvoir créer un arrière-plan animé, mais notre projet reste une belle réussite dont nous sommes fiers et qui mérite une note conséquente !

### WATANABE Romain
Quand nous avons travaillé sur le projet, j'ai eu plusieurs idées, comme par exemple faire des centaines de mini oiseaux de milliers de couleurs différentes. Ce projet m'a permis de m'entraîner à mieux m'exprimer à l'oral.
De mon point de vue, le jeu est très bien fait, même s'il pourrait encore être amélioré à l'avenir.