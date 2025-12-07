import dearpygui.dearpygui as dpg
import tomllib
import locale
import json
import sys 

from os import name, chdir

WIDTH = 620
HEIGHT = 394

HEIGHT_OFFSET = 0
WIDTH_OFFSET = 0
SCALE = 1

REMAP_START = 0x10ec77
REMAP_END = 0x10ffff

IS_NT = name == "nt"  # Windows

# Fix paths for compiled NT app
if IS_NT and getattr(sys, 'frozen', False):
    chdir(sys._MEIPASS)

# Load settings
with open("settings.toml", "rb") as f:
    settings = tomllib.load(f)

# Translations
languages = {
    "ru": "Russian",
    "en": "English",
    "zh": "Chinese",
}

class TranslationDict:
    def __init__(self, value):
        self.value = value

    def __getitem__(self, key):
        if key in self.value:
            return TranslationDict(self.value[key])
        return TranslationDict(key)

    def __setitem__(self, name, new_value):
        self.value[name] = new_value

    def __add__(self, other):
        return self.value + other

    def __repr__(self):
        return str(self.value)

def get_language():
    language = settings["language"]
    is_auto = language == "auto"

    # Try to set system language
    if is_auto:
        system_language, _ = locale.getdefaultlocale()
        print(f"System language is {system_language}")

        if system_language:
            language = system_language[:2]

    if language not in languages:
        language = "en"

    return language

# Load translation dict
i18n = TranslationDict(
    json.load(
        open(
            f"translations/{get_language()}.json",
            encoding="utf-8"
        )
    )
)

# Check things for nt
if IS_NT:
    # DPG don't support non latin title on NT
    i18n["title"] = "Stone Story RPG save editor"

    WIDTH_OFFSET = 26
    HEIGHT_OFFSET = 38  # Windows magic numbers

    if settings["upscale"]:
        WIDTH_OFFSET = 32
        HEIGHT_OFFSET = 38 * 2 - 6
        SCALE = 2

        import ctypes  # Make x2 resolution for Retina screens
        ctypes.windll.shcore.SetProcessDpiAwareness(2)

def init_font():
    with dpg.font_registry():
        font_file = "fonts/mononoki-Regular.ttf"
        font_size = 32 * SCALE

        # Load font with hieroglyphs for Chinese
        if get_language() == "zh":
            font_file = "fonts/SarasaMonoSC-Regular.ttf"

        with dpg.font(font_file, font_size) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Full)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Chinese_Simplified_Common)

            dpg.add_font_chars([ord(c) for c in "♦≈★"])

            dpg.set_global_font_scale(0.5)

            # Remap 5k of Unicode chars to indexes for inventory tab
            dpg.add_font_range(REMAP_START, REMAP_END)
            for char in range(REMAP_START, REMAP_END):
                dpg.add_char_remap(char, 0x20)  # Whitespace

            dpg.bind_font(font)

def init_theme():
    if not (IS_NT and settings["upscale"]):
        return

    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_WindowPadding,
                16,
                16,
                category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_FramePadding,
                8,
                6,
                category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_CellPadding,
                8,
                4,
                category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_ItemSpacing,
                16,
                8,
                category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_ItemInnerSpacing,
                8,
                8,
                category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_ScrollbarSize,
                22,
                category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_TabRounding,
                8,
                category=dpg.mvThemeCat_Core
            )
            dpg.add_theme_style(
                dpg.mvStyleVar_GrabMinSize,
                20,
                category=dpg.mvThemeCat_Core
            )

    dpg.bind_theme(global_theme)
    print("Loaded NT upscaled theme")
