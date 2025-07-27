import dearpygui.dearpygui as dpg

from tools.setup import *

items = {
    "aether_talisman:AEther": "aether_talisman",
    "fire_talisman:Fire": "fire_talisman",
    "bardiche": "bardiche",
    "bashing_shield": "bashing_shield",
    "blade_of_god": "blade_of_god",
    "compound_shield": "compound_shield",
    "crossbow": "crossbow",
    "cult_mask": "cult_mask",
    "crusader_shield:Vigor": "crusader_shield",
    "dashing_shield": "dashing_shield",
    "heavy_hammer": "heavy_hammer",
    "quarterstaff": "quarterstaff",
    "repeating_crossbow": "repeating_crossbow",
    "shield": "shield",
    "skeleton_arm": "skeleton_arm",
    "socketed_crossbow:AEther": "aether_socketed_crossbow",
    "socketed_crossbow:Fire": "fire_socketed_crossbow",
    "socketed_crossbow:Ice": "ice_socketed_crossbow",
    "socketed_crossbow:Poison": "poison_socketed_crossbow",
    "socketed_crossbow:Vigor": "vigor_socketed_crossbow",
    "socketed_hammer:AEther": "aether_socketed_hammer",
    "socketed_hammer:Fire": "fire_socketed_hammer",
    "socketed_hammer:Ice": "ice_socketed_hammer",
    "socketed_hammer:Poison": "poison_socketed_hammer",
    "socketed_hammer:Vigor": "vigor_socketed_hammer",
    "socketed_long_sword:AEther": "aether_socketed_long_sword",
    "socketed_long_sword:Fire": "fire_socketed_long_sword",
    "socketed_long_sword:Ice": "ice_socketed_long_sword",
    "socketed_long_sword:Poison": "poison_socketed_long_sword",
    "socketed_long_sword:Vigor": "vigor_socketed_long_sword",
    "socketed_shield:AEther": "aether_socketed_shield",
    "socketed_shield:Fire": "fire_socketed_shield",
    "socketed_shield:Ice": "ice_socketed_shield",
    "socketed_shield:Poison": "poison_socketed_shield",
    "socketed_shield:Vigor": "vigor_socketed_shield",
    "socketed_staff": "socketed_staff",
    "socketed_staff:AEther": "aether_socketed_staff",
    "socketed_staff:Fire": "fire_socketed_staff",
    "socketed_staff:Ice": "ice_socketed_staff",
    "socketed_staff:Poison": "poison_socketed_staff",
    "socketed_staff:Vigor": "vigor_socketed_staff",
    "socketed_sword:AEther": "aether_socketed_sword",
    "socketed_sword:Fire": "fire_socketed_sword",
    "socketed_sword:Ice": "ice_socketed_sword",
    "socketed_sword:Poison": "poison_socketed_sword",
    "socketed_sword:Vigor": "vigor_socketed_sword",
    "sword": "sword",
    "tower_shield": "tower_shield",
    "wand": "wand",
    "wand:AEther": "aether_wand",
    "wand:Fire": "fire_wand",
    "wand:Ice": "ice_wand",
    "wand:Poison": "poison_wand",
    "wand:Vigor": "vigor_wand"
}

