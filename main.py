import shutil
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

    path = Path(app_data['file_path_name'])

    if not path.exists():
        dpg.set_value(user_data, "Polytrack directory not set")
        return
    polytrack_dir = path
    dpg.set_value(user_data, f"Polytrack directory set! (Set to: {path})")
    on_dir_set(user_data)


def on_dir_set(text):
    asar = polytrack_dir / 'resources' / 'app.asar'
    try:
        extract_asar(asar, 'app/')
    except FileNotFoundError:
        dpg.set_value(text, "Invalid polytrack directory")
        return
    except FileExistsError:
        shutil.rmtree(Path('./app/'))
        extract_asar(asar, 'app/')
    except OSError as e:
        dpg.set_value(text, f"OS Error while trying to access polytrack directory: {e.strerror}")
        return


def car_model_button_callback():
    global polytrack_dir
    if polytrack_dir is None:
        return

    with dpg.file_dialog(
        show=True,
        callback=car_model_callback,
        height=300,
    ):
        dpg.add_file_extension("glTF 2.0 (*.glb){.glb}")


def car_model_callback(_, app_data):
    global polytrack_dir

    car_glb = Path(app_data['file_path_name'])
    models = Path('./app/models/')
    shutil.copy(car_glb, models / 'car.glb')


def show_block_models_node(_, app_data: tuple[int, int]):
    node = app_data[1]
    dpg.delete_item("BMS", children_only=True)
    dpg.add_text("Test2", parent=node)


def patch_game():
    asar = polytrack_dir / 'resources' / 'app.asar'
    pack_asar(Path('./app/'), asar)


def main():
    dpg.create_context()
    dpg.create_viewport(title='Polytrack Assets Patcher', width=700, height=600)

    with dpg.window(tag="Main"):
        dpg.add_text("Tool for patching/replacing Polytrack game assets for modding")
        dpg.add_text("WARNING: Create a backup of your polytrack directory before usage!!!", color=(255, 100, 100))

        dir_set = dpg.add_text("Polytrack directory not set")
        dpg.add_button(label="Select Polytrack Directory", callback=polytrack_dir_button_callback, user_data=dir_set)

        with dpg.tree_node(label="Car Model", tag="CM"):
            dpg.add_button(label="Set Car Model", callback=car_model_button_callback)

        handlers = dpg.add_item_handler_registry()
        dpg.add_item_clicked_handler(parent=handlers, callback=show_block_models_node)
        with dpg.tree_node(label="Block Models", tag="BMS") as block_model_node:
            dpg.bind_item_handler_registry(block_model_node, handlers)

        dpg.add_button(label="Patch Game", callback=patch_game)

    dpg.setup_dearpygui()
    dpg.set_primary_window("Main", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

    # shutil.rmtree(Path('./app/'))


if __name__ == '__main__':
    main()
