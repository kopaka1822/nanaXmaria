init -20 python:
    NON_EXLUSIVES_LIVE2D = [
        # head:
        "head_neutral", "head_left", "head_right", "head_up", "head_sad", "head_back", "head_forward", "head_proud", "head_what", "head_asking",
        # iris:
        "iris_center", "iris_left", "iris_right", "iris_think", "iris_sad", "iris_random",
        # mouth:
        #"mouth_neutral", "mouth_cringe", "mouth_frown", "mouth_pout", "mouth_small", "mouth_smile", "mouth_vampire",
        # eyes:
        "eyes_blink", "eyes_closed_down", "eyes_closed_up", "eyes_squint", "eyes_wink",
        # brows: 
        "brows_neutral", "brows_up", "brows_down", "brows_updown", "brows_angry",
    ]

    # filter attributes with the same prefix, so ["mouth_smile", "mouth_frown"] becomes ["mouth_smile"]
    def live2d_attribute_filter(attr):
        res = []
        seen = set()
        for a in attr:
            prefix = a.split('_', 1)[0]
            if prefix not in seen:
                seen.add(prefix)
                res.append(a)

        return res

image maria = Live2D("images/live2d/maria.model3.json", zoom=0.5, base=1.0, default_fade=0.0, loop=True, nonexclusive=NON_EXLUSIVES_LIVE2D, attribute_filter=live2d_attribute_filter) # TODO update function

image nana = Live2D("images/live2d/nana.model3.json", zoom=0.5, base=1.0, default_fade=0.0, loop=True, nonexclusive=NON_EXLUSIVES_LIVE2D, attribute_filter=live2d_attribute_filter) # TODO update function