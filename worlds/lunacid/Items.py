from random import Random
import logging

from BaseClasses import ItemClassification, Item
from typing import Dict, List, Union, Protocol

from . import Weapon
from .Options import LunacidOptions
from .data.item_data import all_items, LunacidItemData, base_unique_items, starting_weapon, shop_starting_weapons, drop_starting_weapons, \
    base_special_item_counts, shop_unique_items, shop_item_count, all_item_data_by_name, quench_starting_weapons
from .data.weapon_info import all_weapons, ranged_weapons, all_weapon_info_by_name
from .data.spell_info import all_spells, ranged_spells, all_spell_info_by_name
from .strings.items import UniqueItem, Coins, Door, Voucher, Switch, Trap
from .strings.properties import Elements, Types
from .strings.spells import Spell, MobSpell

logger = logging.getLogger(__name__)


class LunacidItemFactory(Protocol):
    def __call__(self, name: Union[str, LunacidItemData], override_classification: ItemClassification = None) -> Item:
        raise NotImplementedError


def initialize_items_by_name() -> List[LunacidItemData]:
    items = []
    for item in all_items:
        items.append(item)
    return items


item_table = initialize_items_by_name()
complete_items_by_name = {item.name: item for item in item_table}
all_items_by_element = {weapon: all_weapon_info_by_name[weapon].element for weapon in all_weapon_info_by_name }
for spell in all_spell_info_by_name:
    all_items_by_element[spell] = all_spell_info_by_name[spell].element


def determine_weapon_elements(options: LunacidOptions, random: Random) -> Dict[str, str]:
    elements = {}
    if options.random_elements == options.random_elements.option_false:
        for weapon in all_weapon_info_by_name:
            elements[weapon] = all_weapon_info_by_name[weapon].element
        for spell in all_spell_info_by_name:
            elements[spell] = all_spell_info_by_name[spell].element
        return elements
    excluded_list = [item.name for item in all_spells if item.style == Types.support or item.element == Elements.ignore]

    weapons = [weapon for weapon in all_weapons if weapon.name not in excluded_list]
    spells = [item.name for item in all_spells if item.name not in excluded_list]
    for item in weapons:
        if item.style == Types.melee:
            elements[item.name] = random.choice(Elements.all_elements)
        else:
            elements[item.name] = random.choice(Elements.spell_elements)
    for item in spells:
        elements[item] = random.choice(Elements.spell_elements)
    for item in excluded_list:
        elements[item] = all_items_by_element[item]
    return elements


def create_items(item_factory: LunacidItemFactory, locations_count: int, items_to_exclude: List[Item], weapon_elements: Dict[str, str], is_christmas: bool,
                 options: LunacidOptions, random: Random) -> (List[Item], Item):
    items = []
    lunacid_items = create_lunacid_items(item_factory, weapon_elements, is_christmas, options)
    for item in items_to_exclude:
        if item in lunacid_items:
            lunacid_items.remove(item)
    assert len(
        lunacid_items) <= locations_count, f"There should be at least as many locations [{locations_count}] as there are mandatory items [{len(lunacid_items)}]"
    items += lunacid_items
    chosen_weapon = determine_starting_weapon(random, options)
    if weapon_elements[chosen_weapon] in [Elements.light, Elements.fire, Elements.dark_and_fire, Elements.normal_and_fire, Elements.dark_and_light]:
        starting_weapon_choice = item_factory(chosen_weapon, ItemClassification.progression)
    elif weapon_elements[chosen_weapon] in [Elements.poison, Elements.ice_and_poison] and chosen_weapon in ranged_weapons or chosen_weapon in ranged_spells:
        starting_weapon_choice = item_factory(chosen_weapon, ItemClassification.progression)
    else:
        starting_weapon_choice = item_factory(chosen_weapon)
    for item in items:
        if item.name == starting_weapon_choice.name:
            items.remove(item)
            break
    logger.debug(f"Created {len(lunacid_items)} unique items")
    filler_slots = locations_count - len(items)
    create_filler(item_factory, options, random, filler_slots, is_christmas, items)

    return items, starting_weapon_choice


def create_lunacid_items(item_factory: LunacidItemFactory, weapon_elements: Dict[str, str], is_christmas: bool, options: LunacidOptions) -> List[Item]:
    items = []
    create_weapons(item_factory, weapon_elements, options, items)
    create_spells(item_factory, weapon_elements, is_christmas, options, items)
    create_special_items(item_factory, options, items)
    create_switch_items(item_factory, options, items)
    create_door_items(item_factory, options, items)
    return items


