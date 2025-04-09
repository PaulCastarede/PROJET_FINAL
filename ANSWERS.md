Semaine 3 :

Q: Comment avez-vous conçu la lecture du fichier ? Comment l'avez-vous structurée de sorte à pouvoir la tester de manière efficace ?
A: On parcourt chaque caractère de chaque ligne du txt à partir des trois tirets '---'.
Dès lors qu'un caractère consacré est rencontré, on ajoute le sprite correspondant à la sprite_list associée, à la position de la colonne et de la ligne multipliée par un facteur pour qu'elle corresponde aux coordonnées in game adéquates.
...

Q: Comment avez-vous adapté vos tests existants au fait que la carte ne soit plus la même qu'au départ ? Est-ce que vos tests résisteront à d'autres changements dans le futur ? Si oui, pourquoi ? Si non, que pensez-vous faire plus tard ?

Q: Le code qui gère la lave ressemble-t-il plus à celui de l'herbe, des pièces, ou des blobs ? Expliquez votre réponse.
A: Le code qui gère la lave s'inspire de celui de l'herbe et de celui des blobs. Il ressemble à l'herbe car on l'a défini comme un sprite qui devait rester toujours à la même position, comme un élément du terrain (avec use_spatial_hash=True), mais partage la même condition que le slime de tuer la joueuse si elle entre en collision avec. On a utilisé la boucle conditionnelle 
if collided_no_go or  collided_slimes   :    #Si le joueur est en collision avec la lave ou un monstre...
     self.death = True

Q: Comment détectez-vous les conditions dans lesquelles les blobs doivent changer de direction ?
A: J'ai défini un sprite invisibile 'front' qui se situe à chaque instant juste devant le blob, et un autre, 'below' qui se situe juste en dessous de lui. Dès lors que le sprite 'front' entre en collision avec un element du terrain (wall), ou dès lors que le sprite 'below' n'est plus en collision avec un élément du terrain (wall), le slime change de direction (slime.change_x *= -1 ) 


Semaine 4 :

Q: Quelles formules utilisez-vous exactement pour l'épée ? Comment passez-vous des coordonnées écran aux coordonnées monde ?
A: 

Q:Comment testez-vous l'épée ? Comment testez-vous que son orientation est importante pour déterminer si elle touche un monstre ?
A:

Q: Comment transférez-vous le score de la joueuse d'un niveau à l'autre ? Où le remettez-vous à zéro ?
A: Le score est (ré)initialisé au niveau de la fonction set-up, qui est appelée uniquement au début du programme, lors de la mort ou lorsque l'on appuie sur la touche échap. Cela correspond exactement aux moments où l'on veut reset le score. En effet, on passe d'une map à une autre sans utiliser la fonction set up mais uniquement la fonction readmap.

Q: Avez-vous du code dupliqué entre les cas où la joueuse perd parce qu'elle a touché un ou monstre ou de la lave ?
A: On a implémenté un "Game_Over" qui s'active dès que le joueur touche un élément léthal
("if not(not collided_no_go) or not(not collided_slimes)  :    self.death = True"). Le booléen "death", lorsqu'il devient True, lance une boucle conditionnelle qui, entre autres, appelle la fonctions set_up, qui réinitialise le score (et la première map)

Q: Comment modélisez-vous la "next-map" ? Où la stockez-vous, et comment la traitez-vous quand la joueuse atteint le point E 
A: La next-map est simplement une valeur string, correspondant au nom du fichier .txt, qui est lue de la même façon que les ints de heigth et width dans la fonction readmap, et stockée dans le str "Next_map". Lorsque la joueuse atteint le point E, on appelle alors la fonction readmap, mais en prenant en argument le str "Next_map" (on a pour cela changé les paramètres de la fonction readmap et adapté son code pour que le chemin d'accès du fichier corresponde au nouveau paramètre map).

Q : Que se passe-t-il si la joueuse atteint le E mais la carte n'a pas de next-map ?
A : Si la carte n'a pas de next map, on considère que le niveau est le dernier niveau et une variable bool "last_level", True par défaut, reste True. Ainsi, si le joueur atteint le E alors que last_level a pour valeur True, le booléen "Victory" devient true (ce qui fait apparaître un message à l'écran, et peut être à l'avenir une musique spécifique).


Semaine 5 :

Q: Quelles formules utilisez-vous exactement pour l'arc et les flèches ?


Q : Quelles formules utilisez-vous exactement pour le déplacement des chauves-souris (champ d'action, changements de direction, etc.) ?
A : J'ai d'abord défini une classe "Bat" à laquelle j'ai attribué un point d'apparition fixe et un angle "theta" qui représente l'orientation de sa direction.
Pour gérer le champ d'action de la chauve souris, j'ai écrit une boucle conditionnelle qui ajoute pi a theta lorsqu'elle dépasse une certaine distance (200 pixels) de son point d'apparition. Elle fait ainsi demi-tour lorsqu'elle sort d'un cercle de rayon 200 centré en son point d'apparition.  J'ai aussi fait en sorte que la boucle ne puisse pas s'exécuter dans un laps de temps trop court, auquel cas la chauve souris pouvait rester en dehors de son cercle d'action à faire des demi-tours indéfiniment.
Pour que le mouvement de la chauve souris soit erratique, j'ai fait en sorte que tous les 15 ticks, le theta de la chauve souris soit redéfini de manière aléatoire suivant une distribution normale centrée en la précédente valeur de theta et avec un écart type de pi/10.


Q: Comment avez-vous structuré votre programme pour que les flèches puissent poursuivre leur vol ?

Q: Comment gérez-vous le fait que vous avez maintenant deux types de monstres, et deux types d'armes ? Comment faites-vous pour ne pas dupliquer du code entre ceux-ci ?
A: Pour les monstres, on a créé une classe abstraite monstre et deux sous-classes 'Slime' et 'Bat' qui héritent de cette classe abstraite. On a ainsi pu mettre les blobs et les chauve-souris dans une même liste 'monsters_list'. Les propriétés qui concernent ces deux monstres s'appliquent sur tous les éléments de la liste monsters, et chaque sous classe de type de monstre définit les méthodes qui sont propres au monstre. Par exemple, les slimes et les chauve souris héritent d'une même classe abstraite 'movement', mais qui est ensuite spécifiée différemment pour chaque type de monstre. Pour les armes, le procédé était à peu près similaire mais la classe Weapon dont elles héritent n'est pas abstraite et définit le gros des méthodes que les armes utilisent, ayant plus de similitudes dans leur comportement (la seule différence intrinsèque étant que l'épée tue les monstres en collision)