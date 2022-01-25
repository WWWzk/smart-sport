import logging

from attribute_container import AttributeContainer
from frame import Frame
import state_machine
from standard_action import StandardAction
from static_similarity import angle_similarity_almost
import math
from util import transform
import time_limiter

IF_LOG = False


class MatchSequence(object):

    def __init__(self, seq_id, cfg, standard_action: StandardAction):
        self.seq_id = seq_id
        self.matched = AttributeContainer(cfg)
        self.standard_action = standard_action

        states = standard_action.states
        repeat = standard_action.repeat
        self.state_machines = state_machine.SimpleStateMachine(states, repeat)

        # 日志部分调参部分
        if IF_LOG:
            self.log = self.gen_log()

        self.cur_id = -1
        self.count = 0
        # 为计数添加的识别帧列表
        if standard_action.rec_type == 0:
            self.contains_frame = [False for i in range(states[-1] + 1)]
        else:
            self.contains_frame = [False for i in range(repeat[0][1] + 1)]
        self.score_list = []

        self.matchId_list = []

    def credit(self, frame: Frame):
        self._match_frame(frame)

    def get_score(self):
        # 先计算分数
        container = self.matched
        scores = [t[1] for t in container.matched_frame]
        frame_num = len(self.contains_frame)
        score = sum(scores) / frame_num
        self.score_list.append(score)
        # 统计是否完成一次完整动作
        self.count += all(self.contains_frame)
        self.contains_frame = [False for i in range(frame_num)]
        # 清空当前分数
        container.matched_frame = container.matched_frame[-1:]

    def _get_score(self, is_last=False):
        # 先计算分数
        container = self.matched
        scores = [t[1] for t in container.matched_frame]
        frame_num = len(self.contains_frame)
        scores_num = len(scores)

        if scores_num == frame_num:
            score = sum(scores) / frame_num
        else:
            score = sum(scores) / scores_num

        self.score_list.append(score)
        # 统计是否完成一次完整动作
        if is_last:
            self.count += all(self.contains_frame)
        else:
            # if sum(self.contains_frame) >= frame_num * 0.5:
            if sum(self.contains_frame) >= 1:
                self.count += 1

        # 将contains_frame更新

        self.contains_frame = [False for i in range(frame_num)]
        # 清空当前分数
        container.matched_frame = container.matched_frame[-1:]

    def gen_log(self):
        name = self.standard_action.name
        log_path = 'log/' + name + '-' + str(self.seq_id) + '.log'
        logger = logging.getLogger(name + str(self.seq_id))
        logger.setLevel(logging.INFO)

        # my_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        my_format = logging.Formatter('%(message)s')
        file_handler = logging.FileHandler(filename=log_path, encoding='utf-8')
        file_handler.setFormatter(my_format)

        logger.addHandler(file_handler)
        return logger

    # def count(self, video, time_limit=None):
    #     limiter = None
    #     if time_limit:
    #         limiter = time_limiter.TimeLimiter(time_limit)
    #     count = 0
    #     for ori, frame_idx in video:
    #         if limiter is not None and not limiter.if_continue(frame_idx):
    #             break
    #         pose_dic, angle_map = self.detector.pre_one_and_angle(transform(ori))
    #         if pose_dic is None:
    #             continue
    #         cur_frame = Frame(frame_idx, pose_dic, angle_map)
    #         is_matched, aspect = self._match_frame(cur_frame)
    #         # 设置动作起始帧的帧号
    #         if is_matched and limiter is not None and len(self.matched[aspect].matched_frame) == 2:
    #             limiter.set_start_time(self.matched[aspect].last_matched_frame[0].order)
    #         if is_matched and self.state_machines[aspect].if_reached_loop_end():
    #             # 重置一下状态
    #             self.state_machines[aspect].reinitialize()
    #             # 判断是否动作完整进行计数
    #             if all(self.contains_frame):
    #                 count += 1
    #             self.contains_frame = [False for i in range(len(self.contains_frame))]
    #     return count

    def _match_frame(self, frame):
        match_log = str(frame.order) + ': '

        # 该过程要匹配所有关键帧
        for state_id in range(len(self.contains_frame)):
            standard_frame = self.standard_action.frames[state_id]
            matched, score, vital_diffs = angle_similarity_almost(frame, standard_frame)
            if IF_LOG:
                if_match = '匹配成功 ' if matched else '匹配失败 '
                match_log += if_match + str(state_id) + ' ' + str(vital_diffs) + '\n'
            if matched:
                self.check_frame(state_id, score, frame)
                break
        if IF_LOG:
            self.log.info(match_log)

    def check_frame(self, state_id, score, frame):
        if state_id == self.cur_id:
            # 更新分数
            if score > self.matched.matched_frame[-1][1]:
                self.matched.update(frame, score, state_id)
        elif state_id > self.cur_id:
            # 继续往下匹配
            self.matched.add(frame, score, state_id)
        else:
            # 返回重新匹配
            self._get_score()
            self.matched.add(frame, score, state_id)
        self.contains_frame[state_id] = True
        self.cur_id = state_id

    def final_res(self):
        if self.matched.matched_frame:
            self._get_score(is_last=True)
        sc = max(self.score_list) if self.score_list else 0

        self.clear()
        return [sc, self.count]

    def clear(self):
        self.state_machines.reinitialize()
        self.matched.clear()
        self.score_list.clear()
        self.contains_frame.clear()
