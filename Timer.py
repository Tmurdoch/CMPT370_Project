# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import time


class Timer(object):
    """
    Timer is an object that keeps and updates the time remaining for a Player.
    Time is in internally stored as nanoseconds (integer).

    Attributes:
        __time_remaining_ns: Int: The remaining time on the timer in nanoseconds.
        __enabled: Bool: Whether or not the timer is enabled.
        __running: Bool: Whether or not timer is running.
        __timeOnStart: Int: The time as of when the timer was last started.
    """

    def __init__(self, allotted_time, enabled):
        """
        Initializes a Timer object.
        :param allotted_time: int: TIME IN SECONDS! The initial time given to a Player to make their moves.
            Remaining time if loading from a file.
        :param enabled: Bool: Boolean that determines if the timer is enabled or not (True for enabled, False otherwise)
        """
        self.__time_remaining_ns = allotted_time * (10 ** 9)  # Can't be manually changed, no setter
        self.__enabled = enabled
        self.__running = False
        self.__timeOnStart = None

    def timed_out(self):
        """
        Used to check if the player has timed out.
        :return: Bool: True if the player is out of time, False otherwise.
        """
        if self.__enabled:
            return self.__time_remaining_ns < 0
        else:
            return False

    def start(self):
        """ Starts the timer. """
        if self.__enabled and not self.__running:
            self.__running = True
            self.__timeOnStart = time.time_ns()
            return True
        else:
            return False

    def stop(self):
        """ Stops the timer and updates the time remaining. """
        if self.__enabled and self.__running:
            self.__time_remaining_ns = self.get_time_remaining_ns()
            self.__running = False
            return True
        else:
            return False

    def get_time_remaining_ns(self):
        """ :return: float: the time remaining for a Player in nanoseconds. """
        if self.__enabled:
            if self.__running:
                return self.__time_remaining_ns - (time.time_ns() - self.__timeOnStart)
            else:
                return self.__time_remaining_ns
        else:
            return False

    def get_time_remaining_s(self):
        """ :return: float: the time remaining for a Player in seconds. """
        if self.__enabled:
            if self.__running:
                return (self.__time_remaining_ns - (time.time_ns() - self.__timeOnStart)) / (10 ** 9)
            else:
                return self.__time_remaining_ns / (10 ** 9)
        else:
            return False

    def get_enabled(self):
        """ :return: bool: True if the timer is enabled, False otherwise. """
        return self.__enabled
