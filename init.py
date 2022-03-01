from threading import Thread
from modules import control, logger
import engines.audio_engine as audio
from pynput import keyboard
import os

#config
os.environ['voice_enabled'] = 'yes'
os.environ['assistant_name'] = 'Assistant'

key_bindings = {
    'voice_command': 'f', #activate speech listener
    'force_close': 'x' #force close application
}

last_key = ''

#functions
def onPress(key):
    global last_key
    try:
        #logger.log_info('alphanumeric key {0} pressed'.format(key.char))
        keys = list(key_bindings.values())
        action_idx = keys.index(key.char)
        actions = list(key_bindings.keys())
        action = actions[action_idx]

        match action:
            case 'voice_command': 
                if os.environ.get('voice_enabled') == 'yes':
                    audio_e.start_listen()
                else:
                    print('Voice not enabled')
            case 'force_close': 
                control.close()


    except AttributeError:
        #logger.log_info('special key {0} pressed'.format(key))
        pass
    except ValueError:
        #logger.log_error('Unassigned key: {}'.format(key.char))
        pass

    last_key = key.char

def onRelease(key):
    #logger.log_info('{0} released'.format(key))
    try:
        if key.char == key_bindings['voice_command']:
            if not audio_e.listening:
                return
            text = audio_e.end_listen()
            print('Got ', text)
        if key == keyboard.Key.esc:
            # Stop listener
            return False
    except:
        pass

#run

logger.log_boot('Started boot')
audio_e = audio.engine()



with keyboard.Listener(
        on_press=onPress,
        on_release=onRelease) as listener:
    logger.log_boot('Finished boot')
    audio_e.say(['Hello'])
    listener.join()