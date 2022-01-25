import copy

MAPPING = {}


def build_func(names):
    def outer(fn):
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)
        for name in names:
            MAPPING[name] = inner
        return inner
    return outer


def frame_trans(name, frame_x):
    rev_towards_angles, rev_action_angles = MAPPING[name]() if name in MAPPING else MAPPING['normal']()
    frame = frame_x
    towards_rev_action = copy.deepcopy(frame)
    rev_towards_action = copy.deepcopy(frame)
    rev_towards_rev_action = copy.deepcopy(frame)

    reverse_by_pair_list(towards_rev_action, rev_action_angles)
    reverse_by_pair_list(rev_towards_action, rev_towards_angles)
    reverse_by_pair_list(rev_towards_rev_action, rev_towards_angles + rev_action_angles)
    return [frame, towards_rev_action, rev_towards_action, rev_towards_rev_action]


def reverse_by_pair_list(frame, pair_list):
    for left, right in pair_list:
        # frame.bone_points[left], frame.bone_points[right] = frame.bone_points[right], frame.bone_points[left]
        frame.angles[left], frame.angles[right] = frame.angles[right], frame.angles[left]


@build_func(['抱膝提踵', 'normal'])
def trans_0():
    rev_towards_angles = [('l_elbow', 'r_elbow'), ('l_armpit', 'r_armpit')]
    rev_action_angles = [('l_waist_leg', 'r_waist_leg'), ('l_leg', 'r_leg'), ('l_knee', 'r_knee'), ('l_foot', 'r_foot')]
    return rev_towards_angles, rev_action_angles


@build_func(['原地弓步跳'])
def trans_1():
    rev_towards_angles = [('l_elbow', 'r_elbow'), ('l_armpit', 'r_armpit')]
    rev_action_angles = [('l_waist_leg', 'r_waist_leg'), ('l_leg', 'r_leg'), ('l_knee', 'r_knee')]
    return rev_towards_angles, rev_action_angles

