# ---INFO-----------------------------------------------------------------------
"""
Functions to set the assets.
"""

__all__ = [
    "set_svg_ico",
    "set_svg_img",
    "set_app_ico",
]


# ---DEPENDENCIES---------------------------------------------------------------
import pathlib

# ---CONSTANTS------------------------------------------------------------------
ASSETS_DIR = pathlib.Path(__file__).resolve().parents[3] / "assets"
SVG_ICO_DIR = ASSETS_DIR / "frontend" / "svg" / "icons"
SVG_IMG_DIR = ASSETS_DIR / "frontend" / "svg" / "images"


# ---FUNCTIONS------------------------------------------------------------------
def set_svg_ico(name: str):
    """
    Set the icon path for the SVG icon.

    Parameters:
    ----------
    - name: str
        The name of the icon.

    Returns:
    -------
    - pth: pathlib.Path
        The path to the icon.
    """
    if ".svg" in name:
        name = name.replace(".svg", "")
    pth = str(SVG_ICO_DIR / f"{name}.svg")
    return pth


def set_svg_img(name: str):
    """
    Set the icon path for the SVG image.

    Parameters:
    ----------
    - name: str
        The name of the image.

    Returns:
    -------
    - pth: pathlib.Path
        The path to the image.
    """
    if ".svg" in name:
        name = name.replace(".svg", "")
    pth = str(SVG_IMG_DIR / f"{name}.svg")
    return pth


def set_app_ico():
    """
    Set the icon path for the application icon.

    Returns:
    -------
    - pth: pathlib.Path
        The path to the icon.
    """
    pth = str(ASSETS_DIR / "frontend" / "icon.ico")
    return pth
