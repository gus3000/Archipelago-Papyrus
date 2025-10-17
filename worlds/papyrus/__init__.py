import typing

import settings
from BaseClasses import Location, Tutorial, Region
from worlds.AutoWorld import World, WebWorld
from .items import item_table, PapyrusItem, item_data_table
from .locations import location_table, location_data_table
from .options import PapyrusOptions


class PapyrusLocation(Location):
    game = "Papyrus"


class PapyrusWebWorld(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to playing Papyrus in Archipelago",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["gus3000"]
    )

    tutorials = [setup_en]


class PapyrusSettings(settings.FolderPath):
    game_location: settings.FolderPath = settings.FolderPath(R"C:\Jeux\ABWFR\PapyrusSecretCitePerdue")


class PapyrusWorld(World):
    """Le meilleur jeu"""
    game = "Papyrus"
    options_dataclass = PapyrusOptions
    options: PapyrusOptions
    web = PapyrusWebWorld()
    settings: typing.ClassVar[PapyrusSettings]
    topology_present = True
    required_client_version = (0, 6, 0)

    base_id = 14 * 3000

    item_name_to_id = item_table
    location_name_to_id = location_table

    def create_item(self, name: str) -> PapyrusItem:
        return PapyrusItem(name, item_data_table[name].type, item_data_table[name].code, self.player)

    def create_items(self) -> None:
        itempool = []

        self.push_precollected(self.create_item("Poney"))
        itempool += [self.create_item("Cheval")]
        itempool += [self.create_item("Citroen C4")]

        self.multiworld.itempool = itempool

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        desert = Region("Désert", self.player, self.multiworld)
        desert.locations += [
            PapyrusLocation(self.player, loc_name, loc_data.address, desert)
            for loc_name, loc_data in location_data_table.items()
        ]

        self.multiworld.regions.append(desert)

        menu_region.connect(desert)

    def set_rules(self) -> None:
        from .rules import set_completion_rules
        set_completion_rules(self, self.player)
