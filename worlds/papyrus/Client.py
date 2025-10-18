import asyncio
from inspect import currentframe, getframeinfo
from typing import Final

import pymem
from pymem import Pymem

from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop
from worlds.papyrus.Database import PapyrusDatabase

PAPYRUS_PROCESS_NAME: Final[str] = "Papyrus"


class PapyrusContext(CommonContext):
    game = "Papyrus"
    items_handling = 0b111  # Indicates you get items sent from other worlds.

    def __init__(self, server_address, password):
        super(PapyrusContext, self).__init__(server_address, password)

        self.papyrus_connected = False
        self.server_connected = False
        self.sending = []

        self.papyrus: Pymem | None = None
        self.database: PapyrusDatabase | None = None

    def connect_to_game(self):
        try:
            if not self.papyrus:
                self.papyrus = pymem.Pymem(process_name=PAPYRUS_PROCESS_NAME)
                self.database = PapyrusDatabase()
        except Exception as e:
            self.papyrus_connected = False
            logger.info("Game is not open")

    def papyrus_read_short(self, address):
        return self.papyrus.read_short(self.papyrus.base_address + address)

    def init_addresses(self):
        if not self.papyrus_connected and self.papyrus is not None:
            self.papyrus_read_short(0)

    def on_package(self, cmd: str, args: dict):
        logger.info(f"on_package cmd:{cmd}")


async def papyrus_watcher(ctx: PapyrusContext):
    while not ctx.exit_event.is_set():
        try:
            if ctx.papyrus_connected and ctx.server_connected:
                ctx.sending = []
            elif not ctx.papyrus_connected and ctx.server_connected:
                logger.info("Papyrus's Server Disconnected")
                ctx.papyrus = None
                while not ctx.papyrus_connected and ctx.server_connected:
                    try:
                        ctx.papyrus = pymem.Pymem(process_name=PAPYRUS_PROCESS_NAME)
                        ctx.init_addresses()
                        logger.info("Game Connection Established.")
                    except Exception as e:
                        await asyncio.sleep(5)
        except Exception as e:
            ctx.papyrus_connected = False
            frameinfo = getframeinfo(currentframe())
            logger.info(e)
            logger.info(f"File {frameinfo.filename}, Line {frameinfo.lineno}")

        await asyncio.sleep(5)


def launch():
    async def main(args):
        ctx = PapyrusContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(papyrus_watcher(ctx), name="PapyrusWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None
        await progression_watcher
        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Papyrus Client")
    args, rest = parser.parse_known_args()
    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
