Semaine 3 :


"





Semaine 4 :



Q: Comment transférez-vous le score de la joueuse d'un niveau à l'autre ? Où le remettez-vous à zéro ?
A: Le score est (ré)initialisé au niveau de la fonction set-up, qui est appelée uniquement au début du programme, lors de la mort ou lorsque l'on appuie sur la touche échap. Cela correspond exactement aux moments où l'on veut reset le score. En effet, on passe d'une map à une autre sans utiliser la fonction set up mais uniquement la fonction readmap.

Q: Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu'elle a touché un ou monstre ou de la lave ?
A: On a implémenté un "Game_Over" qui s'active dès que le joueur touche un élément léthal
("if not(not collided_no_go) or not(not collided_slimes)  :    self.death = True"). Le booléen "death", lorsqu'il devient True, lance une boucle conditionnelle qui, entre autres, appelle la fonctions set_up, qui réinitialise le score (et la première map)

Q: Comment modélisez-vous la "next-map" ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E 
A: La next-map est simplement une valeur string, correspondant au nom du fichier .txt, qui est lue de la même façon que les ints de heigth et width dans la fonction readmap, et stockée dans le str "Next_map". Lorsque la joueuse atteint le point E, on appelle alors la fonction readmap, mais en prenant en argument le str "Next_map" (on a pour cela changé les paramètres de la fonction readmap et adapté son code pour que le chemin d'accès du fichier corresponde au nouveau paramètre map).

Q : Que se passe-t-il si la joueuse atteint le E mais la carte n'a pas de next-map ?
A : Si la carte n'a pas de next map, on considère que le niveau est le dernier niveau et une variable bool "last_level", True par défaut, reste True. Ainsi, si le joueur atteint le E alors que last_level a pour valeur True, le booléen "Victory" devient true (ce qui fait apparaître un message à l'écran, et peut être à l'avenir une musique spécifique).