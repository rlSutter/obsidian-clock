"""The Obsidian Clock - game content.  Everything here is compiled by gen.py
into tables the engine interprets; no assembly needed to change the game.

Rules: rule(verb, noun, conds, acts).  noun None = any, NONE = no noun typed.
Command rules: the first whose conditions pass runs, and the command is done.
Auto rules: run after every turn, all that pass."""

NONE = "-"

TITLE_TEXT = [
    "   AN ADVENTURE IN THE RUINS",
    "  OF THE SIERRA DEL HUMO, 1934",
    "",
    "      PRESS ENTER TO BEGIN",
]

INTRO = ("THE RAINS ARE A DAY AWAY. SOMEWHERE IN THESE RUINS LIES THE OBSIDIAN "
         "CLOCK, THE CALENDAR STONE OF A FORGOTTEN PEOPLE. SILAS GRIEVE, A DEALER "
         "IN STOLEN RELICS, IS ALREADY HERE. FIND THE CLOCK FIRST, DR. VANCE -- "
         "AND GET OUT BEFORE THE VALLEY FLOODS. (TYPE HELP FOR HELP.)")

# rooms: key -> (name, description, picture, exits {dir: room})
ROOMS = {
    "airstrip": ("AIRSTRIP",
        "A GRASS STRIP HACKED FROM THE JUNGLE. TEO LEANS ON THE WING OF HIS "
        "BIPLANE, EYEING THE CLOUDS. A SUPPLY CRATE SITS BY THE TAIL. A TRAIL "
        "LEADS NORTH.", "airstrip", {"N": "trail"}),
    "trail": ("JUNGLE TRAIL",
        "A NARROW TRAIL UNDER DRIPPING TREES. THE AIRSTRIP IS SOUTH.",
        "trail", {"S": "airstrip"}),
    "river": ("THE FORD",
        "A BROWN RIVER RUNS OVER A STONY FORD TO THE NORTH. A HUGE CEIBA TREE "
        "GRIPS THE BANK. THE TRAIL RUNS SOUTH.", "river", {"S": "trail", "N": "plaza"}),
    "plaza": ("RUINED PLAZA",
        "A SUNKEN PLAZA OF CRACKED STONE. A CARVED STELA STANDS HERE. STEPS "
        "CLIMB THE GREAT PYRAMID TO THE NORTH. SMOKE RISES TO THE EAST. THE "
        "FORD IS SOUTH.", "plaza", {"N": "summit", "E": "camp", "S": "river"}),
    "camp": ("GRIEVE'S CAMP",
        "A HASTY CAMP: A TENT, A COLD FIRE, A SMASHED CRATE. NOBODY IS HOME. "
        "THE PLAZA IS WEST.", "camp", {"W": "plaza"}),
    "summit": ("PYRAMID SUMMIT",
        "WIND TEARS AT THE TOP OF THE PYRAMID. A SMALL SHRINE STANDS HERE. "
        "THE JUNGLE ROLLS AWAY ON EVERY SIDE. STEPS DESCEND SOUTH.",
        "summit", {"S": "plaza"}),
    "stairs": ("DARK STAIRWAY",
        "STEEP STEPS DROP INTO THE PYRAMID. YOUR LANTERN THROWS LONG SHADOWS. "
        "UP IS DAYLIGHT. DOWN IS NOT.", "stairs", {"U": "summit", "D": "hall"}),
    "hall": ("HALL OF DAYS",
        "A LONG HALL. THREE GLYPHS ARE CARVED IN THE EAST WALL: A SERPENT, A "
        "SUN AND A JAGUAR. THE STAIRS LEAD UP.", "hall", {"U": "stairs"}),
    "chamber": ("CLOCK CHAMBER",
        "A ROUND CHAMBER. A STONE ALTAR STANDS AT ITS HEART. A SHAFT IN THE "
        "CEILING HAS CAVED IN. THE HALL IS WEST.", "chamber", {"W": "hall"}),
}
START = "airstrip"

