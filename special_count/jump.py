import json


def read_thres():
    cfg_dir = './data/211016/count_threshold.json'
    with open(cfg_dir, 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    return cfg


VIS_FLAG = False


class JumpState(object):
    count_thres = read_thres()

    def __init__(self, action_name):
        self.action_name = action_name

        self.key_point = []
        self.check_angle = {}

        self.first_peak = []
        self.first_peak_index = []
        self.second_peak = []

        self.threshold = self.count_thres[self.action_name]['threshold']
        self.frame_dis = self.count_thres[self.action_name]['frame_dis']

    def get_point(self, pose_dic: dict, angle_map: dict, idx: int):
        key_pose = self.count_thres[self.action_name]["key_point"]
        self.key_point.append(pose_dic[key_pose][1])
        check_map = self.count_thres[self.action_name]["check"]
        for ch in check_map.keys():
            if ch in self.check_angle:
                self.check_angle[ch].append(angle_map[ch][0])
            else:
                self.check_angle[ch] = []
                self.check_angle[ch].append(angle_map[ch][0])

    def first_count(self):
        length = len(self.key_point)
        points = self.key_point
        # 0下降
        # 1上升
        state_now = 0

        i = 1
        # 先找到可能帧
        while i < length:
            head_trend = points[i] - points[i - 1]
            state_pre = state_now
            state_now = 0 if head_trend > 0 else 1

            if state_now == 0 and state_pre == 1:
                print(str(i) + ': ' + str(points[i]))
                self.first_peak.append(points[i])
                self.first_peak_index.append(i)

            i += 1

    def second_count(self):
        threshold = self.threshold
        frame_dis = self.frame_dis
        min_y = min(self.first_peak)
        pre = -20
        for i in range(len(self.first_peak)):
            y = self.first_peak[i]
            if y - min_y < threshold and self.first_peak_index[i] - pre >= frame_dis:
                if not self.check(i):
                    continue
                self.second_peak.append(y)
                pre = self.first_peak_index[i]

    def check(self, index, thres=20):
        check = self.count_thres[self.action_name]["check"]
        for angle_name in self.check_angle:
            if abs(self.check_angle[angle_name][index] - check[angle_name]) < thres:
                return False
        return True

    def get_count(self):
        self.first_count()
        self.second_count()
        if VIS_FLAG:
            self.vis_point()
        ans = len(self.second_peak)
        self.re_init()
        return ans

    def re_init(self):
        self.key_point.clear()
        self.first_peak.clear()
        self.second_peak.clear()

    def vis_point(self):
        import matplotlib.pyplot as plt
        plt.plot(self.key_point)
        name = './data/fig/' + self.action_name + '.png'
        plt.savefig(name)
