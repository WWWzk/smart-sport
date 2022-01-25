import json

import cv2

from action_recognizer import ActionRecognizer
import analyzer
import video_source
from AlphaPose.AlphaDetector import AlphaDetector
from frame import Frame
from jump_counter import JumpCounter

detector = AlphaDetector()
single_analyzer = analyzer.ActionAnalyzer()
cfg_dir = './data/211016/'
with open(cfg_dir + '对照表.txt', 'r', encoding='utf8') as f:
    lines = [line.strip().split(' ') for line in f]
    mapping = {elem[1].strip(): elem[0].strip() for elem in lines}

para_path = cfg_dir + '%s/parameters.json'
data = {}
with open(cfg_dir + 'annotation.json', 'r', encoding='utf8') as f:
    cfg = json.load(f)
    for k in cfg:
        with open(para_path % k[:k.find('.')], 'r', encoding='utf8') as fin:
            para = json.load(fin)
        cfg[k].update(para)
        action = ActionRecognizer(k, cfg[k], detector, single_analyzer)
        data[k] = action


def match(name, video_path, webcam=False, time_limit=None):
    video = video_source.VideoSource(video_path, webcam)
    if name == '跳绳':
        c = JumpCounter()
        count = c.count(video)
        return count
    recognizer = data[mapping[name] + '.mp4']
    rst = recognizer.match(video, time_limit)
    # result = recognizer.report()
    return rst


# def match(name, video_path, webcam=False, time_limit=None):
#     video = VideoSource(video_path, webcam=webcam)
#     recognizer = data[name]
#     recognizer.clear()
#     output = []
#     recognizer.set_output(output)
#     limiter = None
#     if time_limit:
#         limiter = time_limiter.TimeLimiter(time_limit)
#         recognizer.set_time_limiter(limiter)
#
#     for ori, frame_idx in video:
#         cv2.imshow('frame', ori)
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break
#         # if frame_idx == 248:
#         #     cv2.imwrite('./2.png', ori)
#
#         if limiter is not None and not limiter.if_continue(frame_idx):
#             break
#         pose_dic, angle_map = detector.pre_one_and_angle(ori)
#         if pose_dic is None:
#             continue
#         frame = Frame(frame_idx, pose_dic, angle_map)
#         recognizer.match(frame)
#
#     output, reasons = recognizer.report()
#     return output, reasons


def classify_and_judge(video_path, webcam=False):
    video = video_source.VideoSource(video_path, webcam=webcam)
    global output, reasons
    output.clear()
    reasons.clear()

    for ori, frame_idx in video:
        cv2.imshow('frame', ori)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # if frame_idx == 248:
        #     cv2.imwrite('./2.png', ori)

        pose_dic, angle_map = detector.pre_one_and_angle(ori)
        if pose_dic is None:
            continue
        frame = Frame(frame_idx, pose_dic, angle_map)
        for name in data:
            action: ActionRecognizer = data[name]
            action.match(frame)
    print(output)
    print(reasons)
    for name in data:
        action = data[name]
        action.clear()


if __name__ == '__main__':
    video_path = r'E:\graduate\项目\智慧体育\smart_sport\data\AI体测产品练习视频\抱膝提踵-3.mp4'
    output = match('抱膝提踵', video_path, time_limit=None)
    print(output)
