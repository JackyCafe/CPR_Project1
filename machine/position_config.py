from fancy import config as cfg


class PositionConfig(cfg.BaseConfig):
    y1: int = cfg.Option(required=True, type=int)
    y2: int = cfg.Option(required=True, type=int)
    depth: float = cfg.Option(required=True, type=float)
    is_play_sound: bool = cfg.Option(required=True, type=bool)
    is_test: bool = cfg.Option(required=True, type=bool)
