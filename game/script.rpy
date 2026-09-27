# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene black
    show maria idle:
        anchor (0.5, 0.5)
        ypos 1.35 xpos 0.45

    "Welcome to the game!"

    maria "Once more the shriek of the Gryphon, the squeaking of the Lizard’s slate-pencil, and the choking of the suppressed guinea-pigs, filled the air, mixed up with the distant sobs of the miserable Mock Turtle."

    show maria brows_up
    voice "voice/na08.ogg"
    maria "Once more the shriek of the Gryphon, the squeaking of the Lizard’s slate-pencil, and the choking of the suppressed guinea-pigs, filled the air, mixed up with the distant sobs of the miserable Mock Turtle."

    show maria eyes_squint brows_angry
    voice "voice/alice153.ogg"
    maria "'You are old', said the youth, \n'one would hardly suppose\n{space=30}That your eye was as steady as ever;\nYet you balanced an eel \non the end of your nose—\n{space=30}What made you so awfully clever?'"

    show maria eyes_blink iris_sad brows_down
    voice "voice/alice063.ogg"
    maria "I shall be punished for it now, I suppose, by being drowned in my own tears! That will be a queer thing, to be sure! However, everything is queer to-day."

    show maria head_sad
    voice "voice/alice033.ogg"
    maria "(Oh, my poor little feet, I wonder who will put on your shoes and stockings for you now, dears? I’m sure I shan’t be able!)"

    show maria head_forward eyes_squint brows_up iris_center
    voice "voice/alice018.ogg"
    maria "Now, Dinah, tell me the truth: did you ever eat a bat?"


    scene black

    show nana idle brows_up:
        anchor (0.5, 0.5)
        ypos 1.15 xpos 0.45

    voice "voice/na08.ogg"
    nana "Once more the shriek of the Gryphon, the squeaking of the Lizard’s slate-pencil, and the choking of the suppressed guinea-pigs, filled the air, mixed up with the distant sobs of the miserable Mock Turtle."

    show nana eyes_squint brows_neutral iris_center
    voice "voice/alice018.ogg"
    nana "Now, Dinah, tell me the truth: did you ever eat a bat?"

    show nana brows_down iris_center eyes_blink
    voice "voice/duchess23.ogg"
    nana "—or if you’d like it put more simply—‘Never imagine yourself not to be otherwise than what it might appear to others that what you were or might have been was not otherwise than what you had been would have appeared to them to be otherwise’."

    show nana eyes_closed_up brows_up
    "This is nana!"

    return
