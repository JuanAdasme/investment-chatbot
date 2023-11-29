import modules.constants as const
from modules.app import generate_message


def test_message_generation():
    expected = {
        "role": "user",
        "content": "Expected content"
    }

    actual = generate_message(const.USER_ROLE, "Expected content")

    assert expected["role"] == actual["role"]
    assert expected["content"] == actual["content"]
