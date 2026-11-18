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

transform candle_pos:
    anchor (0.5, 0.5)
    ypos 0.5 xpos 0.5

transform window_pos:
    anchor (0.5, 0.5)
    ypos 0.45 xpos 0.5

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

init python:
    # helper functions
    def player_is_maria():
        return player == maria_sheet

    def player_is_nana():
        return player == nana_sheet

label start:
    #jump window_scene

    scene black
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

    $ intimidation_chance = player.skill_success_rate("intimidation", 10)
    $ medicine_chance = player.skill_success_rate("medicine", 16)
    $ charisma_chance = player.ability_success_rate("cha", 18)
    if player_is_maria():
        menu:
            "Potato salad?":
                jump maria_menu_potato_salad
            "Are you out of you mind? (Intimidation [intimidation_chance]\%)":
                jump maria_menu_intimidation1
            "Oh dear lord! Are you hurt? (Medicine [medicine_chance]\%)":
                jump maria_menu_medicine1
            "I suppose the door was too difficult to find? (Charisma [charisma_chance]\%)":
                jump maria_menu_charisma1
    else: # TODO jump to last default
        jump nana_menu_potato_salad

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

    jump scene2

label maria_menu_intimidation1:
    "TODO"
    jump scene2

label maria_menu_medicine1:
    "TODO"
    jump scene2

label maria_menu_charisma1:
    "TODO"
    jump scene2

label scene2:
    "The scene continues..."
