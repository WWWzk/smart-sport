class BentLeg(object):

    def __init__(self):
        self.angle_left_leg = []
        self.index_l = []
        self.angle_right_leg = []
        self.index_r = []

        self.l_res = []
        self.r_res = []

    def get_point(self, pose_dic: dict, angle_dic: dict, idx: int):

        angle_l = angle_dic['l_leg']
        angle_r = angle_dic['r_leg']
        if angle_l[1] >= 0.008 and angle_l[0] <= 160:
            self.angle_left_leg.append(angle_l[0])
            self.index_l.append(idx)

        if angle_r[1] >= 0.008 and angle_r[0] <= 160:
            self.angle_right_leg.append(angle_r[0])
            self.index_r.append(idx)

    def lr_count(self, mod='left', threshold=50, frame_dis=30, action_dis=100):
        angles = self.angle_left_leg
        index = self.index_l
        if mod == 'right':
            angles = self.angle_right_leg
            index = self.index_r

        max_angle = max(angles)
        # lr_window 当两个值都不为-1 且差值超过frame_dis, 与上一个动作差action_dis 可以计数 并且清空该窗口
        left_window = -1
        right_window = -1
        next_loc = 0
        count = 0

        i = 0
        while i < len(angles):
            i += 1
            # 满足计数条件
            if left_window != -1 and right_window != -1 and right_window - left_window >= frame_dis:
                if mod == 'left':
                    self.l_res.append([left_window, right_window])
                else:
                    self.r_res.append([left_window, right_window])
                count += 1
                print(str(left_window) + '---' + str(right_window))
                left_window = -1
                right_window = -1

            if i == len(angles):
                break
            cur_state = -1
            if max_angle >= angles[i] >= max_angle-threshold:
                if angles[i] - angles[i-1] < 0:
                    cur_state = 0  # 角度变小的趋势
                else:
                    cur_state = 1  # 角度变大趋势

            if cur_state == -1:
                continue
            elif cur_state == 0:
                if left_window == -1:
                    if index[i] >= next_loc:
                        left_window = index[i]
                        next_loc = left_window + action_dis
            else:
                right_window = max([index[i], right_window])

        return count

    def get_count(self):
        print('左长度')
        print(len(self.angle_left_leg))
        print('右长度')
        print(len(self.angle_right_leg))
        l_n = self.lr_count()
        r_n = self.lr_count(mod='right')

        if l_n >= r_n:
            res = l_n
            res_list = self.l_res
        elif l_n < r_n:
            res = r_n
            res_list = self.r_res
        else:
            return l_n
        i = 0
        dis_list = []
        while i + 1 < len(res_list):
            dis_list.append(res_list[i+1][1] - res_list[i][1])
            i += 1

        return res - self.get_mid(dis_list)

    def get_mid(self, dis_list, threshold=30):
        length = len(dis_list)
        if length == 0:
            return 0
        tmp_list = sorted(dis_list)
        mid_num = tmp_list[int(length / 2)]
        i = 0
        res = 0
        while i < length:
            if mid_num - dis_list[i] > threshold:
                res += 1
                i += 1
            i += 1
        return res

    def re_init(self):
        self.angle_left_leg.clear()
        self.index_l.clear()
        self.angle_right_leg.clear()
        self.index_r.clear()
