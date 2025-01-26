class GenericItem:
    blood_wine = "Blood Wine"
    light_urn = "Light Urn"
    cloth_bandage = "Cloth Bandage"
    dark_urn = "Dark Urn"


class Alchemy:
    fire_coral = "Fire Coral"
    fiddlehead = "Fiddlehead"
    ectoplasm = "Ectoplasm"
    snowflake_obsidian = "Snowflake Obsidian"
    moon_petal = "Moon Petal"
    fractured_life = "Fractured Life"
    fractured_death = "Fractured Death"
    broken_sword = "Broken Sword"
    fire_opal = "Fire Opal"
    ashes = "Ashes"
    opal = "Opal"
    yellow_morel = "Yellow Morel"
    lotus_seed_pod = "Lotus Seed Pod"
    obsidian = "Obsidian"
    onyx = "Onyx"
    ocean_bone_shard = "Ocean Bone Shard"
    ocean_bone_shell = "Ocean Bone Shell"
    bloodweed = "Bloodweed"
    ikurrilb_root = "Ikurr'ilb Root"
    destroying_angel_mushroom = "Destroying Angel Mushroom"
    poison_urn = "Poison Urn"
    bones = "Bones"
    vampiric_ashes = "Vampiric Ashes"

    necessary_alchemy_items = [ashes, fire_opal, opal, yellow_morel, lotus_seed_pod, snowflake_obsidian, onyx, obsidian, destroying_angel_mushroom, ocean_bone_shard,
                               ocean_bone_shell, moon_petal, bloodweed, ectoplasm, bones, ikurrilb_root]


class Creation:
    wisp_heart = "Wisp Heart"
    staff_of_osiris = "Staff of Osiris"
    moonlight_vial = "Moonlight Vial"
    spectral_candle = "Spectral Candle"
    health_vial = "Health Vial"
    mana_vial = "Mana Vial"
    fairy_moss = "Fairy Moss"
    crystal_shard = "Crystal Shard"
    poison_throwing_knife = "Poison Throwing Knife"
    throwing_knife = "Throwing Knife"
    holy_water = "Holy Water"
    antidote = "Antidote"
    bomb = "Bomb"
    poison_urn = "Poison Urn"


class UniqueItem:
    white_tape = "White VHS Tape"
    ocean_elixir = "Ocean Elixir"
    earth_elixir = "Earth Elixir"
    black_book = "Black Book"
    enchanted_key = "Enchanted Key"
    vhs_tape = "VHS Tape"
    corrupted_key = "Corrupt Key"
    skull_of_josiah = "Skull of Josiah"
    crystal_lantern = "Crystal Lantern"
    terminus_prison_key = "Terminus Prison Key"
    survey_banner = "Survey Banner"
    water_talisman = "Water Talisman"
    earth_talisman = "Earth Talisman"
    oil_lantern = "Oil Lantern"
    skeleton_egg = "Skeleton Egg"
    dried_rat = "Dried Rat"
    dusty_crystal_orb = "Dusty Crystal Orb"
    skeleton_rattle = "Skeletal Rattle"


class RareDrops:
    angel_feather = "Angel Feather"
    shrimp = "Pink Shrimp"
    fools_gold = "Fool's Gold"


class Progressives:
    vampiric_symbol = "Progressive Vampiric Symbol"


class Coins:
    silver = "Silver"
    strange_coin = "Strange Coin"


class CustomItem:
    experience = "Deep Knowledge"
    bestial_mastery = "Bestial Mastery"


class Trap:
    health_viai = "Health ViaI"
    blindness_trap = "Blindness Trap"
    slowness_trap = "Slowness Trap"
    mana_drain_trap = "Mana Drain Trap"
    xp_drain_trap = "XP Drain Trap"
    curse_trap = "Curse Trap"
    poison_trap = "Poison Trap"
    bleed_trap = "Bleed Trap"
    eggnog = "Eggnog"
    coal = "Coal"

    all_traps = [health_viai, slowness_trap, bleed_trap, curse_trap, blindness_trap, mana_drain_trap,
                 xp_drain_trap, poison_trap
                 ]

    christmas_gifts = [eggnog, coal]


