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
        self.__time_remaining = time_remaining
        self.__allotted_time = allotted_time  # for 5 minutes per Player? should this be combined with time_remaining
        self.__enabled = enabled  # is this for starting the timer?
        self.__started = False

    def time_out(self):
        """Notifies the Player that they have run out of time and stops the game?"""
        print("donezo")  # placeholder
        """TODO"""

    def warn_of_little_time(self):
        """Warns a Player if their time remaining is low"""
        if self.__time_remaining <= 30:
            print("Uh oh")

    def display(self):
        """Displays the time remaining for the Player to play their moves"""
        if self.__enabled and self.__started:
            while self.__allotted_time >= self.__time_remaining:
                minutes, seconds = divmod(self.__time_remaining, 60)
                timer = '{:2d}:{:02d}'.format(minutes, seconds)
                print(timer)
                time.sleep(1)
                self.__time_remaining -= 1
            # figure out how to stop it mid count

    def start(self):
        """Starts the time remaining for a Player"""
        self.__started = True

    def stop(self):
        """Stops the time remaining for a Player"""
        self.__started = False

    def get_time_remaining(self):
        """Returns the time remaining for a Player"""
        return self.__time_remaining

    def set_time_remaining(self, time_remaining):
        """Sets the time remaining for a Player"""
        self.__time_remaining = time_remaining

    def get_allotted_time(self):
        """Returns the allotted time for a Player"""
        return self.__allotted_time

    def set_allotted_time(self, allotted_time):
        """Sets the allotted time for a Player"""
        self.__allotted_time = allotted_time

    def get_enabled(self):
        """Returns a boolean value for the timer if it is to be started or stopped"""
        return self.__enabled

    def set_enabled(self, enabled):
        """Sets a boolean value to start or stop the timer"""
        self.__enabled = enabled


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
