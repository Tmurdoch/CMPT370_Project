
#CMPT 370
#Thomas Murdoch, Tjm149, 11258350


def add_two(x):
    return x + 2

def test_answer():
    #fail the test
    assert add_two(2) == 3
    #pass the test
    assert add_two(1) == 3
