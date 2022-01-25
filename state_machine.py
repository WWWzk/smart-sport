class StateMachine(object):
    def __init__(self, states):
        self.states = ['START'] + states + ['END']
        self.length = len(states) + 2
        self.cur_state = 0
        self.next_state = 1
        # self.done = False

    def state_change(self, inp):
        raise NotImplemented

    def get_next_frame_id(self):
        if isinstance(self.next_state, tuple):
            frame_a, frame_b = self.states[self.next_state[0]], self.states[self.next_state[1]]
            frame_a = frame_a if isinstance(frame_a, int) else None
            frame_b = frame_b if isinstance(frame_b, int) else None
            return frame_a, frame_b
        else:
            next_frame = self.states[self.next_state]
            return next_frame if isinstance(next_frame, int) else None

    def next_frame_id(self, pre_frame_id=None):
        if pre_frame_id is None:
            if self.is_start():
                return self.states[1]
            else:
                pre_frame_id = self.get_cur_frame_id()

        next_id = pre_frame_id + 1

        if next_id > self.states[-2]:
            return self.states[-1]
        return next_id

    def get_cur_frame_id(self):
        return self.states[self.cur_state] if not self.is_start() else None

    def is_start(self):
        return self.states[self.cur_state] == 'START'

    def reinitialize(self):
        self.cur_state = 0
        self.next_state = 1


class ChainStateMachine(StateMachine):

    def __init__(self, states):
        super(ChainStateMachine, self).__init__(states)

    def state_change(self, inp):
        if len(self.states) > 2:
            self.cur_state = self.next_state
            self.next_state = (self.next_state + 1) % self.length


class SingleLoopStateMachine(StateMachine):

    def __init__(self, states, repeat):
        self.rep_start, self.rep_end = repeat[0] if len(repeat) > 0 else (None, None)
        super(SingleLoopStateMachine, self).__init__(states)

    # 状态的跳跃改变 由于缺少动作 导致状态的跳跃改变
    def state_change_by_id(self, match_frame_id):
        if len(self.states) > 2:
            self.cur_state = self.states.index(match_frame_id)
            self.next_state = self.cur_state + 1

    def state_change(self, inp):
        if len(self.states) > 2:
            if self.states[self.cur_state] == self.rep_end:
                self.cur_state = self.states.index(inp)
                self.next_state = self.cur_state + 1
            elif self.states[self.next_state] == self.rep_end:
                self.cur_state = self.next_state
                self.next_state = (self.rep_start + 1, self.cur_state + 1)
            else:
                self.cur_state = self.next_state
                self.next_state = self.next_state + 1

    def if_reached_loop_end(self):
        return self.states[self.cur_state] == self.rep_end

    def if_matched(self):
        return self.states[self.next_state] == 'END'

    def print_state(self):
        message = "cur_state为 %s, next_state为 %s, 对应帧为 %s ... %s" % (self.cur_state, self.next_state, self.states[self.cur_state], self.states[self.next_state])
        print(message)


class SimpleStateMachine(object):

    def __init__(self, states, repeat):
        # 用于匹配
        self.states = states
        # 用于计数
        self.repeat = repeat

        self.cur_state = 0
        self.next_state = 1

    def reinitialize(self):
        self.cur_state = 0
        self.next_state = 1


class State(object):

    def __init__(self):
        self.cur_count = 0
        self.max_count = 15

    def next_state(self, inp):
        raise NotImplemented


class StillState(State):

    def __init__(self):
        super(StillState, self).__init__()

    def next_state(self, velocities):
        v = velocities[-1]
        if -3 < v < 3:
            return self
        elif v > 0:
            return DownState()
        elif v < 0:
            return UpState()


class UpState(State):

    def __init__(self):
        super().__init__()

    def next_state(self, velocities):
        v = velocities[-1]
        if -3 < v < 3:
            if self.cur_count < self.max_count:
                self.cur_count += 1
                return self
            else:
                return StillState()
        elif v < 0:
            self.cur_count = 0
            return self
        elif v > 0:
            return DownState()


class DownState(State):

    def __init__(self):
        super().__init__()

    def next_state(self, velocities):
        v = velocities[-1]
        if -3 < v < 3:
            if self.cur_count < self.max_count:
                self.cur_count += 1
                return self
            else:
                return StillState()
        elif v > 0:
            self.cur_count = 0
            return self
        elif v < 0:
            return UpState()
