transform maria_pos:
    anchor (0.5, 0.5)
    ypos 1.35 xpos 0.45

transform nana_pos:
    anchor (0.5, 0.5)
    ypos 1.15 xpos 0.45

transform nana_sit_pos:
    anchor (0.5, 0.5)
    zoom 0.5
    ypos 0.55 xpos 0.75

transform broom_floor_pos:
    anchor (0.5, 0.5)
    zoom 0.5
    ypos 0.75 xpos 0.7

transform maria_nana_sit_pos:
    anchor (0.5, 0.5)
    zoom 0.65
    ypos 0.9 xpos 0.5

transform nana_duo_pos:
    anchor (0.5, 0.5)
    zoom 0.7
    ypos 0.9 xpos 0.65

transform maria_duo_pos:
    anchor (0.5, 0.5)
    zoom 0.7
    ypos 0.97 xpos 0.35

transform candle_pos:
    anchor (0.5, 0.5)
    ypos 0.5 xpos 0.5

transform window_pos:
    anchor (0.5, 0.5)
    ypos 0.45 xpos 0.5

######################################################
## JUMP LABELS #######################################
######################################################
default jump_label_maria1 = "nana_menu_potato_salad"
default jump_label_maria2 = "scene_nana_onmyway_boulder2"
default jump_label_maria3 = "scene_nana_onmyway_boulder3"
default jump_label_maria4 = ""
default jump_label_nana1 = "scene_nana_onmyway_boulder"
default jump_label_nana2 = "scene_nana_mayonnaise"
default jump_label_nana3 = ""
default jump_label_nana4 = ""

transform candle_unlit_and_dark:
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(-0.1)

transform candle_unlit:
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(0.0)

transform candle_lit:
    matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(0.17)
    ease 2.0 matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(0.21)
    ease 2.0 matrixcolor SaturationMatrix(0.0) * BrightnessMatrix(0.17)
    repeat

default maria_sheet = CharacterSheet(
    name="Maria", 
    ability_values={"str": 8, "dex": 12, "con": 10, "int": 10, "wis": 14, "cha": 8}, 
    skill_values={"religion": 6}
)
default nana_sheet = CharacterSheet(
    name="Nana",
    ability_values={"str": 12, "dex": 6, "con": 12, "int": 14, "wis": 10, "cha": 6},
    skill_values={"arcana": 2, "nature": 2}
)
default player = maria_sheet # in the first run, the player is maria (This variable is used to display the character sheet)
default time_loop_count = 1

init python:
    # helper functions
    def player_is_maria():
        return player == maria_sheet

    def player_is_nana():
        return player == nana_sheet

    class _PopupHistoryEntry(object):
        def __init__(self, who, what, who_args=None):
            self.who = who
            self.what = what
            self.who_args = who_args if who_args is not None else {}

    def push_popup_history(text, who=None, who_args=None):
        global _history_list
        _history_list.append(_PopupHistoryEntry(who, text, who_args))

screen time_loop_popup():

    modal True
    tag day_popup

    on "show" action Function(push_popup_history, _("Loop %d") % time_loop_count, None, {"color": gui.accent_color})
    
    button:
        xfill True
        yfill True
        background Solid("#0008")
        action Return()

        text _("Loop [time_loop_count]"):
            xalign 0.5
            yalign 0.5
            size 96
            color "#fff"

