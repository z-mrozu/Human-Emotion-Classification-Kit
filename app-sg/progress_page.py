import os.path

import PySimpleGUI as sg
from utils import list_all_pictures, load_res9pt, load_res50tf, prediction_combo
from result_page import result_loop
import dlib


def progress_layout():
    BAR_MAX = 100
    layout = [[sg.Text('Please wait while prediction is in progress', font=('Courier New', 20), pad=((0, 0), (60, 0)))],
              [sg.HSep(pad=((0, 0), (0, 26)))],
              [sg.ProgressBar(max_value=BAR_MAX, orientation='h', size=(40, 40), key='-PROGRESS BAR-')],
              [sg.Listbox([], background_color='white', key='-PROGRESS TEXT-', highlight_background_color='white', highlight_text_color='black',
                          font=('Courier New', 12), size=(70, 15), enable_events=False, pad=(0, 20),
                          no_scrollbar=True, )],
              [sg.Button('Cancel', size=(10, 1), font=('Courier New', 12), pad=(10, 20)),
               sg.Button('Continue', size=(10, 1), font=('Courier New', 12), pad=(10, 20), disabled=True)]]
    return layout


def progress_loop(window, chosen_stuff, values, faceCascade, models, predictor):
    pic_list = list_all_pictures(chosen_stuff)
    num_pics = len(pic_list)
    # print('Counted:')
    # print(num_pics)
    test = []

    res9pt = values['-RESNET9-']
    res50tf = values['-RESNET50-']
    detection = values['-FACE DETECTION-']
    save_dir = values['-RESULT FOLDER-']

    if res9pt:
        model_text = '-RESNET9-'
    else:
        model_text = '-RESNET50-'

    steps = num_pics + 2

    i = 1
    progress_text = ['Loading model...']
    window['-PROGRESS TEXT-'].update(progress_text)
    window['-PROGRESS BAR-'].update(i, steps)

    if res9pt and not models['res9pt']:
        models['res9pt'] = load_res9pt()
    elif res50tf and not models['res50tf']:
        models['res50tf'] = load_res50tf()
    if not predictor:
        predictor = dlib.shape_predictor('faceutils/shape_predictor_68_face_landmarks.dat')

    i = 2
    window['-PROGRESS BAR-'].update(i, steps)
    progress_text.append('Predicting emotions and saving results...')
    window['-PROGRESS TEXT-'].update(progress_text)

    for image_path in pic_list:
        event, values = window.read(0)

        if event == "Exit" or event == sg.WIN_CLOSED or event is None:
            break

        if 'Cancel' in event:
            window[f'-COL5-'].update(visible=False)
            window[f'-COL4-'].update(visible=True)
            return models, predictor

        try:
            rest, pic_name = os.path.split(image_path)
            tmp_text = 'Predicting: ' + pic_name
            tmp_text2 = 'Saving:     ' + pic_name
            progress_text.append(tmp_text)
            progress_text.append(tmp_text2)
            n = len(progress_text)
            print(image_path)
            if n > 14:
                progress_text = progress_text[n - 14:n]
            window['-PROGRESS TEXT-'].update(progress_text)

            if res9pt:
                # out = predict_res9pt(image_path, models['res9pt'])
                out = prediction_combo(image_path, save_dir, models['res9pt'], model_text, detection, faceCascade,
                                       values['-FD1-'], values['-FD2-'], values['-FD3-'])
                test.append(out)

            elif res50tf:
                # out = predict_res50tf(image_path, models['res50tf'], predictor)
                out = prediction_combo(image_path, save_dir, models['res50tf'], model_text, detection, faceCascade,
                                       values['-FD1-'], values['-FD2-'], values['-FD3-'], predictor)
                test.append(out)
        except Exception:
            pass

        i += 1
        window['-PROGRESS BAR-'].update(i, steps)

    saved_stuff = []
    for image_path in pic_list:
        try:
            sth, image_name = os.path.split(image_path)
            saved_path = f'{save_dir}/{image_name}'
            saved_stuff.append(saved_path)
        except Exception:
            pass

    progress_text.append('Done!')
    window['-PROGRESS TEXT-'].update(progress_text)

    window['Continue'].update(disabled=False)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED or event is None:
            break

        if 'Cancel' in event:
            window[f'-COL5-'].update(visible=False)
            window[f'-COL4-'].update(visible=True)
            return models, predictor

        if event == 'Continue':
            window[f'-COL5-'].update(visible=False)
            window[f'-COL6-'].update(visible=True)
            result_loop(window, saved_stuff)
            break

    return models, predictor


if __name__ == "__main__":
    layout = progress_layout()
    window = sg.Window("Progress Page", layout, element_justification='center',
                       size=(800, 600))
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
    window.close()
