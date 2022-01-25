from util import get_all_angle, get_towards


class Frame(object):

    def __init__(self, order, bone_points, angles=None, aspect=None, cfg=None):
        self.order = order
        self.aspect = aspect
        self.bone_points = bone_points
        self.angles = angles
        # self.face_towards = cfg['face_towards'] if cfg else None
        if cfg is not None:
            self.angle_thresholds = cfg['0_angle_thresholds'] if aspect == 0 else cfg['1_angle_thresholds']
            self.angle_weights = cfg['0_angle_weights'] if aspect == 0 else cfg['1_angle_weights']
            self.vital_thresholds = cfg['0_vital_thresholds'][order] if aspect == 0 else cfg['1_vital_thresholds'][order]
            # self.frame_weight = cfg['0_frame_weights'][str(order)] if aspect == 0 else cfg['1_frame_weights'][str(order)]

    def get_angles(self):
        if not self.angles:
            self.angles = get_all_angle(self.bone_points)
        return self.angles

    def get_face_towards(self):
        if not self.face_towards:
            self.face_towards = get_towards(self.bone_points)
        return self.face_towards