label start:
    #jump scene2

    scene black
    call screen time_loop_popup()

    show candle idle flame_off at candle_pos, candle_unlit_and_dark

    "The chapel is dimly lit by the last traces of daylight."
    
    show candle at candle_pos, candle_unlit
    $ show_character_sheet_overlay = True
    maria "It's getting late. I should light the candles."

    play sound "sfx/get_match.ogg"
    "Maria takes a match out of a box."

    maria "And God said, \"Let there be light.\""

    # "She strikes the match, and..."

    if not maria_sheet.ability_test("dex", 12):
        play sound "sfx/match_breaks.ogg"
        maria "but the match snapped out of spite..."

        maria "Let me try again."

        if not maria_sheet.ability_test("dex", 12):
            play sound "sfx/match_breaks2.ogg"
            "Another match is struck, but it breaks again."

            while not maria_sheet.ability_test("dex", 12):
                play sound "sfx/match_breaks.ogg"
                "And another one."

    show candle flame_on at candle_pos, candle_lit
    play sound "sfx/match_on.ogg"
    play ambient "sfx/candle_sounds.ogg" fadein 3.0
    maria "And there was light! ~ Genesis 1:3"

    # end candle scene
    scene black
    
    show maria idle iris_left mouth_neutral at maria_pos
    "Maria looks around the otherwise empty chapel."

    show maria iris_center brows_updown
    maria "Though, I doubt we'll be having any visitors tonight."

    show maria eyes_squint brows_neutral
    play sound "sfx/match_on.ogg"
    "She starts lighting another candle."

    show maria eyes_blink iris_right brows_down
    maria "What is the use of a chapel, without worshipers or visitors?"

    show maria iris_sad mouth_pout
    maria "A chapel should be a place where people come to find the Lord, after all."

    show maria iris_center brows_neutral mouth_neutral
    play ambient2 "sfx/rain.ogg" volume 0.4 fadein 1.0
    stop ambient fadeout 10.0 # fade out the candle sounds
    "The sound of water droplets can be heard from outside."

    show maria brows_up
    maria "Oh, it's starting to rain! ... again."

    play music "audio/Prelude in C.mp3"
    show maria eyes_closed_up brows_down mouth_smile
    maria "Well, that's to be expected from the rainy season."

    if maria_sheet.skill_test("religion", 10):
        show maria eyes_squint mouth_neutral brows_neutral
        maria "The rain falls on the righteous and the unrighteous alike ~ Matthew 5:45"
    else:
        "..."

    show maria eyes_blink mouth_neutral brows_neutral iris_think mouth_frown
    play ambient2 "sfx/rain.ogg" volume 0.6 fadein 1.0
    "The rain starts to get heavier, and the sound of water droplets from outside becomes louder."

    show maria iris_center brows_updown mouth_neutral
    maria "And apparently, He has decided that we need all of it."

    show maria brows_neutral mouth_neutral:
        ease 0.5 xoffset -200
    "Maria has finished lighting the candles on this spot and walks toward the other side of the chapel."

    show maria eyes_closed_up mouth_smile brows_down:
        xoffset -200
    maria "Still, I suppose there is a reason this chapel was built here, in the middle of nowhere."

    show maria eyes_blink brows_neutral
    maria "The mountain road can be quite dangerous during the rainy season."

    show maria iris_sad brows_down mouth_frown
    maria "Travellers caught in the rain sometimes have nowhere else to go."

    show maria iris_center
    maria "And a warm dry chapel is certainly better than a cold chapel!"

    show maria iris_think brows_updown
    maria "Actually there used to be a lot of accidents here during the rainy season, at least that's what my grandfather used to tell me."

    show maria iris_center brows_down
    maria "Apparently, my great-great-grandfather helped build this chapel for that reason, and supposedly, there have not been any serious accidents since then."

    if maria_sheet.skill_test("religion", 12):
        show maria eyes_closed_up brows_neutral mouth_smile
        maria "Before you were born, I set you apart for my holy purpose. ~ Jeremiah 1:5"

    show maria eyes_blink brows_up mouth_smile
    maria "It's a wonderful feeling, knowing that the Lord's house can offer shelter to those in need."

    show maria iris_right brows_neutral mouth_neutral eyes_squint
    maria "Though most of the time, it only shelters me... from my sister's constant bragging back home."

    show maria iris_left eyes_blink
    "Maria pauses for a moment, looking at the rain outside."

    show maria iris_think brows_up
    maria "I wonder how my sister Camilla is doing in Willowe."

    show maria iris_center brows_neutral
    maria "She is probably busy with her potion shop. She always is."

    show maria iris_right eyes_squint
    maria "Unlike some other people, who get sent to the middle of nowhere to take care of a chapel."

    show maria iris_center eyes_closed_up mouth_smile
    "Maria shakes her head and smiles."

    show maria eyes_blink
    maria "But I shouldn't complain. The Lord has chosen this path for me, and I should walk it faithfully."

    show maria eyes_squint brows_down mouth_neutral
    maria "Though I do wish the path had a few more people on it..."

    # TODO sfx with rain and thunder taking over
    show maria eyes_blink brows_neutral
    play ambient2 "sfx/rain.ogg" volume 0.8
    "The rain is getting even more intense outside."

    show maria brows_down
    maria "Ohh, sounds like someone didn't finish their dinner yesterday!"

    show maria mouth_smile eyes_closed_up
    maria "At least, that's something my parents used to say: 'If you don't eat up, there will be bad weather tomorrow.'"

    show maria eyes_blink brows_neutral mouth_neutral
    maria "Well, it's not going to stop anytime soon. Just like a soul that doesn't know Jesus, wandering around until damnation."
    
    show maria brows_neutral mouth_neutral:
        ease 0.5 xoffset -400
    "Maria walks over to light another candle, briefly turning her back to the window."

