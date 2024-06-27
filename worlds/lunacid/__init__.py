from typing import Dict, Any, Iterable, TextIO
import logging
from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from . import Options
from .data.item_data import money, max_item_count_by_item, all_item_data_by_name, all_filler_items
from .data.spell_data import starting_spells, drop_starting_spells
from .data.weapon_data import starting_weapon, drop_starting_weapons, shop_starting_weapons, weapons_by_element
from .strings.items import Creation, Coins, UniqueItem, Progressives, Switch, Door, Trap
from .strings.weapons import Weapon
from .strings.options import Endings, Victory, Settings
from .strings.regions_entrances import LunacidRegion
from .strings.locations import BaseLocation, ShopLocation, unique_drop_locations, other_drop_locations
from .Items import item_table, complete_items_by_name, ItemDict, create_items, determine_starting_weapon, \
    determine_weapon_elements, all_filler, ITEM_CODE_START
from .Locations import (location_table, base_location_table, shop_locations_table, unique_drop_locations_table,
                        LocationDict, other_drop_locations_table, LOCATION_CODE_START)
from .Regions import link_lunacid_areas, create_regions
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

    item_name_groups = {
        "Vampiric Symbols": [Progressives.vampiric_symbol],
        "Switch Keys": Switch.switches,
        "Door Keys": Door.all_door_keys,
        "VHS Tapes": [UniqueItem.vhs_tape, UniqueItem.white_tape],
        "Talismans": [UniqueItem.earth_talisman, UniqueItem.water_talisman],
        "Traps": Trap.all_traps,
        "Junk": all_filler_items
    }

    location_name_groups = {
        "Daedalus Spells": [BaseLocation.archives_daedalus_one, BaseLocation.archives_daedalus_two, BaseLocation.archives_daedalus_third],
        "Tower of Abyss": BaseLocation.abyss_locations,
        "Coins": BaseLocation.coin_locations,
        "Shops": ShopLocation.shop_locations,
        "Unique Drops": unique_drop_locations,
        "Non-unique Drops": other_drop_locations,
    }

    required_client_version = (0, 5, 0)

    options_dataclass = LunacidOptions
    options: LunacidOptions
    starting_weapon: LunacidItem
    weapon_elements: Dict[str, str]
    randomized_entrances: Dict[str, str]
    web = LunacidWeb()
    logger = logging.getLogger()

    def __init__(self, multiworld, player):
        super(LunacidWorld, self).__init__(multiworld, player)

    def generate_early(self) -> None:
        # Universal tracker stuff, shouldn't do anything in standard gen
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Lunacid" in self.multiworld.re_gen_passthrough:
                passthrough = self.multiworld.re_gen_passthrough["Lunacid"]
                self.options.ending.value = passthrough["ending"]
                self.options.dropsanity.value = passthrough["dropsanity"]
                self.options.shopsanity.value = passthrough["shopsanity"]
                self.options.random_elements.value = passthrough["random_elements"]
                self.options.entrance_randomization.value = passthrough["entrance_randomization"]
                self.options.door_locks.value = passthrough["door_locks"]
                self.options.switch_locks.value = passthrough["switch_locks"]
                self.options.secret_door_lock.value = passthrough["secret_door_lock"]

    def create_item(self, name: str, override_classification: ItemClassification = None) -> "LunacidItem":
        item_id: int = self.item_name_to_id[name]

        if override_classification is None:
            override_classification = complete_items_by_name[name].classification

        return LunacidItem(name, override_classification, item_id, player=self.player)

    def create_event(self, event: str):
        return Item(event, ItemClassification.progression_skip_balancing, None, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(money)

    def set_rules(self):
        LunacidRules(self).set_lunacid_rules(self.weapon_elements)

    def create_items(self):
        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)]) - 3
        excluded_items = self.multiworld.precollected_items[self.player]
        if self.options.random_elements == self.options.random_elements.option_true:
            self.weapon_elements = determine_weapon_elements(self.multiworld.random)
        else:
            self.weapon_elements = weapons_by_element
        (potential_pool, starting_weapon_choice) = create_items(self.create_item, locations_count, excluded_items, self.weapon_elements, self.options,
                                                                self.multiworld.random)
        self.starting_weapon = starting_weapon_choice
        if potential_pool.count(self.starting_weapon) > 1:
            potential_pool.remove(self.starting_weapon)
        self.multiworld.itempool += potential_pool

        starting_location = self.multiworld.get_location(BaseLocation.hollow_basin_starting_sword, self.player)
        starting_location.place_locked_item(self.starting_weapon)

    def create_regions(self):
        world = self.multiworld
        player = self.player

        def create_region(name: str, exits: Iterable[str]) -> Region:
            lunacid_region = Region(name, player, world)
            lunacid_region.exits = [Entrance(player, exit_name, lunacid_region) for exit_name in exits]
            return lunacid_region

        world_regions, self.randomized_entrances = create_regions(create_region, self.multiworld.random, self.options)

        for location in location_table:
            name = location.name
            code = location.code
            if location in shop_locations_table and self.options.shopsanity == self.options.shopsanity.option_false:
                continue
            if location in unique_drop_locations_table and self.options.dropsanity == self.options.dropsanity.option_off:
                continue
            if location in other_drop_locations_table and self.options.dropsanity != self.options.dropsanity.option_randomized:
                continue
            if location.name in BaseLocation.abyss_locations and self.options.exclude_tower == self.options.exclude_tower.option_true:
                continue
            if location.name in BaseLocation.coin_locations and self.options.exclude_coin_locations == self.options.exclude_coin_locations.option_true:
                continue
            region: Region = world_regions[location.region]
            region.add_locations({name: code})

        self.multiworld.regions.extend(world_regions.values())

        if self.options.ending == self.options.ending.option_ending_b:
            ending_region = world.get_region(LunacidRegion.labyrinth_of_ash, player)
        elif self.options.ending != self.options.ending.option_any_ending:
            ending_region = world.get_region(LunacidRegion.grave_of_the_sleeper, player)
        else:
            ending_region = world.get_region(LunacidRegion.forlorn_arena, player)
        throne_region = world.get_region(LunacidRegion.throne_chamber, player)
        crilall = Location(player, "Throne of Prince Crilall Fanu", None, throne_region)
        crilall.place_locked_item(self.create_event("Defeat Prince Crilall Fanu"))
        throne_region.locations.append(crilall)
        grotto_region = world.get_region(LunacidRegion.boiling_grotto, player)
        hicket = Location(player, "Free Sir Hicket", None, grotto_region)
        hicket.place_locked_item(self.create_event("Sir Hicket's Freedom from Armor"))
        if self.options.ending == self.options.ending.option_ending_cd:
            victory = Location(player, Endings.look_into_abyss, None, ending_region)
        elif self.options.ending == self.options.ending.option_ending_b:
            victory = Location(player, Endings.open_door, None, ending_region)
        elif self.options.ending == self.options.ending.option_ending_a or self.options.ending == self.options.ending.option_ending_e:
            victory = Location(player, Endings.wake_dreamer, None, ending_region)
        else:
            victory = Location(player, "The Dreamer or the Door", None, ending_region)
        victory.place_locked_item(self.create_event(Victory.victory))
        ending_region.locations.append(victory)

        if self.options.ending == self.options.ending.option_ending_b:
            set_rule(victory, lambda state: LunacidRules(self).has_coins_for_door(self.options, state))
        elif self.options.ending == self.options.ending.option_ending_e:
            set_rule(victory, lambda state: LunacidRules(self).has_every_spell(state, self.options) and state.has(UniqueItem.white_tape, self.player))
        elif self.options.ending == self.options.ending.option_any_ending:
            set_rule(victory, lambda state: state.can_reach_region(LunacidRegion.grave_of_the_sleeper, self.player) or
                                            (LunacidRules(self).has_coins_for_door(self.options, state) and
                                             state.can_reach_region(LunacidRegion.labyrinth_of_ash, self.player)))

        world.completion_condition[self.player] = lambda state: state.has(Victory.victory, player)

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        """Write to the spoiler header. If individual it's right at the end of that player's options,
        if as stage it's right under the common header before per-player options."""
        self.add_entrances_to_spoiler_log()

    def add_entrances_to_spoiler_log(self):
        if self.options.entrance_randomization == self.options.entrance_randomization.option_false:
            return
        for original_entrance, replaced_entrance in self.randomized_entrances.items():
            self.multiworld.spoiler.set_entrance(original_entrance, replaced_entrance, "entrance", self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {
            "seed": self.random.randrange(1000000000),  # Seed should be max 9 digits
            "client_version": "0.6.2",
            "starting_weapon": self.starting_weapon,
            "elements": self.weapon_elements,
            **self.options.as_dict("ending", "entrance_randomization", "experience", "weapon_experience", "required_strange_coin",
                                   "filler_bundle", "shopsanity", "dropsanity", "switch_locks", "door_locks", "random_elements", "secret_door_lock",
                                   "death_link", "exclude_tower", "exclude_coin_locations", "starting_class", "normalized_drops"),
            "entrances": self.randomized_entrances
        }

        return slot_data

    # for the universal tracker, doesn't get called in standard gen
    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        self.starting_weapon = slot_data["starting_weapon"]
        self.weapon_elements = slot_data["elements"]
        self.randomized_entrances = slot_data["entrances"]
        return slot_data
