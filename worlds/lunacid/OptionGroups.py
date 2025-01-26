from Options import DeathLink, ProgressionBalancing, Accessibility, OptionGroup
from .Options import (Ending, Class, EntranceRandomization, Experience, WeaponExperience, RandomElements, RequiredStrangeCoins, TotalStrangeCoins,
                      Shopsanity, Dropsanity, Quenchsanity, EtnasPupil, NormalizedDrops, SecretDoorLock, SwitchLocks, DoorLocks,
                      TrapPercent, ItemColors, CustomClass, Filler, Traps)

lunacid_option_groups = [
    OptionGroup("General", [
        Ending,
        Class,
        RandomElements,
        EntranceRandomization,
        RequiredStrangeCoins,
        TotalStrangeCoins
    ]),
    OptionGroup("Extra Shuffling", [
        Shopsanity,
        Dropsanity,
        Quenchsanity,
        EtnasPupil,
    ]),
    OptionGroup("Locks", [
        DoorLocks,
        SwitchLocks,
        SecretDoorLock
    ]),
    OptionGroup("Tweaks", [
        Experience,
        WeaponExperience,
        NormalizedDrops,
        Filler,
        Traps,
        TrapPercent
    ]),
    OptionGroup("Advanced Options", [
        ItemColors,
        CustomClass,
        DeathLink,
        ProgressionBalancing,
        Accessibility,
    ])
]
