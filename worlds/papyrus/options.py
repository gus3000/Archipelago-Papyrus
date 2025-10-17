from dataclasses import dataclass

from Options import PerGameCommonOptions, FreeText


class PapyrusFolderPath(FreeText):
    default = R"Blabla"
    display_name = "Path to the Papyrus install directory"


@dataclass
class PapyrusOptions(PerGameCommonOptions):
    path: PapyrusFolderPath
