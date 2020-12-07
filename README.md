# Group 4

Tuesday Tutorial

Group Members:
Michael Luciuk [mrl280@usask.ca]
Thomas Murdoch [tjm149@usask.ca]
Antoni Jann Palazo [amp183@usask.ca]
Brian Denton [bwd257@usask.ca]
Joel Berryere [jtb648@usask.ca]

Project Description:
Our project is a Checkers and Chess Board Game simulator, that has basic functionality for classic checkers or chess. That is: local multiplayer or against an AI, game state recognition, a GUI, and the ability to recognize when a player has won. The program is runnable on all operating systems. Target users are casual board gamers, or anyone who wants to play/learn how to play checkers or chess. The program features additional customization options for Board and Piece styles. It also includes save game states, one for each of chess and checkers.


Our program will not work with any Python version below 3.7.  Make sure you are using an updated version of python before proceeding with the required downloads.
To check python version, use:
> python3 --version 

PyGObject is required to run the Chess and Checkers Board Game Simulator.  Instructions for getting PyGObject set up on all operating systems can be found here:
https://pygobject.readthedocs.io/en/latest/getting_started.html.  If your operaing system is not found, please defer to your distribution's package manager.
Note: The Pytest MSYS2 package will need to be installed to run the testing suite: 
> pacman -S mingw-w64-x86_64-python-pytest

To run the Chess and Checkers Board Game Simulator, navigate to the project's home directory, and use
> python3 Main.py

To run the unit and integration test suite run pytest in test_unit_and_integration_suite.py. If running on terminal use:
> pytest 

in the project directory.

If wish to see passed tests use:
> pytest -rpP 

This will create __pycache__ folder, just ignore this.
