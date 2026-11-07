transform test_popup_fade:
    alpha 0.0
    linear 0.1 alpha 1.0   # fade in over 1s
    pause 3.0
    linear 2.0 alpha 0.0   # fade out over 2s

transform test_dice_shake:
    xoffset 0
    yoffset 0
    block:
        linear 0.04 xoffset -3 yoffset 1
        linear 0.04 xoffset 3 yoffset -1
        repeat 5
    xoffset 0
    yoffset 0

style cs_popup_label:
    size 28
    color "#dddddd"
    min_width 100
    bold True

screen test_result_popup(message, success, roll_value, bonus_tooltip=""):
    zorder 400
    modal False

    if success:
        on "show" action Play("sound", "sfx/roll_success.ogg")
    else:
        on "show" action Play("sound", "sfx/roll_failed.ogg")
    
    $ result_color = "#00ff00" if success else "#ff4444"

    frame:
        at test_popup_fade
        xalign 0.23
        yalign 0.72
        background Frame(Solid("#2f2f2fcc"), 6, 6)
        padding (20, 15)

        hbox:
            spacing 14

            fixed:
                at test_dice_shake
                xysize (64, 64)

                add "images/dice_template.png":
                    xalign 0.5
                    yalign 0.5
                    zoom 0.2

                text str(roll_value):
                    xalign 0.5
                    yalign 0.6
                    color "#000000"
                    size 20
                    bold True

            fixed:
                xfit True
                ysize 64

                textbutton message:
                    yalign 0.5
                    style "cs_label_button"
                    text_style "cs_popup_label"
                    text_size 28
                    text_color result_color
                    action NullAction()
                    tooltip bonus_tooltip

    $ tooltip = GetTooltip()

    if tooltip:
        nearrect:
            focus "tooltip"
            prefer_top True

            frame:
                xalign 0.5
                xmaximum 500
                background Frame(Solid("#1e1e1ee6"), 6, 6)
                padding (14, 10)

                text tooltip:
                    size 22
                    color "#dddddd"

    timer 5.0 action Hide("test_result_popup")