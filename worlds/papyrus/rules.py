from worlds.papyrus import PapyrusWorld


def set_completion_rules(world: PapyrusWorld, player: int) -> None:
    world.multiworld.completion_condition[player] = \
        lambda state: (True)
