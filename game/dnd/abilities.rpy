init -100 python:
    import random

    # Internal handles for abilities and skills
    ABILITIES = ["str", "dex", "con", "int", "wis", "cha"]
    SKILLS = [
        "intimidation",
        "athletics",
        "acrobatics",
        "stealth",
        "sleight_of_hand",
        "history",
        "arcana",
        "investigation",
        "nature",
        "religion",
        "insight",
        "perception",
        "animal_handling",
        "medicine",
        "deception",
        "performance",
        "persuasion",
    ]

    # translatable display + description metadata for abilities and skills
    ABILITY_DATA = {
        "str": {
            "display": _("Strength"),
            "short_display": _("STR"),
            "description": _("Physical strength. Affects intimidation and athletics rolls."),
        },
        "dex": {
            "display": _("Dexterity"),
            "short_display": _("DEX"),
            "description": _("Agility, reflexes and balance. Affects acrobatics, stealth, and sleight of hand rolls."),
        },
        "con": {
            "display": _("Constitution"),
            "short_display": _("CON"),
            "description": _("Health and stamina."),
        },
        "int": {
            "display": _("Intelligence"),
            "short_display": _("INT"),
            "description": _("Knowledge and mental acuity. Affects history, arcana, investigation, nature, and religion rolls."),
        },
        "wis": {
            "display": _("Wisdom"),
            "short_display": _("WIS"),
            "description": _("Awareness and intuition. Affects insight, perception, animal handling, and medicine rolls."),
        },
        "cha": {
            "display": _("Charisma"),
            "short_display": _("CHA"),
            "description": _("Personal charm. Affects deception, performance, and persuasion rolls."),
        },
    }

    SKILL_DATA = {
        "intimidation": {
            "display": _("Intimidation"),
            "ability": "str",  # per doc note: Strength-based for this game
            "description": _("Pressure someone into giving information."),
        },
        "athletics": {
            "display": _("Athletics"),
            "ability": "str",
            "description": _("Climb, jump, or perform feats of strength."),
        },
        "acrobatics": {
            "display": _("Acrobatics"),
            "ability": "dex",
            "description": _("Keep your balance."),
        },
        "stealth": {
            "display": _("Stealth"),
            "ability": "dex",
            "description": _("Move quietly and avoid being noticed."),
        },
        "sleight_of_hand": {
            "display": _("Sleight of Hand"),
            "ability": "dex",
            "description": _("Perform delicate hand movements without being noticed."),
        },
        "history": {
            "display": _("History"),
            "ability": "int",
            "description": _("Recall information about history or people."),
        },
        "arcana": {
            "display": _("Arcana"),
            "ability": "int",
            "description": _("Knowledge about magic."),
        },
        "investigation": {
            "display": _("Investigation"),
            "ability": "int",
            "description": _("Analyze clues and ask clever questions."),
        },
        "nature": {
            "display": _("Nature"),
            "ability": "int",
            "description": _("Recall information about plants, animals, and weather."),
        },
        "religion": {
            "display": _("Religion"),
            "ability": "int",
            "description": _("Recall information about gods, rituals, and holy symbols."),
        },
        "insight": {
            "display": _("Insight"),
            "ability": "wis",
            "description": _("Notice hidden meaning in wording and intonation."),
        },
        "perception": {
            "display": _("Perception"),
            "ability": "wis",
            "description": _("Notice small movements and changes in body language."),
        },
        "animal_handling": {
            "display": _("Animal Handling"),
            "ability": "wis",
            "description": _("Calm or train an animal."),
        },
        "medicine": {
            "display": _("Medicine"),
            "ability": "wis",
            "description": _("Diagnose illnesses and help the injured."),
        },
        "deception": {
            "display": _("Deception"),
            "ability": "cha",
            "description": _("Tell a convincing lie."),
        },
        "performance": {
            "display": _("Performance"),
            "ability": "cha",
            "description": _("Entertain through humor or acting."),
        },
        "persuasion": {
            "display": _("Persuasion"),
            "ability": "cha",
            "description": _("Convince someone with charm."),
        },
    }

    def get_ability_display(handle):
        return ABILITY_DATA[handle]["display"]

    def get_ability_short_display(handle):
        return ABILITY_DATA[handle]["short_display"]

    def get_ability_description(handle):
        return ABILITY_DATA[handle]["description"]

    def get_skill_display(handle):
        return SKILL_DATA[handle]["display"]

    def get_skill_description(handle):
        return SKILL_DATA[handle]["description"]

    def get_skill_base_ability(skill_handle):
        return SKILL_DATA[skill_handle]["ability"]