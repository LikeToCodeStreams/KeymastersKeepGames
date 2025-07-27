from __future__ import annotations

import functools
from typing import List, Dict, Set

from dataclasses import dataclass

from Options import Toggle, OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms

@dataclass
class PD3ArchipelagoOptions:
    pd3_include_overkill: PD3IncludeOverkill
    pd3_dlc_owned: PD3DLCOwned

class PAYDAY3Game(Game):
    name = "PAYDAY 3"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.XSX
        ]

    is_adult_only_or_unrated = True

    options_cls = PD3ArchipelagoOptions

    #objectives

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat LOUDHEIST on DIFFICULTY in Loud",
                data={
                    "LOUDHEIST": (self.loud_heist, 1),
                    "DIFFICULTY": (self.difficulty, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat STEALTHHEIST on DIFFICULTY in Stealth",
                data={
                    "STEALTHHEIST": (self.stealth_heist, 1),
                    "DIFFICULTY": (self.difficulty, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            
        ]
    
    #datasets

    @property
    def include_overkill(self) -> bool:
        return bool(self.archipelago_options.pd3_include_overkill.value)
    
    @property
    def dlc_owned(self) -> Set[str]:
        return self.archipelago_options.pd3_dlc_owned.value
    
    @property
    def has_syntax_error(self) -> bool:
        return "Syntax Error" in self.dlc_owned

    @property
    def has_boys_in_blue(self) -> bool:
        return "Boys In Blue" in self.dlc_owned

    @property
    def has_houston_breakout(self) -> bool:
        return "Houston Breakout" in self.dlc_owned

    @property
    def has_fear_greed(self) -> bool:
        return "Fear & Greed" in self.dlc_owned
    
    @property
    def has_party_powder(self) -> bool:
        return "Party Powder" in self.dlc_owned


    @functools.cached_property
    def base_difficulty(self) -> List[str]:
        return [
            "Normal",
            "Hard",
            "Very Hard"
        ]
    
    def difficulty(self) -> List[str]:
        difficulty: List[str] = self.base_difficulty[:]

        if self.include_overkill:
            difficulty.append("Overkill")
        
        return sorted(difficulty)
    
    @functools.cached_property
    def loud_heist_base(self) -> List[str]:
        return [
            "No Rest For The Wicked",
            "Road Rage",
            "Dirty Ice",
            "Rock The Cradle",
            "Under The Surphaze",
            "Gold & Sharke",
            "99 Boxes",
            "Touch The Sky",
            "Cook Off",
            "Diamond District",
            "First World Bank",
            "Bank Withdrawal",
            "Search And Seizure"
        ]
    
    def loud_heist(self) -> List[str]:
        loud_heist: List[str] = self.loud_heist_base[:]

        if self.has_syntax_error:
            loud_heist.append("Syntax Error")
        
        if self.has_boys_in_blue:
            loud_heist.append("Boys In Blue")
        
        if self.has_houston_breakout:
            loud_heist.append("Houston Breakout")
        
        if self.has_fear_greed:
            loud_heist.append("Fear & Greed")
        
        if self.has_party_powder:
            loud_heist.append("Party Powder")

        return sorted(loud_heist)

    @functools.cached_property
    def stealth_heist_base(self) -> List[str]:
        return [
            "No Rest For The Wicked",
            "Dirty Ice",
            "Rock The Cradle",
            "Under The Surphaze",
            "Gold & Sharke",
            "99 Boxes",
            "Touch The Sky",
            "Turbid Station",
            "Diamond District",
            "First World Bank",
            "Bank Withdrawal",
            "Search And Seizure"
        ]
    
    def stealth_heist(self) -> List[str]:
        stealth_heist: List[str] = self.stealth_heist_base[:]

        if self.has_syntax_error:
            stealth_heist.append("Syntax Error")
        
        if self.has_boys_in_blue:
            stealth_heist.append("Boys In Blue")
        
        if self.has_houston_breakout:
            stealth_heist.append("Houston Breakout")
        
        if self.has_fear_greed:
            stealth_heist.append("Fear & Greed")
        
        if self.has_party_powder:
            stealth_heist.append("Party Powder")
        
        return sorted(stealth_heist)

    #options

class PD3IncludeOverkill(Toggle):
    """
    If toggled, will add Overkill to the Difficulty pool for Objectives
    """

    display_name = "PAYDAY 3 Include Overkill"

class PD3DLCOwned(OptionSet):
    """
    Adds DLC Heists into the Heist pool for Objectives
    """

    display_name = "PAYDAY 3 DLC Owned"
    valid_keys = [
        "Syntax Error",
        "Boys In Blue",
        "Houston Breakout",
        "Fear & Greed",
        "Party Powder"
    ]

    default = valid_keys