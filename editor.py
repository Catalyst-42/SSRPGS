import dearpygui.dearpygui as dpg

from subprocess import check_output
from sys import executable

from save import Save
from main_tab import MainTab
from locations_tab import LocationsTab
from inventory_tab import InventoryTab

from utils import loading

class Editor:
    def __init__(self):
        self.init_dpg()
        self.init_font()

        self.save = Save()

        self.main_tab = MainTab(self.save)
        self.locations_tab = LocationsTab(self.save)
        self.inventory_tab = InventoryTab(self.save)
        # self.quests_tab = None

    def init_dpg(self):
        dpg.create_context()

    def init_font(self):
        with dpg.font_registry():
            with dpg.font("mononoki-Regular.ttf", 32) as font:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.add_font_chars([ord(c) for c in "♦≈★"])
                dpg.set_global_font_scale(0.5)
                dpg.bind_font(font)

    def load(self):
        save_file = check_output([executable, "get_file.py"])  # I don't know what's wrong with dpg
        
        if not save_file:
            return

        with loading():
            self.save.open(save_file)

        dpg.configure_item(
            "save_slots",
            items=self.save.save_slots,
            default_value=self.save.save_slot
        )
        
        # Load data to tabs
        self.main_tab.load()
        self.locations_tab.load()
        self.inventory_tab.load()

    def dump(self):
        with loading():
            self.main_tab.dump()
            self.locations_tab.dump()
            self.save.save("primary_save.txt")

    def change_slot(self, _, new_save_slot):
        # Save previous values
        self.main_tab.dump()
        self.locations_tab.dump()
        self.inventory_tab.dump()
        
        self.save.save_slot = new_save_slot

        # Sync values to fields
        self.main_tab.load()
        self.locations_tab.load()
        self.inventory_tab.load()

    def json_export(self):
        self.save.save_as_json("formatted.json")

    def gui(self):
        with dpg.window(tag="Editor"):            
            # Header
            with dpg.group(horizontal=True):
                dpg.add_button(label="Открыть", callback=self.load)
                dpg.add_button(label="Сохранить", callback=self.dump)
                dpg.add_combo(label="Слот сохранения", width=196, items=[], callback=self.change_slot, tag="save_slots")
                
            # Tabs
            with dpg.tab_bar():
                with dpg.tab(label="Настройки"):
                    dpg.add_text("Stone Story RPG save editor\nv 0.0.0")
                    dpg.add_button(label="Экспортировать JSON", callback=self.json_export)

                with dpg.tab(label="Общее"):
                    self.main_tab.gui()

                with dpg.tab(label="Локации"):
                    self.locations_tab.gui()

                with dpg.tab(label="Инвентарь"):
                    self.inventory_tab.gui()

    def run(self):
        self.gui()
        dpg.create_viewport(
            title="Редактор сохранений Stone Story RPG",
            width=600,
            height=412
        )

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window("Editor", True)
        dpg.start_dearpygui()
        dpg.destroy_context()

editor = Editor()
editor.run()