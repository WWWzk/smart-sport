import matplotlib.pyplot as plt
import numpy as np


def moving_average(x, width):
    return np.convolve(x, np.ones(width), 'same') / width


def show_curve(positions):
    x = np.arange(0, len(positions))
    y = positions
    plt.plot(x, y, color='red', linewidth=1)
    plt.show()


if __name__ == '__main__':
    # pos = np.sin(np.arange(0, 2, 0.01))
    # show_curve(pos)
    from video_source import VideoSource
    from AlphaPose.AlphaDetector import AlphaDetector

    video_path = './4.mp4'
    vs = VideoSource(video_path, webcam=False)
    dt = AlphaDetector()
    positions = []
    ratio = []
    for ori, fid in vs:
        pose_dic = dt.pre_one(ori)
        if not pose_dic:
            continue
        positions.append(pose_dic['19'][1])
        ratio.append(pose_dic['19'][1] - pose_dic['18'][1])
        print(pose_dic['19'][1])
        print(pose_dic['18'][1] - pose_dic['19'][1])

    positions = np.array(positions)
    avg_positions = moving_average(positions, 3)

    ratio = np.array(ratio)
    velocitys = positions[1:] - positions[:-1]
    modified_ratio = (ratio[1:] + ratio[:-1]) / 2
    modified_velocitys = velocitys * (170 / modified_ratio)

    avg_velocity = moving_average(modified_velocitys, 3)
    show_curve(modified_velocitys)
    show_curve(avg_velocity)
    # show_curve(positions)
    # show_curve(avg_positions)
