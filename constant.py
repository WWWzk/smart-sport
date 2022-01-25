other_config = {
    "size": 3,
    # 面部朝向
    # front\back\left\right\up\down
    "face": ["front", "down", "up", "down", "up", "down"],
    # 角度的权重
    "0_angle_weights": {
        "l_elbow": 1 / 18,
        "r_elbow": 1 / 18,
        "l_armpit": 1 / 18,
        "r_armpit": 1 / 18,
        "two_leg": 1 / 18,
        "l_leg": 1 / 18,
        "r_leg": 1 / 18,
        "l_knee": 1 / 18,
        "r_knee": 1 / 18,
        "l_head": 1 / 18,
        "r_head": 1 / 18,
        "bow_head": 1 / 18,
        "l_wrist": 1 / 18,
        "r_wrist": 1 / 18,
        "l_foot": 1 / 18,
        "r_foot": 1 / 18,
        "l_hand": 1 / 18,
        "r_hand": 1 / 18
    },
    "1_angle_weights": {
        "l_elbow": 1 / 18,
        "r_elbow": 1 / 18,
        "l_armpit": 1 / 18,
        "r_armpit": 1 / 18,
        "two_leg": 1 / 18,
        "l_leg": 1 / 18,
        "r_leg": 1 / 18,
        "l_knee": 1 / 18,
        "r_knee": 1 / 18,
        "l_head": 1 / 18,
        "r_head": 1 / 18,
        "bow_head": 1 / 18,
        "l_wrist": 1 / 18,
        "r_wrist": 1 / 18,
        "l_foot": 1 / 18,
        "r_foot": 1 / 18,
        "l_hand": 1 / 18,
        "r_hand": 1 / 18
    },
    # 关键帧的权重
    "0_frame_weights": {
        "0": 0.0909090909090909,
        "1": 0.1818181818181818,
        "2": 0.1818181818181818,
        "3": 0.1818181818181818,
        "4": 0.1818181818181818,
        "5": 0.1818181818181818,
    },
    "1_frame_weights": {
        "0": 0.0909090909090909,
        "1": 0.1818181818181818,
        "2": 0.1818181818181818,
        "3": 0.1818181818181818,
        "4": 0.1818181818181818,
        "5": 0.1818181818181818,
    },
    # 角度的阈值
    "0_angle_thresholds": {
        "l_elbow": 10,
        "r_elbow": 10,
        "l_armpit": 10,
        "r_armpit": 10,
        "two_leg": 10,
        "l_leg": 10,
        "r_leg": 10,
        "l_knee": 10,
        "r_knee": 10,
        "l_head": 10,
        "r_head": 10,
        "bow_head": 10,
        "l_wrist": 10,
        "r_wrist": 10,
        "l_foot": 10,
        "r_foot": 10,
        "l_hand": 10,
        "r_hand": 10
    },
    "1_angle_thresholds": {
        "l_elbow": 10,
        "r_elbow": 10,
        "l_armpit": 10,
        "r_armpit": 10,
        "two_leg": 10,
        "l_leg": 10,
        "r_leg": 10,
        "l_knee": 10,
        "r_knee": 10,
        "l_head": 10,
        "r_head": 10,
        "bow_head": 10,
        "l_wrist": 10,
        "r_wrist": 10,
        "l_foot": 10,
        "r_foot": 10,
        "l_hand": 10,
        "r_hand": 10
    },
    # 视角的权重
    "aspect_weight": [0.5, 0.5],
    # frame_id帧需要持续endure_time秒
    "hold": [
        [
            0,
            4
        ],
        [
            1,
            2
        ],
        [
            2,
            1
        ], [3, 1], [4, 1], [5, 1]
    ],
    "transition": [[0, 1, 4], [1, 2, 2], [2, 3, 2], [3, 4, 2], [4, 5, 2]],
    "whole_time": 35,
    # 是否要判断上下
    "updown": True,
    # 是否要计算人体是垂直还是水平
    "rotate": False,
    # frame_id_start, frame_id_end
    "repeat": [
        [1, 5, 2]
    ]
}
