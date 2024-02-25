from typing import Dict, List, Any
import logging
from collections import Counter
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld
from . import Options
from .data.item_count_data import base_spells, drop_spells
from .data.location_data import shop_items, base_items, drop_items
from .data.item_data import money, max_item_count_by_item, all_item_data_by_name
from .data.spell_data import starting_spells, drop_starting_spells
from .data.weapon_data import starting_weapon, drop_starting_weapons, shop_starting_weapons
from .strings.items import Creation, Coins, UniqueItem
from .strings.weapons import Weapon
from .strings.options import Endings, Victory, Settings
from .strings.regions_entrances import LunacidRegion
from .strings.locations import BaseLocation
from .Items import item_table, complete_items_by_name, group_table, ITEM_CODE_START, ItemDict, create_items, get_coin_count, determine_starting_weapon
from .Locations import (location_table, base_location_table, shop_locations_table, mob_drop_locations_table, LocationDict,
                        LOCATION_CODE_START)
from .Regions import link_lunacid_areas, lunacid_entrances, lunacid_regions
from .Rules import LunacidRules
from worlds.generic.Rules import set_rule
from .Options import LunacidOptions


class LunacidItem(Item):
    game: str = "Lunacid"


class LunacidWeb(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Lunacid randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Albrekka", "Tesseract (Advice/Direction)"]
    )]


class LunacidWorld(World):
    """
    Lunacid is a first person dungeon crawler inspired by old FROMSOFT games like Shadow Tower and King’s Field.

    Long ago a great beast arose from the sea and covered the earth in a poison fog. Now those deemed undesirable
    are thrown into a great well, which has become a pit of chaos and disease. You awaken in a moonlit subterranean world,
    having been thrown into the Great Well for crimes unknown. The only way out is to go further down and confront the
    sleeping old one below. On the way there will be many creatures and secrets to discover.
    """

    game = "Lunacid"
    topology_present = False
    item_name_to_id = {item.name: item.code for item in item_table}
    location_name_to_id = {loc.name: loc.code for loc in location_table}

    data_version = 1
    required_client_version = (0, 4, 3)

    options_dataclass = LunacidOptions
    options: LunacidOptions
    starting_weapon: LunacidItem
    web = LunacidWeb()
    logger = logging.getLogger()

    def __init__(self, multiworld, player):
        super(LunacidWorld, self).__init__(multiworld, player)

    def create_item(self, name: str, override_classification: ItemClassification = None) -> "LunacidItem":
        item_id: int = self.item_name_to_id[name]

        if override_classification is None:
            override_classification = complete_items_by_name[name].classification

        return LunacidItem(name, override_classification, item_id, player=self.player)

    def create_event(self, event: str):
        return Item(event, ItemClassification.progression_skip_balancing, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(money)

    def set_rules(self):
        LunacidRules(self).set_lunacid_rules()

    def create_items(self):
        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)]) - 3
        excluded_items = self.multiworld.precollected_items[self.player]

        (potential_pool, starting_weapon_choice) = create_items(self.create_item, locations_count, excluded_items, self.options, self.multiworld.random)
        self.starting_weapon = starting_weapon_choice
        if potential_pool.count(self.starting_weapon) > 1:
            potential_pool.remove(self.starting_weapon)
        self.multiworld.itempool += potential_pool

        starting_location = self.multiworld.get_location(BaseLocation.hollow_basin_starting_sword, self.player)
        starting_location.place_locked_item(self.starting_weapon)

    def create_regions(self):
        world = self.multiworld
        player = self.player

        def lunacid_region(region_name: str, entrances):
            single_region = Region(region_name, player, world)
            for entrance in entrances:
                single_region.exits.append(Entrance(player, entrance, single_region))
            return single_region

        world.regions += [lunacid_region(*r) for r in lunacid_regions]
        link_lunacid_areas(world, player)

        for location in location_table:
            name = location.name
            code = location.code
            if location in shop_locations_table and self.options.shopsanity == self.options.shopsanity.option_false:
                continue
            if location in mob_drop_locations_table and self.options.dropsanity == self.options.dropsanity.option_false:
                continue
            region: Region = world.get_region(location.region, player)
            region.add_locations({name: code})

        if self.options.ending == self.options.ending.option_ending_b:
            ending_region = world.get_region(LunacidRegion.labyrinth_of_ash, player)
        else:
            ending_region = world.get_region(LunacidRegion.grave_of_the_sleeper, player)
        throne_region = world.get_region(LunacidRegion.throne_chamber, player)
        crilall = Location(player, "Throne of Prince Crilall Fanu", None, throne_region)
        crilall.place_locked_item(self.create_event("Defeat Prince Crilall Fanu"))
        throne_region.locations.append(crilall)
        grotto_region = world.get_region(LunacidRegion.boiling_grotto, player)
        hicket = Location(player, "Free Sir Hicket", None, grotto_region)
        hicket.place_locked_item(self.create_event("Sir Hicket's Freedom from Armor"))
        victory = Location(player, Endings.wake_dreamer, None, ending_region)
        if self.options.ending == self.options.ending.option_ending_cd:
            victory = Location(player, Endings.look_into_abyss, None, ending_region)
        elif self.options.ending == self.options.ending.option_ending_b:
            victory = Location(player, Endings.open_door, None, ending_region)
        victory.place_locked_item(self.create_event(Victory.victory))
        ending_region.locations.append(victory)

        if self.options.ending == self.options.ending.option_ending_b:
            coin_count = get_coin_count(self.options)
            set_rule(victory, lambda state: state.has(Coins.strange_coin, player, coin_count))
        elif self.options.ending == self.options.ending.option_ending_e:
            set_rule(victory, lambda state: LunacidRules(self).has_every_spell(state, self.options) and state.has(UniqueItem.white_tape, self.player))

        world.completion_condition[self.player] = lambda state: state.has(Victory.victory, player)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {
            "seed": self.multiworld.per_slot_randoms[self.player].randrange(1000000000),  # Seed should be max 9 digits
            "client_version": "0.1.0",
            **self.options.as_dict("ending", "experience", "weaponexperience", "strangecoinbundle",
                                   "fillerbundle", "shopsanity", "dropsanity", "switchlocks")
        }

        return slot_data
