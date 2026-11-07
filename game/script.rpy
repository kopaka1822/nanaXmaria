transform maria_pos:
    anchor (0.5, 0.5)
    ypos 1.35 xpos 0.45

transform nana_pos:
    anchor (0.5, 0.5)
    ypos 1.15 xpos 0.45

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

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    # basic idea: maria lights up candles and tells about her situation
    scene black
    #show candle notlit # TODO

    "The chapel is dimly lit by the last traces of daylight."
    
    maria "It's getting late. I should light the candles."

    # TODO sound of match
    "*Scrrrch*"

    # TODO sound of lighting up the candle
    #show candle lit # TODO
    # TODO sound of match fire
    "*fwoosh*"

    #show maria idle mouth_smile at maria_pos

    maria "There, that's better."

    #show maria eyes_squint
    maria "God said: \"Let there be light.\" And there was light! ~ Genesis 1:3"

    # end candle scene
    scene black
    $ show_character_sheet_overlay = True # enable character sheet once maria is visible
    show maria idle iris_left mouth_neutral at maria_pos
    "Maria looks around the otherwise empty chapel."

    show maria iris_center brows_updown
    maria "Though, I doubt we'll be having any visitors tonight."

    # TODO sfx?
    show maria eyes_squint brows_neutral
    "She starts lighting another candle."

    show maria eyes_blink iris_right brows_down
    maria "What is the use of a chapel, without worshipers or visitors?"

    show maria iris_sad mouth_pout
    maria "A chapel should be a place where people come to find the Lord, after all."

    # TODO rain sound
    show maria iris_center brows_neutral mouth_neutral
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
    maria "Apparently, my great-great-grandfather helped building this chapel for that reason, and supposedly, there have not been any serious accidents since then."

    if maria_sheet.skill_test("religion", 12):
        show maria eyes_closed_up brows_neutral mouth_smile
        maria "Before you were born, I set you apart for my holy purpose. ~ Jeremiah 1:5"

    show maria eyes_blink brows_up mouth_smile
    maria "It's a wonderful feeling, knowing that the Lord's house can offer shelter to those in need."

    show maria iris_right brows_neutral mouth_neutral eyes_squint
    maria "Though most of the time, it only shelters me... from the constant bragging of my sister at home."

    show maria iris_left eyes_blink
    "Maria pauses for a moment, looking at the rain outside."

    show maria iris_think brows_up
    maria "I wonder how my sister Camilla is doing in Willowe."

    show maria iris_center brows_neutral
    maria "She is probably busy with her potion shop. She is always busy with that."

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
    "The rain is getting even more intense outside."

    show maria brows_down
    maria "It sounds like someone did not eat up their meal yesterday."

    show maria mouth_smile eyes_closed_up
    maria "At least, that's something my parents used to say: 'If you don't eat up, there will be bad weather tomorrow.'"

    show maria eyes_blink brows_neutral mouth_neutral
    maria "Well, it's not going to stop anytime soon. Just like a soul that doesn't know Jesus, wandering around until damnation."
    
    show maria brows_neutral mouth_neutral:
        ease 0.5 xoffset -400
    "Maria walks over to light another candle, briefly turning her back to the window."

    stop music fadeout 2.0 
    "..."

    # tODO crash boom ouw


    return