class CosmeticsTab:
    def __init__(self, save):
        self.save = save
        self.cosmetics = None
        self.golden = None
        self.prismatic = None
        self.extra = None

    def load(self):
        self.cosmetics = self.save["progress_data"]["cosmetics"]

        # Ensure golden, glitch and prismatics lists
        for skin_type in ("golden", "glitch", "prismatic", "extra"):
            if skin_type not in self.cosmetics:
                self.cosmetics[skin_type] = []

        self.golden = self.cosmetics["golden"]
        self.glitch = self.cosmetics["glitch"]
        self.prismatic = self.cosmetics["prismatic"]
        self.extra = self.cosmetics["extra"]

        # Check global switchers
        all_golden = len(self.golden) == len(items)
        all_golden_new = all([item.endswith(";new") for item in self.golden] + [len(self.golden)])
        all_glitch = len(self.glitch) == len(items)
        all_glitch_new = all([item.endswith(";new") for item in self.glitch] + [len(self.glitch)])
        all_prismatic = len(self.prismatic) == len(items)
        all_prismatic_new = all([item.endswith(";new") for item in self.prismatic] + [len(self.prismatic)])

        dpg.configure_item("golden", default_value=all_golden)
        dpg.configure_item("golden-new", default_value=all_golden_new)

        dpg.configure_item("glitch", default_value=all_glitch)
        dpg.configure_item("glitch-new", default_value=all_glitch_new)

        dpg.configure_item("prismatic", default_value=all_prismatic)
        dpg.configure_item("prismatic-new", default_value=all_prismatic_new)

        # Check switchers for each item
        for item in items:
            golden = False
            golden_is_new = False
            index = self.get_index(item, "golden")
            if index != -1:
                golden = True
                golden_is_new = self.cosmetics["golden"][index].endswith(";new")

            glitch = False
            glitch_is_new = False
            index = self.get_index(item, "glitch")
            if index != -1:
                glitch = True
                glitch_is_new = self.cosmetics["glitch"][index].endswith(";new")

            prismatic = False
            prismatic_is_new = False
            extra = (0, 0, 0)
            index = self.get_index(item, "prismatic")
            if index != -1:
                prismatic = True
                prismatic_is_new = self.cosmetics["prismatic"][index].endswith(";new")
                
                c = self.cosmetics["extra"][index]["c"]
                extra = [int(rgb, 16) for rgb in (c[1:3], c[3:5], c[5:7])]

            dpg.configure_item(f"{item}-golden", default_value=golden)
            dpg.configure_item(f"{item}-golden-new", default_value=golden_is_new, show=golden)

            dpg.configure_item(f"{item}-glitch", default_value=glitch)
            dpg.configure_item(f"{item}-glitch-new", default_value=glitch_is_new, show=glitch)

            dpg.configure_item(f"{item}-prismatic", default_value=prismatic)
            dpg.configure_item(f"{item}-prismatic-new", default_value=prismatic_is_new, show=prismatic)
            dpg.configure_item(f"{item}-extra", default_value=extra, show=prismatic)

    def open(self, _, value, group_and_item):
        if not self.cosmetics:
            return

        group, item = group_and_item
        index = self.get_index(item, group)

        if value and index == -1:  # Open
            self.cosmetics[group].append(f"{item};new")
            if group == "prismatic":
                self.cosmetics["extra"].append({"c": "#000000"})
                dpg.configure_item(f"{item}-extra", default_value=(0, 0, 0), show=True)

            dpg.configure_item(f"{item}-{group}-new", default_value=True, show=True)
            print(f"Opened {item} {group} skin")

        elif not value and index != -1:  # Close
            self.cosmetics[group].pop(index)
            if group == "prismatic":
                self.cosmetics["extra"].pop(index)
                dpg.configure_item(f"{item}-extra", show=False)

            dpg.configure_item(f"{item}-{group}-new", default_value=False, show=False)
            print(f"Closed {item} {group} skin")

    def open_all(self, _, value, group):
        if not self.cosmetics:
            return

        for item in items:
            self.open(_, value, (group, item))
            dpg.configure_item(f"{item}-{group}", default_value=value)

    def mark(self, _, value, group_and_item):
        if not self.cosmetics:
            return

        group, item = group_and_item
        index = self.get_index(item, group)

        if index != -1:
            # Add ";new"
            if value and not self.cosmetics[group][index].endswith(";new"):
                self.cosmetics[group][index] += ";new"
                print(f"Marked as new {item} {group} skin")

            # Remove ";new"
            if not value:
                print(f"Marked as old {item} {group} skin")
                self.cosmetics[group][index] = self.cosmetics[group][index].replace(";new", "")

    def mark_all(self, _, value, group):
        if not self.cosmetics:
            return
        
        for item in items:
            self.mark(_, value, (group, item))
            dpg.configure_item(f"{item}-{group}-new", default_value=value)

    def get_index(self, search_item, cosmetics_type):
        for i, item in enumerate(self.cosmetics[cosmetics_type]):
            if item.replace(";new", "") == search_item:
                return i

        return -1

    def color(self, _, value, group_and_item):
        if not self.cosmetics:
            return

        group, item = group_and_item
        index = self.get_index(item, group)

        if index != -1:
            r, g, b, a = [int(c * 255) for c in value]
            color = "#%02x%02x%02x" % (r, g, b)
            self.cosmetics["extra"][index]["c"] = color

            print(f"Changed color for {item} on {color}")

    def colors_all(self, _, value, group):
        if not self.cosmetics:
            return

        for item in items:
            self.color(_, value, ("prismatic", item))
            dpg.configure_item(
                f"{item}-{group}",
                default_value=list(map(lambda x: int(x * 255), value))
            )

    def prepare_table(self, table_type):
        with dpg.table(
            tag=f"{table_type}_table",
            header_row=False,
            resizable=True,
        ):
            dpg.add_table_column()
            dpg.add_table_column()

            # Header
            with dpg.table_row():
                dpg.add_text(i18n["item"])
                dpg.add_text(i18n[table_type])

            # Mark all
            with dpg.table_row():
                dpg.add_text(i18n["all_items"])

                with dpg.group(horizontal=True):
                    dpg.add_checkbox(
                        label=i18n["opened"],
                        tag=table_type,
                        callback=self.open_all,
                        user_data=(table_type)
                    )
                    dpg.add_checkbox(
                        label=i18n[f"{table_type}_new"],
                        tag=f"{table_type}-new",
                        callback=self.mark_all,
                        user_data=(table_type)
                    )

                    if table_type == "prismatic":
                        dpg.add_color_edit(
                            label=i18n["color"],
                            tag="extra",
                            callback=self.colors_all,
                            user_data=("extra"),
                            no_alpha=True,
                            display_mode=dpg.mvColorEdit_hex,
                            no_drag_drop=True,
                            no_tooltip=True,
                            no_inputs=True
                        )
                                        
            # Swithers for each item
            for item in items:
                with dpg.table_row():
                    dpg.add_text(i18n["cosmetics"][items[item]])

                    with dpg.group(horizontal=True):
                        dpg.add_checkbox(
                            label=i18n["opened"],
                            tag=f"{item}-{table_type}",
                            callback=self.open,
                            user_data=(table_type, item)
                        )
                        dpg.add_checkbox(
                            label=i18n[f"{table_type}_new"],
                            tag=f"{item}-{table_type}-new",
                            callback=self.mark,
                            user_data=(table_type, item)
                        )

                        if table_type == "prismatic":
                            dpg.add_color_edit(
                                label=i18n["color"],
                                tag=f"{item}-extra",
                                no_alpha=True,
                                display_mode=dpg.mvColorEdit_hex,
                                no_drag_drop=True,
                                no_tooltip=True,
                                no_inputs=True,
                                callback=self.color,
                                user_data=(table_type, item)
                            )

    def gui(self):
        with dpg.child_window(no_scrollbar=True, border=False):
            for table_type in ["golden", "glitch", "prismatic"]:
                with dpg.collapsing_header(
                    label=i18n[table_type],
                    default_open=True
                ):
                    self.prepare_table(table_type)
