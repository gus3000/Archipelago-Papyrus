from typing import NamedTuple, Dict

from BaseClasses import Item, ItemClassification


class PapyrusItem(Item):
    game = "Papyrus"


class PapyrusItemData(NamedTuple):
    code: int
    type: ItemClassification


base_id = 14 * 3000

item_data_table: Dict[str, PapyrusItemData] = {
    "Poney": PapyrusItemData(base_id + 1, ItemClassification.progression),
    "Cheval": PapyrusItemData(base_id + 2, ItemClassification.progression),
    "Citroen C4": PapyrusItemData(base_id + 3, ItemClassification.progression),
}

item_table = {name: data.code for name, data in item_data_table.items()}
