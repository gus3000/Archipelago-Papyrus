from access_parser import AccessParser
from tabulate import tabulate


class PapyrusDatabase:
    def __init__(self):
        #TODO name in param
        db = AccessParser(r"C:\Jeux\ABWFR\PapyrusSecretCitePerdue\db\Data.pp2")
        table_dieux = db.parse_table("Tbl_Dieux")
        print(tabulate(table_dieux, headers="keys", disable_numparse=True))


# table_objects = db.parse_table("Tbl_Objects")
# print(tabulate(table_objects, headers="keys", disable_numparse=True))

# table_lieux = db.parse_table("Tbl_Lieux")
# print(tabulate(table_lieux, headers="keys", disable_numparse=True))
