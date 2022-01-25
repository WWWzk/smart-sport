from AlphaPose.AlphaDetector import AlphaDetector
from state_machine import *
from video_source import VideoSource


class JumpCounter(object):

    def __init__(self):
        self.cur_state = StillState()
        self.detector = AlphaDetector()
        self.standard_dis = 170
        self.positions = []
        self.velocities = [0]
        self.results = []

    def count(self, vs: VideoSource):
        '''计数接口，输入视频流， 返回计数结果
            目前无法检测是否具备绳子'''
        for ori, fid in vs:
            pose_dict = self.detector.pre_one(ori)
            if not pose_dict:
                continue
            self.update_info(pose_dict)
            last_state = self.cur_state
            self.cur_state = self.cur_state.next_state(self.velocities)
            if isinstance(last_state, UpState) and isinstance(self.cur_state, DownState):
                self.results.append((fid, self.velocities[-1]))
        return len(self.results)

    def update_info(self, pos_dict):
        '''更新人体位置、速度等信息'''
        # pos是髋关节骨骼点的位置
        pos = pos_dict['19'][1]
        self.positions.append(pos)
        if len(self.positions) > 1:
            # 计算相邻两帧的位置差距
            raw_velocity = pos - self.positions[-2]
            # 对人体大小进行归一化调整
            modified_velocity = raw_velocity * (self.standard_dis / (pos - pos_dict['18'][1]))
            self.velocities.append(modified_velocity)
        # 平滑函数曲线
        self.moving_avg()

    def moving_avg(self, width=3):
        '''移动平均计算'''
        if len(self.velocities) >= width:
            self.velocities[-1] = sum(self.velocities[-width:]) / width


if __name__ == '__main__':
    c = JumpCounter()
    video_path = '1.mp4'
    vs = VideoSource(video_path, webcam=False)
    count = c.count(vs)
    print(count)