def create_weapons(item_factory: LunacidItemFactory, equipment_by_elements: Dict[str, str], options: LunacidOptions, items: List[Item]) -> List[Item]:
    for item in Weapon.base_weapons:
        if item == Weapon.moonlight and "Tower of Abyss" in options.remove_locations:
            continue
        append_item_with_progression_determined_by_element_and_range(item_factory, item, ranged_weapons, options, equipment_by_elements, items)
    if options.shopsanity == options.shopsanity.option_true:
        for item in Weapon.shop_weapons:
            append_item_with_progression_determined_by_element_and_range(item_factory, item, ranged_weapons, options, equipment_by_elements, items)
    if options.dropsanity != options.dropsanity.option_off:
        for item in Weapon.drop_weapons:
            append_item_with_progression_determined_by_element_and_range(item_factory, item, ranged_weapons, options, equipment_by_elements, items)
    if options.quenchsanity == options.quenchsanity.option_true:
        for item in Weapon.quenchsanity_weapons:
            append_item_with_progression_determined_by_element_and_range(item_factory, item, ranged_weapons, options, equipment_by_elements, items)
    if options.etnas_pupil == options.etnas_pupil.option_true:
        append_item_with_progression_determined_by_element_and_range(item_factory, Weapon.limbo, ranged_weapons, options, equipment_by_elements, items)
    return items


def append_item_with_progression_determined_by_element_and_range(item_factory: LunacidItemFactory, item: str, ranged_list: List[str], options: LunacidOptions,
                                                                 equipment_by_elements: Dict[str, str], items: List[Item]):
    if equipment_by_elements[item] in [Elements.light, Elements.fire, Elements.dark_and_fire, Elements.normal_and_fire, Elements.dark_and_light]:
        items.append(item_factory(item, ItemClassification.progression | ItemClassification.useful))
    elif equipment_by_elements[item] in [Elements.poison, Elements.ice_and_poison] and item in ranged_list:
        items.append(item_factory(item, ItemClassification.progression | ItemClassification.useful))
    elif options.quenchsanity == options.quenchsanity.option_true and item in Weapon.quenchable_weapons:
        items.append(item_factory(item, ItemClassification.progression))
    else:
        items.append(item_factory(item))


def create_spells(item_factory: LunacidItemFactory, equipment_by_elements: Dict[str, str], is_christmas: bool, options: LunacidOptions, items: List[Item]) -> List[Item]:
    force_progressive = (options.ending == options.ending.option_ending_e)
    for item in Spell.base_spells:
        if not is_christmas and item == Spell.jingle_bells:
            continue
        if all_spell_info_by_name[item].style == Types.support:
            items.append(item_factory(item, determine_item_classification(item, force_progressive)))
        elif [item] in [Elements.light, Elements.fire, Elements.dark_and_fire, Elements.normal_and_fire, Elements.dark_and_light]:
            items.append(item_factory(item, ItemClassification.progression | ItemClassification.useful))
        elif equipment_by_elements[item] in [Elements.poison, Elements.ice_and_poison] and item in ranged_spells:
            items.append(item_factory(item, ItemClassification.progression | ItemClassification.useful))
        else:
            items.append(item_factory(item, determine_item_classification(item, force_progressive)))
    if options.dropsanity != options.dropsanity.option_off:
        for item in MobSpell.drop_spells:
            if all_spell_info_by_name[item].style == Types.support:
                items.append(item_factory(item, determine_item_classification(item, force_progressive)))
            elif equipment_by_elements[item] in [Elements.light, Elements.fire, Elements.dark_and_fire, Elements.normal_and_fire, Elements.dark_and_light]:
                items.append(item_factory(item, ItemClassification.progression | ItemClassification.useful))
            elif equipment_by_elements[item] in [Elements.poison, Elements.ice_and_poison] and item in ranged_spells:
                items.append(item_factory(item, ItemClassification.progression | ItemClassification.useful))
            else:
                items.append(item_factory(item, determine_item_classification(item, force_progressive)))
    return items


def determine_starting_weapon(random: Random, options: LunacidOptions) -> str:
    starting_selection = starting_weapon
    if options.shopsanity == options.shopsanity.option_true:
        starting_selection += shop_starting_weapons
    if options.dropsanity != options.dropsanity.option_off:
        starting_selection += drop_starting_weapons
    if options.quenchsanity == options.quenchsanity.option_true:
        starting_selection += quench_starting_weapons
    chosen_weapon_name = random.choice(starting_selection)
    return chosen_weapon_name


