from match_sequence import MatchSequence
from standard_action import StandardAction
from frame import Frame
from special_count.jump import JumpState
from special_count.bent_leg import BentLeg


class ActionRecognizer(object):

    def __init__(self, name, cfg, detector, analyzer):
        self.standard_action = StandardAction(name, cfg)
        self.analyzer = analyzer
        self.detector = detector

        self.count_detector = self.init_count()
        self.sequences = self.init_seqs(cfg)

    def init_seqs(self, cfg):
        standard_actions = self.standard_action.get_trans()
        return [MatchSequence(i, cfg, standard_actions[i]) for i in range(4)]

    def init_count(self):
        if self.standard_action.rec_type == 0:
            return BentLeg()
        else:
            return JumpState(self.standard_action.name)

    def match(self, video, time_limit=None):
        # 遍历每一帧
        for ori, frame_idx in video:
            # 预测
            pose_dic, angle_map = self.detector.pre_one_and_angle(ori)
            if pose_dic is None:
                continue
            self.count_detector.get_point(pose_dic, angle_map, frame_idx)
            for seq in self.sequences:
                seq.credit(Frame(frame_idx, pose_dic, angle_map))
        count = self.count_detector.get_count()
        score = self.get_score()
        return score, count

    def get_score(self):
        res = []
        for seq in self.sequences:
            res.append(seq.final_res())
        print(res)
        index = 0 if self.standard_action.rec_type == 0 else 1
        return max(i[index] for i in res)

    def clear(self):
        pass