label window_scene:

    scene black
    show chapel_window idle at window_pos

    #stop music fadeout 2.0 

    "The raindrops gently patter agains the chapel window, playing a soothing melody."

    play sound "sfx/thunderstrike.ogg"
    stop music
    show chapel_window nana_on

    show black as black2:
        matrixcolor BrightnessMatrix(1.0)
    "A sudden strike of lighting illuminates the scene."

    show black as black2:
        alpha 1.0
        linear 0.5 alpha 0.0
    "And for a brief moment, something appears right behind the window."

    scene black
    play sound "sfx/shatter.mp3"
    "The sound of shattering glass echoes through the chapel and Maria turns around in shock."

    show broom_floor at broom_floor_pos
    show nana_sit nana_sit_idle brows_down iris_sad mouth_frown head_sad at nana_sit_pos
    show maria idle brows_neutral mouth_frown brows_up iris_right at maria_nana_sit_pos:
        xoffset -400

    $ show_character_sheet_overlay = True    
    nana "Ouch, ouch, ouch! Oh no, potato salad! Are you alright?!"

    play music "audio/mozart sonata in c slow.ogg"
    "Nana reaches out to the broom."

    $ charisma_chance = player.ability_success_rate("cha", 14)
    if player_is_maria():
        menu:
            "Potato salad?":
                $ jump_label_maria1 = "maria_menu_potato_salad"
            "I suppose the door was too difficult to find? (Charisma [charisma_chance]\%)":
                $ jump_label_maria1 = "maria_menu_charisma1"
    
    $ renpy.jump(jump_label_maria1)

label maria_menu_potato_salad:
    show maria brows_updown mouth_neutral iris_center head_what
    maria "Potato salad?"

    show nana_sit mouth_pout
    "Nana is still examining the broom, and does not appear to have heard Maria's question."

    show maria head_neutral brows_neutral
    show nana_sit mouth_bigsmile brows_up 
    nana "Oh, thank goodness! You're alright!"

    show nana_sit eyes_closed_up head_neutral iris_center
    "Nana gives the broom a little hug before finally noticing Maria."

    if player_is_maria():
        if maria_sheet.skill_test("perception", 10):
            "The broom makes a small rustling sound when Nana picks it up."
        else:
            "..."
    
    show nana_sit eyes_blink mouth_neutral brows_neutral
    nana "Oh! Um, sorry! I didn't notice you! Did you say something?"

    show maria mouth_smile brows_up
    maria "Potato salad? Pray tell, is that the name of the broom?"

    show nana_sit mouth_bigsmile brows_up
    nana "Oh, yes! This is potato salad! And it's, um... just a normal broom. Nothing special!"

    show nana_sit iris_right brows_neutral
    if player_is_maria():
        if maria_sheet.skill_test("insight", 10):
            "Nana seems to be hiding something, but she is trying her best to act normal."
        else:
            "..."
    show nana_sit iris_center mouth_smile
    show maria iris_left brows_neutral
    maria "It is an awfully peculiar name for something so ordinary."

    show nana_sit iris_right
    show maria iris_center
    nana "Well, I suppose it is a bit peculiar."

    show nana_sit iris_center mouth_bigsmile brows_up
    nana "I named it after my favorite food!"

    show maria mouth_neutral brows_neutral
    "Nana looks at Maria with a smile and wide eyes, as if she is awaiting a compliment."

    show nana_sit mouth_neutral brows_neutral
    "Maria decides not to comment."

    show nana_sit iris_center mouth_bigsmile brows_up
    nana "His first name is Potato, and his last name is Salad!"

    show nana_sit mouth_neutral brows_neutral
    show maria eyes_closed_down
    "Maria closes her eyes to relax for a moment, and then opens them again."

    jump scene2

