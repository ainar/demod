"""Utility functions for CREST."""
from ...utils.parse_helpers import translate_1d


def crest_act_to_demod(crest_activities):
    """Transform the crest activity names into demod.

    Args:
        crest_activities: [description]
    """
    translate_dict = {
        "LEVEL": "level",
        "ACTIVE_OCC": "active_occupancy",
        "ACT_IRON": "ironing",
        "ACT_HOUSECLEAN": "cleaning",
        "ACT_TV": "watching_tv",
        "ACT_COOKING": "cooking",
        "ACT_LAUNDRY": "laundry",
        "ACT_WASHDRESS": "self_washing",
    }
    return translate_1d(crest_activities, translate_dict)


def crest_appname_to_demod_type(names):
    """Transform the crest appliances names into demod.

    Args:
        names: [description]
    """
    translate_dict = {
        "CHEST_FREEZER": "chest_freezer",
        "FRIDGE_FREEZER": "fridge_freezer",
        "FRIDGE": "fridge",
        "UPRIGHT_FREEZER": "upright_freezer",
        "ANSWER_MACHINE": "answermachine_phone",
        "CD_PLAYER": "cd_speaker",
        "CLOCK": "clock",
        "PHONE": "fixed_phone",
        "HIFI": "hifi_speaker",
        "IRON": "iron",
        "VACUUM": "vacuum_cleaner",
        "FAX": "fax_printer",
        "PC": "fixed_computer",
        "PRINTER": "printer",
        "TV1": "tv",
        "TV2": "tv",
        "TV3": "tv",
        "VCR_DVD": "dvd_console",
        "RECEIVER": "dual_box",
        "HOB": "hob",
        "OVEN": "oven",
        "MICROWAVE": "microwave",
        "KETTLE": "kettle",
        "SMALL_COOKING": "toaster",
        "DISH_WASHER": "dishwasher",
        "TUMBLE_DRYER": "tumble_dryer",
        "WASHING_MACHINE": "washingmachine",
        "WASHER_DRYER": "washer_dryer",
        "DESWH": "des_water_heater",
        "E_INST": "einst_water_heater",
        "ELEC_SHOWER": "electric_shower",
        "BASIN": "basin",
        "SINK": "sink",
        "SHOWER": "shower",
        "BATH": "bath",
        "VENTILATION": "ventilation",
        "BASELOAD_ONE": "baseload_one",
        "BASELOAD_TWO": "baseload_two",
        "BASELOAD_THREE": "baseload_three",
        "BASELOAD_FOUR": "baseload_four",
        "BASELOAD_FIVE": "baseload_five",
		"OTHER_ICT": "other_ict",
        "BOX": "box",
		"FRIDGE_AMERICAN": "fridge_american",
        "BIG_MULTIMEDIA": "big_multimedia",
        "BIG_COOKING": "big_cooking",
    }
    return translate_1d(names, translate_dict)
