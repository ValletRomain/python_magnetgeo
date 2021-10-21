#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
Provides definition for Bitter:

* Geom data: r, z
* Model Axi: definition of helical cut (provided from MagnetTools)
* Model 3D: actual 3D CAD
"""

import json
import yaml
from . import deserialize

from . import ModelAxi

class Bitter(yaml.YAMLObject):
    """
    name :
    r :
    z :

    axi :
    """

    yaml_tag = 'Bitter'

    def __init__(self, name, r=[], z=[], axi=ModelAxi.ModelAxi()):
        """
        initialize object
        """
        self.name = name
        self.r = r
        self.z = z
        self.axi = axi

    def __repr__(self):
        """
        representation of object
        """
        return "%s(name=%r, r=%r, z=%r, axi=%r)" % \
               (self.__class__.__name__,
                self.name,
                self.r,
                self.z,
                self.axi
               )

    def dump(self):
        """
        dump object to file
        """
        try:
            ostream = open(self.name + '.yaml', 'w')
            yaml.dump(self, stream=ostream)
            ostream.close()
        except:
            raise Exception("Failed to Bitter dump")

    def load(self):
        """
        load object from file
        """
        data = None
        try:
            istream = open(self.name + '.yaml', 'r')
            data = yaml.load(stream=istream)
            istream.close()
        except:
            raise Exception("Failed to load Bitter data %s.yaml"%self.name)

        self.name = data.name
        self.r = data.r
        self.z = data.z
        self.axi = data.axi

    def to_json(self):
        """
        convert from yaml to json
        """
        return json.dumps(self, default=deserialize.serialize_instance, sort_keys=True, indent=4)


    def from_json(self, string):
        """
        convert from json to yaml
        """
        return json.loads(string, object_hook=deserialize.unserialize_object)

    def write_to_json(self):
        """
        write from json file
        """
        ostream = open(self.name + '.json', 'w')
        jsondata = self.to_json()
        ostream.write(str(jsondata))
        ostream.close()

    def read_from_json(self):
        """
        read from json file
        """
        istream = open(self.name + '.json', 'r')
        jsondata = self.from_json(istream.read())
        print (type(jsondata))
        istream.close()

    def get_Nturns(self):
        """
        returns the number of turn
        """
        return self.axi.get_Nturns()

def Bitter_constructor(loader, node):
    """
    build an bitter object
    """
    values = loader.construct_mapping(node)
    name = values["name"]
    r = values["r"]
    z = values["z"]
    axi = values["axi"]

    return Bitter(name, r, z, axi)

yaml.add_constructor(u'!Bitter', Bitter_constructor)

#
# To operate from command line

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of the bitter model to be stored", type=str, nargs='?' )
    parser.add_argument("--tojson", help="convert to json", action='store_true')
    args = parser.parse_args()

    if not args.name:
        bitter = Bitter("ttt", [1, 2],[-1, 1], True)
        bitter.dump()
    else:
        with open(args.name, 'r') as f:
            bitter =  yaml.load(f)
            print (bitter)

    if args.tojson:
        bitter.write_to_json()