# objects: key -> dict(nouns, loc, take, list, room=line shown in room,
#                      inv=line in inventory, desc=examine text)
OBJECTS = {
    "journal": dict(nouns=["JOURNAL", "BOOK", "NOTES"], loc="carried", take=True,
        room="YOUR FIELD JOURNAL LIES HERE.", inv="YOUR FIELD JOURNAL",
        desc="YOUR NOTES: THE CLOCK WAS HIDDEN BENEATH THE GREAT PYRAMID. "
             "THE STELA IN THE PLAZA TELLS HOW TO REACH IT."),
    "crate": dict(nouns=["CRATE"], loc="airstrip",
        desc="A WOODEN SUPPLY CRATE. THE LID IS LOOSE."),
    "machete": dict(nouns=["MACHETE", "BLADE", "KNIFE"], loc=None, take=True,
        room="THERE IS A MACHETE HERE.", inv="A MACHETE",
        desc="HEAVY, SHARP AND MADE FOR JUNGLE."),
    "lantern": dict(nouns=["LANTERN", "LAMP"], loc=None, take=True,
        room="THERE IS A LANTERN HERE.", inv="A LANTERN",
        desc="A BRASS STORM LANTERN, FULL OF KEROSENE."),
    "matches": dict(nouns=["MATCHES", "MATCH"], loc=None, take=True,
        room="THERE IS A BOX OF MATCHES HERE.", inv="A BOX OF MATCHES",
        desc="DRY, FOR NOW."),
    "teo": dict(nouns=["TEO", "PILOT"], loc="airstrip",
        desc="TEO HAS FLOWN YOU THROUGH WORSE WEATHER THAN THIS. MOSTLY."),
    "plane": dict(nouns=["PLANE", "BIPLANE"], loc="airstrip",
        desc="A PATCHED BIPLANE. IT HAS NEVER LET YOU DOWN. YET."),
    "vines": dict(nouns=["VINES", "VINE"], loc="trail", list=True,
        room="THICK VINES CHOKE THE WAY NORTH.",
        desc="TOUGH, WET VINES. YOU WILL NEED A BLADE."),
    "tree": dict(nouns=["TREE", "CEIBA"], loc="river",
        desc="AN ANCIENT CEIBA, ITS ROOTS LIKE WALLS. A FINE ANCHOR."),
    "river": dict(nouns=["RIVER", "FORD", "WATER"], loc="river",
        desc="KNEE-DEEP AND FAST. IT WILL BE WORSE WHEN THE RAINS COME."),
    "ropeline": dict(nouns=["ROPE"], loc=None, list=True,
        room="A ROPE IS STRUNG ACROSS THE FORD FROM THE CEIBA.",
        desc="TIED FAST. IT SHOULD HOLD."),
    "ropestela": dict(nouns=["ROPE"], loc=None, list=True,
        room="A ROPE RUNS FROM THE STELA ACROSS THE FORD.",
        desc="LASHED TO THE STELA, SNAGGED FAST IN THE CEIBA'S ROOTS ACROSS THE WATER."),
    "stela": dict(nouns=["STELA", "GLYPHS"], loc="plaza",
        desc="WITH YOUR JOURNAL'S KEY THE CARVING READS: 'FIRST THE SERPENT "
             "WAKES. THEN THE SUN IS BORN. LAST THE JAGUAR HUNTS.'"),
    "tent": dict(nouns=["TENT"], loc="camp",
        desc="GRIEVE'S TENT. THE FLAP HANGS OPEN."),
    "crowbar": dict(nouns=["CROWBAR", "BAR"], loc=None, take=True,
        room="THERE IS A CROWBAR HERE.", inv="A CROWBAR",
        desc="A STOUT IRON CROWBAR."),
    "rope": dict(nouns=["ROPE"], loc=None, take=True,
        room="THERE IS A COIL OF ROPE HERE.", inv="A COIL OF ROPE",
        desc="FIFTY FEET OF GOOD HEMP."),
    "slab": dict(nouns=["SLAB", "DOOR", "DOORWAY", "SHRINE"], loc="summit", list=True,
        room="A STONE SLAB SEALS THE SHRINE'S DOORWAY.",
        desc="A HEAVY SLAB, FITTED TIGHT. A GOOD LEVER MIGHT SHIFT IT."),
    "wall": dict(nouns=["WALL", "GLYPHS"], loc="hall",
        desc="A SERPENT, A SUN AND A JAGUAR. EACH IS CARVED ON A STONE THAT "
             "LOOKS LIKE IT COULD BE PRESSED."),
    "serpent": dict(nouns=["SERPENT", "SNAKE"], loc="hall", desc="A COILED SERPENT."),
    "sun": dict(nouns=["SUN"], loc="hall", desc="A RAYED SUN."),
    "jaguar": dict(nouns=["JAGUAR", "CAT"], loc="hall", desc="A SPOTTED JAGUAR, MID-SNARL."),
    "clock": dict(nouns=["CLOCK", "DISC"], loc="chamber", take=True, list=True,
        room="THE OBSIDIAN CLOCK RESTS ON THE ALTAR.", inv="THE OBSIDIAN CLOCK",
        desc="A DISC OF BLACK VOLCANIC GLASS, CARVED WITH THE DAYS OF A LOST "
             "YEAR. IT HAS NO WORKS. YOU COULD SWEAR IT TICKS."),
    "altar": dict(nouns=["ALTAR"], loc="chamber", desc="PLAIN STONE, WORN SMOOTH."),
    "silas": dict(nouns=["SILAS", "GRIEVE", "MAN"], loc="chamber", list=True,
        room="SILAS GRIEVE IS PINNED UNDER FALLEN STONES, GROANING.",
        desc="HIS LEG IS CAUGHT UNDER A BLOCK FROM THE SHAFT. HE WON'T GET OUT ALONE."),
}

