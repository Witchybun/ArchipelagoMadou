from BaseClasses import CollectionState
from typing import Dict, List, TYPE_CHECKING

from .data.item_count_data import base_spells
from .strings.properties import Elements
from ..generic.Rules import CollectionRule

from .data.spell_data import spell_light_sources, jump_spells, drop_spells, ranged_spells, blood_spells
from .data.weapon_data import ranged_weapons, weapon_light_sources
from .data.item_data import item_light_sources
from .Options import LunacidOptions
from .strings.regions_entrances import LunacidEntrance, LunacidRegion
from .strings.spells import Spell
from .strings.items import UniqueItem, Progressives, Switch, Alchemy
from .strings.locations import BaseLocation, ShopLocation, DropLocation
if TYPE_CHECKING:
    from . import LunacidWorld


class LunacidRules:
    player: int
    world: "LunacidWorld"
    region_rules: Dict[str, CollectionRule]
    entrance_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]
    elements: Dict[str, str]

    def __init__(self, world: "LunacidWorld") -> None:
        self.player = world.player
        self.world = world
        self.world.options = world.options

        self.region_rules = {
            LunacidRegion.temple_of_silence_entrance: lambda state: self.has_light_source(state) and self.has_keys_for_basin_door(state, self.world.options),
            LunacidRegion.temple_of_silence_interior: lambda state: self.has_light_source(state) and
                                                                    self.has_key_to_switch(state, Switch.temple_switch, self.world.options),
            LunacidRegion.temple_of_silence_secret: lambda state: self.has_light_source(state) and
                                                                  self.has_key_to_switch(state, Switch.temple_switch, self.world.options) and
                                                                  self.has_crystal_orb(state, self.world.options),
            LunacidRegion.fetid_mire_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidRegion.forest_canopy: lambda state: self.has_keys_for_canopy(state, self.world.options),
            LunacidRegion.throne_chamber: lambda state: state.has(Progressives.vampiric_symbol, self.player, 3),
            LunacidRegion.castle_le_fanu_white: lambda state: state.has(Progressives.vampiric_symbol, self.player, 1),
            LunacidRegion.castle_le_fanu_blue: lambda state: state.has(Progressives.vampiric_symbol, self.player, 2),
            LunacidRegion.chamber_of_fate: lambda state: state.has_all({UniqueItem.earth_talisman, UniqueItem.water_talisman}, self.player),
            LunacidRegion.sealed_ballroom: lambda state: self.can_reach_region(LunacidRegion.castle_le_fanu, state) and (self.has_ranged_element_access(
                [Elements.dark, Elements.dark_and_fire, Elements.dark_and_light, Elements.poison, Elements.ice_and_poison], state) or
                        (self.has_element_access([Elements.dark, Elements.dark_and_fire, Elements.dark_and_light, Elements.poison, Elements.ice_and_poison], state) and
                         state.has(Spell.rock_bridge, self.player))),
            LunacidRegion.sealed_ballroom_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidRegion.vampire_tomb: lambda state: self.has_element_access([Elements.light, Elements.dark_and_light], state),
            LunacidRegion.mausoleum: lambda state: self.has_element_access([Elements.light, Elements.dark_and_light], state),
            LunacidRegion.sand_temple: lambda state: self.has_all_keys_to_switch(state,
                                                                                 [Switch.grotto_valve_switch_1, Switch.grotto_valve_switch_2],
                                                                                 self.world.options),
            LunacidRegion.forlorn_arena: lambda state: self.has_key_to_switch(state, Switch.prison_arena_switch, self.world.options)
                                                       and state.has(UniqueItem.terminus_prison_key, self.player),
            LunacidRegion.terminus_prison_dark: lambda state: self.has_key_to_switch(state, Switch.prison_shortcut_switch, self.world.options) or
                                                              state.has(Spell.icarian_flight, self.player),
            LunacidRegion.terminus_prison_upstairs: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
        }

        self.entrance_rules = {
            LunacidEntrance.archives_to_chasm: lambda state: state.has(Progressives.vampiric_symbol, self.player, 2) and
                                                             state.has(Spell.icarian_flight, self.player),
            LunacidEntrance.wings_to_surface: lambda state: state.has_all({Spell.icarian_flight, Spell.spirit_warp}, self.player) or
                                                            (state.has(Spell.icarian_flight, self.player) and self.can_reach_region(
                                                                state, LunacidRegion.temple_of_silence_interior)),
            LunacidEntrance.basin_to_surface: lambda state: state.has_all({Spell.icarian_flight, Spell.spirit_warp}, self.player) or
                                                            (state.has(Spell.icarian_flight, self.player) and state.can_reach(
                                                                LunacidRegion.temple_of_silence_interior, None, self.player)),
            LunacidEntrance.yosei_to_yosei_lower: lambda state: self.can_jump_high(state) or self.has_blood_spell_access(state),
            LunacidEntrance.castle_to_red: self.has_blood_spell_access,
            LunacidEntrance.archives_3_to_archives_1b: lambda state: self.has_key_to_switch(state, Switch.archives_elevator_switch_1_to_3, self.world.options)
                                                                     or self.can_jump_high(state),
            LunacidEntrance.archives_2_to_archives_3: lambda state: self.has_key_to_switch(state, Switch.archives_elevator_switch_2_to_3, self.world.options)
                                                                    or self.can_jump_high(state),
            LunacidEntrance.throne_to_prison: lambda state: state.has("Defeat Prince Crilall Fanu", self.player),
        }

        self.location_rules = {
            "Throne of Prince Crilall Fanu": lambda state: state.can_reach(LunacidEntrance.white_to_throne, "Entrance", self.player),
            BaseLocation.wings_rest_demi_orb: lambda state: self.can_reach_region(state, LunacidRegion.grave_of_the_sleeper),
            BaseLocation.temple_blood_altar: self.has_blood_spell_access,
            BaseLocation.hollow_basin_dark_item: lambda state: state.has(UniqueItem.enchanted_key, self.player),
            BaseLocation.temple_sewer_puzzle: lambda state: state.has(UniqueItem.vhs_tape, self.player) and self.can_reach_region(state,
                                                                                                                                  LunacidRegion.vampire_tomb) and
                                                            self.has_crystal_orb(state, self.world.options),
            BaseLocation.archives_strange_corpse: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.archives_hidden_room_lower: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.archives_hidden_room_upper: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.archives_daedalus_one: lambda state: state.has(UniqueItem.black_book, self.player),
            BaseLocation.archives_daedalus_two: lambda state: state.has(UniqueItem.black_book, self.player, 2),
            BaseLocation.archives_daedalus_third: lambda state: state.has(UniqueItem.black_book, self.player, 3),
            BaseLocation.sea_pillar: lambda state: state.has_any({Spell.icarian_flight, Spell.rock_bridge}, self.player),
            BaseLocation.tomb_demi_chest: self.can_jump_high,
            BaseLocation.chasm_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.tomb_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.tomb_hidden_room: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.catacombs_hidden_room: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.mausoleum_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.mausoleum_upper_table: self.can_jump_high,
            BaseLocation.mausoleum_kill_death: lambda state: state.has_all({Alchemy.fractured_life, Alchemy.fractured_death, Alchemy.broken_sword},
                                                                           self.player),
            BaseLocation.corrupted_room: lambda state: state.has(UniqueItem.corrupted_key, self.player),
            BaseLocation.yosei_hanging_in_trees: lambda state: state.has_any(ranged_weapons, self.player),
            BaseLocation.yosei_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.castle_hidden_cell: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.castle_upper_floor_coffin_double: lambda state: state.has(Progressives.vampiric_symbol, self.player, 3) and
                                                                         self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f3_bottomless_pit: lambda state: state.has_any({Spell.icarian_flight, Spell.spirit_warp}, self.player),
            BaseLocation.grotto_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.grotto_triple_secret_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.sand_hidden_sarcophagus: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.sand_second_floor_snake: lambda state: self.has_crystal_orb(state, self.world.options) or self.can_jump_high(state),
            BaseLocation.sand_chest_overlooking_crypt: self.can_jump_high,
            BaseLocation.arena_earth_hidden_room: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_earth_hidden_plant_haven: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_water_hidden_alcove_before: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_water_hidden_alcove_right: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_water_hidden_alcove_left: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_water_hidden_basement_left: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_water_hidden_basement_right: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_water_hidden_laser_room: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_water_underwater_temple: lambda state: state.has_any({Spell.icarian_flight, Spell.rock_bridge}, self.player) and
                                                                      self.has_crystal_orb(state, self.world.options),
            BaseLocation.arena_earth_earthen_temple: lambda state: self.can_jump_high(state) and self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_b2_egg_resting_place: lambda state: state.has(UniqueItem.skeleton_egg, self.player),
            BaseLocation.prison_f1_hidden_cell: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f1_hidden_debris_room: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f4_hidden_beds: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f4_maledictus_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f3_locked_left: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            BaseLocation.prison_f3_locked_right: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            BaseLocation.prison_f3_locked_south: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            "Free Sir Hicket": lambda state: state.has(Spell.ignis_calor, self.player),
            BaseLocation.castle_cell_center: lambda state: self.has_element_access(Elements.fire, state),
            BaseLocation.ash_path_maze: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.ash_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            ShopLocation.buy_steel_needle: lambda state: self.can_reach_region(state, LunacidRegion.sanguine_sea),  # Push out of sphere 0
            ShopLocation.buy_crossbow: lambda state: self.can_reach_region(state, LunacidRegion.sanguine_sea),  # Push out of sphere 0
            ShopLocation.buy_rapier: lambda state: self.can_reach_region(state, LunacidRegion.sanguine_sea),  # Push out of sphere 0
            ShopLocation.buy_ocean_elixir_sheryl: lambda state: self.can_purchase_item(state, self.world.options),
            ShopLocation.buy_privateer_musket: lambda state: self.can_purchase_item(state, self.world.options),
            ShopLocation.buy_oil_lantern: lambda state: self.can_purchase_item(state, self.world.options),
            ShopLocation.buy_jotunn_slayer: lambda state: self.can_reach_location(state, BaseLocation.fate_lucid_blade),
            DropLocation.sucsarian_drop_1: lambda state: self.can_reach_region(state, LunacidRegion.forlorn_arena),
            DropLocation.sucsarian_drop_2: lambda state: self.can_reach_region(state, LunacidRegion.forlorn_arena),
            DropLocation.jailor_drop: lambda state: self.can_reach_region(state, LunacidRegion.terminus_prison) and
                                                    state.has(UniqueItem.terminus_prison_key, self.player),
            DropLocation.cetea_drop: lambda state: self.can_reach_region(state, LunacidRegion.labyrinth_of_ash),
            DropLocation.vampire_drop: lambda state: self.can_reach_any_region(state, [LunacidRegion.castle_le_fanu_red,
                                                                                       LunacidRegion.castle_le_fanu_white]),
            DropLocation.horse_drop: lambda state: self.can_reach_region(state, LunacidRegion.sealed_ballroom),
            DropLocation.anpu_drop_1: lambda state: self.can_reach_region(state, LunacidRegion.sand_temple),
            DropLocation.anpu_drop_2: lambda state: self.can_reach_region(state, LunacidRegion.sand_temple),
            DropLocation.obsidian_skeleton_drop_1: lambda state: self.can_reach_any_region(state, [LunacidRegion.boiling_grotto,
                                                                                                   LunacidRegion.terminus_prison_dark]),
            DropLocation.obsidian_skeleton_drop_2: lambda state: self.can_reach_any_region(state, [LunacidRegion.boiling_grotto,
                                                                                                   LunacidRegion.terminus_prison_dark]),
            DropLocation.phantom_drop: lambda state: self.can_reach_any_region(state, [LunacidRegion.mausoleum, LunacidRegion.castle_le_fanu]),
            DropLocation.chimera_drop: lambda state: self.can_reach_any_region(state, [LunacidRegion.forbidden_archives_3,
                                                                                       LunacidRegion.forbidden_archives_1b]),
            DropLocation.skeleton_spell_drop: lambda state: self.can_reach_any_region(state, [LunacidRegion.fetid_mire, LunacidRegion.boiling_grotto,
                                                                                              LunacidRegion.terminus_prison_dark]),
            DropLocation.skeleton_weapon_drop: lambda state: self.can_reach_any_region(state, [LunacidRegion.fetid_mire, LunacidRegion.boiling_grotto,
                                                                                               LunacidRegion.terminus_prison_dark]),
            DropLocation.kodama_drop: lambda state: self.can_reach_region(state, LunacidRegion.yosei_forest),
            DropLocation.mummy_drop: lambda state: self.can_reach_region(state, LunacidRegion.temple_of_silence_interior),
            DropLocation.sea_demon: lambda state: self.can_reach_any_region(state, [LunacidRegion.sanguine_sea, LunacidRegion.mausoleum]),
            DropLocation.snail_drop: lambda state: self.can_reach_region(state, LunacidRegion.hollow_basin),
            DropLocation.milk_snail_drop: lambda state: self.can_reach_region(state, LunacidRegion.hollow_basin),
        }

    def can_reach_region(self, state: CollectionState, spot: str):
        return state.can_reach(spot, "Region", self.player)

    def can_reach_any_region(self, state: CollectionState, spots: List[str]):
        any_rule = False
        for spot in spots:
            any_rule = any_rule or self.can_reach_region(state, spot)
        return any_rule

    def can_reach_all_regions(self, state: CollectionState, spots: List[str]):
        all_rule = True
        for spot in spots:
            all_rule = all_rule and self.can_reach_region(state, spot)
        return all_rule

    def can_reach_location(self, state: CollectionState, spot: str):
        return state.can_reach(spot, "Location", self.player)

    def can_jump_high(self, state: CollectionState) -> bool:
        return state.has_any(jump_spells, self.player)

    def has_light_source(self, state: CollectionState) -> bool:
        sources = []
        sources.extend(source for source in spell_light_sources)
        sources.extend(source for source in weapon_light_sources)
        sources.extend(source for source in item_light_sources)
        return state.has_any(sources, self.player)

    def has_spell(self, spell: str, state: CollectionState):
        return state.has(spell, self.player)

    def has_all_spells(self, spells: List[str], state: CollectionState):
        return state.has_all(spells, self.player)

    def has_every_spell(self, state: CollectionState, options: LunacidOptions, starting_weapon: str = None) -> bool:
        every_spell = list(set.union(set(base_spells), set(drop_spells)))
        if starting_weapon is not None and starting_weapon in every_spell:
            every_spell.remove(starting_weapon)
        mob_spell_regions = [LunacidRegion.forlorn_arena, LunacidRegion.castle_le_fanu_red, LunacidRegion.castle_le_fanu_white,
                             LunacidRegion.terminus_prison_dark,
                             LunacidRegion.labyrinth_of_ash, LunacidRegion.boiling_grotto, LunacidRegion.forbidden_archives_3, LunacidRegion.sand_temple,
                             LunacidRegion.temple_of_silence_interior, LunacidRegion.sealed_ballroom]
        if options.dropsanity == options.dropsanity.option_false:
            every_spell = base_spells
            return self.has_all_spells(every_spell, state) & self.can_reach_all_regions(state, mob_spell_regions)
        else:
            return self.has_all_spells(every_spell, state)

    def can_purchase_item(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.shopsanity == options.shopsanity.option_false:
            return True
        return state.has("Sir Hicket's Freedom from Armor", self.player)

    def has_blood_spell_access(self, state: CollectionState) -> bool:
        return state.has_any(blood_spells, self.player)

    def has_keys_for_basin_door(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.shopsanity == options.shopsanity.option_false:
            return True
        return state.has(UniqueItem.enchanted_key, self.player)

    def has_keys_for_canopy(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.shopsanity == options.shopsanity.option_false:
            return state.has(UniqueItem.enchanted_key, self.player)
        return state.has(UniqueItem.enchanted_key, self.player, 2)

    def has_key_to_switch(self, state: CollectionState, key: str, options: LunacidOptions) -> bool:
        if options.switch_locks == options.switch_locks.option_false:
            return True
        return state.has(key, self.player)

    def has_all_keys_to_switch(self, state: CollectionState, keys: List[str], options: LunacidOptions) -> bool:
        rule = True
        for key in keys:
            rule = rule and self.has_key_to_switch(state, key, options)
        return rule

    def has_crystal_orb(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.secret_door_lock == options.secret_door_lock.option_false:
            return True
        return state.has(UniqueItem.dusty_crystal_orb, self.player)

    def has_element_access(self, element: str | List[str], state: CollectionState):
        if isinstance(element, str):
            element = [element]
        element_options = [item for item in self.elements if self.elements[item] in element]
        return state.has_any(element_options, self.player)

    def has_ranged_element_access(self, element: str | List[str], state: CollectionState):
        if isinstance(element, str):
            element = [element]
        ranged_options = [item for item in ranged_weapons]
        ranged_options.extend([item for item in ranged_spells])
        element_options = [item for item in self.elements if self.elements[item] in element and item in ranged_options]
        return state.has_any(element_options, self.player)

    def set_lunacid_rules(self, world_elements: Dict[str, str]) -> None:
        multiworld = self.world.multiworld
        self.elements = world_elements
        for region in multiworld.get_regions(self.player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
            for entrance in region.entrances:
                if entrance.name in self.entrance_rules:
                    entrance.access_rule = entrance.access_rule and self.entrance_rules[entrance.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]
