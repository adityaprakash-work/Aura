# ---INFO-----------------------------------------------------------------------
"""
Settings for the frontend.
"""

__all__ = [
    "FrontendSettings",
    "DEFAULT_FRONTEND_SETTINGS",
]


# ---DEPEDENCIES----------------------------------------------------------------
import yaml
import pathlib
import typing as tp
import pydantic as pyd


# ---CONSTANTS------------------------------------------------------------------
CONFIG_DIR = pathlib.Path(__file__).resolve().parents[3] / "config"
FGUI_SETTINGS_PATH = CONFIG_DIR / "frontend" / "frontend-gui-settings.yaml"


# ---SRC------------------------------------------------------------------------
class FrontendSettings(pyd.BaseModel):
    """
    Pydantic model for the frontend settings.
    """

    app_name: str
    version: str
    copyright: str
    year: int
    theme_name: str
    custom_title_bar: bool
    startup_size: tp.Tuple[int, int]
    minimum_size: tp.Tuple[int, int]
    left_menu_size: tp.Dict[str, int]
    left_menu_content_margins: int
    left_column_size: tp.Dict[str, int]
    right_column_size: tp.Dict[str, int]
    time_animation: int
    font: tp.Dict[str, str | int]


DEFAULT_FRONTEND_SETTINGS = FrontendSettings(
    **yaml.load(FGUI_SETTINGS_PATH.read_text(), Loader=yaml.FullLoader)
)
