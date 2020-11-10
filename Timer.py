# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import time


class Timer(object):
    """
    A Timer is an object that keeps, updates and displays the current time for a Player
    to play their moves.
    """
    def __init__(self, time_remaining, allotted_time, enabled):
        """
        Initializes a Timer object.
        :param time_remaining: The time remaining for the Player.
        :param allotted_time: The initial time given to a Player to make their moves.
        :param: enabled: Determines if the timer is enabled or not
        """
        self.time_remaining = time_remaining
        self.allotted_time = allotted_time  # for 5 minutes per Player? should this be combined with time_remaining
        self.enabled = enabled  # is this for starting the timer?

    def time_out(self):
        """TODO"""

    def warn_of_little_time(self):
        """Warns a Player if their time remaining is low"""
        if self.time_remaining <= 30:
            print("Uh oh")

    def display(self):
        """Displays the time remaining for the Player to play their moves"""
        if self.enabled:
            start_time = time.time()
            seconds = 0
            while seconds < self.time_remaining:                      # Problem will be when paused, how to
                time.sleep(1)                                         # pause time.time() and will time.sleep
                print(self.allotted_time - time.time() - start_time)  # stop everything else
                Timer.set_time_remaining(self, self.time_remaining - 1)
                seconds += 1
        """TODO"""

    def start(self):
        """Starts the time remaining for a Player"""
        # Should instead put get/set_enabled into the start and stop and have them determine enabled?
        """TODO"""

    def stop(self):
        """Stops the time remaining for a Player"""
        # Should instead put get/set_enabled into the start and stop and have them determine enabled?
        """TODO"""

    def get_time_remaining(self):
        """Returns the time remaining for a Player"""
        return self.time_remaining

    def set_time_remaining(self, time_remaining):
        """Sets the time remaining for a Player"""
        self.time_remaining = time_remaining

    def get_allotted_time(self):
        """Returns the allotted time for a Player"""
        return self.allotted_time

    def set_allotted_time(self, allotted_time):
        """Sets the allotted time for a Player"""
        self.allotted_time = allotted_time

    def get_enabled(self):
        """Returns a boolean value for the timer if it is to be started or stopped"""
        return self.enabled

    def set_enabled(self, enabled):
        """Sets a boolean value to start or stop the timer"""
        self.enabled = enabled

def test_timer():
    t = Timer(300, 300, False)
    assert(t.get_time_remaining() == 300)
    t.set_time_remaining(30)
    assert(t.get_time_remaining() == 30)
    t.set_allotted_time(200)
    assert(t.get_allotted_time() == 200)
    assert(not t.get_enabled())
    t.set_enabled(True)
    assert(t.get_enabled())
    t.warn_of_little_time()