label maria_menu_charisma1:
    
    show maria brows_updown mouth_smile
    maria "I suppose the door was too difficult to find?"

    show nana_sit brows_up mouth_neutral iris_center head_neutral
    nana "Oh! I... well..."

    show nana_sit brows_updown iris_think
    if maria_sheet.ability_test("cha", 14):
        "Nana pauses for a moment, before realizing that Maria was making a joke."

        show nana_sit mouth_bigsmile brows_up eyes_closed_up iris_center
        nana "Oh! Haha! Yes, I suppose it was!"

        show nana_sit brows_neutral mouth_smile eyes_blink 
        show maria iris_center brows_neutral mouth_smile
        nana "You know, you can always come in through the door, but you can only come in through the window once!"

        show maria mouth_neutral
        "Maria is waiting for the punchline."

        show nana_sit iris_right
        nana "Because it will be broken after that..."

        show maria mouth_smile eyes_closed_up
        show nana_sit iris_center
        "Maria manages to force a small smile, mostly out of politeness."

    else:
        "Nana is thinking about Maria's question, but she doesn't seem to understand the joke."

        show nana_sit brows_neutral iris_center mouth_smile
        nana "Oh! The door? I think it should be... right over there!"

        show maria iris_center brows_neutral mouth_neutral
        maria "..."

        nana "Why are you asking?"

        show nana_sit brows_updown mouth_neutral
        nana "Wait, how did you even get in without the door? Did you also crash into a window?"

        show maria eyes_closed_up mouth_smile
        maria "Never mind, forget I asked."

    jump scene2

label scene2:
    scene black
    nana "Wait, let me get up!"

label scene_maria_introduces_herself:
    scene black
    show nana idle mouth_frown brows_down at nana_duo_pos
    show maria idle mouth_smile at maria_duo_pos

    nana "I am sorry Sister, I didn't mean to intrude like that!"

    if player_is_nana():
        if nana_sheet.skill_test("perception", 14):
            "Maria's eye twitches slightly at the word 'Sister'."
        else:
            "..."
    
    maria "Oh, please. Just call me Maria."

    show nana brows_up mouth_neutral
    nana "So- sorry Sister! I mean, Maria!"

    show nana brows_updown mouth_pout iris_left
    nana "But you are a Sister, right? I mean a follower of the church."

    show nana mouth_neutral
    show maria eyes_closed_up mouth_bigsmile brows_up
    maria "We are all brothers and sisters of Jesus." # ~ Galatians 3:26

    show maria eyes_blink brows_neutral mouth_smile
    show nana iris_center
    if maria_sheet.skill_test("religion", 10):
        maria "The Spirit himself testifies that we are God's children. ~ Romans 8:16"
    elif player_is_maria():
        "..."

    show maria iris_right
    maria "But yes, though I am actually the appointed priestess of this chapel."

    show nana mouth_bigsmile brows_up eyes_closed_up iris_center
    show maria iris_center brows_neutral mouth_neutral
    nana "I see! Sister Maria, that is impressive!"

    show maria eyes_closed_down mouth_neutral brows_down
    maria "Like I said, just Maria is fine."

    if player_is_nana():
        if nana_sheet.skill_test("insight", 14):
            "It appears that Maria is slowly losing her patience."
        else:
            "..."

    show maria eyes_blink brows_neutral mouth_neutral
    show nana eyes_blink mouth_smile
    maria "The youngest daughter of my parents already calls me sister, and I don't need anyone else to call me that."

    if nana_sheet.ability_test("int", 12):
        show nana brows_up mouth_bigsmile
        nana "Um, Oh! You have a younger sister? I see! That is wonderful!"
        show maria iris_left mouth_smile
        maria "Yes, wonderful indeed. Bless the Lord!"
        if player_is_nana():
            if nana_sheet.skill_test("insight", 14):
                "This remark sounded a bit sarcastic."
            else:
                "..."
    else:
        show nana iris_think mouth_frown brows_down
        nana "Um, what?"
        show maria eyes_closed_down mouth_neutral brows_down
        maria "Forget it, just call me Maria."


    # short scene switch to the window
    scene black
    show chapel_window idle at window_pos

    "The raindrops continue to patter against the remaining chapel windows."

    #play ambient "sfx/wind.ogg" fadein 2.0
    "A howling gust of wind rushes through the broken window."

