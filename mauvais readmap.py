def readmap(self) -> None:
        with open("maps/map1.txt", "r", encoding="utf-8") as file:     
            for i in range(2):
                    line = file.readline()  # Retirer les espaces et sauts de ligne
                    if ": " in line:
                        key, value = line.split(":", 1)  # Séparer la clé et la valeur
                        key = key.strip()
                        value_int = int(value)  # Convertir la valeur en entier
                        if key == "width":
                            self.map_width = value_int
                        elif key == "height":
                            self.map_height = value_int

            if self.map_width == 0 or self.map_height == 0 : 
                    raise ValueError()
            
            self.wall_list.clear()
            self.coins_list.clear()           #On enlève les sprites qui étaient générés auparavant
            self.slimes_list.clear()
            self.no_go_list.clear()
            self.player_sprite_list.clear()                                                              
            
            for i, line in enumerate(file, start=3):           #On parcourt chaque ligne et chaque colonne de la map 
                if i > self.map_height + 3 :
                    break
                for j, character in enumerate(line):
                    print(line)
                    match character :
                        case "=":   
                            grass= arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.wall_list.append(grass)
                                
                        case "-":   
                            half_grass = arcade.Sprite(":resources:/images/tiles/grassHalf_mid.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.wall_list.append(half_grass)
                    
                        case "x":   
                            crate= arcade.Sprite(":resources:/images/tiles/boxCrate_double.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.wall_list.append(crate)
                                        
                        case "*":   
                            coin = arcade.Sprite(":resources:/images/items/coinGold.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            self.coins_list.append(coin)
                    
                        case "o":   
                            slime = arcade.Sprite(":resources:/images/enemies/slimeBlue.png", scale=0.5, center_x=64*j, center_y= 64*(self.map_height - i))
                            slime.change_x = SLIMES_SPEED
                            self.slimes_list.append(slime)
                            
                    
                        case "£":   
                            lava = arcade.Sprite(":resources:/images/tiles/lava.png", scale=0.5, center_x=64*j, center_y=64*(self.map_height - i))
                            self.no_go_list.append(lava)
                    
                        case "S":   
                            self.S_x = 64*j
                            self.S_y = 64*(self.map_height - i)