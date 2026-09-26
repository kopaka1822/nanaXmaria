# Lipsync system for layered images and Live2D models based on Rhubarb's lip sync system
# By default, it requires mouth shapes: A, B, C, D, E, F, G, H
# If you work with less shapes, adjust the shape_converter() function below
#
# Example usage for (layered) images:
# define w = Character("Wynne", callback = lipsync_callback("wynne"))
# image wynne = WhileSpeaking_ABC("wynne", "images/wynne_mouth_", ".png") 
# This expects the files named: wynne_mouth_A.png, wynne_mouth_B.png, wynne_mouth_C.png, etc.
#
# Example usage for Live2D models:
# define w = Character("Wynne", callback = lipsync_callback("wynne"))
# image wynne = Live2D("images/live2d/wynne.model3.json", update_function=live2d_lipsync_callback("wynne"))
# This expects the corresponding mouth shapes to be defined by MouthOpen and MouthForm parameters, as indicated below at SHAPE_COORD_DICT.

init -20 python: 
    import random
    import time

    current_speaker = None # character name
    speaking_text = "" # for text based lipsync
    speaking_index = 0
    current_lip_file = "" # for actual lip sync
    current_lip_data = None
    current_has_audio = False
    next_animation_time = 0.0 # only for text based lipsync
    live2d_coord_cache = {} # cache for smooth live2d shape coordinates

    # Shapes in live2d are organized as follows in:
    # X-Axis: Mouth Form
    # Y-Axis: Mouth Open
    #
    # Mouth Open (0 to 1) 
    # ^
    # | E | H | D
    # | F | C | B
    # | G | X | A
    # o-----------> Mouth Form (-1 to 1)
    SHAPE_COORD_DICT = {
        "G": (-1.0, 0.0), # bottom row
        "X": (0.0, 0.0),
        "A": (1.0, 0.0),            
        "F": (-1.0, 0.5), # middle row
        "C": (0.0, 0.5),
        "B": (1.0, 0.5),
        "E": (-1.0, 1.0), # top row
        "H": (0.0, 1.0),
        "D": (1.0, 1.0),
    }

    # converts an input shape (A,B,C,D,E,F,G,H,X) to a supported output shape
    def shape_converter(shape):
        # if shape == "X": return "A" # treat "X" (closed) as "A" (neutral)
        # if shape == "G": return "F" # optional shape
        # if shape == "H": return "C" # optional shape
        return shape # all other shapes stay the same

    def letter_to_shape(c):
        if c in "pbm": return "A" # A: Closed mouth for the “P”, “B”, and “M” sounds.
        # B is used for most consonants => fallback if none of the below match
        if c in "eh": return "C" # C: vowels like “EH” as in men and “AE” as in bat
        if c in "a": return "D" # D: vowels like “AA” as in father.
        if c in "r": return "E" # E: vowels like “AO” as in off and “ER” as in bird.
        if c in "wuo": return "F" # F: “UW” as in you, “OW” as in show, and “W”
        if c in "fv": return "G" # G: for “F” as in for and “V” as in very.
        if c == "l": return "H" # H: long “L” sounds
        if c.isspace(): return "X"
        return "B" # Fallback, likely consonants

    def live2d_set_shape(live2d, shape, t=0.3):
        # t = interpolation parameter, 1 = instant transition
        shape = shape_converter(shape)
        coords = SHAPE_COORD_DICT.get(shape, (0.0, 0.0))
        lastCoord = live2d_coord_cache.get(live2d, SHAPE_COORD_DICT["A"])
        c = ((1.0 - t) * lastCoord[0] + t * coords[0], (1.0 - t) * lastCoord[1] + t * coords[1])
        live2d.blend_parameter("ParamMouthForm", "Overwrite", c[0])
        live2d.blend_parameter("ParamMouthOpenY", "Overwrite", c[1])
        live2d_coord_cache[live2d] = c
        #live2d.blend_parameter("ParamMouthForm", "Add", coords[0], intensity)
        #live2d.blend_parameter("ParamMouthOpenY", "Add", coords[1], intensity)

    def text_based_lipsync():
        global speaking_text, speaking_index, next_animation_time

        if speaking_index >= len(speaking_text):
            return "A", None

        letter = speaking_text[speaking_index % len(speaking_text)].lower()
        shape = letter_to_shape(letter)
        shape = shape_converter(shape)
        dt = random.uniform(0.04, 0.18)

        # advance speaking index
        if time.time() >= next_animation_time:
            speaking_index += 1
            next_animation_time += dt # do this, because live2d replays faster then the requested pause, resulting in playback that is too fast => manually guard with next_animation_time

        return shape, dt

    def abc_tuple_to_displayable(abc_plus_time, prefix, suffix):
        abc, time = abc_plus_time
        return prefix + abc + suffix, time

    # WhileSpeaking with extended mouth shapes for Dynamic Displayable
    def _while_speaking_abc(name, prefix, suffix, st, at):
        global current_lip_file, current_lip_data, current_has_audio
        
        silent_d = prefix + "A" + suffix
        if current_speaker != name:
            return silent_d, None

        playing_name = renpy.music.get_playing('voice')
        if playing_name is None:
            if current_has_audio: return silent_d, None # finished playing 
            return abc_tuple_to_displayable(text_based_lipsync(), prefix, suffix) # no audio, fallback to text based lipsync
        else:
            current_has_audio = True # set once per interaction

        if playing_name != current_lip_file:
            # load lipsync data for current audio
            lip_file = playing_name.replace(".ogg", ".json")
            try:
                with renpy.loader.load(lip_file) as f:
                    current_lip_data = renpy.python.py_eval(f.read())
            except:
                current_lip_data = None
            current_lip_file = playing_name
        
        if current_lip_data is None:
            print(f"WARNING: No lip sync data found for {playing_name}")
            return abc_tuple_to_displayable(text_based_lipsync(), prefix, suffix)
        
        cues = current_lip_data.get("mouthCues", [])
        pos = renpy.music.get_pos('voice')
        if pos is None: pos = 0.0
        # find first occurence in cues where 'start' is greater than or equal to pos
        for cue in cues:
            if pos >= cue['start'] and pos <= cue['end']:
                # found cue!
                shape = cue['value']
                shape = shape_converter(shape)
                requested_d = prefix + shape + suffix
                pauseTime = max(0.0, cue['end'] - pos)
                return requested_d, pauseTime
        
        # replay finished
        return silent_d, None

    # live 2D function for lipsync
    def live2d_tuple_set_and_return(shape_plus_time, live2d):
        shape, time = shape_plus_time
        live2d_set_shape(live2d, shape)
        return time

    def _live2d_lipsync_callback(name, live2d, st):
        global current_lip_file, current_lip_data, current_has_audio

        if current_speaker != name:
            live2d_set_shape(live2d, "A", 1)
            return None # finished interaction

        playing_name = renpy.music.get_playing('voice')
        if playing_name is None:
            if current_has_audio:
                live2d_set_shape(live2d, "A", 1)
                return None # finished playing 
            return live2d_tuple_set_and_return(text_based_lipsync(), live2d) # no audio, fallback to text based lipsync
        else:
            current_has_audio = True # set once per interaction

        if playing_name != current_lip_file:
            # load lipsync data for current audio
            lip_file = playing_name.replace(".ogg", ".json")
            try:
                with renpy.loader.load(lip_file) as f:
                    current_lip_data = renpy.python.py_eval(f.read())
            except:
                current_lip_data = None
            current_lip_file = playing_name
        
        if current_lip_data is None:
            print(f"WARNING: No lip sync data found for {playing_name}")
            return live2d_tuple_set_and_return(text_based_lipsync(), live2d)

        cues = current_lip_data.get("mouthCues", [])
        pos = renpy.music.get_pos('voice')
        if pos is None: pos = 0.0
        # find first occurence in cues where 'start' is greater than or equal to pos
        for cue in cues:
            if pos >= cue['start'] and pos <= cue['end']:
                # found cue!
                shape = cue['value']
                pauseTime = max(0.0, cue['end'] - pos)
                live2d_set_shape(live2d, shape)
                return min(pauseTime, 0.1)
        
        # replay finished
        live2d_set_shape(live2d, "A", 1)
        return None

    live2d_lipsync_callback = renpy.curry(_live2d_lipsync_callback)

    # dynamic displayable for lipsync
    while_speaking_abc = renpy.curry(_while_speaking_abc)

    def WhileSpeaking_ABC(name, prefix, suffix):
        return DynamicDisplayable(while_speaking_abc(name, prefix, suffix))

    # automating mouth open when speaking
    def _speaker_callback(name, event, what, interact=True, **kwargs):
        global current_speaker, speaking_text, speaking_index, current_has_audio, next_animation_time
        
        if not interact:
            return
        if event == "show_done":
            current_speaker = name
            speaking_text = what
            speaking_index = 0
            current_has_audio = False # assume false by default
            next_animation_time = time.time()
        elif event == "end":
            current_speaker = None

    lipsync_callback = renpy.curry(_speaker_callback)