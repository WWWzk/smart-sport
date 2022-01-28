from frame import Frame
from util import get_towards


def angle_similarity_almost(frame_x: Frame, frame_standard: Frame, eta=1):
    weights = frame_standard.angle_weights
    score_thresholds = frame_standard.angle_thresholds
    match_thresholds = frame_standard.vital_thresholds
    standard_angles = frame_standard.get_angles()
    angles = frame_x.get_angles()
    face_towards = get_towards(frame_x.bone_points)

    # diffs = {key: abs(standard_vital_angles[key][0] - angles[key][0])
    #          for key in angles if standard_angles[key][1] > confidence}
    diffs = {key: angles[key][0] - standard_angles[key][0] for key in standard_angles}
    vital_diffs = {key: diffs[key] for key in match_thresholds}
    # if len(vital_diffs) < len(standard_vital_angles):
    #     return False, None

    matched = sum((-match_thresholds[key][0] < vital_diffs[key] <= 0 or 0 < vital_diffs[key] < match_thresholds[key][1])
                  for key in vital_diffs) >= len(vital_diffs) * eta

    score_diffs = {key: diffs[key] for key in score_thresholds}
    sum_weight = sum(weights[key] for key in score_thresholds)
    weights = {key: weights[key] / sum_weight for key in score_thresholds}
    score = 0
    for key in score_thresholds:
        s = score_diffs[key]
        threshold = score_thresholds[key][1] if s > 0 else score_thresholds[key][0]
        s = abs(s)
        if angles[key][1] > 0.009:
            score += (1 - min(s, threshold) / threshold) * weights[key]
        else:
            score += 0.8*weights[key]
    return matched, score, vital_diffs
