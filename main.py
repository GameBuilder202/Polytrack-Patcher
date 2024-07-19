from pathlib import Path

import dearpygui.dearpygui as dpg
from asarPy import pack_asar, extract_asar, Asar


polytrack_dir: 'Path | None' = None


def polytrack_dir_button_callback(_, __, user_data):
    dpg.add_file_dialog(
        directory_selector=True,
        show=True,
        callback=polytrack_dir_callback,
        user_data=user_data,
        height=300
    )


def polytrack_dir_callback(_, app_data, user_data):
    global polytrack_dir

    _path = app_data['file_path_name']
    path = Path(_path)

    if not path.exists():
        dpg.set_value(user_data, "Polytrack directory not set")
        return
    polytrack_dir = path
    dpg.set_value(user_data, f"Polytrack directory set! (Set to: {path})")
    on_dir_set()


def on_dir_set():
    asar = polytrack_dir / 'resources' / 'app.asar'
    extract_asar(asar, 'app/')


def show_block_models_node(_, app_data: tuple[int, int]):
    node = app_data[1]
    dpg.delete_item("BMS", children_only=True)
    dpg.add_text("Test2", parent=node)


def main():
    dpg.create_context()
    dpg.create_viewport(title='Polytrack Assets Patcher', width=700, height=600)

    with dpg.window(tag="Main"):
        dpg.add_text("Tool for patching/replacing Polytrack game assets for modding")
        dpg.add_text("WARNING: Create a backup of your polytrack directory before usage!!!", color=(255, 100, 100))

        dir_set = dpg.add_text("Polytrack directory not set")
        dpg.add_button(label="Select Polytrack Directory", callback=polytrack_dir_button_callback, user_data=dir_set)

        with dpg.tree_node(label="Car Model", tag="CM"):
            dpg.add_text("Test1")

        handlers = dpg.add_item_handler_registry()
        dpg.add_item_clicked_handler(parent=handlers, callback=show_block_models_node)
        with dpg.tree_node(label="Block Models", tag="BMS") as block_model_node:
            dpg.bind_item_handler_registry(block_model_node, handlers)

    dpg.setup_dearpygui()
    dpg.set_primary_window("Main", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()
