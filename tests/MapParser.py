'''
Created on Jan 1, 2014

@author: Rob
'''
import unittest

class MapParserTest(unittest.TestCase):
    def setUp(self):
        from byond.map.format.dmm import DMMFormat
        from byond.map import Map
        self.map = Map()
        self.dmm = DMMFormat(self.map)
    
    def test_basic_SplitAtoms_operation(self):
        testStr = '/obj/effect/landmark{name = "carpspawn"},/obj/structure/lattice,/turf/space,/area'
        expectedOutput = ['/obj/effect/landmark{name = "carpspawn"}', '/obj/structure/lattice', '/turf/space', '/area']
        
        out = self.dmm.SplitAtoms(testStr)
        self.assertListEqual(out, expectedOutput)
    
    def test_basic_SplitProperties_operation(self):
        testStr = 'd1 = 1; d2 = 2; icon_state = "1-2"; tag = ""'
        expectedOutput = ['d1 = 1', ' d2 = 2', ' icon_state = "1-2"', ' tag = ""']
        
        out = self.dmm.SplitProperties(testStr)
        self.assertListEqual(out, expectedOutput)
    
    def test_basic_consumeTile_operation(self):
        from byond.map import Map, Tile
        '''
        "aaK" = (
            /obj/structure/cable{
                d1 = 1;
                d2 = 2; 
                icon_state = "1-2";
                tag = ""
            },
            /obj/machinery/atmospherics/pipe/simple/supply/hidden{
                dir = 4
            },
            /turf/simulated/floor{
                icon_state = "floorgrime"
            },
            /area/security/prison
        )
        '''
        testStr = '"aaK" = (/obj/structure/cable{d1 = 1; d2 = 2; icon_state = "1-2"; tag = ""},/obj/machinery/atmospherics/pipe/simple/supply/hidden{dir = 4},/turf/simulated/floor{icon_state = "floorgrime"},/area/security/prison)'
        testSerData='/obj/structure/cable{d1=1;d2=2;icon_state="1-2";tag=""},/obj/machinery/atmospherics/pipe/simple/supply/hidden{dir=4},/turf/simulated/floor{icon_state="floorgrime"},/area/security/prison{}'
        
        out = self.dmm.consumeTile(testStr, False) # :type out: Tile
        #print('IIDs: {0}'.format(repr(out.instances)))

        self.assertEquals(out.origID, 'aaK', 'origID')
        self.assertEquals(len(out.instances), 4, 'instances size')
        self.assertEquals(len(out.GetAtom(0).properties), 4, 'instances[0] properties')
        self.assertIn('d1', out.GetAtom(0).properties, 'd1 not present in properties')
        self.assertListEqual(out.GetAtom(0).mapSpecified,['d1','d2','icon_state','tag'])
        
        self.assertEquals(len(out.GetAtom(2).properties), 1, 'Failure to parse /turf/simulated/floor{icon_state = "floorgrime"}')
        self.assertIn('icon_state', out.GetAtom(2).properties, 'Failure to parse /turf/simulated/floor{icon_state = "floorgrime"}')
        
        self.assertEqual(out._serialize(), testSerData)
        
    def _show_expected_vs_actual(self,expected,actual):
        if expected != actual:
            print((' > EXPECTED: {}'.format(expected)))
            print((' > ACTUAL:   {}'.format(actual)))
        
    
    def test_basic_SerializeTile_operation(self):
        from byond.map import Map, Tile
        '''
        "aaK" = (
            /obj/structure/cable{
                d1 = 1;
                d2 = 2; 
                icon_state = "1-2";
                tag = ""
            },
            /obj/machinery/atmospherics/pipe/simple/supply/hidden{
                dir = 4
            },
            /turf/simulated/floor{
                icon_state = "floorgrime"
            },
            /area/security/prison
        )
        '''
        testStr = '"aaK" = (/obj/structure/cable{d1 = 1; d2 = 2; icon_state = "1-2"; tag = ""},/obj/machinery/atmospherics/pipe/simple/supply/hidden{dir = 4},/turf/simulated/floor{icon_state = "floorgrime"},/area/security/prison)'
        expected = testStr.split('=',1)[1].strip()
        tile = self.dmm.consumeTile(testStr, False) # :type tile: Tile
        out = self.dmm.SerializeTile(tile)
        self._show_expected_vs_actual(expected, out)
        self.assertEqual(out, expected)
    def test_consumeTile_secureArea(self):
        '''
        "aai" = (
            /obj/structure/sign/securearea{
                desc = "A warning sign which reads \'HIGH VOLTAGE\'"; 
                icon_state = "shock"; 
                name = "HIGH VOLTAGE"; 
                pixel_y = -32
            },
            /turf/space,
            /area
        )
        '''
        testStr = '"aai" = (/obj/structure/sign/securearea{desc = "A warning sign which reads \'HIGH VOLTAGE\'"; icon_state = "shock"; name = "HIGH VOLTAGE"; pixel_y = -32},/turf/space,/area)'

        tile = self.dmm.consumeTile(testStr, False) # :type tile: Tile
        
        self.assertEquals(tile.origID, 'aai', 'origID')
        self.assertEquals(len(tile.instances), 3, 'instances size')
        self.assertEquals(len(tile.GetAtom(0).properties), 4, 'instances[0] properties')
        self.assertIn('desc', tile.GetAtom(0).properties, 'desc not present in properties')
        self.assertListEqual(tile.GetAtom(0).mapSpecified,['desc','icon_state','name','pixel_y'])
        
        expected = testStr.split('=',1)[1].strip()
        out = self.dmm.SerializeTile(tile)
        self._show_expected_vs_actual(expected, out)
        self.assertEqual(out, expected)

        
    def test_consumeTile_landmark(self):
        testStr='"aah" = (/obj/effect/landmark{name = "carpspawn"},/obj/structure/lattice,/turf/space,/area)'
        testSerData='/obj/effect/landmark{name="carpspawn"},/obj/structure/lattice{},/turf/space{},/area{}'
        out = self.dmm.consumeTile(testStr)
        self.assertEqual(out._serialize(), testSerData)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