label scene_nana_introduces_herself:

    scene black
    show nana idle mouth_bigsmile brows_neutral at nana_duo_pos
    show maria idle mouth_smile at maria_duo_pos

    nana "Nana."

    show nana brows_up
    nana "My name is Nana!"

    show nana brows_neutral iris_think mouth_smile
    nana "I was um..."

    if player_is_nana():
        $ deception_chance = nana_sheet.ability_success_rate("cha", 8)
        menu:
            "On my way to the boulder.":
                $ jump_label_nana1 = "scene_nana_onmyway_boulder"
            "Gathering herbs (Deception [deception_chance]\%)":
                $ jump_label_nana1 = "scene_nana_onmyway_herbs"
            # "Just passing through (Persuasion)"
    
    $ renpy.jump(jump_label_nana1)

label scene_nana_onmyway_boulder:
    # TODO set a flag about destination to boulder?

    show nana iris_center brows_up
    nana "I was on my way to the boulder."

    show maria brows_updown
    maria "The boulder? Are you talking about the mountain peak?"

    show maria brows_neutral
    show nana eyes_closed_up
    nana "Yes! There's a gathering there, and..."

    show nana eyes_blink brows_down iris_right
    if player_is_nana():
        nana "(Oh no wait, I can't tell her that I'm on my way to a witch gathering!)"
    
    nana "I mean a family gathering of course!"

    if player_is_maria():
        menu:
            "A family gathering?":
                $ jump_label_maria2 = "scene_nana_onmyway_boulder2"
            "I see, that's nice!":
                $ jump_label_maria2 = "scene_nana_onmyway_boulder_finish"
    $ renpy.jump(jump_label_maria2)

label scene_nana_onmyway_boulder2:

    maria "A family gathering?"

    show nana iris_sad
    nana "Yes! Um, my family is gathering there every few years to do... um, family things!"

    if player_is_maria():
        menu:
            "Family things?":
                $ jump_label_maria3 = "scene_nana_onmyway_boulder3"
            "I see, that's nice!":
                $ jump_label_maria3 = "scene_nana_onmyway_boulder_finish"
    $ renpy.jump(jump_label_maria3)

label scene_nana_onmyway_boulder3:

    maria "Family things?"

    show nana iris_right brows_neutral
    nana "Yeah, you know, like, singing and dancing and ... stuff."

    show nana iris_center brows_down
    nana "I mean, what do you want me to say? Do you want me to sing one of the songs?"

    show maria eyes_closed_up brows_up mouth_smile
    maria "Oh no, I was just curious."

    jump scene_maria_nana_discuss_magic

label scene_nana_onmyway_boulder_finish:

    show maria eyes_closed_up brows_up mouth_smile
    maria "I see, that's nice!"

    jump scene_maria_nana_discuss_magic

label scene_nana_onmyway_herbs:
    "TODO"
    if nana_sheet.skill_test("deception", 8):
        "success"
    else:
        "fail"

    jump scene_maria_nana_discuss_magic
    
