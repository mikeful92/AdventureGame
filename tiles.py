import items, enemies, actions, world
 
class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def intro_text(self):
        raise NotImplementedError()
 
    def modify_player(self, player):
        raise NotImplementedError()

    def adjacent_moves(self):
        """Returns all move actions for adjacent tiles."""
        moves = []
        if world.tile_exists(self.x + 1, self.y):
            moves.append(actions.MoveEast())
        if world.tile_exists(self.x - 1, self.y):
            moves.append(actions.MoveWest())
        if world.tile_exists(self.x, self.y - 1):
            moves.append(actions.MoveNorth())
        if world.tile_exists(self.x, self.y + 1):
            moves.append(actions.MoveSouth())
        return moves
     
    def available_actions(self):
        """Returns all of the available actions in this room."""
        moves = self.adjacent_moves()
        moves.append(actions.ViewInventory())
     
        return moves

class StartingRoom(MapTile):
    def intro_text(self):
        return """
        Hello Queen Erica Paige Ross. You are currently in the palace.
        Princess Satsuki awaits you in her sanctuary.
        You can make out four paths, but becareful, not all paths are safe.
        """
 
    def modify_player(self, player):
        #Room has no action on player
        pass

class LootRoom(MapTile):
    """A room that adds something to the player's inventory"""
    def __init__(self, x, y, item):
        self.item = item
        super().__init__(x, y)

    def add_loot(self, the_player):
        the_player.inventory.append(self.item)

    def modify_player(self, the_player):
        self.add_loot(the_player)

class EnemyRoom(MapTile):
    def __init__(self, x, y, enemy):
        self.enemy = enemy
        super().__init__(x, y)
 
    def modify_player(self, the_player):
        if self.enemy.is_alive():
            the_player.hp = the_player.hp - self.enemy.damage
            print("Enemy does {} damage. You have {} HP remaining.".format(self.enemy.damage, the_player.hp))

    def available_actions(self):
        if self.enemy.is_alive():
            return [actions.Flee(tile=self), actions.Attack(enemy=self.enemy)]
        else:
            return self.adjacent_moves()

class EmptyCavePath(MapTile):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """
 
    def modify_player(self, player):
        #Room has no action on player
        pass
 
class GiantSpiderRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.GiantSpider())
 
    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """
 
class FindDaggerRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Dagger())
 
    def intro_text(self):
        return """
        Your notice something shiny in the corner.
        It's a dagger! You pick it up.
        """

class LeaveCaveRoom(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
 
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        player.victory = True

class SatsukiSanctuary(MapTile):
    def intro_text(self):
        return """
        You walk into the most elegant room in the palace.
        Satsuki is napping atop her shelf.
        She smells you comming in.
        Walks up to you and gives you a big HUG!
        You clean her eyes and nap with her. 
 
        Victory is yours!
        """
 
    def modify_player(self, player):
        player.victory = True

class Find5GoldRoom(LootRoom):
    def __init__(self, x, y):
        super().__init__(x, y, items.Gold(5))

    def intro_text(self):
        return """
        Someone dropped a 5 gold piece. You pick it up.
        """

class NinjaRoom(EnemyRoom):
    def __init__(self, x, y):
        super().__init__(x, y, enemies.Ninja())

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            There is something odd about this room.
            As you are walking around a shuriken hits the column next to you.
            You duck, trying to find your opponent. A ninja is here.
            """
        else:
            return """
            A dead ninja reminds you of your triumph.
            """

class SnakePitRoom(MapTile):
    def intro_text(self):
        return """
        You have fallen into a pit of deadly snakes!
        You have died!
        """

    def modify_player(self, player):
        player.hp = 0