DIRS = {"N": ["N", "NORTH"], "S": ["S", "SOUTH"], "E": ["E", "EAST"],
        "W": ["W", "WEST"], "U": ["U", "UP", "CLIMB", "ASCEND"], "D": ["D", "DOWN", "DESCEND"]}

# verbs: key -> words.  The engine knows go, look, inv, take, drop, examine,
# read, score, wait, help and quit; the rest are handled only by rules.
VERBS = {
    "go": ["GO", "WALK", "RUN"], "look": ["LOOK", "L"], "inv": ["INVENTORY", "I", "INV"],
    "take": ["TAKE", "GET", "GRAB"], "drop": ["DROP", "LEAVE"],
    "examine": ["EXAMINE", "X", "INSPECT", "SEARCH"], "read": ["READ"],
    "score": ["SCORE"], "wait": ["WAIT", "Z"], "help": ["HELP", "HINT"], "quit": ["QUIT"],
    "open": ["OPEN"], "cut": ["CUT", "CHOP", "HACK", "SLASH"], "light": ["LIGHT", "IGNITE"],
    "tie": ["TIE", "KNOT"], "pry": ["PRY", "LEVER", "FORCE", "MOVE", "LIFT"],
    "press": ["PRESS", "PUSH", "TOUCH"], "talk": ["TALK", "ASK", "SPEAK"],
    "free": ["FREE", "RESCUE"], "board": ["BOARD", "ENTER", "FLY"],
}
NOISE = ["THE", "A", "AN", "AT", "TO", "WITH", "ON", "USING", "INTO", "IN"]

MSG = {   # the engine's own messages, by fixed name
    "huh": "I DON'T UNDERSTAND THAT.",
    "word": "I DON'T KNOW THAT WORD.",
    "noway": "YOU CAN'T GO THAT WAY.",
    "gowhere": "GO WHERE?",
    "notsee": "YOU DON'T SEE THAT HERE.",
    "have": "YOU ALREADY HAVE IT.",
    "cant": "YOU CAN'T TAKE THAT.",
    "taken": "TAKEN.",
    "dropped": "DROPPED.",
    "notcarry": "YOU AREN'T CARRYING THAT.",
    "carrying": "YOU ARE CARRYING:",
    "nothing": "  NOTHING AT ALL.",
    "plain": "YOU SEE NOTHING SPECIAL.",
    "nohappen": "NOTHING HAPPENS.",
    "what": "WHAT DO YOU WANT TO DO THAT TO?",
    "time": "TIME PASSES.",
    "scor1": "YOUR SCORE IS ",
    "scor2": " OF 100.",
    "again": "PLAY AGAIN? (Y/N) ",
    "newg": "STARTING A NEW GAME...",
    "bye": "GOODBYE.",
    "more": "--MORE--",
    "help": "TYPE ONE OR TWO WORDS: GO NORTH, TAKE LAMP, LOOK, INVENTORY. "
            "N S E W U D TO MOVE. EXAMINE THINGS.",
    "intro": INTRO,
    "win": "TEO GUNS THE ENGINE. THE BIPLANE CLAWS UP INTO THE STORM AS THE VALLEY "
           "VANISHES UNDER BROWN WATER. IN YOUR LAP THE OBSIDIAN CLOCK TICKS ONCE -- "
           "THOUGH IT HAS NO WORKS AT ALL. ** YOU HAVE WON **",
    "dead": "** YOUR ADVENTURE IS OVER **",
}

