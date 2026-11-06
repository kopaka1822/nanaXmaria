# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

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

    show maria idle mouth_smile:
        anchor (0.5, 0.5)
        ypos 1.35 xpos 0.45

    maria "There, that's better."

    show maria eyes_squint
    maria "God said: \"Let there be light.\" And there was light! ~ Genesis 1:3"

    show maria eyes_blink iris_left
    "Maria looks around the otherwise empty chapel."

    show maria iris_center brows_updown
    maria "Though, I doubt we'll be having any visitors tonight."

    # TODO sfx?
    show maria mouth_smile eyes_closed_up
    "She starts lighting another candle."

    show maria eyes_blink
    maria "What is the use of a chapel, without worshipers or visitors?"

    maria "A chapel should be a place where people come to find the Lord, after all."

    # TODO rain sound
    "The sound of water droplets can be heard from outside."

    maria "Oh, it's starting to rain! ... again."

    play music "audio/Prelude in C.mp3"

    maria "Well, that's to be expected from the rainy season."

    maria "The rain falls on the righteous and the unrighteous alike ~ Matthew 5:45"

    "The rain starts to get heavier, and the sound of water droplets from outside becomes louder."

    maria "And apparently, He has decided that we need all of it."

    "Maria has finished lighting the candles on this spot and walks toward the other side of the chapel."

    maria "Still, I suppose there is a reason this chapel was built here, in the middle of nowhere."

    maria "The mountain road can be quite dangerous during the rainy season."

    maria "Travellers caught in the rain sometimes have nowhere else to go."

    maria "And a warm dry chapel is certainly better than a cold chapel!"

    maria "Actually there used to be a lot of accidents here during the rainy season, at least that's what my grandfather used to tell me."

    maria "Apparently, my great-great-grandfather helped building this chapel for that reason, and supposedly, there have not been any serious accidents since then."

    maria "Before you were born, I set you apart for my holy purpose. ~ Jeremiah 1:5"

    maria "It's a wonderful feeling, knowing that the Lord's house can offer shelter to those in need."

    maria "Though most of the time, it only shelters me... from the constant bragging of my sister at home."

    "Maria pauses for a moment, looking at the rain outside."

    maria "I wonder how my sister Camilla is doing in Willowe."

    maria "She is probably busy with her potion shop. She is always busy with that."

    maria "Unlike some other people, who get sent to the middle of nowhere to take care of a chapel."

    "Maria shakes her head and smiles."

    maria "But I shouldn't complain. The Lord has chosen this path for me, and I should walk it faithfully."

    maria "Though I do wish the path had a few more people on it..."

    # TODO sfx with rain and thunder taking over
    "The rain is getting even more intense outside."

    maria "It sounds like someone did not eat up their meal yesterday."

    maria "At least, that's something my parents used to say: 'If you don't eat up, there will be bad weather tomorrow.'"

    maria "Well, it's not going to stop anytime soon. Just like a soul that doesn't know Jesus, floating without purpose."
    
    "Maria walks over to light another candle, briefly turning her back to the window."

    stop music fadeout 2.0 
    "..."

    # tODO crash boom ouw
    

    show nana idle brows_up mouth_neutral:
        anchor (0.5, 0.5)
        ypos 1.15 xpos 0.45

    voice "voice/na08.ogg"
    nana "Once more the shriek of the Gryphon, the squeaking of the Lizard’s slate-pencil, and the choking of the suppressed guinea-pigs, filled the air, mixed up with the distant sobs of the miserable Mock Turtle."

    show nana eyes_squint brows_neutral iris_center mouth_pout
    voice "voice/alice018.ogg"
    nana "Now, Dinah, tell me the truth: did you ever eat a bat?"

    show nana brows_down iris_center eyes_blink mouth_smile
    voice "voice/duchess23.ogg"
    nana "—or if you’d like it put more simply—‘Never imagine yourself not to be otherwise than what it might appear to others that what you were or might have been was not otherwise than what you had been would have appeared to them to be otherwise’."

    show nana eyes_closed_up brows_up mouth_bigsmile
    "This is nana!"

    return
