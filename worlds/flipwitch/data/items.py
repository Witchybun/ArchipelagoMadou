from dataclasses import dataclass
from typing import List
from BaseClasses import ItemClassification

from ..strings.items import QuestItem, Upgrade, Coin, Gacha, Unlock, Key, Costume


@dataclass(frozen=True)
class FlipwitchItemData:
    code: int
    name: str
    classification: ItemClassification

    def __repr__(self):
        return f"{self.code} {self.name} (Classification: {self.classification})"


all_items: List[FlipwitchItemData] = []


def create_item(code: int, name: str, classification: ItemClassification):
    item = FlipwitchItemData(code, name, classification)
    all_items.append(item)

    return item

# ID - Classification Data


# Uses a structure of BASE ITEM + type offset + pseudo value.  The base item ID will eventually be deprecated in favor of starting at 1.
ITEM_CODE_START = 0


base_start_id = 0
base_items = [
    create_item(ITEM_CODE_START + base_start_id + 2, Upgrade.peachy_peach, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 5, Key.rundown_house, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 6, Upgrade.bewitched_bubble, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 9, Unlock.crystal_block, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 10, "Nothing", ItemClassification.filler),  # REMOVE LATER NOTHING SUCKS
]

quest_item_id = 50
quest_items = [
    create_item(ITEM_CODE_START + quest_item_id + 1, QuestItem.cowbell, ItemClassification.progression),
    create_item(ITEM_CODE_START + quest_item_id + 2, QuestItem.fairy_bubble, ItemClassification.progression),

]

gacha_item_id = 100
gacha_items = [
    create_item(ITEM_CODE_START + gacha_item_id + 3, Coin.lucky_coin, ItemClassification.progression),
    create_item(ITEM_CODE_START + gacha_item_id + 4, Gacha.special_promotion, ItemClassification.useful),
]

shop_item_id = 150
shop_items = [

]

costume_item_id = 200
costume_items = [
    create_item(ITEM_CODE_START + costume_item_id + 1, Costume.navy, ItemClassification.useful),
]

item_table = {
    "Mimic Chest Key":1,
    "Ghost Form":2,
    "Black Witch Costume":3,
    "Fortune Cat":4,
    "Ending":5,
    "Sacrificial Dagger":6,
    "Toxic Slime Vial":7,
    "Haunted Scythe":8,
    "Magical Mushroom":9,
    "Goblin Bomb":10,
    "Ring Of The Moon":11,
    "Harpy Feather":12,
    "Disarming Bell":13,
    "Slime Form":14,
    "Slime Sentry":15,
    "Frilly Panties":16,
    "Demonic Cuff":17,
    "Magnetic Hairpin":18,
    "Cursed Talisman":19,
    "Portable Portal":20,
    "Ring Of The Sun":21,
    "Star Bracelet":22,
    "Yellow Frog Talisman":23,
    "Mind Mushroom":24,
    "Heart Necklace":25,
    "Flutterknife Garter":26,
    "Blue Frog Talisman":27,
    "Chaos Key Piece":28,
    "Bewitched Bubble":34,
    "Goblin Crystal":35,
    "Demon Wings":36,
    "Angel Feathers":37,
    "Mermaid Scale":38,
    "Red Wizard Costume":39,
    "Nun Costume":40,
    "Priest Costume":41,
    "Miko Costume":42,
    "Farmer Costume":43,
    "Cat Costume":44,
    "Goblin Costume":45,
    "Maid Costume":46,
    "Pigman Costume":47,
    "Bunny Costume":48,
    "Rat Costume":49,
    "Nurse Costume":50,
    "Angler Costume":51,
    "Dominating Costume":52,
    "Postman Costume":53,
    "Fairy Costume":54,
    "Alchemist Costume":55,
    "Rundown House Key":56,
    "Ghostly Castle Key":57,
    "The Beast's Key":58,
    "Secret Club Door Key":59,
    "Slime Citadel Key":60,
    "Frog Boss Key":61,
    "Goblin Queen Key":62,
    "Rose Garden Key":63,
    "Collapsed Temple Key":64,
    "Demon Boss Key":65,
    "Slimy Sub Boss Key":66,
    "Chaos Sanctum Key":67,
    "Abandoned Apartment Key":68,
    "Secret Garden Key":69,
    "Demon Club Door Key":70,
    "Forgotten Fungal Door Key":71,
    "Slime Boss Key":72,
    "Peachy Peach":73, #11 or 12 upgrades?
    "Gacha Coin":74, #44 of these
    "Gold Coins":75, #Money
    "Progressive Belle Item":76,
    "Momo Server Admin Password":78,
    "Bundle of Clothes":79,
    "Progressive Gobliana Item":80,
    "Progressive Kyoni Item":82,
    "Soul Fragment":84,
    "Legendary Halo":87,
    "Progressive Letter":88,
    "Silky Slime":90,
    "Red Wine":92,
    "Blue Jelly Mushroom":93,
    "Maid Contract":94,
    "Progressive Tatil Item":95,
    "Summon Stone":96,
    "Health Upgrade":99, #10 of these
    "Mana Upgrade":100, #10 of these
    "Wand Upgrade":101,
    "Fairy Bubble":102,
    "Progressive Animal Girl Gacha":110,
    "Progressive Bunny Girl Gacha":120,
    "Progressive Angels & Demons Gacha":130,
    "Progressive Monster Girl Gacha":140,
    "Special Promo Gacha":143,
    "Peachy Peach Upgrade":144,
    "Deed to Fungal Forest":145,

    #junk items
    #"AG Figure 1":201,
    #"AG Figure 2":202,
    #"AG Figure 3":203,
    #"AG Figure 4":204,
    #"AG Figure 5":205,
    #"AG Figure 6":206,
    #"AG Figure 7":207,
    #"AG Figure 8":208,
    #"AG Figure 9":209,
    #"AG Figure 10":210,
    #"BG Figure 1":211,
    #"BG Figure 2":212,
    #"BG Figure 3":213,
    #"BG Figure 4":214,
    #"BG Figure 5":215,
    #"BG Figure 6":216,
    #"BG Figure 7":217,
    #"BG Figure 8":218,
    #"BG Figure 9":219,
    #"BG Figure 10":220,
    #"AD Figure 1":221,
    #"AD Figure 2":222,
    #"AD Figure 3":223,
    #"AD Figure 4":224,
    #"AD Figure 5":225,
    #"AD Figure 6":226,
    #"AD Figure 7":227,
    #"AD Figure 8":228,
    #"AD Figure 9":229,
    #"AD Figure 10":230,
    #"MG Figure 1":231,
    #"MG Figure 2":232,
    #"MG Figure 3":233,
    #"MG Figure 4":234,
    #"MG Figure 5":235,
    #"MG Figure 6":236,
    #"MG Figure 7":237,
    #"MG Figure 8":238,
    #"MG Figure 9":239,
    #"MG Figure 10":240,
    #"SP Figure":241,
#}
#
#quest_table = {
    "Completed Quests":3001,
    "Belle 1":3002,
    "Belle 2":3003,
    "Belle 3":3004,
    "Goblin 1":3005,
    "Goblin 2":3006,
    "Rover 1":3007,
    "Rover 2":3008,
    "Rover 3":3009,
    "Merchant 1":3010,
    "Milk & Cream 1":3011,
    "Milk & Cream 2":3012,
    "Milk & Cream 3":3013,
    "Janic 1":3014,
    "Janic 2":3015,
    "Kyoni 1":3016,
}