def r(verb, noun, conds, acts): return (verb, noun, conds, acts)

RULES = [
    # --- the airstrip
    r("open", "crate", [("flag", "crate")], [("msg", "IT'S EMPTY NOW.")]),
    r("open", "crate", [("here", "crate")],
      [("msg", "YOU PRY UP THE LID. INSIDE: A MACHETE, A LANTERN AND A BOX OF MATCHES."),
       ("move", "machete", "airstrip"), ("move", "lantern", "airstrip"),
       ("move", "matches", "airstrip"), ("set", "crate")]),
    r("examine", "crate", [("flag", "crate"), ("here", "crate")], [("msg", "AN EMPTY CRATE.")]),
    r("talk", "teo", [("here", "teo"), ("carry", "clock")], [("msg", "'GET IN, DOC!'")]),
    r("talk", "teo", [("here", "teo")],
      [("msg", "'THE RIVER RISES FAST ONCE THE RAIN STARTS, DOC. DON'T GET CAUGHT ON THE FAR SIDE.'")]),
    r("board", None, [("room", "airstrip"), ("ncarry", "clock")],
      [("msg", "TEO SHAKES HIS HEAD. 'NOT WITHOUT THE CLOCK. THAT'S THE JOB.'")]),
    # --- the vines
    r("cut", "vines", [("here", "vines"), ("carry", "machete")],
      [("msg", "YOU HACK THROUGH THE VINES. THE TRAIL OPENS NORTH."),
       ("move", "vines", None), ("exit", "trail", "N", "river"), ("score", 5)]),
    r("cut", "vines", [("here", "vines")], [("msg", "WITH YOUR BARE HANDS? YOU NEED A BLADE.")]),
    r("take", "vines", [("here", "vines")], [("msg", "THEY'RE ROOTED FAST. CUT THEM.")]),
    # --- the lantern
    r("light", "lantern", [("flag", "lit")], [("msg", "IT'S ALREADY LIT.")]),
    r("light", "lantern", [("carry", "lantern"), ("carry", "matches")],
      [("msg", "THE LANTERN FLARES INTO LIFE."), ("set", "lit"), ("score", 5)]),
    r("light", "lantern", [("carry", "lantern")], [("msg", "YOU HAVE NOTHING TO LIGHT IT WITH.")]),
    r("light", "matches", [("carry", "matches")], [("msg", "SAVE THEM FOR THE LANTERN.")]),
    # --- the rope at the ford
    r("tie", "rope", [("room", "river"), ("carry", "rope")],
      [("msg", "YOU TIE THE ROPE TO THE CEIBA AND STRING IT ACROSS THE FORD."),
       ("move", "rope", None), ("move", "ropeline", "river"), ("score", 10)]),
    r("tie", "rope", [("room", "plaza"), ("carry", "rope")],
      [("msg", "YOU LASH THE ROPE AROUND THE STELA AND FLING THE COIL ACROSS THE FORD. "
               "IT SNAGS FAST IN THE CEIBA'S ROOTS ON THE FAR BANK."),
       ("move", "rope", None), ("move", "ropestela", "plaza"), ("score", 10)]),
    r("tie", "rope", [("carry", "rope")], [("msg", "THERE'S NOTHING USEFUL TO TIE IT TO HERE.")]),
    r("take", "rope", [("here", "ropeline")], [("msg", "LEAVE IT. YOU MAY NEED IT TO GET BACK.")]),
    r("take", "rope", [("here", "ropestela")], [("msg", "LEAVE IT. YOU MAY NEED IT TO GET BACK.")]),
    # --- the stela
    r("read", "stela", [("here", "stela"), ("nflag", "readstela")],
      [("msg", "WITH YOUR JOURNAL'S KEY THE CARVING READS: 'FIRST THE SERPENT WAKES. "
               "THEN THE SUN IS BORN. LAST THE JAGUAR HUNTS.'"), ("set", "readstela"), ("score", 5)]),
    r("examine", "stela", [("here", "stela"), ("nflag", "readstela")],
      [("msg", "WITH YOUR JOURNAL'S KEY THE CARVING READS: 'FIRST THE SERPENT WAKES. "
               "THEN THE SUN IS BORN. LAST THE JAGUAR HUNTS.'"), ("set", "readstela"), ("score", 5)]),
    # --- the camp
    r("examine", "tent", [("here", "tent"), ("nflag", "tent")],
      [("msg", "AMONG GRIEVE'S LITTER: A CROWBAR, A COIL OF ROPE, AND A NOTE. 'FOUND A "
               "SHAFT ON THE EAST FACE. GOING DOWN. -- S.G.'"),
       ("move", "crowbar", "camp"), ("move", "rope", "camp"), ("set", "tent"), ("score", 5)]),
    r("open", "tent", [("here", "tent")], [("msg", "IT'S ALREADY OPEN. TRY SEARCHING IT.")]),
    # --- the slab
    r("pry", "slab", [("here", "slab"), ("carry", "crowbar")],
      [("msg", "YOU LEVER THE SLAB ASIDE. STEPS LEAD DOWN INTO DARKNESS."),
       ("move", "slab", None), ("exit", "summit", "D", "stairs"), ("score", 10)]),
    r("open", "slab", [("here", "slab"), ("carry", "crowbar")],
      [("msg", "YOU LEVER THE SLAB ASIDE. STEPS LEAD DOWN INTO DARKNESS."),
       ("move", "slab", None), ("exit", "summit", "D", "stairs"), ("score", 10)]),
    r("pry", "slab", [("here", "slab")], [("msg", "IT WON'T BUDGE BY HAND.")]),
    r("open", "slab", [("here", "slab")], [("msg", "IT WON'T BUDGE BY HAND.")]),
    # --- the dark
    r("D", NONE, [("room", "summit"), ("at", "slab", None), ("nflag", "lit")],
      [("msg", "YOU STEP INTO BLACKNESS, MISS A STAIR, AND FALL A VERY LONG WAY."), ("die",)]),
    r("D", NONE, [("room", "summit"), ("at", "slab", None), ("ncarry", "lantern")],
      [("msg", "YOU STEP INTO BLACKNESS, MISS A STAIR, AND FALL A VERY LONG WAY."), ("die",)]),
    # --- the hall of days
    r("press", "serpent", [("room", "hall"), ("flag", "dooropen")], [("msg", "NOTHING MORE HAPPENS.")]),
    r("press", "sun", [("room", "hall"), ("flag", "dooropen")], [("msg", "NOTHING MORE HAPPENS.")]),
    r("press", "jaguar", [("room", "hall"), ("flag", "dooropen")], [("msg", "NOTHING MORE HAPPENS.")]),
    r("press", "serpent", [("room", "hall"), ("eq", "glyph", 0)],
      [("msg", "THE SERPENT STONE SINKS INTO THE WALL WITH A GRINDING SOUND."), ("ctr", "glyph", 1)]),
    r("press", "sun", [("room", "hall"), ("eq", "glyph", 1)],
      [("msg", "THE SUN STONE SINKS INTO THE WALL."), ("ctr", "glyph", 2)]),
    r("press", "jaguar", [("room", "hall"), ("eq", "glyph", 2)],
      [("msg", "THE JAGUAR STONE SINKS IN. A DOOR GRINDS OPEN TO THE EAST!"),
       ("exit", "hall", "E", "chamber"), ("set", "dooropen"), ("score", 15)]),
    r("press", None, [("room", "hall")],
      [("msg", "CLICK. THE STONES SNAP BACK OUT. SOMEWHERE WATER TRICKLES."), ("ctr", "glyph", 0)]),
    # --- the clock chamber
    r("take", "clock", [("here", "clock"), ("nflag", "flood")],
      [("msg", "YOU LIFT THE CLOCK. ABOVE YOU, STONE GROANS -- AND OUTSIDE, THE RAIN BEGINS TO FALL!"),
       ("get", "clock"), ("set", "flood"), ("ctr", "flood", 0), ("score", 15)]),
    r("free", "silas", [("here", "silas"), ("carry", "crowbar")],
      [("msg", "YOU LEVER UP THE BLOCK AND GRIEVE DRAGS HIMSELF FREE. 'I OWE YOU, VANCE,' "
               "HE GASPS. 'THE FORD WILL BE A TORRENT. HOPE YOU BROUGHT ROPE.' HE LIMPS AWAY."),
       ("move", "silas", None), ("score", 15)]),
    r("pry", "silas", [("here", "silas"), ("carry", "crowbar")],
      [("msg", "YOU LEVER UP THE BLOCK AND GRIEVE DRAGS HIMSELF FREE. 'I OWE YOU, VANCE,' "
               "HE GASPS. 'THE FORD WILL BE A TORRENT. HOPE YOU BROUGHT ROPE.' HE LIMPS AWAY."),
       ("move", "silas", None), ("score", 15)]),
    r("free", "silas", [("here", "silas")], [("msg", "THE BLOCK IS FAR TOO HEAVY TO LIFT BY HAND.")]),
    r("pry", "silas", [("here", "silas")], [("msg", "THE BLOCK IS FAR TOO HEAVY TO LIFT BY HAND.")]),
    r("talk", "silas", [("here", "silas")],
      [("msg", "'TAKE THE CURSED THING,' HE SNARLS. 'JUST GET THIS ROCK OFF ME.'")]),
    # --- the flood at the ford, heading home
    # --- the flooded ford: across on a rope tied at either bank, or not at all
    r("S", NONE, [("room", "plaza"), ("flag", "flood"), ("at", "ropeline", "river")],
      [("msg", "THE FORD IS A TORRENT. YOU HAUL YOURSELF ACROSS ON THE ROPE."), ("goto", "river")]),
    r("S", NONE, [("room", "plaza"), ("flag", "flood"), ("at", "ropestela", "plaza")],
      [("msg", "THE FORD IS A TORRENT. YOU HAUL YOURSELF ACROSS ON THE ROPE."), ("goto", "river")]),
    r("S", NONE, [("room", "plaza"), ("flag", "flood")],
      [("msg", "THE FORD IS A TORRENT NOW. ONE STEP IN AND IT WOULD TAKE YOU. "
               "IF ONLY SOMETHING STRETCHED ACROSS TO HOLD ON TO...")]),
    r("N", NONE, [("room", "river"), ("flag", "flood"), ("at", "ropeline", "river")],
      [("msg", "YOU HAUL YOURSELF ACROSS ON THE ROPE."), ("goto", "plaza")]),
    r("N", NONE, [("room", "river"), ("flag", "flood"), ("at", "ropestela", "plaza")],
      [("msg", "YOU HAUL YOURSELF ACROSS ON THE ROPE."), ("goto", "plaza")]),
    r("N", NONE, [("room", "river"), ("flag", "flood")],
      [("msg", "THE FORD IS A TORRENT NOW. YOU WOULDN'T LAST A MOMENT IN IT.")]),
]

AUTO = [
    # home (first, so reaching the plane on the flood's last turn still wins)
    r(None, None, [("room", "airstrip"), ("carry", "clock")], [("score", 15), ("win",)]),
    # the rains come anyway, eventually
    r(None, None, [("ge", "turns", 220), ("nflag", "flood")],
      [("msg", "THE SKY OPENS. THE RAINS HAVE COME, AND THE RIVER BEGINS TO RISE."),
       ("set", "flood"), ("ctr", "flood", 0)]),
    r(None, None, [("flag", "flood")], [("inc", "flood")]),
    r(None, None, [("eq", "flood", 5)], [("msg", "RAIN HAMMERS DOWN. SOMEWHERE, WATER ROARS.")]),
    r(None, None, [("eq", "flood", 10)], [("msg", "THE GROUND IS TURNING TO MUD. HURRY!")]),
    r(None, None, [("eq", "flood", 15)], [("msg", "THE VALLEY IS FILLING. YOU HAVE MINUTES.")]),
    r(None, None, [("ge", "flood", 20)],
      [("msg", "BROWN WATER SWEEPS OVER EVERYTHING. THE VALLEY KEEPS ITS SECRETS."), ("die",)]),
]
