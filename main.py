from ursina import *
from battleground3d import Battleground
from ursina.shaders import lit_with_shadows_shader

class MenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text, scale=(.25, .075), highlight_color=color.azure, **kwargs)

        for key, value in kwargs.items():
            setattr(self, key ,value)


def set_visible(content, state=True):
    for key in content:
        content[key].visible=state


app = Ursina(vsync=True)

battleground = Battleground()

button_spacing = .075 * 1.25
menu_parent = Entity(parent=camera.ui)
main_menu = Entity(parent=menu_parent)      # Main menu. Init page
load_menu = Entity(parent=menu_parent)      # Load IP Server Menu
options_menu = Entity(parent=menu_parent)   # Menu Options

state_handler = Animator({
    'main_menu'     : main_menu,
    'load_menu'     : load_menu,
    'options_menu'  : options_menu,
})

# Defining settings in transitions
def from_main_menu_2_load_menu():
    state_handler.state = 'load_menu'
    set_visible(load_menu_content)

def from_load_menu_2_main_menu():
    state_handler.state = 'main_menu'
    set_visible(load_menu_content, False)

def from_main_menu_2_option_menu():
    state_handler.state = 'options_menu'
    set_visible(options_menu_content)

def from_options_menu_2_main_menu():
    state_handler.state = 'main_menu'
    set_visible(options_menu_content, False)

def enter_room():
    print("Username:", load_menu_content['username_field'].text)
    print("Server IP:", load_menu_content['server_ip_field'].text)
    set_visible(main_menu_content, False)
    set_visible(load_menu_content, False)
    background.visible = False
    battleground.enable()

def stopgame_input(key):
    if key == 'escape':
        background.visible = True
        battleground.disable()
        set_visible(load_menu_content)
        set_visible(main_menu_content)


stopgame_handler = Entity(ignore_paused=True, input=stopgame_input)

# MAIN MENU CONTENT
main_menu_content = {
    'start_button'      : MenuButton(parent=main_menu, text='start', y=0*button_spacing, on_click=from_main_menu_2_load_menu),
    'options_button'    : MenuButton(parent=main_menu, text='options', y=-1*button_spacing, on_click=from_main_menu_2_option_menu),
    'quit_button'       : MenuButton(parent=main_menu, text='quit', y=-2*button_spacing, on_click=Sequence(Wait(.01), Func(sys.exit))),
    'title_text'        : Text(text='BATTLEGROUND 3D', x=-.75, y=.3, scale=5, color=color.red),
}


# LOAD MENU CONTENT
load_menu_content = {
    'username_field'    : InputField(x=.2, y=0.1),
    'server_ip_field'   : InputField(default_value='127.0.0.1', x=.2, y=-.02, limit_content_to='0123456789.'),
    'username_text'     : Text(parent=load_menu, text='USERNAME:', x=-0.45, y=0.11, scale=1.5, color=color.black),
    'server_ip_text'    : Text(parent=load_menu, text='SERVER IP:', x=-.45, y=-.01, scale=1.5, color=color.black),
    'back_button'       : MenuButton(parent=load_menu, text='Back', x=-.2, y=-.15, on_click=from_load_menu_2_main_menu),
    "enter_button"      : MenuButton(parent=load_menu, text='Enter Room', x=.2, y=-.15, on_click=enter_room),
}


# OPTIONS MENU CONTENT
options_menu_content = {
    'back_button'       : MenuButton(parent=options_menu, text='Back', x=-.2, y=-.15, on_click=from_load_menu_2_main_menu),
    'title_text'        : Text(text='BATTLEGROUND 3D', x=-.75, y=.3, scale=5, color=color.red),
}


# animate the buttons in nicely when changing menu
for menu in (main_menu, load_menu, options_menu):
    def animate_in_menu(menu=menu):
        for i, e in enumerate(menu.children):
            e.original_x = e.x
            e.x += .1
            e.animate_x(e.original_x, delay=i*.05, duration=.1, curve=curve.out_quad)

            e.alpha = 0
            e.animate('alpha', .7, delay=i*.05, duration=.1, curve=curve.out_quad)

            if hasattr(e, 'text_entity'):
                e.text_entity.alpha = 0
                e.text_entity.animate('alpha', 1, delay=i*.05, duration=.1)

    menu.on_enable = animate_in_menu


background = Entity(model='quad', texture='shore', parent=camera.ui, scale=(camera.aspect_ratio,1), color=color.white, z=1)

# Init menu
set_visible(main_menu_content)
set_visible(load_menu_content, False)
set_visible(options_menu_content, False)

app.run()

