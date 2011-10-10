story = "Once upon a day, you were a-walking in a forest, when you accidentally stepped on some railroads, upon which you were driven, against your will, to a cave and thrown within. Good thing you have that handy light source in your pocket."
l = 8
startt = "B7"
from Maps.TheMap.Types import *
class Place:
        def __init__(self, Type, dirlinks, cordlinks, **kwargs):
                self.cordlinks = cordlinks
                self.dirlinks = dirlinks
                if Type == "sp":
                        self.look = kwargs["sp"]
                else:
                        self.look = types[Type]
                self.exits = "Exits: "
                for i in cordlinks:
                        self.exits += i+", "
                self.exits = self.exits[:-2]
                if "end" in kwargs:
                        self.end = True
                else:
                        self.end = False




A1 = Place("SharpCorner", ["S", "E"], ["A2", "B1"])
B1 = Place("SharpCorner", ["S", "W"], ["B2", "A1"])
C1 = Place("sp", ["S"], ["C2"], end = True, sp = "Finally! You've found the way out, although the unholy splendor of the obsidian stairway out is somewhat unsettling.")
D1 = Place("EvilCorner", ["S", "E"], ["D2", "E1"])
E1 = Place("sp", ["W", "E"], ["D1", "F1"], sp = "Contrary to the pure light right next to this part of the tunnel, this passage is rather dark and damp, and you can smell rot.")
F1 = Place("sp", ["E", "W", "T"], ["G1", "E1", "H8"], sp = "A large portal, made of pure marble and filled with pure white light, stands in the middle of this shining passage.")
G1 = Place("sp", ["W", "E"], ["F1", "H1"], sp = "The pure white light shining from the walls of this massive hallway lifts your mood.")
H1 = Place("sp", ["W", "S"], ["G1", "H2"], sp = "This turn seems full of good spirits and warmness.")
A2 = Place("SlimeTunnel", ["N", "S"], ["A1", "A3"])
B2 = Place("OddWall", ["N"], ["B1"])
C2 = Place("EvilCorner", ["N", "E"], ["C1", "D2"])
D2 = Place("sp", ["N", "W"], ["D1", "C2"], sp = "You've found the source of the rotting smell: Zombies who weren't deemed fit for the attack. Or so you think- there are old zombies in this bent corridor, anyways.")
E2 = Place("MeetHall", ["S", "E"], ["E3", "F2"])
F2 = Place("MeetHall", ["S", "W"], ["F3", "E2"])
G2 = Place("CrumbCorner", ["S", "E"], ["G3", "H2"])
H2 = Place("sp", ["S", "W", "N"], ["H3", "G2", "H1"], sp = "What used to be a grand intersection is now a slightly less grand intersection due to the fact that one passage is caved in.")
A3 = Place("OldCorner", ["N", "E"], ["A2", "B3"])
B3 = Place("OldCorner", ["W", "S"], ["A3", "B4"])
C3 = Place("IceHall", ["S", "E"], ["C4", "D3"])
D3 = Place("IceHall", ["S", "W"], ["D4", "C3"])
E3 = Place("MeetHall", ["N", "E"], ["E2", "F3"])
F3 = Place("MeetHall", ["W", "S", "N"], ["E3", "F4", "F2"])
G3 = Place("sp", ["N", "S"], ["G2", "G4"], sp = "You have to avoid chunks fallen from the ceiling as you navigate this hall.")
H3 = Place("sp", ["T"], ["B7"], sp = "Walking forward, you trip over the none-to-good floor. Your fall dislodges some sharp rocks from the ceiling, which impale you. (T to start over)")
A4 = Place("WordCorner", ["E", "S"], ["B4", "A5"])
B4 = Place("ImageCorner", ["N", "W"], ["B3", "A4"])
C4 = Place("IceHall", ["N", "S", "E"], ["C3", "C5", "D4"])
D4 = Place("IceHall", ["N", "W"], ["D3", "C4"])
E4 = Place("FancyCorner2", ["E", "S"], ["F4", "E5"])
F4 = Place("sp", ["E", "N", "S"], ["E4", "F3", "F5"], sp = "Entering, you see a fabulous marble-shot room, with two ways out. In the center is a dual statue, made of marble. The northern part of it is a paladin with an upraised hammer, to the south, a fearsome lich with a bundle of something black in his hands.")
G4 = Place("CrumbCorner", ["N", "E"], ["G3", "H4"])
H4 = Place("CrumbCorner", ["W", "S"], ["G4", "H5"])
A5 = Place("WordCorner", ["N", "E"], ["A4", "B5"])
B5 = Place("ImageCorner", ["W", "S"], ["A5", "B6"])
C5 = Place("ImageCorner", ["N", "E"], ["C4", "D5"])
D5 = Place("sp", ["W", "E", "S"], ["C5", "E5", "D6"], sp = "The tunnel-path opens into a large room with two exits. In the middle stands a large scale. On the west part of the scale is a viper twisted into a mobius strip, on the east side, a mongoose in a priest's robe. Both of them are alive, and while they try not to move, every so often one of them gets out of position, flickers, and returned to it's original state.")
E5 = Place("FancyCorner", ["W", "N"], ["D5", "E4"])
F5 = Place("BoneBranch", ["N", "E", "S"], ["F4", "G5", "F6"])
G5 = Place("OldCorner", ["W", "S"], ["F5", "G6"])
H5 = Place("sp", ["N"], ["H4"], sp = "There's no way south in this crumbling passage anymore, since the roof has done it's thing and crumbled down behind you.")
A6 = Place("FancyCorner", ["E", "S"], ["B6", "A7"])
B6 = Place("sp", ["E", "N"], ["C6", "B5"], sp = "The tunnel-road exits into a medium-sized stone caravan. The two exits are perpendicular to each other. In the center of the caravan, you see an worn, engraved, table. The title seems to be ZGHCVQ PELCGB WHAXVRF, and what's beneath the title is very worn out, but you can make out the general shape of an 8x8 map.")
C6 = Place("FancyCorner2", ["S", "E"], ["C7", "D6"])
D6 = Place("sp", ["W", "N"], ["C6", "D5"], sp = "Expecting to see another superbly made turn, you are startled too see a exquisitely and tastefully designed bend in the passage.")
E6 = Place("OldCorner", ["S", "E"], ["E7", "F6"])
F6 = Place("BoneBranch", ["N", "W", "S"], ["F5", "E6", "F7"])
G6 = Place("OldCorner", ["N", "E"], ["G5", "H6"])
H6 = Place("CrumbCorner", ["N", "W"], ["H5", "G6"])
A7 = Place("sp", ["N", "S"], ["A6", "A8"], sp = "On the walls of this rather magnificent and grand wall, you observe a stately mural or a rather large number of heroes spouting blood and guts, and dieing horribly in no uncertain manner. There are also a number of paintings and statues of the same- heroes. You decide that normal eyes don't look like that, and part hurriedly.")
B7 = Place("sp", ["S"], ["B8"], sp = "Behind you, you see not only the awesome foe that is the Rough Ground of Unwalkability, but also an Indestructible Fallen Log, which had fallen immediately after your entrance. There is no escape, but forward. Such is life, for those lacking in motivation.")
C7 = Place("FancyCorner", ["N", "E"], ["C6", "D7"])
D7 = Place("FancyCorner2", ["W", "S"], ["C7", "D8"])
E7 = Place("SlimeTunnel", ["N", "S"], ["E6", "E8"])
F7 = Place("EvilCorner", ["N", "E"], ["F6", "G7"])
G7 = Place("sp", ["W", "E"], ["F7", "H7"], sp = "A large hallway, with a vile emerald haze here and there, snaking out in tendrils, as well as some dark, snaky lines tracing here and there.")
H7 = Place("EvilCorner", ["W", "S"], ["G7", "H8"])
A8 = Place("FancyCorner", ["N", "E"], ["A7", "B8"])
B8 = Place("sp", ["N", "W", "E"], ["B7", "A8", "C8"], sp = "The tunnel goes into an ornate room, with two doors out. The one two the west posses a magnificent grandeur, whilst the one two the east seems rather flimsy and fake, although both are equally splendid. In the middle is depicted the god Janus, as a statue, with a particularly mocking expression.")
C8 = Place("sp", ["W", "E"], ["B8", "D8"], sp = "A wide and ornate hall, covered in all manner of shiny things, all of which are firmly affixed, ultimately, to the floor.")
D8 = Place("FancyCorner", ["W", "N"], ["C8", "D7"])
E8 = Place("OldCorner", ["N", "E"], ["E7", "F8"])
F8 = Place("sp", ["W", "E"], ["E8", "G8"], sp = "You have to bend over as the tunnel gets smaller and narrower, for quite some time.")
G8 = Place("OddWall", ["W"], ["F8"])
H8 = Place("sp", ["N", "T"], ["H7", "F1"], sp = "You observe a large portal, made of bone. The emerald haze, which has been rampant up to this point along the trail, is practically solid within the portal.")