def determine_item_classification(item: str, progression: bool) -> ItemClassification:
    if progression:
        return ItemClassification.progression | ItemClassification.useful
    else:
        return all_item_data_by_name[item].classification


def create_special_items(item_factory: LunacidItemFactory, options: LunacidOptions, items: List[Item]) -> List[Item]:
    for item in base_unique_items:
        if item == UniqueItem.white_tape and options.ending == options.ending.option_ending_e:
            items.append(item_factory(item, ItemClassification.progression))
            continue
        elif item == UniqueItem.dusty_crystal_orb and options.secret_door_lock == options.secret_door_lock.option_true:
            items.append(item_factory(item, ItemClassification.progression))
            continue
        items.append(item_factory(item))
    for item in base_special_item_counts:
        items.extend(item_factory(special_item) for special_item in [item] * base_special_item_counts[item])
    if "Daedalus" not in options.remove_locations:
        items.extend(item_factory(book) for book in [UniqueItem.black_book] * 2)
    if "Tower of Abyss" not in options.remove_locations:
        items.append(item_factory(UniqueItem.earth_elixir))
        items.append(item_factory(UniqueItem.ocean_elixir))
        items.append(item_factory(UniqueItem.crystal_lantern))
    if options.shopsanity == options.shopsanity.option_true:
        for item in shop_unique_items:
            items.append(item_factory(item))
        for item in shop_item_count:
            items.extend([item_factory(filler) for filler in [item] * shop_item_count[item]])
        for item in Voucher.vouchers:
            items.append(item_factory(item, ItemClassification.progression))
    else:
        for item in Voucher.vouchers:
            items.append(item_factory(item))
    if options.dropsanity != options.dropsanity.option_off:
        items.append(item_factory(UniqueItem.black_book))

    #  if options.movement_items == options.movement_items.option_true:
    #    items.extend(item_factory(jump_item) for jump_item in [Upgrade.jump_power] * 4)
    create_strange_coins(item_factory, options, items)
    return items

def create_strange_coins(item_factory: LunacidItemFactory, options: LunacidOptions, items: List[Item]) -> None:
    if options.ending != options.ending.option_ending_b and options.ending != options.ending.option_any_ending:
        return
    total_coins = max(options.required_strange_coin.value, options.total_strange_coin.value)
    required_coins = options.required_strange_coin.value
    count = 0
    while count < required_coins:
        items.append(item_factory(Coins.strange_coin, ItemClassification.progression))
        count += 1
    count = 0
    while count < total_coins - required_coins:
        items.append(item_factory(Coins.strange_coin, ItemClassification.progression | ItemClassification.useful))
        count += 1


def create_switch_items(item_factory: LunacidItemFactory, options: LunacidOptions, items: List[Item]) -> List[Item]:
    if options.switch_locks == options.switch_locks.option_false:
        return items
    for item in Switch.switches:
        items.append(item_factory(item))
    return items


def create_door_items(item_factory: LunacidItemFactory, options: LunacidOptions, items: List[Item]) -> List[Item]:
    if options.door_locks == options.door_locks.option_false:
        return items
    for key in Door.doors_no_tower:
        items.append(item_factory(key))
    if "Tower of Abyss" not in options.remove_locations:
        items.append(item_factory(Door.tower_key))
    return items


def create_filler(item_factory: LunacidItemFactory, options: LunacidOptions, random: Random, filler_slots: int, is_christmas: bool, items: List[Item]) -> List[Item]:
    if filler_slots == 0:
        return items
    filler_list = [Coins.silver] + list(options.filler.value)
    trap_list = list(options.traps.value)
    if not is_christmas:
        trap_list = [trap for trap in trap_list if trap != Trap.coal or trap != Trap.eggnog]
    trap_percent = options.trap_percent.value / 100
    if not trap_list:
        trap_percent = 0
    filler_count = filler_slots
    if trap_percent != 0:
        trap_count = int(filler_slots * trap_percent)
        filler_count = filler_slots - trap_count
        items.extend([item_factory(filler) for filler in random.choices(trap_list, k=trap_count)])
    items.extend([item_factory(filler) for filler in random.choices(filler_list, k=filler_count)])
    return items


all_filler = [item for item in item_table if item.classification is ItemClassification.filler]
