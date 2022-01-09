import PySimpleGUI as sg
from utils import back_event
from PIL import Image
from io import BytesIO
import os


def train_layout():
    layout = [[sg.Column([[sg.Text('Change training settings', font=('Courier New', 20))],
                          [sg.HSep(pad=((0, 0), (0, 4)))]])],
              [sg.Frame('Choose model to train',
                        [[sg.Radio("ResNet9 PyTorch", group_id=1, default=True, key="-RESNET9PT-",
                                   circle_color='blue')],
                         [sg.Radio("ResNet9 TensorFlow", group_id=1, key="-ResNet9TF-", circle_color='blue')],
                         [sg.Radio("VGG16 modified TensorFlow", group_id=1, key="-ResNet9TF-", circle_color='blue')],

                         ],
                        expand_x=True, pad=((0, 0), (8, 0)), size=(700, 145), border_width=0,
                        font=('Courier New', 12), element_justification='center', vertical_alignment='middle')],
              [sg.HSep()],
              [sg.Frame('Something else',
                        [[sg.Radio("Yes", group_id=2, default=True, key="-FACE DETECTION-", enable_events=True,
                                   circle_color='blue'),
                          sg.Radio("No", group_id=2, key="-NO FACE DETECTION-", enable_events=True,
                                   circle_color='blue')],
                         [sg.Frame(' .............. ', [
                             [sg.Text('Choose folder/image for preview:')],
                             [sg.DropDown(['Load images to get Face Detection preview'], key='-FACEDET DROPDOWN-',
                                          background_color='#e3e3e3',
                                          auto_size_text=True, expand_x=True, readonly=True, text_color='black',
                                          enable_events=True)],
                             [sg.Frame('', [[sg.Text('Scale Factor', size=(15, 1)),
                                             sg.Slider((1.05, 3), orientation='horizontal', resolution=0.05,
                                                       pad=((0, 0), (0, 5)),
                                                       default_value=1.1, relief=sg.RELIEF_FLAT, trough_color='#e3e3e3',
                                                       key="-FD1-",
                                                       size=(20, 16))],
                                            [sg.Text('Min. Neighbors', size=(15, 1)),
                                             sg.Slider((1, 10), orientation='horizontal', resolution=1,
                                                       pad=((0, 0), (0, 5)),
                                                       default_value=5, relief=sg.RELIEF_FLAT, trough_color='#e3e3e3',
                                                       key="-FD2-",
                                                       size=(20, 16))],
                                            [sg.Text('Min. Size', size=(15, 1)),
                                             sg.Slider((30, 300), orientation='horizontal', resolution=5,
                                                       pad=((0, 10), (0, 5)),
                                                       default_value=70, relief=sg.RELIEF_FLAT, trough_color='#e3e3e3',
                                                       key="-FD3-",
                                                       size=(20, 16))],
                                            [sg.Button('Detect Face', pad=((90, 0), (15, 0)), key="-FDSUB-",
                                                       enable_events=True)]
                                            ],
                                       expand_x=True, expand_y=True, border_width=0, pad=(0, 0),
                                       ),
                              sg.Frame('', [[sg.Image(key="-FD IMAGE-")]],
                                       expand_x=True, expand_y=True, border_width=0, pad=(0, 0),
                                       element_justification='center')],
                         ], expand_x=True, expand_y=True, border_width=0, font=('Courier New', 11))]],
                        expand_x=True, pad=((0, 0), (5, 0)), size=(560, 315), border_width=0,
                        font=('Courier New', 12), element_justification="center")],
              [sg.Frame("",
                        [[
                            sg.Button("Back", enable_events=True, size=(10, 1), font=('Courier New', 12))]],
                        element_justification='center', border_width=0, pad=((0, 0), (16, 0)),
                        vertical_alignment='center')],
              ]
    return layout


def train_loop(window):
    while True:
        event, values = window.read()
        width, height = (390, 180)

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if "Back" in event:
            back_event(window)
            return

        if event == "-NO FACE DETECTION-":
            window['-FACEDET DROPDOWN-'].update(disabled=True)
            window['-FD1-'].update(disabled=True)
            window['-FD2-'].update(disabled=True)
            window['-FD3-'].update(disabled=True)
            window['-FDSUB-'].update(disabled=True)
            window["-FD IMAGE-"].update(data=[])

        if event == "-FACE DETECTION-":
            window['-FACEDET DROPDOWN-'].update(disabled=False)
            window['-FD1-'].update(disabled=False)
            window['-FD2-'].update(disabled=False)
            window['-FD3-'].update(disabled=False)
            window['-FDSUB-'].update(disabled=False)
            event = '-FACEDET DROPDOWN-'

        if event == '-FACEDET DROPDOWN-':
            filepath = values['-FACEDET DROPDOWN-']
            if os.path.isdir(filepath):
                file_list = os.listdir(filepath)
                file_list = [f"{filepath}/{f}" for f in file_list
                             if os.path.isfile(f"{filepath}/{f}")]
                filepath = file_list[0]
            if os.path.isfile(filepath):
                try:
                    im = Image.open(filepath)
                except:
                    pass
                width, height = width, height
                scale = max(im.width / width, im.height / height)
                if scale > 1:
                    w, h = int(im.width / scale), int(im.height / scale)
                    im = im.resize((w, h), resample=Image.CUBIC)
                with BytesIO() as output:
                    im.save(output, format="PNG")
                    data = output.getvalue()
                window["-FD IMAGE-"].update(data=data)

        if event == '-FDSUB-':
            filepath = values['-FACEDET DROPDOWN-']
            if os.path.isdir(filepath):
                file_list = os.listdir(filepath)
                file_list = [f"{filepath}/{f}" for f in file_list
                             if os.path.isfile(f"{filepath}/{f}")]
                filepath = file_list[0]
            if os.path.isfile(filepath):
                tmpsave = f"{tmpdirpath}/detect_test.png"
                try:
                    simple_detect_draw_face(img_path=filepath, save_dir=f"{tmpdirpath}/detect_test.png",
                                            faceCascade=faceCascade,
                                            scale=values['-FD1-'], minneigh=values['-FD2-'], minsize=values['-FD3-'])
                    im = Image.open(tmpsave)
                except:
                    pass
                width, height = width, height
                scale = max(im.width / width, im.height / height)
                if scale > 1:
                    w, h = int(im.width / scale), int(im.height / scale)
                    im = im.resize((w, h), resample=Image.CUBIC)
                with BytesIO() as output:
                    im.save(output, format="PNG")
                    data = output.getvalue()
                window["-FD IMAGE-"].update(data=data)


if __name__ == "__main__":
    layout = settings_layout()
    window = sg.Window("Settings Page", layout,
                       size=(800, 600))
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()
