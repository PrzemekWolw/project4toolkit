import os
import matplotlib.pyplot as plt
from struct import unpack

class NodeParser:
    def __init__(self):
        self.carnodes = []
        self.boatpathlinknodes = []
        self.mCarpathlinks = []
        
    def load_nod_files(self, path):
        with open(path, 'rb') as self.path:
            header = self.path.read(8)
            self.path.seek(0)
            self.mPathnodes = [{'x': 0, 'y': 0, 'unk1': 0, 'unk2': 0, 'speed_limit': 0, 'flags': 0, 'unk4': False} for i in range(int(unpack("I", self.path.read(4))[0] / 16))]
            for i in range(len(self.mPathnodes)):
                self.mPathnodes[i]['x'] = float(unpack('h', self.path.read(2))[0]) / 8.0
                self.mPathnodes[i]['y'] = float(unpack('h', self.path.read(2))[0]) / 8.0
                self.mPathnodes[i]['z'] = float(unpack('h', self.path.read(2))[0]) / 128.0
                self.mPathnodes[i]['speed_limit'] = unpack('B', self.path.read(1))[0]
                self.mPathnodes[i]['width'] = float(unpack('b', self.path.read(1))[0]) / 8.0
                self.mPathnodes[i]['areaID'] = unpack('h', self.path.read(2))[0]
                self.mPathnodes[i]['nodeID'] = unpack('h', self.path.read(2))[0]
                self.mPathnodes[i]['middleX'] = float(unpack('h', self.path.read(2))[0]) / 8.0
                self.mPathnodes[i]['middleY'] = float(unpack('h', self.path.read(2))[0]) / 8.0
                self.path.seek(6, 1)
            self.carnodes.extend(self.mPathnodes)

    def seperate_nodes(self, odict_path_files):
        for path_file in odict_path_files:
            if path_file.endswith('.nod'):
                self.load_nod_files(path_file)

    def read_carpathlinks(self):
        if len(self.mCarpathlinks) != self.mHeader['NumCarPathLinks']:
            self.path.seek(self.___offset + (self.mHeader['NumNodes'] * 32), 0)
            for i in range(self.mHeader['NumCarPathLinks']):
                self.mCarpathlinks.append({})
                self.mCarpathlinks[i]['targetArea'] = unpack('h', self.path.read(2))[0]
                self.mCarpathlinks[i]['targetNode'] = unpack('h', self.path.read(2))[0]
                flags = unpack('B', self.path.read(1))[0]
                self.mCarpathlinks[i]['trafficLightBehaviour'] = flags & 3
                self.mCarpathlinks[i]['isTrainCrossing'] = (flags >> 2) & 1
                flags = unpack('B', self.path.read(1))[0]
                self.mCarpathlinks[i]['numLeftLanes'] = flags & 7
                self.mCarpathlinks[i]['numRightLanes'] = (flags >> 3) & 7
                self.mCarpathlinks[i]['trafficLightDirection'] = (flags >> 4) & 1
                self.mCarpathlinks[i]['length'] = unpack('b', self.path.read(1))[0] / 8
                flags = unpack('B', self.path.read(1))[0]
        return self.mCarpathlinks            
    def export_nodes_to_text_file(self, filename):
        with open(filename, 'w') as f:
            for node in self.carnodes:
                f.write("Node data: x:{} y:{} z:{} speed_limit:{} width:{} length:{} leftlanes{} rightlanes{} areaID{} targetArea nodeID{} targetNode{}\n".format(node['x'], node['y'], node['z'], node['speed_limit'], node['width'], node['length'], node['numLeftLanes'], node['numRightLanes'], node['areaID'], node['targetArea'], node['nodeID'], node['targetNode']))




if __name__ == '__main__':
    parser = NodeParser()
    odict_path_files = [f for f in os.listdir() if os.path.isfile(f)]
    parser.seperate_nodes(odict_path_files)
    parser.export_nodes_to_text_file("nodes.txt")
    
