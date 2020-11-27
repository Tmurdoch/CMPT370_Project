# Board Game Simulator
# CMPT 370 Group 4, Fall 2020
# Authors: Antoni Jann Palazo, Brian Denton, Joel Berryere, Michael Luciuk, Thomas Murdoch

import os


def initializeFS():
    """initialize filesystem for storing stuff
    :returns: directory string"""
    if os.name == "posix":
        home = os.path.expanduser("~")
        if not (os.path.exists(home + "/.cmpt370checkerschess")):
            os.mkdir(home + "/.cmpt370checkerschess")
        return home + "/.cmpt370checkerschess"
    elif os.name == "nt":
        app_data = os.getenv("LOCALAPPDATA")
        if not (os.path.exists(app_data + "/.cmpt370checkerschess")):
            os.mkdir(app_data + "/.cmpt370checkerschess")
        return (app_data + "/.cmpt370checkerschess")
    else:
        print("unknown os")
        return
