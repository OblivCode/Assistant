from threading import Thread
from modules import control, logger
import engines.audio_engine as ae
from pynput import keyboard



key_bindings = {
    'voice_command': 'f',
    'force_close': 'x'
}

def on_press(key):

    try:
        #logger.log_info('alphanumeric key {0} pressed'.format(key.char))
        keys = list(key_bindings.values())
        action_idx = keys.index(key.char)
        actions = list(key_bindings.keys())
        action = actions[action_idx]

        match action:
            case 'voice_command': e.start_listen(),
            case 'force_close': control.close()


    except AttributeError:
        #logger.log_info('special key {0} pressed'.format(key))
        pass
    except ValueError:
        #logger.log_error('Unassigned key: {}'.format(key.char))
        pass

    last_key = key.char

def on_release(key):
    #logger.log_info('{0} released'.format(key))
    try:
        if key.char == key_bindings['voice_command']:
            text = e.end_listen()
            print('Got ', text)
        if key == keyboard.Key.esc:
            # Stop listener
            return False
    except:
        pass

#run

logger.log_boot('Started boot')

e = ae.engine()
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    logger.log_boot('Finished boot')
    print('Al ready')
    listener.join()