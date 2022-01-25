import copy

from frame import Frame
import frame_trans


class StandardAction(object):

    def __init__(self, name, cfg):
        self.name = name
        self.rec_type = cfg['identification_type']
        self.size = cfg['size']
        self.frames = []

        if cfg['0']:
            for i in range(self.size):
                bone_points = cfg['0'][i]
                frame_angles = cfg['0_angle'][i]
                self.frames.append(Frame(i, bone_points, frame_angles, 0, cfg))
        else:
            for i in range(self.size):
                bone_points = cfg['1'][i]
                frame_angles = cfg['1_angle'][i]
                self.frames.append(Frame(i, bone_points, frame_angles, 1, cfg))

        self.repeat = cfg['repeat']
        self.states = cfg['frames']
        self.updown = cfg['updown']
        self.rotate = cfg['rotate']

    def copy(self):
        sa = copy.deepcopy(self)
        sa.frames.clear()
        return sa

    def get_trans(self):
        standard_trans = [self.copy() for i in range(4)]

        for frame in self.frames:
            trans_frames = frame_trans.frame_trans(self.name, frame)
            for i in range(4):
                standard_trans[i].frames.append(trans_frames[i])
        return standard_trans
