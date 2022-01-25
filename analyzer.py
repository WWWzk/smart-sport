# class Analyzer(object):
#     def __init__(self):
#         self.trans = []
#         self.endure = []
#         self.beta1 = 0.9
#         self.beta2 = 0.9
#
#     def analyze(self, container, standard_frames):
#         score = self.get_total_score(container)
#         frames = [f[0] for f in container.matched_frame]
#         reasons = []
#         for frame_x, frame_y in zip(frames, standard_frames):
#             standard_angles = frame_y.get_angles()
#             angles = frame_x.get_angles()
#
#             diffs = {key: abs(standard_angles[key] - angles[key]) for key in angles if key in standard_angles}
#             k = sorted(diffs.keys(), key=lambda k: diffs[k], reverse=True)[0]
#             reason = [k, standard_angles[k], angles[k]]
#             reasons.append(reason)
#         # for idx in self.endure:
#         #     reasons[idx].append('动作持续时间较短')
#         #
#         # for idx, idy in self.trans:
#         #     reasons[idx].append('与第%d个动作切换时间太快'%idy)
#         #     reasons[idy].append('与第%d个动作切换时间太快' % idx)
#         return score, reasons
#
#     def get_total_score(self, container):
#         scores = [t[1] for t in container.matched_frame]
#         if len(container.action_endure) > 0:
#             frame_endure = container.endure_analysis()
#             for i in range(len(frame_endure)):
#                 edr_time, need_time = frame_endure[i]
#                 if need_time:
#                     portion = edr_time / need_time if edr_time < need_time else 1
#                     eta = self.beta1 + (1 - self.beta1) * portion
#                     scores[i] *= eta
#                     self.endure.append(i)
#         if len(container.time_transfer_require) > 0:
#             transfer_times = container.transfer_analysis()
#             for t in transfer_times:
#                 for idx, idy, dur_time, real_time in t:
#                     portion = real_time / dur_time if real_time < dur_time else 1
#                     eta = self.beta2 + (1 - self.beta2) * portion
#                     scores[idx] *= eta
#                     scores[idy] *= eta
#                     self.trans.append((idx, idy))
#
#         return sum(scores) / len(scores)
#
#     def clear(self):
#         self.trans.clear()
#         self.endure.clear()

class ActionAnalyzer(object):

    def analyze(self, aspect, containers, standard_action):
        matched_frame = containers[aspect].matched_frame
        rst = self.partition(standard_action.size, matched_frame)

        standard_frames = standard_action.frames[aspect]
        reasons = {}
        max_score = 0
        min_score = 1
        for frames in rst:
            score = sum(item[1] for item in frames) / len(frames)
            reason = self.get_reason(frames, standard_frames)
            if score > max_score:
                reasons['max'] = reason
                reasons['max_score'] = score
                max_score = score
            if score < min_score:
                reasons['min'] = reason
                reasons['min_score'] = score
                min_score = score
        return reasons

    def get_reason(self, matched_frames, standard_frames):
        reasons = {}
        for f_a, f_b in zip(matched_frames, standard_frames):
            angles = f_a[0].get_angles()
            score_angles = f_b.angle_thresholds.keys()
            score_angles = {k: angles[k][0] for k in score_angles}
            reasons[f_a[0].order] = score_angles
        return reasons

    def partition(self, size, matched_frame):
        i = 0
        length = len(matched_frame)
        rst = []
        while i < length:
            temp = []
            for j in range(size):
                if i < length and j == matched_frame[i][2]:
                    temp.append(matched_frame[i])
                    i += 1
                else:
                    break
            if len(temp) == size:
                rst.append(temp)
        return rst

