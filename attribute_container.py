class AttributeContainer(object):

    def __init__(self, cfg):
        self.time_transfer_require = cfg['transition']
        self.action_endure = cfg['hold']
        self.total_endure = cfg['whole_time']

        self.matched_frame = []

        self.first_matched_frame = []
        self.last_matched_frame = []
        self.frame_endure = []
        self.diff_list = [0]
        self.total_time = 0
        self.fps = 25
        self.base = 0

    def add(self, frame, score, matched_id, is_endure=False):
        if not is_endure or self.total_endure == 0 or (frame.order - self.base) / self.fps < self.total_endure:
            self.first_matched_frame.append(frame)
            self.last_matched_frame.append(frame)
            self.matched_frame.append((frame, score, matched_id))
            self.frame_endure.append(1 / self.fps)
            self.diff_list.append(frame.order - sum(self.diff_list))
            return True
        else:
            return False

    def update_endure(self, frame):
        old_frame = self.first_matched_frame[-1]
        self.last_matched_frame[-1] = frame
        self.frame_endure[-1] = (frame.order - old_frame.order) / self.fps

    def update(self, frame, score, matched_id, is_endure=False):
        if not is_endure or self.total_endure == 0 or (frame.order - self.base) / self.fps < self.total_endure:
            old_frame = self.matched_frame[-1][0]
            self.matched_frame[-1] = (frame, score, matched_id)
            # self.frame_endure[-1] += (frame.order - old_frame.order) / self.fps
            self.diff_list[-1] += frame.order - old_frame.order

    def endure_analysis(self):
        for i in range(len(self.matched_frame)):
            self.frame_endure[i] = (self.frame_endure[i], None)
            for x, dur_time in self.action_endure:
                if self.matched_frame[i][2] == x:
                    self.frame_endure[i] = (self.frame_endure[i][0], dur_time)
                    break
        return self.frame_endure

    def transfer_analysis(self):
        transfer_times = []
        for x, y, dur_time in self.time_transfer_require:
            matched = self.matched_frame
            start = end = 0
            start_index = end_index = 0
            temp = []
            for i, (frame, _, matched_id) in enumerate(matched):
                if matched_id == x:
                    start = frame.order
                    start_index = i
                if matched_id == y:
                    end = frame.order
                    end_index = i
                    temp.append((start_index, end_index, dur_time, (end - start) / self.fps))
            transfer_times.append(temp)
        return transfer_times

    def clear(self):
        self.matched_frame = []
        self.first_matched_frame = []
        self.last_matched_frame = []
        self.frame_endure = []
        self.diff_list = [0]
        self.base = 0
