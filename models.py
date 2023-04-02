from dataclasses import dataclass
import pandas as pd

@dataclass
class Player:
    name: str
    realm: str
    fort_keys: dict
    tyrrannical_keys: dict