story = 'You were walking about in a forset, when you stumbeled upon some tracks. Accedtly step on them, you were driven agaisnt your will up to a cave, and trown in.'
l = 8
startt = 'B7'
from Maps.TheMap.Types import *
class Place:
        def __init__(self, Type, dirlinks, cordlinks, **kwargs):
                self.cordlinks = cordlinks
                self.dirlinks = dirlinks
                if Type == 'sp':
                        self.look = kwargs['sp']
                else:
                        self.look = types[Type]
                self.exits = 'Exits: '
                for i in cordlinks:
                        self.exits += i+', '
                self.exits = self.exits[:-2]
                if 'end' in kwargs:
                        self.end = True
                else:
                        self.end = False


A1 = Place('cornerO', ['S', 'E'], ['A2', 'B1'])
B1 = Place('cornerO', ['S', 'W'], ['B2', 'A1'])
C1 = Place('Exit', ['S'], ['C2'], end = True)
D1 = Place('cornerE', ['S', 'E'], ['D2', 'E1'])
E1 = Place('SpassE', ['W', 'E'], ['D1', 'F1'])
F1 = Place('PpassG', ['E', 'W', 'T'], ['G1', 'E1', 'H8'])
G1 = Place('BpassG', ['W', 'E'], ['F1', 'H1'])
H1 = Place('cornerG', ['W', 'S'], ['G1', 'H2'])
A2 = Place('SpassO', ['N', 'S'], ['A1', 'A3'])
B2 = Place('deadO', ['N'], ['B1'])
C2 = Place('cornerE', ['N', 'E'], ['C1', 'D2'])
D2 = Place('cornerE', ['N', 'W'], ['D1', 'C2'])
E2 = Place('HcornerO', ['S', 'E'], ['E3', 'F2'])
F2 = Place('HcornerO', ['S', 'W'], ['F3', 'E2'])
G2 = Place('cornerC', ['S', 'E'], ['G3', 'H2'])
H2 = Place('TjctC', ['S', 'W', 'N'], ['H3', 'G2', 'H1'])
A3 = Place('cornerO', ['N', 'E'], ['A2', 'B3'])
B3 = Place('cornerO', ['W', 'S'], ['A3', 'B4'])
C3 = Place('HcornerM', ['S', 'E'], ['C4', 'D3'])
D3 = Place('HcornerM', ['S', 'W'], ['D4', 'C3'])
E3 = Place('HcornerO', ['N', 'E'], ['E2', 'F3'])
F3 = Place('HcornerO', ['W', 'S'], ['E3', 'F4'])
G3 = Place('BpassC', ['N', 'S'], ['G2', 'G4'])
H3 = Place('PdeadC', ['N', 'T'], ['H2', 'B7'])
A4 = Place('cornerM', ['E', 'S'], ['B4', 'A5'])
B4 = Place('cornerM', ['N', 'W'], ['B3', 'A4'])
C4 = Place('HcornerM', ['N', 'S', 'E'], ['C3', 'C5', 'D4'])
D4 = Place('HcornerM', ['N', 'W'], ['D3', 'C4'])
E4 = Place('cornerN', ['E', 'S'], ['F4', 'E5'])
F4 = Place('TjctO', ['E', 'N', 'S'], ['E4', 'F3', 'F5'])
G4 = Place('cornerC', ['N', 'E'], ['G3', 'H4'])
H4 = Place('cornerC', ['W', 'S'], ['G4', 'H5'])
A5 = Place('cornerM', ['N', 'E'], ['A4', 'B5'])
B5 = Place('cornerM', ['W', 'S'], ['A5', 'B6'])
C5 = Place('cornerM', ['N', 'E'], ['C4', 'D5'])
D5 = Place('TjctM', ['W', 'E', 'S'], ['C5', 'E5', 'D6'])
E5 = Place('cornerN', ['W', 'N'], ['D5', 'E4'])
F5 = Place('BjctO', ['N', 'E', 'S'], ['F4', 'G5', 'F6'])
G5 = Place('cornerO', ['W', 'S'], ['F5', 'G6'])
H5 = Place('CpassC', ['N'], ['H4'])
A6 = Place('cornerN', ['E', 'S'], ['B6', 'A7'])
B6 = Place('cornerR', ['E', 'N'], ['C6', 'B5'])
C6 = Place('cornerN', ['S', 'E'], ['C7', 'D6'])
D6 = Place('cornerN', ['W', 'N'], ['C6', 'D5'])
E6 = Place('cornerO', ['S', 'E'], ['E7', 'F6'])
F6 = Place('BjctO', ['N', 'W', 'S'], ['F5', 'E6', 'F7'])
G6 = Place('cornerO', ['N', 'E'], ['G5', 'H6'])
H6 = Place('cornerC', ['N', 'W'], ['H5', 'G6'])
A7 = Place('BpassN', ['N', 'S'], ['A6', 'A8'])
B7 = Place('Entry', ['S'], ['B8'])
C7 = Place('cornerN', ['N', 'E'], ['C6', 'D7'])
D7 = Place('cornerN', ['W', 'S'], ['C7', 'D8'])
E7 = Place('SpassO', ['N', 'S'], ['E6', 'E8'])
F7 = Place('cornerE', ['N', 'E'], ['F6', 'G7'])
G7 = Place('BpassE', ['W', 'E'], ['F7', 'H7'])
H7 = Place('cornerE', ['W', 'S'], ['G7', 'H8'])
A8 = Place('cornerN', ['N', 'E'], ['A7', 'B8'])
B8 = Place('TjctN', ['N', 'W', 'E'], ['B7', 'A8', 'C8'])
C8 = Place('WpassN', ['W', 'E'], ['B8', 'D8'])
D8 = Place('cornerN', ['W', 'N'], ['C8', 'D7'])
E8 = Place('cornerO', ['N', 'E'], ['E7', 'F8'])
F8 = Place('CpassO', ['W', 'E'], ['E8', 'G8'])
G8 = Place('deadO', ['W'], ['F8'])
H8 = Place('PdeadE', ['N', 'T'], ['H7', 'F1'])
