# This file display the character sheet overlay for the active player, which should be stored in the "player" variable
default show_character_sheet_overlay = False

screen character_sheet_overlay():
    zorder 400
    if show_character_sheet_overlay:
        frame:
            xpos 20
            ypos 20
            xminimum 300
            background Frame(Solid("#2f2f2fcc"), 6, 6)
            padding (24, 24)

            vbox:
                spacing 4
                text _(player.get_name()) style "cs_header"

                for ability_handle in ABILITIES:
                    $ ability_is_hl = cs_is_ability_highlighted(player.get_name(), ability_handle)
                    $ ability_label_color = "#ffff66" if ability_is_hl else "#dddddd"
                    $ ability_value_color = "#ffff66" if ability_is_hl else "#ffffff"
                    $ ability_bonus_color = "#ffff66" if ability_is_hl else "#aaaaaa"

                    hbox:
                        spacing 14

                        textbutton get_ability_short_display(ability_handle):
                            style "cs_label_button"
                            text_style "cs_label"
                            text_color ability_label_color
                            action NullAction()
                            tooltip get_ability_description(ability_handle)

                        text str(player.get_effective_ability_level(ability_handle)):
                            style "cs_value"
                            color ability_value_color

                        textbutton "({:+d})".format(player.get_effective_ability_bonus(ability_handle)):
                            style "cs_bonus_button"
                            text_style "cs_bonus"
                            text_color ability_bonus_color
                            action NullAction()
                            tooltip _("{bonus:+d} for all {ability} rolls.").format(
                                bonus=player.get_effective_ability_bonus(ability_handle),
                                ability=get_ability_display(ability_handle)
                            )

                python:
                    active_skills = [s for s in SKILLS if player.get_effective_skill_level(s) != 0]

                if active_skills:
                    null height 14
                    text _("Skills") style "cs_header"
                    for skill_handle in active_skills:
                        $ skill_is_hl = cs_is_skill_highlighted(player.get_name(), skill_handle)
                        $ skill_label_color = "#ffff66" if skill_is_hl else "#dddddd"
                        $ skill_value_color = "#ffff66" if skill_is_hl else "#ffffff"

                        hbox:
                            spacing 14

                            textbutton get_skill_display(skill_handle):
                                style "cs_label_button"
                                text_style "cs_label"
                                text_color skill_label_color
                                action NullAction()
                                tooltip get_skill_description(skill_handle)

                            textbutton _("LV {lv}").format(lv=player.get_effective_skill_level(skill_handle)):
                                style "cs_bonus_button"
                                text_style "cs_value"
                                text_color skill_value_color
                                action NullAction()
                                tooltip _("{total:+d} for all {skill} rolls.\n   {base:+d} from {ability}\n   {skill_mod:+d} from {skill_name}").format(
                                    total=player.get_effective_ability_bonus(get_skill_base_ability(skill_handle)) + player.get_effective_skill_level(skill_handle),
                                    skill=get_skill_display(skill_handle),
                                    base=player.get_effective_ability_bonus(get_skill_base_ability(skill_handle)),
                                    ability=get_ability_display(get_skill_base_ability(skill_handle)),
                                    skill_mod=player.get_effective_skill_level(skill_handle),
                                    skill_name=get_skill_display(skill_handle)
                                )

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

style cs_header:
    size 28
    color "#aaaaaa"
    bold True

style cs_label:
    size 28
    color "#dddddd"
    min_width 100

style cs_value:
    size 28
    color "#ffffff"
    bold True

style cs_bonus:
    size 28
    color "#aaaaaa"

style cs_label_button:
    background None
    hover_background None
    xpadding 0
    ypadding 0
    left_padding 0
    right_padding 0
    top_padding 0
    bottom_padding 0

style cs_bonus_button:
    background None
    hover_background None
    xpadding 0
    ypadding 0
    left_padding 0
    right_padding 0
    top_padding 0
    bottom_padding 0

# for auto highlighting in the character sheet: tells when to stop highlighting abilities/skills after a test is performed
default cs_highlight_player = None # name of the player whose abilities/skills should be highlighted
default cs_highlight_ability = None
default cs_highlight_ability_until = 0.0
default cs_highlight_skill = None
default cs_highlight_skill_until = 0.0

init python:
    import time

    # Hook overlay into say and choice screens via config
    config.overlay_screens.append("character_sheet_overlay")

    # marks ability and clears skill highlight
    def cs_mark_ability_highlight(player_name, ability_handle, duration=5.0):
        # Overwrite any previous ability highlight with this one and set expiry.
        store.cs_highlight_player = player_name
        store.cs_highlight_ability = ability_handle
        store.cs_highlight_ability_until = time.time() + duration
        store.cs_highlight_skill = None  # Clear any skill highlight since we're now highlighting an ability.
        renpy.restart_interaction()

    # marks base ability and skill highlight
    def cs_mark_skill_highlight(player_name, skill_handle, duration=5.0):
        # Overwrite any previous skill highlight with this one and set expiry.
        store.cs_highlight_player = player_name
        store.cs_highlight_skill = skill_handle
        store.cs_highlight_skill_until = time.time() + duration
        # highlight base ability of the skill as well
        base_ability = get_skill_base_ability(skill_handle)
        store.cs_highlight_ability = base_ability
        store.cs_highlight_ability_until = store.cs_highlight_skill_until
        renpy.restart_interaction()

    def cs_is_ability_highlighted(player_name, ability_handle):
        if store.cs_highlight_player != player_name: return False
        return (store.cs_highlight_ability == ability_handle and
                store.cs_highlight_ability_until > time.time())

    def cs_is_skill_highlighted(player_name, skill_handle):
        if store.cs_highlight_player != player_name: return False
        return (store.cs_highlight_skill == skill_handle and
                store.cs_highlight_skill_until > time.time())

