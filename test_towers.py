from unittest import TestCase, main
from unittest.mock import patch

from towers import Tower, TowersOfHanoi, NoRingAvailable, NonDecreasingOrder, \
    NoRoom, MAX_HEIGHT, Step


class TestTowerCreate(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def tearDown(self):
        TestCase.tearDown(self)

    def testTowerIsList(self):
        self.assertTrue(issubclass(Tower, list), 'Tower is not a list type ')

    def testTowerProperties(self):
        o = Tower()
        for attr in ('height', 'label', 'error', 'top'):
            self.assertTrue(hasattr(o, attr), 'Tower is missing property: {}'.format(attr))

    def testTowerMethods(self):
        o = Tower()
        for attr in ('add', 'addfrom', 'pop', 'press', 'autofill', 'validate', 'new'):
            self.assertTrue(hasattr(o, attr), 'Tower is missing method: {}'.format(attr))
                
    def testTowerNewReturnsTower(self):
        o = Tower.new(3)
        self.assertTrue(isinstance(o, Tower))

    def testTowerNewSize(self):
        size = expected = 3
        o = Tower.new(size)
        self.assertEqual(len(o), expected, 'Size of Tower should be {}, but is {}'.format(expected, len(o)))

    def testAutoFill(self):
        o = Tower.new(3)
        size = 3
        expected = [x for x in range(size, 0, -1)]
        self.assertEqual(o, [0] * size)
        o.autofill()
        self.assertEqual(o, expected)



class TestTowerFunctions(TestCase):
    def setUp(self):
        self.size = 3
        self.o = Tower.new(self.size)
        
        attrs = ('size', 'o')
        for attr in attrs:
            self.addCleanup(delattr, self, attr)

    def tearDown(self):
        TestCase.tearDown(self)


    def testTopGetter(self):
        self.assertIsNone(self.o.top)
        self.o.autofill()
        self.assertEqual(self.o.top, 1)

    def testTopSetter(self):
        expected = self.size
        self.assertIsNone(self.o.top)
        self.o.top = self.size
        self.assertEqual(self.o.top, expected, 'Top ring is not set correctly. It should be \'{}\', but received \'{}\''.format(expected, self.o.top))
        
    def testHeight(self):
        self.assertEqual(self.o.height, 0)
        self.o.top = self.size
        self.assertEqual(self.o.height, 1)
        self.o.autofill()
        self.assertEqual(self.o.height, self.size)
    
    def testPop(self):
        expected = size = 3
        self.o.top = size
        self.assertEqual(self.o.height, 1, 'Failed to add ring to Tower')
        v = self.o.pop()
        self.assertEqual(self.o.height, 0)
        self.assertEqual(v, expected, 'Popped value should have been {}, received {}'.format(expected, v))

    def testPopEmptyRaisesError(self):
        with self.assertRaises(NoRingAvailable):
            self.o.pop()

    def testValidatePasses(self):
        testValues = [
            [0,0,0],
            [1,0,0],
            [2,0,0],
            [2,1,0],
            [3,2,1],
            [4,2,0,0,0],
        ]
        for t in testValues:
            try:
                o = Tower(t)
                self.assertTrue(o.validate(False), 'Failed validation: {}'.format(t))
                self.assertTrue(o.validate(), 'Failed validation (failed to raise): {}'.format(t))
            except NonDecreasingOrder as e:
                self.fail('Validate failed, exception was raised: {}'.format(e))
            del(o)

    def testValidateFails(self):
        testValues = [
            [0,0,0,1],
            [1,2,0],
            [2,0,1],
            [2,1,3],
            [0,3,2,1],
            [4,2,0,0,1],
            [1,2,0,0,4],
        ]
        for t in testValues:
            o = Tower(t)
            self.assertFalse(o.validate(False), 'Validation passed bad validation: {}'.format(t))
            with self.assertRaises(NonDecreasingOrder):
                o.validate()
                self.fail('Failed to raise: {}'.format(t))
            
    def testPress(self):
        testValues = [
            [[0,0,0], [0,0,0]],
            [[1,0,0], [1,0,0]],
            [[0,1,0], [1,0,0]],
            [[0,0,1], [1,0,0]],
            [[2,1,0], [2,1,0]],
            [[2,0,1], [2,1,0]],
            [[0,2,1], [2,1,0]],
            [[3,1,0], [3,1,0]],
            [[3,0,1], [3,1,0]],
            [[0,3,1], [3,1,0]],
            [[3,2,0], [3,2,0]],
            [[3,0,2], [3,2,0]],
            [[0,3,2], [3,2,0]],
            [[3,2,1], [3,2,1]],
        ]
        for t in testValues:
            vals = t[0]
            expected = t[1]
            o = Tower(vals)
            with patch.object(Tower, 'validate', return_value=True) as mockValidate:
                o.press()
                self.assertEqual(o, expected)
            mockValidate.assert_called_once()
            
    def testPressAutoSort(self):
        testValues = [
            [[0,0,0], [0,0,0]],
            [[1,0,0], [1,0,0]],
            [[0,1,0], [1,0,0]],
            [[0,0,1], [1,0,0]],
            [[2,1,0], [2,1,0]],
            [[2,0,1], [2,1,0]],
            [[0,2,1], [2,1,0]],
            [[3,1,0], [3,1,0]],
            [[3,0,1], [3,1,0]],
            [[0,3,1], [3,1,0]],
            [[3,2,0], [3,2,0]],
            [[3,0,2], [3,2,0]],
            [[0,3,2], [3,2,0]],
            [[3,2,1], [3,2,1]],
            [[1,2,3], [3,2,1]],
            [[2,3,1], [3,2,1]],
            [[2,1,3], [3,2,1]],
            [[3,1,2], [3,2,1]],
            [[0,2,1], [2,1,0]],
            [[0,2,0], [2,0,0]],
            [[1,2,0], [2,1,0]],
            [[4,1,2,3], [4,3,2,1]],            
            [[4,1,2,0], [4,2,1,0]],            
        ]
        for t in testValues:
            vals = t[0]
            expected = t[1]
            o = Tower(vals)
            with patch.object(Tower, 'validate', return_value=True):
                o.press(True)
                self.assertEqual(o, expected)
            
    @patch.object(Tower, 'press')
    def testAdd(self, mockPress):
        self.assertNotIn(1, self.o, 'Value is already in Tower when it should not be. Did a test not clean up after itself?')
        self.o.add(1)
        self.assertIn(1, self.o, 'Failed to add value to Tower.')
        mockPress.assert_called_once()

    def testAddRaisesWhenNoRoom(self):
        t = Tower([3,2,1])
        with self.assertRaises(NoRoom):
            t.add(4)

    @patch.object(Tower, 'press')
    def testAddFrom(self, mockPress):
        t1 = Tower([0,0,0])
        t2 = Tower([1,0,0])
        self.assertNotIn(1, t1)
        t1.addfrom(t2)
        self.assertIn(1, t1)
        mockPress.assert_called_once()

    def testAddFromRaisesWhenNoRoom(self):
        t1 = Tower([4,3,2])
        t2 = Tower([1,0,0])
        with self.assertRaises(NoRoom):
            t1.addfrom(t2)



class TowersOfHanoiCreate(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def tearDown(self):
        TestCase.tearDown(self)

    def testCreateTowerGame(self):
        try:
            TowersOfHanoi(3)
        except Exception as e:
            self.fail('Game creation caused exception: '.format(e))
    
    def testCreateTowerGameSizeTooLarge(self):
        with self.assertRaises(ValueError):
            TowersOfHanoi(MAX_HEIGHT+1)
            
    def testCreateTowerGameProperties(self):
        toh = TowersOfHanoi(3)
        
        attrs = ['Tower{:d}'.format(x+1) for x in range(3)] + ['towers', 'size']
        for attr in attrs:
            self.assertTrue(hasattr(toh, attr), 'Missing property: {}'.format(attr))

    def testCreateTowerGameMethods(self):
        toh = TowersOfHanoi(3)
        
        attrs = ['solve']
        for attr in attrs:
            self.assertTrue(hasattr(toh, attr), 'Missing property: {}'.format(attr))



class TowersOfHanoiSolve(TestCase):
    def setUp(self):
        TestCase.setUp(self)

    def tearDown(self):
        TestCase.tearDown(self)

    def testSolveIterative(self):
        tests = [
            [2, [Step(ring=1, orig=0, dest=1), Step(ring=2, orig=0, dest=2), Step(ring=1, orig=1, dest=2)]],
            [3, [Step(ring=1, orig=0, dest=2), Step(ring=2, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=3, orig=0, dest=2), Step(ring=1, orig=1, dest=0), Step(ring=2, orig=1, dest=2), Step(ring=1, orig=0, dest=2)]],
            [4, [Step(ring=1, orig=0, dest=1), Step(ring=2, orig=0, dest=2), Step(ring=1, orig=1, dest=2), Step(ring=3, orig=0, dest=1), Step(ring=1, orig=2, dest=0), Step(ring=2, orig=2, dest=1), Step(ring=1, orig=0, dest=1), Step(ring=4, orig=0, dest=2), Step(ring=1, orig=1, dest=2), Step(ring=2, orig=1, dest=0), Step(ring=1, orig=2, dest=0), Step(ring=3, orig=1, dest=2), Step(ring=1, orig=0, dest=1), Step(ring=2, orig=0, dest=2), Step(ring=1, orig=1, dest=2)]],
            [5, [Step(ring=1, orig=0, dest=2), Step(ring=2, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=3, orig=0, dest=2), Step(ring=1, orig=1, dest=0), Step(ring=2, orig=1, dest=2), Step(ring=1, orig=0, dest=2), Step(ring=4, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=2, orig=2, dest=0), Step(ring=1, orig=1, dest=0), Step(ring=3, orig=2, dest=1), Step(ring=1, orig=0, dest=2), Step(ring=2, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=5, orig=0, dest=2), Step(ring=1, orig=1, dest=0), Step(ring=2, orig=1, dest=2), Step(ring=1, orig=0, dest=2), Step(ring=3, orig=1, dest=0), Step(ring=1, orig=2, dest=1), Step(ring=2, orig=2, dest=0), Step(ring=1, orig=1, dest=0), Step(ring=4, orig=1, dest=2), Step(ring=1, orig=0, dest=2), Step(ring=2, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=3, orig=0, dest=2), Step(ring=1, orig=1, dest=0), Step(ring=2, orig=1, dest=2), Step(ring=1, orig=0, dest=2)]],
        ]
        for n, expected in tests:
            toh = TowersOfHanoi(n)
            toh._iter = True
            self.assertEqual(toh.solve(), expected)

    def testSolveRecursive(self):
        tests = [
            [2, [Step(ring=1, orig=0, dest=1), Step(ring=2, orig=0, dest=2), Step(ring=1, orig=1, dest=2)]],
            [3, [Step(ring=1, orig=0, dest=2), Step(ring=2, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=3, orig=0, dest=2), Step(ring=1, orig=1, dest=0), Step(ring=2, orig=1, dest=2), Step(ring=1, orig=0, dest=2)]],
            [4, [Step(ring=1, orig=0, dest=1), Step(ring=2, orig=0, dest=2), Step(ring=1, orig=1, dest=2), Step(ring=3, orig=0, dest=1), Step(ring=1, orig=2, dest=0), Step(ring=2, orig=2, dest=1), Step(ring=1, orig=0, dest=1), Step(ring=4, orig=0, dest=2), Step(ring=1, orig=1, dest=2), Step(ring=2, orig=1, dest=0), Step(ring=1, orig=2, dest=0), Step(ring=3, orig=1, dest=2), Step(ring=1, orig=0, dest=1), Step(ring=2, orig=0, dest=2), Step(ring=1, orig=1, dest=2)]],
            [5, [Step(ring=1, orig=0, dest=2), Step(ring=2, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=3, orig=0, dest=2), Step(ring=1, orig=1, dest=0), Step(ring=2, orig=1, dest=2), Step(ring=1, orig=0, dest=2), Step(ring=4, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=2, orig=2, dest=0), Step(ring=1, orig=1, dest=0), Step(ring=3, orig=2, dest=1), Step(ring=1, orig=0, dest=2), Step(ring=2, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=5, orig=0, dest=2), Step(ring=1, orig=1, dest=0), Step(ring=2, orig=1, dest=2), Step(ring=1, orig=0, dest=2), Step(ring=3, orig=1, dest=0), Step(ring=1, orig=2, dest=1), Step(ring=2, orig=2, dest=0), Step(ring=1, orig=1, dest=0), Step(ring=4, orig=1, dest=2), Step(ring=1, orig=0, dest=2), Step(ring=2, orig=0, dest=1), Step(ring=1, orig=2, dest=1), Step(ring=3, orig=0, dest=2), Step(ring=1, orig=1, dest=0), Step(ring=2, orig=1, dest=2), Step(ring=1, orig=0, dest=2)]],
        ]
        for n, expected in tests:
            toh = TowersOfHanoi(n)
            toh._iter = False
            solution = toh.solve()
            self.assertEqual(solution, expected)



if __name__ == '__main__':
    main()
    #main(TowersOfHanoiSolve, 'testSolveRecursive')

