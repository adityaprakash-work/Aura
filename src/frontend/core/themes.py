# ---INFO-----------------------------------------------------------------------
"""
Themes for the frontend.
"""

__all__ = [
    "FrontendThemes",
    "DEFAULT_FRONTEND_THEME",
]


# ---DEPEDENCIES----------------------------------------------------------------
import yaml
import pathlib
import typing as tp
import pydantic as pyd


# ---CONSTANTS------------------------------------------------------------------
CONFIG_DIR = pathlib.Path(__file__).resolve().parents[3] / "config"
THEMES_DIR = CONFIG_DIR / "frontend" / "themes"


# ---SRC------------------------------------------------------------------------
class AppColor(pyd.BaseModel):
    """
    Pydantic model for the app color.
    """

    dark_one: str
    dark_two: str
    dark_three: str
    dark_four: str
    bg_one: str
    bg_two: str
    bg_three: str
    icon_color: str
    icon_hover: str
    icon_pressed: str
    icon_active: str
    context_color: str
    context_hover: str
    context_pressed: str
    text_title: str
    text_foreground: str
    text_description: str
    text_active: str
    white: str
    pink: str
    green: str
    red: str
    yellow: str


class FrontendTheme(pyd.BaseModel):
    """
    Pydantic model for the frontend themes.
    """

    theme_name: str
    app_color: AppColor


DEFAULT_FRONTEND_THEME = FrontendTheme(
    **yaml.load(
        (THEMES_DIR / "default.yaml").read_text(),
        Loader=yaml.FullLoader,
    )
)
