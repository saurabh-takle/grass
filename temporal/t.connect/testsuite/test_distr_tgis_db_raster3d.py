"""test distributed temporal databases with str3ds

(C) 2014 by the GRASS Development Team
This program is free software under the GNU General Public
License (>=v2). Read the file COPYING that comes with GRASS
for details.

:authors: Soeren Gebbert
"""

import os
from pathlib import Path

from grass.gunittest.case import TestCase
from grass.gunittest.gmodules import SimpleModule
from grass.gunittest.utils import silent_rmtree


class testRaster3dExtraction(TestCase):
    mapsets_to_remove = []
    outfile = "rast3dlist.txt"

    @classmethod
    def setUpClass(cls):
        gisenv = SimpleModule("g.gisenv", get="MAPSET")
        TestCase.runModule(gisenv, expecting_stdout=True)
        cls.old_mapset = gisenv.outputs.stdout.strip()
        os.putenv("GRASS_OVERWRITE", "1")
        for i in range(1, 5):
            mapset_name = "test3d%i" % i
            cls.runModule("g.mapset", flags="c", mapset=mapset_name)
            cls.mapsets_to_remove.append(mapset_name)
            cls.runModule("g.region", s=0, n=80, w=0, e=120, b=0, t=50, res=10, res3=10)
            # Use always the current mapset as temporal database
            cls.runModule("r3.mapcalc", expression="a1 = 100")
            cls.runModule("r3.mapcalc", expression="a2 = 200")
            cls.runModule("r3.mapcalc", expression="a3 = 300")
            # Create the temporal database
            cls.runModule("t.connect", flags="d")
            cls.runModule("t.info", flags="d")
            cls.runModule(
                "t.create",
                type="str3ds",
                temporaltype="absolute",
                output="A",
                title="A test3d",
                description="A test3d",
            )
            cls.runModule(
                "t.register",
                flags="i",
                type="raster_3d",
                input="A",
                maps="a1,a2,a3",
                start="2001-01-01",
                increment="%i months" % i,
            )

        # Add the new mapsets to the search path
        for mapset in cls.mapsets_to_remove:
            cls.runModule("g.mapset", mapset=mapset)
            cls.runModule(
                "g.mapsets", operation="add", mapset=",".join(cls.mapsets_to_remove)
            )

    @classmethod
    def tearDownClass(cls):
        gisenv = SimpleModule("g.gisenv", get="GISDBASE")
        cls.runModule(gisenv, expecting_stdout=True)
        gisdbase = gisenv.outputs.stdout.strip()
        gisenv = SimpleModule("g.gisenv", get="LOCATION_NAME")
        cls.runModule(gisenv, expecting_stdout=True)
        location = gisenv.outputs.stdout.strip()
        cls.runModule("g.mapset", mapset=cls.old_mapset)
        for mapset_name in cls.mapsets_to_remove:
            mapset_path = os.path.join(gisdbase, location, mapset_name)
            silent_rmtree(mapset_path)

    def test_tlist(self):
        self.runModule("g.mapset", mapset="test3d1")

        list_string = """A|test3d1|2001-01-01 00:00:00|2001-04-01 00:00:00|3
                                A|test3d2|2001-01-01 00:00:00|2001-07-01 00:00:00|3
                                A|test3d3|2001-01-01 00:00:00|2001-10-01 00:00:00|3
                                A|test3d4|2001-01-01 00:00:00|2002-01-01 00:00:00|3"""

        t_list = SimpleModule(
            "t.list",
            quiet=True,
            columns=["name", "mapset,start_time", "end_time", "number_of_maps"],
            type="str3ds",
            where='name = "A"',
        )
        self.assertModule(t_list)

        out = t_list.outputs["stdout"].value

        for a, b in zip(list_string.split("\n"), out.split("\n")):
            self.assertEqual(a.strip(), b.strip())

        t_list = SimpleModule(
            "t.list",
            quiet=True,
            columns=["name", "mapset,start_time", "end_time", "number_of_maps"],
            type="str3ds",
            where='name = "A"',
            output=self.outfile,
        )
        self.assertModule(t_list)
        self.assertFileExists(self.outfile)
        read_data = Path(self.outfile).read_text()
        for a, b in zip(list_string.split("\n"), read_data.split("\n")):
            self.assertEqual(a.strip(), b.strip())
        # self.assertLooksLike(reference=read_data, actual=list_string)
        if os.path.isfile(self.outfile):
            os.remove(self.outfile)

    def test_trast_list(self):
        self.runModule("g.mapset", mapset="test3d1")

        list_string = """a1|test3d1|2001-01-01 00:00:00|2001-02-01 00:00:00
                                a2|test3d1|2001-02-01 00:00:00|2001-03-01 00:00:00
                                a3|test3d1|2001-03-01 00:00:00|2001-04-01 00:00:00"""

        trast_list = SimpleModule(
            "t.rast3d.list", quiet=True, flags="s", input="A@test3d1"
        )
        self.assertModule(trast_list)

        out = trast_list.outputs["stdout"].value

        for a, b in zip(list_string.split("\n"), out.split("\n")):
            self.assertEqual(a.strip(), b.strip())

        list_string = """a1|test3d2|2001-01-01 00:00:00|2001-03-01 00:00:00
                                a2|test3d2|2001-03-01 00:00:00|2001-05-01 00:00:00
                                a3|test3d2|2001-05-01 00:00:00|2001-07-01 00:00:00"""

        trast_list = SimpleModule(
            "t.rast3d.list", quiet=True, flags="s", input="A@test3d2"
        )
        self.assertModule(trast_list)

        out = trast_list.outputs["stdout"].value

        for a, b in zip(list_string.split("\n"), out.split("\n")):
            self.assertEqual(a.strip(), b.strip())

        list_string = """a1|test3d3|2001-01-01 00:00:00|2001-04-01 00:00:00
                                a2|test3d3|2001-04-01 00:00:00|2001-07-01 00:00:00
                                a3|test3d3|2001-07-01 00:00:00|2001-10-01 00:00:00"""

        trast_list = SimpleModule(
            "t.rast3d.list", quiet=True, flags="s", input="A@test3d3"
        )
        self.assertModule(trast_list)

        out = trast_list.outputs["stdout"].value

        for a, b in zip(list_string.split("\n"), out.split("\n")):
            self.assertEqual(a.strip(), b.strip())

        list_string = """a1|test3d4|2001-01-01 00:00:00|2001-05-01 00:00:00
                                a2|test3d4|2001-05-01 00:00:00|2001-09-01 00:00:00
                                a3|test3d4|2001-09-01 00:00:00|2002-01-01 00:00:00"""

        trast_list = SimpleModule(
            "t.rast3d.list", quiet=True, flags="s", input="A@test3d4"
        )
        self.assertModule(trast_list)

        out = trast_list.outputs["stdout"].value

        for a, b in zip(list_string.split("\n"), out.split("\n")):
            self.assertEqual(a.strip(), b.strip())

        trast_list = SimpleModule(
            "t.rast3d.list",
            quiet=True,
            flags="s",
            input="A@test3d4",
            output=self.outfile,
        )
        self.assertModule(trast_list)
        self.assertFileExists(self.outfile)
        read_data = Path(self.outfile).read_text()
        for a, b in zip(list_string.split("\n"), read_data.split("\n")):
            self.assertEqual(a.strip(), b.strip())
        if os.path.isfile(self.outfile):
            os.remove(self.outfile)

    def test_strds_info(self):
        self.runModule("g.mapset", mapset="test3d4")
        tinfo_string = """id=A@test3d1
                                    name=A
                                    mapset=test3d1
                                    start_time='2001-01-01 00:00:00'
                                    end_time='2001-04-01 00:00:00'
                                    granularity='1 month'"""

        info = SimpleModule("t.info", flags="g", type="str3ds", input="A@test3d1")
        self.assertModuleKeyValue(
            module=info, reference=tinfo_string, precision=2, sep="="
        )

        self.runModule("g.mapset", mapset="test3d3")
        tinfo_string = """id=A@test3d2
                                    name=A
                                    mapset=test3d2
                                    start_time='2001-01-01 00:00:00'
                                    end_time='2001-07-01 00:00:00'
                                    granularity='2 months'"""

        info = SimpleModule("t.info", flags="g", type="str3ds", input="A@test3d2")
        self.assertModuleKeyValue(
            module=info, reference=tinfo_string, precision=2, sep="="
        )

        self.runModule("g.mapset", mapset="test3d2")
        tinfo_string = """id=A@test3d3
                                    name=A
                                    mapset=test3d3
                                    start_time='2001-01-01 00:00:00'
                                    end_time='2001-10-01 00:00:00'
                                    granularity='3 months'"""

        info = SimpleModule("t.info", flags="g", type="str3ds", input="A@test3d3")
        self.assertModuleKeyValue(
            module=info, reference=tinfo_string, precision=2, sep="="
        )

        self.runModule("g.mapset", mapset="test3d1")
        tinfo_string = """id=A@test3d4
                                    name=A
                                    mapset=test3d4
                                    start_time='2001-01-01 00:00:00'
                                    end_time='2002-01-01 00:00:00'
                                    granularity='4 months'"""

        info = SimpleModule("t.info", flags="g", type="str3ds", input="A@test3d4")
        self.assertModuleKeyValue(
            module=info, reference=tinfo_string, precision=2, sep="="
        )

    def test_raster_info(self):
        self.runModule("g.mapset", mapset="test3d3")
        tinfo_string = """id=a1@test3d1
                                name=a1
                                mapset=test3d1
                                temporal_type=absolute
                                start_time='2001-01-01 00:00:00'
                                end_time='2001-02-01 00:00:00'"""

        info = SimpleModule("t.info", flags="g", type="raster_3d", input="a1@test3d1")
        self.assertModuleKeyValue(
            module=info, reference=tinfo_string, precision=2, sep="="
        )

        tinfo_string = """id=a1@test3d2
                                name=a1
                                mapset=test3d2
                                temporal_type=absolute
                                start_time='2001-01-01 00:00:00'
                                end_time='2001-03-01 00:00:00'"""

        info = SimpleModule("t.info", flags="g", type="raster_3d", input="a1@test3d2")
        self.assertModuleKeyValue(
            module=info, reference=tinfo_string, precision=2, sep="="
        )

        tinfo_string = """id=a1@test3d3
                                name=a1
                                mapset=test3d3
                                temporal_type=absolute
                                start_time='2001-01-01 00:00:00'
                                end_time='2001-04-01 00:00:00'"""

        info = SimpleModule("t.info", flags="g", type="raster_3d", input="a1@test3d3")
        self.assertModuleKeyValue(
            module=info, reference=tinfo_string, precision=2, sep="="
        )

        tinfo_string = """id=a1@test3d4
                                name=a1
                                mapset=test3d4
                                temporal_type=absolute
                                start_time='2001-01-01 00:00:00'
                                end_time='2001-05-01 00:00:00'"""

        info = SimpleModule("t.info", flags="g", type="raster_3d", input="a1@test3d4")
        self.assertModuleKeyValue(
            module=info, reference=tinfo_string, precision=2, sep="="
        )


if __name__ == "__main__":
    from grass.gunittest.main import test

    test()
