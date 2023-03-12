from typing import Set, List

from worlds.stardew_valley.game_item import FishItem

spring = {"Spring"}
summer = {"Summer"}
fall = {"Fall"}
winter = {"Winter"}
spring_summer = {*spring, *summer}
spring_fall = {*spring, *fall}
spring_winter = {*spring, *winter}
summer_fall = {*summer, *fall}
summer_winter = {*summer, *winter}
fall_winter = {*fall, *winter}
spring_summer_fall = {*spring, *summer, *fall}
spring_summer_winter = {*spring, *summer, *winter}
spring_fall_winter = {*spring, *fall, *winter}
all_seasons = {*spring, *summer, *fall, *winter}

town = {"Town"}
beach = {"Beach"}
mountain = {"Mountain"}
forest = {"Forest"}
secret_woods = {"Secret Woods"}
desert = {"The Desert"}
mines_20 = {"The Mines - Floor 20"}
mines_60 = {"The Mines - Floor 60"}
mines_100 = {"The Mines - Floor 100"}
sewers = {"Sewers"}
mutant_bug_lair = {"Mutant Bug Lair"}
witch_swamp = {"Witch's Swamp"}
ginger_island = {"Ginger Island"}
ginger_island_ocean = {*ginger_island}
ginger_island_river = {*ginger_island}
pirate_cove = {*ginger_island}
night_market = {*beach}
lakes = {*mountain, *secret_woods, *sewers}
ocean = {*beach}
rivers = {*town, *forest}
rivers_secret_woods = {*rivers, *secret_woods}
forest_mountain = {*forest, *mountain}
rivers_mountain_lake = {*town, *forest, *mountain}
mines_20_60 = {*mines_20, *mines_60}

crimson_badlands = {"Crimson Badlands"}
shearwater = {"Shearwater Bridge"}
highlands = {"Highlands"}
sprite_spring = {"Sprite Spring"}
fable_reef = {"Fable Reef"}
vineyard = {"Blue Moon Vineyard"}


all_fish_items: List[FishItem] = []


def fish(name: str, item_id: int, locations: Set[str], seasons: Set[str], difficulty: int, mod_name: str) -> FishItem:
    fish_item = FishItem(name, item_id, frozenset(locations), frozenset(seasons), difficulty, mod_name)
    all_fish_items.append(fish_item)
    return fish_item