class Switch:
    hollow_basin_switch_near_demi = "Hollow Basin Switch Key"
    temple_switch = "Temple of Silence Switch Key"
    fetid_mire_switch = "Fetid Mire Switch Key"
    tomb_switches = "Accursed Tomb Switch Keyring"
    tomb_light_switches = "Prometheus Fire Switch Keyring"
    archives_switch = "Forbidden Archives Shortcut Switch Key"
    archives_elevator_switches = "Forbidden Archives Elevator Switch Keyring"
    ballroom_switch = "Sealed Ballroom Switch Key"
    grotto_valves_switches = "Grotto Fire Switch Keyring"
    grotto_switches = "Sand Temple Switches Keyring"
    prison_shortcut_switch = "Terminus Prison Back Alley Switch Key"
    prison_arena_switch = "Forlorn Arena Gate Switch Key"
    arena_water_switch = "Temple of Water Switch Key"
    arena_earth_switch = "Temple of Earth Switch Key"
    ash_switch = "Labyrinth of Ash Switch Key"

    switches = [hollow_basin_switch_near_demi, temple_switch, fetid_mire_switch, archives_switch,
                archives_elevator_switches, tomb_switches, tomb_light_switches, ballroom_switch,
                grotto_valves_switches, grotto_switches, prison_shortcut_switch, prison_arena_switch,
                arena_water_switch, arena_earth_switch, ash_switch,
                ]


class Door:
    basin_broken_steps = "Broken Steps Door Key"
    basin_rickety_bridge = "Lower Rickety Bridge Door Key"
    basin_temple_sewers = "Sewers Door Key"
    forest_door_in_trees = "Treetop Door Key"
    forest_patchouli = "Tomb Secret Door Key"
    sea_westward = "Sewers Sea Door Key"
    sea_eastward = "Accursed Door Key"
    sea_double_doors = "Castle Doors Key"
    archives_sealed_door = "Library Exit Door Key"
    chasm_surface_door = "Surface Door Key"
    ballroom_key = "Light Accursed Door Key"
    throne_key = "Queen's Throne Door Key"
    prison_key = "Prison Main Door Key"
    forlorn_key = "Secondary Lock Key"
    burning_key = "Burning Hot Key"
    ash_key = "Forbidden Door Key"
    sucsarian_key = "Sucsarian Key"
    sleeper_key = "Dreamer Key"
    ballroom_rooms_key = "Ballroom Side Rooms Keyring"
    tower_key = "Tower of Abyss Keyring"
    musical_key = "Ashen Doors Keyring"

    doors_no_tower = [basin_temple_sewers, basin_broken_steps, basin_rickety_bridge, chasm_surface_door,
                      ballroom_rooms_key, sleeper_key, sucsarian_key, ash_key, burning_key, forlorn_key,
                      prison_key, ballroom_key, throne_key, archives_sealed_door, sea_double_doors,
                      sea_eastward, sea_westward, forest_patchouli, forest_door_in_trees, musical_key
                      ]

    all_door_keys = [basin_temple_sewers, basin_broken_steps, basin_rickety_bridge, chasm_surface_door,
                     ballroom_rooms_key, sleeper_key, sucsarian_key, ash_key, burning_key, forlorn_key,
                     prison_key, ballroom_key, throne_key, archives_sealed_door, sea_double_doors,
                     sea_eastward, sea_westward, forest_patchouli, forest_door_in_trees, tower_key, musical_key
                     ]


class Upgrade:
    jump_power = "Progressive Jump Power"
    drop_chance = "Text on Great Well Resourcefulness"


class Voucher:
    sheryl_initial_voucher = "Sheryl's Initial Offerings Voucher"
    sheryl_golden_voucher = "Sheryl's Golden Armor Voucher"
    sheryl_dreamer_voucher = "Sheryl's Dreamer Voucher"
    patchouli_simp_discount = "Patchouli's Drink Voucher"

    vouchers = [sheryl_dreamer_voucher, sheryl_initial_voucher, sheryl_golden_voucher, patchouli_simp_discount]
