#Classes for towers
from math import log2
from collections import namedtuple
MAX_HEIGHT = 10

class Tower (list):
    height = 0
    label = None
    id = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) 
        self.error = None
        self.label = "no_name"
    
    def add(self, ringNumber: int):
        if self[len(self)-1] != 0:
            raise NoRoom
        self[len(self)-1] = ringNumber
        self.press()

    def addfrom(self, tower):
        ringNumber = tower.pop()
        self.add(ringNumber)

    def pop(self):
        if self.top is None:
            raise NoRingAvailable
        top_value = self.top
        self.top = 0
        return top_value

    @property
    def height(self):
        if 0 in self:
            return self.index(0)
        return len(self)

    @property
    def top(self):
        if self.height == 0:
            return None
        return self[self.height-1]
    
    @top.setter
    def top(self, v: int):
        i = 0 if self.height == 0 else self.height - 1
        self[i] = v

    def press(self, autosort=False):
        if autosort:
            s = list(reversed(sorted(self)))
            for i in range(len(self)):
                self[i] = s[i]
        else:
            last_nonzero_i = len(self)
            for i in range(len(self)-2, -1, -1):
                if self[i] == 0 and self[i+1] != 0:
                    for j in range(i, last_nonzero_i - 1):
                        self[j] = self[j+1]
                        self[j+1] = 0
        self.validate(True)
        
    def autofill(self):
        s = len(self)
        for i in range(s):
            self[i] = s - i

    def validate(self, raise_exeption=True):
        for i in range(len(self) - 1):
            if self[i] < self[i+1]:
                error_text = 'index {}, value {} is less than the following value {}.'.format(i, self[i], self[i+1])
                if raise_exeption:
                    raise NonDecreasingOrder(error_text)
                self.error = error_text
                return False
        return True
    
    @classmethod
    def new(cls, size: int):
        return cls((0,) * size)



class TowersOfHanoi(object):
    Tower1 = Tower2 = Tower3 = None
    _max_size = MAX_HEIGHT
    _iter = False

    def __init__(self, size: int):
        if size > self._max_size:
            raise ValueError('size can be max of {}'.format(self._max_size))
        self.size = size

        for i in range(3):  # Create towers
            tower = towerLabel = 'Tower{:d}'.format(i+1)
            setattr(self, tower, Tower.new(size))
            t = getattr(self, tower)
            t.label = towerLabel
            t.id = i

        self.Tower1.autofill()
            
    @property
    def towers(self):
        return (self.Tower1, self.Tower2, self.Tower3)

    def __str__(self):
        return '{{Tower1: {}, Tower2: {}, Tower3: {}}}'.format(self.Tower1, self.Tower2, self.Tower3)

    def solve(self, pretty=False, verbose=False):
        if self._iter:
            solution = self._solve_iter()
        else:
            solution = self._solve_recu(self.towers[0].height, self.towers[0], self.towers[2], self.towers[1])
        instructions = []
        ctr = 1
        for i in solution:
            instruction = ''
            if pretty:
                instruction += 'step {}: move ring {} from {} to {}'.format(ctr, i.ring, self.towers[i.orig].label, self.towers[i.dest].label)
            self.towers[i.dest].addfrom(self.towers[i.orig])
            if pretty and verbose:
                instruction += ': {}'.format(self)
            instructions.append(instruction)
            ctr += 1
            
        return instructions if pretty else solution

    def _can_move(self, ring, fromTower, toTower):
        if ring == fromTower.top:
            if (toTower.top is None or ring < toTower.top):
                return True
        return False

    def _solve_recu(self, ring, fromTower, toTower, passTower, instructionsList=None, depth=1):
        if instructionsList is None:
            instructionsList = []
        if depth > MAX_HEIGHT:
            raise Exception("reachedMaxRecursion")

        if not self._can_move(ring, fromTower, toTower) and ring > 1:
            instructionsList = self._solve_recu(ring-1, fromTower, passTower, toTower, instructionsList, depth+1)

        instructionsList.append(Step(ring, fromTower.id, toTower.id))

        if ring > 1:
            self._solve_recu(ring-1, passTower, toTower, fromTower, instructionsList, depth+1)
        return instructionsList

    def _skip(self, n): # determines which numbers get skipped when using switching pattern
        bitmax = int(log2(n)) + 1
        if n >3:
            for i in range(2, bitmax, 2):
                if n & 1 << i and not (n-1) & 1 << i:
                    return True
        return False

    def _iter_ring_number(self, step):
        if step < 1:
            return 0
        ring = 1
        while(not (step & 1)):
            ring += 1
            step = step >> 1
        return ring
    
    def _solve_iter(self):
        instructionsList = []
        t = [self.Tower1]
        if self.size % 2:
            t.append(self.Tower2)
            t.append(self.Tower3)
        else:
            t.append(self.Tower3)
            t.append(self.Tower2)

        cnt = 2 ** self.size - 1    
        for i in range(cnt):
            # b = (i+1) % 3
            if i % 2 == 0 or self._skip(i + 1):
                a = t[i %3]
                c = t[(i+2) %3]
            else:
                a = t[(i+2) %3]
                c = t[i %3]
            
            instructionsList.append(Step(self._iter_ring_number(i+1), a.id, c.id))
        return instructionsList


Step = namedtuple('Step', ['ring', 'orig', 'dest'])



class NonDecreasingOrder (Exception):
    pass

class NoRoom (Exception):
    pass

class NoRingAvailable (Exception):
    pass

if __name__ == '__main__':
    challenge = 3
    toh = TowersOfHanoi(challenge)
    print('\n'.join(toh.solve(True, True)))