carp = fish("Carp", 142, lakes, all_seasons, 15, "Vanilla")
herring = fish("Herring", 147, ocean, spring_winter, 25, "Vanilla")
smallmouth_bass = fish("Smallmouth Bass", 137, rivers, spring_fall, 28, "Vanilla")
anchovy = fish("Anchovy", 129, ocean, spring_fall, 30, "Vanilla")
sardine = fish("Sardine", 131, ocean, spring_fall_winter, 30, "Vanilla")
sunfish = fish("Sunfish", 145, rivers, spring_summer, 30, "Vanilla")
perch = fish("Perch", 141, rivers_mountain_lake, winter, 35, "Vanilla")
chub = fish("Chub", 702, forest_mountain, all_seasons, 35, "Vanilla")
bream = fish("Bream", 132, rivers, all_seasons, 35, "Vanilla")
red_snapper = fish("Red Snapper", 150, ocean, summer_fall, 40, "Vanilla")
sea_cucumber = fish("Sea Cucumber", 154, ocean, fall_winter, 40, "Vanilla")
rainbow_trout = fish("Rainbow Trout", 138, rivers_mountain_lake, summer, 45, "Vanilla")
walleye = fish("Walleye", 140, rivers_mountain_lake, fall, 45, "Vanilla")
shad = fish("Shad", 706, rivers, spring_summer_fall, 45, "Vanilla")
bullhead = fish("Bullhead", 700, mountain, all_seasons, 46, "Vanilla")
largemouth_bass = fish("Largemouth Bass", 136, mountain, all_seasons, 50, "Vanilla")
salmon = fish("Salmon", 139, rivers, fall, 50, "Vanilla")
ghostfish = fish("Ghostfish", 156, mines_20_60, all_seasons, 50, "Vanilla")
tilapia = fish("Tilapia", 701, ocean, summer_fall, 50, "Vanilla")
woodskip = fish("Woodskip", 734, secret_woods, all_seasons, 50, "Vanilla")
flounder = fish("Flounder", 267, ocean, spring_summer, 50, "Vanilla")
halibut = fish("Halibut", 708, ocean, spring_summer_winter, 50, "Vanilla")
lionfish = fish("Lionfish", 837, ginger_island_ocean, all_seasons, 50, "Vanilla")
slimejack = fish("Slimejack", 796, mutant_bug_lair, all_seasons, 55, "Vanilla")
midnight_carp = fish("Midnight Carp", 269, forest_mountain, fall_winter, 55, "Vanilla")
red_mullet = fish("Red Mullet", 146, ocean, summer_winter, 55, "Vanilla")
pike = fish("Pike", 144, rivers, summer_winter, 60, "Vanilla")
tiger_trout = fish("Tiger Trout", 699, rivers, fall_winter, 60, "Vanilla")
blue_discus = fish("Blue Discus", 838, ginger_island_river, all_seasons, 60, "Vanilla")
albacore = fish("Albacore", 705, ocean, fall_winter, 60, "Vanilla")
sandfish = fish("Sandfish", 164, desert, all_seasons, 65, "Vanilla")
stonefish = fish("Stonefish", 158, mines_20, all_seasons, 65, "Vanilla")
tuna = fish("Tuna", 130, ocean, summer_winter, 70, "Vanilla")
eel = fish("Eel", 148, ocean, spring_fall, 70, "Vanilla")
catfish = fish("Catfish", 143, rivers_secret_woods, spring_fall, 75, "Vanilla")
squid = fish("Squid", 151, ocean, winter, 75, "Vanilla")
sturgeon = fish("Sturgeon", 698, mountain, summer_winter, 78, "Vanilla")
dorado = fish("Dorado", 704, forest, summer, 78, "Vanilla")
pufferfish = fish("Pufferfish", 128, ocean, summer, 80, "Vanilla")
void_salmon = fish("Void Salmon", 795, witch_swamp, all_seasons, 80, "Vanilla")
super_cucumber = fish("Super Cucumber", 155, ocean, summer_fall, 80, "Vanilla")
stingray = fish("Stingray", 836, pirate_cove, all_seasons, 80, "Vanilla")
ice_pip = fish("Ice Pip", 161, mines_60, all_seasons, 85, "Vanilla")
lingcod = fish("Lingcod", 707, rivers_mountain_lake, winter, 85, "Vanilla")
scorpion_carp = fish("Scorpion Carp", 165, desert, all_seasons, 90, "Vanilla")
lava_eel = fish("Lava Eel", 162, mines_100, all_seasons, 90, "Vanilla")
octopus = fish("Octopus", 149, ocean, summer, 95, "Vanilla")

midnight_squid = fish("Midnight Squid", 798, night_market, winter, 55, "Vanilla")
spook_fish = fish("Spook Fish", 799, night_market, winter, 60, "Vanilla")
blob_fish = fish("Blobfish", 800, night_market, winter, 75, "Vanilla")

crimsonfish = fish("Crimsonfish", 159, ocean, summer, 95, "Vanilla")
angler = fish("Angler", 160, town, fall, 85, "Vanilla")
legend = fish("Legend", 163, mountain, spring, 110, "Vanilla")
glacierfish = fish("Glacierfish", 775, forest, winter, 100, "Vanilla")
mutant_carp = fish("Mutant Carp", 682, sewers, all_seasons, 80, "Vanilla")

