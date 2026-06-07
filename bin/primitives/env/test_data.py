from primitives.env.data import Env


def test_home():
    env = Env()

    assert len(env.home) > 0
    assert env.home.startswith("/home")
