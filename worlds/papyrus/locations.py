from typing import NamedTuple, Dict

from BaseClasses import Location


class PapyrusLocation(Location):
    game = "Papyrus"


class PapyrusLocationData(NamedTuple):
    region: str
    address: int


base_id: int = 14 * 3000 + 100

location_data_table: Dict[str, PapyrusLocationData] = {
    f"Endroit {i}": PapyrusLocationData("Désert", base_id + i) for i in range(1, 3)
}

location_table = {name: data.address for name, data in location_data_table.items()}