baby_lunaloo = fish("Baby Lunaloo", 3006, ginger_island, all_seasons, 15, "Stardew Valley Expanded")
bonefish = fish("Bonefish", 3013, crimson_badlands, all_seasons, 70, "Stardew Valley Expanded")
bull_trout = fish("Bull Trout", 3014, forest, summer, 45, "Stardew Valley Expanded")
butterfish = fish("Butterfish", 3015, shearwater, summer, 75, "Stardew Valley Expanded")
clownfish = fish("Clownfish", 3016, ginger_island, all_seasons, 45, "Stardew Valley Expanded")
daggerfish = fish("Daggerfish", 3017, highlands, all_seasons, 50, "Stardew Valley Expanded")
frog = fish("Frog", 3023, mountain, spring, 70, "Stardew Valley Expanded")
gemfish = fish("Gemfish", 3027, highlands, all_seasons, 100, "Stardew Valley Expanded")
goldenfish = fish("Goldenfish", 3031, sprite_spring, all_seasons, 60, "Stardew Valley Expanded")
grass_carp = fish("Grass Carp", 3034, secret_woods, spring, 85, "Stardew Valley Expanded")
king_salmon = fish("King Salmon", 3044, forest, spring, 80, "Stardew Valley Expanded")
kittyfish = fish("Kittyfish", 3045, shearwater, fall, 85, "Stardew Valley Expanded")
lunaloo = fish("Lunaloo", 3049, ginger_island, all_seasons, 70, "Stardew Valley Expanded")
meteor_carp = fish("Meteor Carp", 3051, sprite_spring, all_seasons, 80, "Stardew Valley Expanded")
minnow = fish("Minnow", 3052, town, all_seasons, 1, "Stardew Valley Expanded")
puppyfish = fish("Puppyfish", 3061, shearwater, spring, 85, "Stardew Valley Expanded")
radioactive_bass = fish("Radioactive Bass", 3062, sewers, all_seasons, 90, "Stardew Valley Expanded")
seahorse = fish("Seahorse", 3068, ginger_island, all_seasons, 25, "Stardew Valley Expanded")
shiny_lunaloo = fish("Shiny Lunaloo", 3070, ginger_island, all_seasons, 110, "Stardew Valley Expanded")
snatcher_worm = fish("Snatcher Worm", 3075, mutant_bug_lair, all_seasons, 75, "Stardew Valley Expanded")
starfish = fish("Starfish", 3079, ginger_island, all_seasons, 75, "Stardew Valley Expanded")
torpedo_trout = fish("Torpedo Trout", 3084, fable_reef, all_seasons, 70, "Stardew Valley Expanded")
undeadfish = fish("Undeadfish", 3085, crimson_badlands, all_seasons, 80, "Stardew Valley Expanded")
void_eel = fish("Void Eel", 3087, witch_swamp, all_seasons, 100, "Stardew Valley Expanded")
water_grub = fish("Water Grub", 3094, mutant_bug_lair, all_seasons, 60, "Stardew Valley Expanded")
sea_sponge = fish("Sea Sponge", 3067, ginger_island, all_seasons, 40, "Stardew Valley Expanded")
dulse_seaweed = fish("Dulse Seaweed", 3020, vineyard, all_seasons, 50, "Stardew Valley Expanded")



crayfish = fish("Crayfish", 716, rivers, all_seasons, -1, "Vanilla")
snail = fish("Snail", 721, rivers, all_seasons, -1, "Vanilla")
periwinkle = fish("Periwinkle", 722, rivers, all_seasons, -1, "Vanilla")
lobster = fish("Lobster", 715, ocean, all_seasons, -1, "Vanilla")
clam = fish("Clam", 372, ocean, all_seasons, -1, "Vanilla")
crab = fish("Crab", 717, ocean, all_seasons, -1, "Vanilla")
cockle = fish("Cockle", 718, ocean, all_seasons, -1, "Vanilla")
mussel = fish("Mussel", 719, ocean, all_seasons, -1, "Vanilla")
shrimp = fish("Shrimp", 720, ocean, all_seasons, -1, "Vanilla")
oyster = fish("Oyster", 723, ocean, all_seasons, -1, "Vanilla")

legendary_fish = {crimsonfish, angler, legend, glacierfish, mutant_carp}
special_fish = {*legendary_fish, blob_fish, lava_eel, octopus, scorpion_carp, ice_pip, super_cucumber, dorado}

all_fish_items_by_name = {fish.name: fish for fish in all_fish_items}
all_fish_items_by_id = {fish.item_id: fish for fish in all_fish_items}
