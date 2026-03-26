# Boid's Night
## 1. C'est quoi une simulation de boids
Une simulation de boids, contraction de bird-oid (qui a la forme d'un oiseau), permet de simuler le comportement d'une nuée d'oiseaux en vol.

## 2. Comment ça fonctionne
Les boids suivent trois règles :
- **La cohésion**, chaque boid se dirige vers la position moyenne des boids aux alentours
- **La séparation**, chaque boid évite de rester trop proche d'un autre boid
- **L'alignement**, chaque boid s'oriente dans la direction moyenne des boids proches

## 3. Pourquoi ce projet ?
Lorsque que l'on a découvert le thème *Nature & Informatique*, on s'est souvenus de quelque chose dont notre professeur de NSI nous avait parlé, les Boids.
C'est donc comme ça que **Boid's Night** est né.

## 4. La phase de recherches
Pour pouvoir mener à bien ce projet, il a fallu rechercher comment peuvent être implémenter en code, on est tombé sur un [article génial](http://www.kfish.org/boids/pseudocode.html) qui expliquait exactement cela, on s'est également aidés d'un autre [article](https://blog-a93.pages.dev/blog/boids).

## 5. Les difficultés rencontrées
La chose la plus difficile à réaliser a été de faire en sorte que la simulation puisse tourner de manière fluide. On a donc utilisé ChatGPT pour générer les fonctions ``build_grid`` et ``get_neighbours``, cependant on les a beaucoup modifiées.
On a aussi eu recourt à [cette page](https://gist.github.com/laundmo/b224b1f4c8ef6ca5fe47e132c8deab56) pour certains calculs en rapport avec les vecteurs.
