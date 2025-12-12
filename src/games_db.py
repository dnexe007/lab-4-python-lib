from src.game import Game
from src.game_collection import GameCollection

GAMES_DATABASE = GameCollection([
    #0
    Game("Control", "Remedy Entertainment", 2019, "Action", "CTL_RMD"),
    #1
    Game("Quantum Break", "Remedy Entertainment", 2016, "Action", "QTM_RMD"),
    #2
    Game("Alan Wake 2", "Remedy Entertainment", 2023, "Survival Horror", "AW2_RMD"),

    #3
    Game("Uncharted 4: A Thief's End", "Naughty Dog", 2016, "Action-Adventure", "U4_NDG"),
    #4
    Game("The Last of Us", "Naughty Dog", 2013, "Action-Adventure", "TLOU_ND"),

    #5
    Game("Half-Life 2", "Valve", 2004, "FPS", "HL2_VLV"),
    #6
    Game("Portal 2", "Valve", 2011, "Puzzle", "PRT2_VLV"),

    #7
    Game("The Talos Principle", "Croteam", 2014, "Puzzle", "TLS_CRT"),

    #8
    Game("Metro Exodus", "4A Games", 2019, "FPS", "MTX_4AG"),

    Game("Amnesia: The Bunker", "Frictional Games", 2023, "Survival Horror", "AMB_FRG"),

    Game("Need for Speed: Rivals", "Electronic Arts", 2013, "Racing", "NFS_EA"),

    Game("GRID Legends", "Codemasters", 2022, "Racing", "GRD_CDM"),
])
