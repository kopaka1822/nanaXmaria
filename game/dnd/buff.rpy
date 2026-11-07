init -95 python:
    import random

    BUFF_TARGET_ABILITY = "ability"
    BUFF_TARGET_SKILL = "skill"
    BUFF_TARGET_ANY_ROLL = "any_roll"

    BUFF_DURATION_PERMANENT = "permanent"
    BUFF_DURATION_THIS_DAY = "this_day"


    class Buff(object):
        POSITIVE_MAGNITUDE_RANGES = {
            BUFF_TARGET_ABILITY: {
                BUFF_DURATION_PERMANENT: (6, 8),
                BUFF_DURATION_THIS_DAY: (8, 12),
            },
            BUFF_TARGET_SKILL: {
                BUFF_DURATION_PERMANENT: (4, 8),
                BUFF_DURATION_THIS_DAY: (8, 12),
            },
            BUFF_TARGET_ANY_ROLL: {
                BUFF_DURATION_THIS_DAY: (8, 16),
            },
        }

        NEGATIVE_MAGNITUDE_RANGES = POSITIVE_MAGNITUDE_RANGES

        def __init__(
            self,
            target_type,
            target_handle,
            value,
            duration,
            expires_on_day=None,
        ):
            self.target_type = target_type
            self.target_handle = target_handle
            self.value = int(value)
            self.duration = duration

            # Used for BUFF_DURATION_THIS_DAY, where expiration happens next morning.
            self.expires_on_day = expires_on_day

        @property
        def is_positive(self):
            return self.value > 0

        @property
        def is_negative(self):
            return self.value < 0

        @property
        def is_permanent(self):
            return self.duration == BUFF_DURATION_PERMANENT

        @property
        def is_this_day(self):
            return self.duration == BUFF_DURATION_THIS_DAY

        @property
        def description(self):
            """Auto-generates description based on Buff type."""
            if self.target_type == BUFF_TARGET_ABILITY:
                return get_ability_description(self.target_handle)
            elif self.target_type == BUFF_TARGET_SKILL:
                return get_skill_description(self.target_handle)
            else:  # BUFF_TARGET_ANY_ROLL
                return _("Boosts any roll")

        def is_expired(self, current_day):
            """
            Returns True when a THIS_DAY Buff has reached its expiry day.
            For all other durations, returns False.
            """
            if not self.is_this_day():
                return False

            if self.expires_on_day is None:
                return False

            return int(current_day) > int(self.expires_on_day)

        @property
        def display_title(self):
            sign = "+" if self.value > 0 else ""

            if self.target_type == BUFF_TARGET_ABILITY:
                base_name = get_ability_display(self.target_handle)
            elif self.target_type == BUFF_TARGET_SKILL:
                base_name = get_skill_display(self.target_handle)
            else:
                base_name = _("Any Roll")

            return "{} {}{}".format(base_name, sign, self.value)

        def affects_roll(self, roll_kind, handle):
            """
            roll_kind: BUFF_TARGET_ABILITY or BUFF_TARGET_SKILL
            handle: ability handle for ability rolls, skill handle for skill rolls
            """
            if self.target_type == BUFF_TARGET_ANY_ROLL:
                return True

            if roll_kind == BUFF_TARGET_ABILITY:
                return self.target_type == BUFF_TARGET_ABILITY and self.target_handle == handle

            if roll_kind == BUFF_TARGET_SKILL:
                if self.target_type == BUFF_TARGET_SKILL:
                    return self.target_handle == handle

                if self.target_type == BUFF_TARGET_ABILITY:
                    return get_skill_base_ability(handle) == self.target_handle

            return False

        @classmethod
        def get_recommended_range(cls, target_type, duration, negative=False):
            table = cls.NEGATIVE_MAGNITUDE_RANGES if negative else cls.POSITIVE_MAGNITUDE_RANGES
            return table[target_type][duration]

        @classmethod
        def create_random(
            cls,
            target_type,
            target_handle,
            duration,
            negative=False,
        ):
            minimum, maximum = cls.get_recommended_range(target_type, duration, negative=negative)
            value = random.randint(minimum, maximum)

            if negative:
                value = -value

            return cls(
                target_type=target_type,
                target_handle=target_handle,
                value=value,
                duration=duration,
            )


    # for side-story 1
    def generate_draw_buff_options():
        return [
            Buff.create_random(
                target_type=BUFF_TARGET_ABILITY,
                target_handle=random.choice(ABILITIES),
                duration=BUFF_DURATION_PERMANENT,
            ),
            Buff.create_random(
                target_type=BUFF_TARGET_SKILL,
                target_handle=random.choice(SKILLS),
                duration=BUFF_DURATION_PERMANENT,
            ),
            Buff.create_random(
                target_type=BUFF_TARGET_SKILL,
                target_handle=random.choice(SKILLS),
                duration=BUFF_DURATION_PERMANENT,
            ),
            Buff.create_random(
                target_type=BUFF_TARGET_SKILL,
                target_handle=random.choice(SKILLS),
                duration=BUFF_DURATION_PERMANENT,
            ),
        ]


    def generate_draw_buff_options_with_locked(offered_buffs, locked_buff):
        """Generates 3 new buffs, keeping the locked_buff in its original position."""
        new_draws = generate_draw_buff_options()
        try:
            locked_index = offered_buffs.index(locked_buff)
        except ValueError:
            return new_draws

        new_buffs = []
        buff_index = 0

        for i in range(4):
            if i == locked_index:
                new_buffs.append(locked_buff)
            else:
                new_buffs.append(new_draws[buff_index])
                buff_index += 1

        return new_buffs
