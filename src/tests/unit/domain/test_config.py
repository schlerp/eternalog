from eternalog.domain import config


class TestConfig:
    def test_private_key_same_on_multiple_access(self) -> None:
        assert config.PUBLIC_KEY is not None
        assert config.PRIVATE_KEY == config.PRIVATE_KEY

    def test_public_key_same_on_multiple_access(self) -> None:
        assert config.PRIVATE_KEY is not None
        assert config.PUBLIC_KEY == config.PUBLIC_KEY
