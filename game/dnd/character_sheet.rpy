init -90 python:
    import random

    class RollModifier(object):
        def __init__(self, ability_level=0, skill_level=0):
            self.ability_level = int(ability_level)
            self.skill_level = int(skill_level)

        def apply_buff(self, buff):
            if buff.target_type == BUFF_TARGET_ABILITY:
                self.ability_level += buff.value
            else:
                # Includes skill Buffs and any-roll Buffs as flat roll bonus.
                self.skill_level += buff.value

        def apply_buffs(self, buffs):
            for buff in buffs:
                self.apply_buff(buff)

        @staticmethod
        def calc_ability_bonus(score):
            return (int(score) - 10) // 2 # D&D based ability bonus

        def get_roll_bonus(self):
            return self.calc_ability_bonus(self.ability_level) + self.skill_level

    class CharacterSheet(object):
        def __init__(self, name="Player", ability_values=None, skill_values=None, buffs=None):
            self.name = name
            self.abilities = {a: 8 for a in ABILITIES} 
            self.skills = {s: 0 for s in SKILLS}
            self.buffs = list(buffs) if buffs else []

            if ability_values:
                for k, v in ability_values.items():
                    self.abilities[k] = v

            if skill_values:
                for k, v in skill_values.items():
                    self.skills[k] = v

        def get_name(self):
            return self.name

        def add_buff(self, buff):
            self.buffs.append(buff)

        def remove_expired_buffs(self, current_day):
            self.buffs = [buff for buff in self.buffs if not buff.is_expired(current_day)]

        def _build_roll_modifier(self, roll_kind, handle):
            if roll_kind == BUFF_TARGET_ABILITY:
                modifier = RollModifier(ability_level=self.abilities[handle])
            else:
                base_ability = get_skill_base_ability(handle)
                modifier = RollModifier(
                    ability_level=self.abilities[base_ability],
                    skill_level=self.skills[handle],
                )

            for buff in self.buffs:
                if not (buff.is_permanent or buff.is_this_day):
                    continue

                if buff.affects_roll(roll_kind, handle):
                    modifier.apply_buff(buff)

            return modifier

        def _build_roll_bonus_breakdown(self, roll_kind, handle, total_bonus):
            """Builds a tooltip text describing where the roll bonus comes from."""

            if roll_kind == BUFF_TARGET_ABILITY:
                ability_display = get_ability_display(handle)
                base_ability_bonus = self.get_effective_ability_bonus(handle)
                buff_bonus = total_bonus - base_ability_bonus

                text = _("{total:+d} total for {ability} rolls.\n   {base:+d} from {ability}").format(
                    total=total_bonus,
                    ability=ability_display,
                    base=base_ability_bonus,
                )
                if buff_bonus:
                    text += _("\n   {buffs:+d} from Buffs").format(buffs=buff_bonus)
                return text
            
            # Buff target skill:
            base_ability = get_skill_base_ability(handle)
            ability_display = get_ability_display(base_ability)
            skill_display = get_skill_display(handle)
            base_ability_bonus = self.get_effective_ability_bonus(base_ability)
            base_skill_bonus = self.get_effective_skill_level(handle)
            buff_bonus = total_bonus - base_ability_bonus - base_skill_bonus

            text = _("{total:+d} total for {skill} rolls.\n   {base:+d} from {ability}\n   {skill_mod:+d} from {skill}").format(
                total=total_bonus,
                skill=skill_display,
                base=base_ability_bonus,
                ability=ability_display,
                skill_mod=base_skill_bonus,
            )
            if buff_bonus:
                text += _("\n   {buffs:+d} from Buffs").format(buffs=buff_bonus)
            return text

        def get_effective_ability_level(self, ability_handle):
            '''Ability level plus bonus from Buffs'''
            assert ability_handle in self.abilities
            modifier = self._build_roll_modifier(BUFF_TARGET_ABILITY, ability_handle)
            return max(1, int(modifier.ability_level))

        def get_effective_skill_level(self, skill_handle):
            '''Skill level plus bonus from Buffs'''
            assert skill_handle in self.skills
            modifier = self._build_roll_modifier(BUFF_TARGET_SKILL, skill_handle)
            return int(modifier.skill_level)

        def get_effective_ability_bonus(self, ability_handle):
            '''Ability bonus including Buffs'''
            return RollModifier.calc_ability_bonus(self.get_effective_ability_level(ability_handle))

        @staticmethod
        def _roll_d20():
            return random.randint(1, 20)

        @staticmethod
        def _success_from_roll(raw_d20, modifier, dc):
            if raw_d20 == 20:
                return True
            if raw_d20 == 1:
                return False
            return (raw_d20 + modifier) >= dc

        
        def ability_test(self, ability_handle, dc):
            """
            Rolls a D20 and return True if the test succeded.

            Args:
                ability_handle (str): "wis", "int", "cha"
                dc (int): test difficulty class, typically between 5 and 20

            Returns:
                bool: True if the roll succeeded, False otherwise. Nat 20 always succeeds, Nat 1 always fails.

            Example:
                succeeded = player.ability_test("wis", 14)
            """
            raw = self._roll_d20()
            ability_display = get_ability_display(ability_handle)
            modifier = self._build_roll_modifier(BUFF_TARGET_ABILITY, ability_handle)

            mod = modifier.get_roll_bonus()
            success = self._success_from_roll(raw, mod, dc)

            # auto-highlight used ability for ~5s
            cs_mark_ability_highlight(ability_handle, 5.0)

            # show popup with result
            ability_display = get_ability_display(ability_handle)
            result_text = "{} {} {{color=#ddd}}({}/{}){{/color}}".format(ability_display, _("succeeded") if success else _("failed"), raw+mod, dc)
            bonus_breakdown = self._build_roll_bonus_breakdown(BUFF_TARGET_ABILITY, ability_handle, mod)
            renpy.hide_screen("test_result_popup")
            renpy.show_screen("test_result_popup", message=result_text, success=success, roll_value=raw, bonus_tooltip=bonus_breakdown)

            return success

        def skill_test(self, skill_handle, dc):
            """
            Rolls a D20 and return True if the test succeded.

            Args:
                skill_handle (str): "deception", "history", etc.
                dc (int): test difficulty class, typically between 5 and 20

            Returns:
                bool: True if the roll succeeded, False otherwise. Nat 20 always succeeds, Nat 1 always fails.

            Example:
                succeeded = player.skill_test("deception", 12)
            """
            assert skill_handle in self.skills, "Unknown skill handle: {}".format(skill_handle)

            raw = self._roll_d20()
            base_ability = get_skill_base_ability(skill_handle)
            skill_display = get_skill_display(skill_handle)
            modifier = self._build_roll_modifier(BUFF_TARGET_SKILL, skill_handle)

            mod = modifier.get_roll_bonus()
            success = self._success_from_roll(raw, mod, dc)

            # auto-highlight used skill + its base ability for ~5s
            cs_mark_skill_highlight(skill_handle, 5.0)

            # show popup with result
            skill_display = get_skill_display(skill_handle)
            result_text = "{} {} {{color=#ddd}}({}/{}){{/color}}".format(skill_display, _("succeeded") if success else _("failed"), raw+mod, dc)
            bonus_breakdown = self._build_roll_bonus_breakdown(BUFF_TARGET_SKILL, skill_handle, mod)
            renpy.hide_screen("test_result_popup")
            renpy.show_screen("test_result_popup", message=result_text, success=success, roll_value=raw, bonus_tooltip=bonus_breakdown)

            return success

        @staticmethod
        def _success_rate_from_modifier(modifier, dc):
            successes = 0
            for raw in range(1, 21): # iterate over all possible D20 rolls (lazy but good enough for now)
                if CharacterSheet._success_from_roll(raw, modifier, dc):
                    successes += 1
            return successes / 20.0

        def ability_success_rate(self, ability_handle, dc):
            modifier = self._build_roll_modifier(BUFF_TARGET_ABILITY, ability_handle)
            mod = modifier.get_roll_bonus()
            rate = self._success_rate_from_modifier(mod, dc)
            return int(round(rate * 100.0))

        def skill_success_rate(self, skill_handle, dc):
            modifier = self._build_roll_modifier(BUFF_TARGET_SKILL, skill_handle)
            mod = modifier.get_roll_bonus()
            rate = self._success_rate_from_modifier(mod, dc)
            return int(round(rate * 100.0))