label scene_maria_nana_discuss_magic:

    "Nana seems to have trouble managing social situations."

    show maria eyes_blink brows_neutral mouth_neutral
    show nana iris_center
    "Meanwhile, Maria takes another look at the broom and Nana's attire."

    show maria eyes_squint mouth_neutral
    if maria_sheet.skill_test("religion", 12):
        maria "Death has come through our windows and entered our palaces ~ Jeremiah 9:21"
    else:
        "..."

    show maria brows_down    
    maria "Say, you are not by any chance a witch, are you?"

    show nana mouth_bigsmile brows_up iris_right
    show maria brows_up eyes_blink
    nana "A witch? Me? No, no no. How did you get that idea?"

    show nana iris_think
    nana "I mean: in a world with gods and magic, what even is a witch?"

    show maria mouth_smile eyes_closed_up
    maria "Oh dear lord! I believe there is an important distinction."

    show maria brows_down
    show nana iris_center
    scene black with dissolve
    stop ambient fadeout 1.0
    stop ambient2 fadeout 1.0
    play music "audio/Canon in D Major.mp3" fadein 2.0

    show shaping idle
    maria "In the beginning, there was nothing but chaos."

    maria "Aether particles were everywhere."

    maria "Just like souls who don't know Jesus, floating without purpose."
    
    show shaping gather_on
    maria "But then, the Lord gathered the scattered aether particles."
    
    show shaping hammer_on hammerrotate_on
    play sound ["<silence 0.2>", "sfx/hammer.ogg"]
    maria "He created the {b}First Spells{/b} to form the particles into shapes."

    # flame with flame sfx
    show shaping flame_on
    play sound "sfx/match_on.ogg"
    play ambient "sfx/candle_sounds.ogg" fadein 3.0
    maria "And with that, he created all the First Shapes, such as fire, water, dirt and stone."

    maria "And God saw that it was good."

    maria "It is also known as the 'First Shaping', and it's the first of the Lord's many miracles."

    maria "Everything that exists naturally in this world is made from first shapes."

    scene black
    stop ambient
    stop ambient2
    play ambient2 "sfx/rain.ogg" volume 0.8 fadein 2.0 # continue ambient sfx from before

    show nana idle mouth_smile at nana_duo_pos
    show maria idle mouth_smile at maria_duo_pos

    nana "So everything that 'naturally' exists is made from first shapes?"

    maria "Yes, precisely."

    if player_is_nana():
        menu:
            "Is mayonnaise a first shape?":
                $ jump_label_nana2 = "scene_nana_mayonnaise"
            "Is Horseradish a first shape?":
                $ jump_label_nana2 = "scene_nana_horseradish"
    
    $ renpy.jump(jump_label_nana2)

label scene_nana_mayonnaise:

    nana "Is mayonnaise a first shape?"

    maria "Well..."

    if maria_sheet.skill_test("arcana", 10):
        maria "No, mayonnaise is not a first shape. It is a mixture of first shapes, such as water and oil."
    else:
        maria "I think it could be... but I am not sure. I haven't studied arcana."

    jump scene_magic2

label scene_nana_horseradish:

    nana "Is horseradish a first shape?"

    if maria_sheet.skill_test("arcana", 10):
        maria "No, horseradish is not a first shape. Living beings are complex and consist of multiple first shapes."
    else:
        maria "I don't think it is... There was some catch to it, I forgot."

    jump scene_magic2
label scene_magic2:

    maria "Anyways, let me continue:"

    maria "The devil grew envious of the Lord's creation and wanted to spread chaos and destruction."

    maria "So he created the {b}Second Spells{/b} to create unimaginable things."

    maria "These Second Spells can make curses, illusions and even monsters."

    nana "So the Second Spells are evil, and the First Spells are good?"

    maria "Yes, and while mages generally use the First Spells, there are also witches, who use the evil Second Spells."

    nana "Oh, don't worry! I am a mage that only uses First Spells!"

    nana "Mostly, -I mean exclusively! First Spells!"
    
    "Nana looks at Maria with big eyes and a large smile, as if she was waiting for praise."

    if player_is_maria():
        if maria_sheet.skill_test("insight", 12):
            maria "(Did she just slip up by saying 'mostly'?)"
        else:
            "..."

label scene_window_fix:

    scene black
    show chapel_window idle at window_pos

    "The rain outside continues..."

    #play ambient "sfx/wind.ogg" fadein 2.0
    "And the wind that is entering through the broken window is getting colder and colder."

label scene_nana_introduces_herself:

    scene black
    show nana idle mouth_bigsmile brows_neutral at nana_duo_pos
    show maria idle mouth_smile at maria_duo_pos

    maria "I think we have more important matters to address."

    maria "How are we going to fix the window?"

    if player_is_nana():
        menu:
            "I know a second spell to fix the window!":
                $ jump_label_nana3 = "scene_nana_window_fix_spell"

