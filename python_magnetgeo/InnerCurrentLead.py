#!/usr/bin/env python3
# encoding: UTF-8

"""
Provides Inner and OuterCurrentLead class
"""

import json
import yaml
from deserialize import *

class InnerCurrentLead(yaml.YAMLObject):
    """
    name :
    r : [R0, R1]
    h :
    holes: [H_Holes, Shift_from_Top, Angle_Zero, Angle, Angular_Position, N_Holes]
    support: [R2, DZ]
    fillet:
    """
    yaml_tag = 'InnerCurrentLead'

    def __init__(self, name="None", r=[], h=0., holes=[], support=[], fillet=False):
        """
        initialize object
        """
        self.name = name
        self.r = r
        self.h = h
        self.holes = holes
        self.support = support
        self.fillet = fillet

    def __repr__(self):
        """
        representation of object
        """
        return "%s(name=%r, r=%r, h=%r, holes=%r, support=%r, fillet=%r)" % \
               (self.__class__.__name__,
                self.name,
                self.r,
                self.h,
                self.holes,
                self.support,
                self.fillet
               )

    def dump(self):
        """
        dump object to file
        """
        try:
            yaml.dump(self, open(self._name + '.yaml', 'w'))
        except:
            raise Exception("Failed to dump InnerCurrentLead data")

    def load(self):
        """
        load object from file
        """
        data = None
        try:
            istream = open(self._name + '.yaml', 'r')
            data = yaml.load(istream)
            istream.close()
        except:
            raise Exception("Failed to load InnerCurrentLead data %s.yaml"%self._name)

        self._name = data.name
        self.r = data.r
        self.h = data.h
        self.holes = data.holes
        self.support = data.support
        self.fillet = data.fillet

    def to_json(self):
        """
        convert from yaml to json
        """
        return json.dumps(self, default=deserialize.serialize_instance, \
                          sort_keys=True, indent=4)

    def from_json(self, string):
        """
        convert from json to yaml
        """
        print ("from_json(%s)" % string)
        return json.loads(string, object_hook=deserialize.unserialize_object)

    def write_to_json(self):
        """
        write from json file
        """
        jsondata = self.to_json()
        try:
            ofile = open(self.name + '.json', 'w')
            ofile.write(str(jsondata))
            ofile.close()
        except:
            raise Exception("Failed to write to %s.json"%self.name)

    def read_from_json(self):
        """
        read from json file
        """
        istream = open(self.name + '.json', 'r')
        jsondata = self.from_json(istream.read())
        istream.close()
        print (type(jsondata))
        print (jsondata.name)
        try:
            print (jsondata.r)
        except:
            pass
        print (jsondata.h)
        print (jsondata.holes)
        print (jsondata.support)
        print (jsondata.fillet)

def InnerCurrentLead_constructor(loader, node):
    """
    build an inner object
    """
    values = loader.construct_mapping(node)
    name = values["name"]
    r = values["r"]
    h = values["h"]
    holes = values["holes"]
    support = values["support"]
    fillet = values["fillet"]
    return InnerCurrentLead(_name, r, h, holes, support, fillet)


yaml.add_constructor(u'!InnerCurrentLead', InnerCurrentLead_constructor)

#
# To operate from command line

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of the inner currentlead model to be stored", type=str, nargs='?' )
    parser.add_argument("--tojson", help="convert to json", action='store_true')
    args = parser.parse_args()

    if not args.name:
        r = [38.6/2., 48.4/2.]
        h = 480.
        bars = [123, 12, 90, 60, 45, 3]
        support = [24.2, 0]
        lead = InnerCurrentLead('Inner', r, 480., bars, support, False)
        lead.dump()
    else:    
        try:
            lead = yaml.load(open(args.name, 'r'))
            print ("lead=", lead)
        except:
            print ("Failed to load Inner currentlead definition from %s" % args.name)

    if args.tojson:
        lead.write_to_json()
