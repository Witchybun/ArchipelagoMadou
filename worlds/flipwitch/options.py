from dataclasses import dataclass

from Options import Toggle, Choice, Range, PerGameCommonOptions


class StartingGender(Choice):
    """Decides the starting gender state."""
    internal_name = "starting_gender"
    display_name = "Starting Gender"
    option_female = 0
    option_male = 1
    default = 0


class ShuffleChaosPieces(Toggle):
    """Shuffles the six Chaos Pieces in your game.
    Off: All pieces are placed in their original locations.
    On: All six Chaos Pieces can be found anywhere in the multiworld.
    If you want to plando these, turn this on first.
    """
    internal_name = "shuffle_chaos_pieces"
    display_name = "Shuffle Chaos Pieces"


class Shopsanity(Toggle):
    """Shuffles all items normally sold in your game. Opens 29 locations."""
    internal_name = "shopsanity"
    display_name = "Shopsanity"
    default = True


class ShopPrices(Range):
    """Sets, as a percentage, the price of all goods in the game."""
    internal_name = "shop_prices"
    display_name = "Shop Prices"
    range_start = 0
    range_end = 200
    default = 100


class StatShuffle(Toggle):
    """Shuffles all Heart and Mana Container upgrades in your game.  Adds 20 locations."""
    internal_name = "stat_shuffle"
    display_name = "Stat Shuffle"
    default = True


class GachaponShuffle(Choice):
    """Shuffles the rewards of the gachapon rewards.
    Off: All gacha coins are placed locally in their coin locations.  Gacha machines give nothing.
    Coins: All gacha coins are shuffled into the multiworld.  Opens 41 locations.
    All: All gacha coins and gacha prizes are shuffled into the multiworld.  Opens 82 locations.
    Note that the gacha machine order is deterministic based on the seed rolled."""
    internal_name = "gachapon_shuffle"
    display_name = "Gachapon Shuffle"
    option_off = 0
    option_coin = 1
    option_all = 2
    default = 1


class QuestForSex(Choice):
    """Shuffles locations relevant to quest and sex experience.
    Off: All quests give no reward, all quest items are vanilla, and all sex experience is tied to the sexual experience.
    Sensei Minimal: Rewards for sex experience are shuffled.  Opens 14 locations.
    Quests: All quests give a reward and all quest items are shuffled but the resulting cutscenes still give sex experience as normal.  Opens 79 locations.
    All: All quests give a reward, and sex experience is included in the multiworld.  Cutscenes do not reward sex experience.  Opens 79 locations."""
    internal_name = "quest_for_sex"
    display_name = "Quest for Sex"
    option_off = 0
    option_sensei = 1
    option_quests = 2
    option_all = 3
    default = 2


class CrystalTeleports(Toggle):
    """Shuffles the crystal teleports other than the starting warp.  Item is obtained by interacting with a teleport panel.
    Chaos Castle cannot be warped to unless you have six chaos key pieces."""
    internal_name = "crystal_teleports"
    display_name = "Crystal Teleports"


class FuckLink(Toggle):
    """When you get fucked, everyone gets fucked (or dies, I suppose). Of course the reverse is true too."""
    display_name = "FuckLink"


@dataclass
class FlipwitchOptions(PerGameCommonOptions):
    starting_gender: StartingGender
    shuffle_chaos_pieces: ShuffleChaosPieces
    shopsanity: Shopsanity
    shop_prices: ShopPrices
    stat_shuffle: StatShuffle
    gachapon_shuffle: GachaponShuffle
    quest_for_sex: QuestForSex
    crystal_teleports: CrystalTeleports
    death_link: FuckLink
