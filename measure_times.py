
"""
Mesure des temps d'exécution.
Test du chargement et de l'update avec timeit.
"""

import timeit
import create_world

number = 1000

def test_loading(map_file: str) -> float:
    """Teste le temps de chargement d'une carte"""
    
    def load_map(map_file: str = map_file) -> None:
        world = create_world.World()
        create_world.readmap(world, map_file)
    
    # Mesurer avec timeit
    time_taken = timeit.timeit(lambda: load_map(), number=number)
    return time_taken / number

def test_update(map_file: str) -> float:
    """Teste le temps d'update avec les ennemis"""
    
    # Charger la carte
    world = create_world.World()
    create_world.readmap(world, map_file)
    
    def do_update(world : create_world.World) -> None:
        # Mouvement des ennemis
        for monster in world.monsters_list:
            monster.movement()
    
    # Mesurer
    time_taken = timeit.timeit(lambda: do_update(world=world), number=number)
    return time_taken / number


test_values = [1, 3, 5, 10, 50, 100, 500, 1000]
    
for n in test_values: 
        print(f"Test {n} plateformes...")
        print(test_loading(f"platforms_{n}.txt"))
        
    
for n in test_values:
    print(f"Test {n} ennemis...")
    print(test_update(f"enemies_{n}.txt"))
    
