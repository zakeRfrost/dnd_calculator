from calculations.success_rate import *
from calculations.damage_per_round import damage_per_round

def calculate_and_display_hit_chance(modifier, proficiency, additional_bonus, ac):
    """Calculate the hit chance and return the message to display to the user."""
    normal_percentage = calculate_success_rate(modifier, proficiency, additional_bonus, ac)
    advantage_percentage = calculate_success_rate(modifier, proficiency, additional_bonus, ac, 1)
    bonus_text = f", bonus of {additional_bonus}" if additional_bonus != "" else ""
    response = (f"The hit chance, given a modifier of {modifier}, proficiency of {proficiency}"
                f"{bonus_text}, and an AC of {ac} is: "
                f"\r\nNormal roll = {normal_percentage:.2f}% \tAdvantage roll = {advantage_percentage:.2f}%")
    return response

def calculate_and_display_skill_check(modifier, additional_bonus, dc):
    """Calculate the chance of succeeding on a skill check and return the message to display to the user."""
    normal_percentage = calculate_success_rate(modifier, 0, additional_bonus, dc)
    advantage_percentage = calculate_success_rate(modifier, 0, additional_bonus, dc, 1)
    bonus_text = f", bonus of {additional_bonus}" if additional_bonus != "" else ""
    response = (f"The chance to pass the skill check, given a flat modifier of {modifier}"
                f"{bonus_text}, and an DC of {dc} is: "
                f"\r\nNormal roll = {normal_percentage:.2f}% \tAdvantage roll = {advantage_percentage:.2f}%")
    return response

def calculate_and_display_saving_throw(modifier, additional_bonus, dc):
    """Calculate the chance of succeeding on a saving throw and return the message to display to the user."""
    normal_percentage = calculate_success_rate(modifier, 0, additional_bonus, dc)
    advantage_percentage = calculate_success_rate(modifier, 0, additional_bonus, dc, 1)
    bonus_text = f", bonus of {additional_bonus}" if additional_bonus != "" else ""
    response = (f"The chance to pass the saving throw, given a flat modifier of {modifier}"
                f"{bonus_text}, and an DC of {dc} is: "
                f"\r\nNormal roll = {normal_percentage:.2f}% \tAdvantage roll = {advantage_percentage:.2f}%")
    return response

def calculate_and_display_probability_one_dice_meets(dice, target):
    """Calculate the probability of at least one of the dice succeeding in meeting
    the target result or surpasses it, and return the message to display to the user."""
    percentages = probability_one_die_meets(dice, target)
    response_parts = []
    for i, percentage in enumerate(percentages, start=1):
        response_parts.append(f"{i}: {percentage:.2f}%")

    response = "\r\n".join(response_parts)
    num_dice, value_dice = dice.split('d')
    response = f"Probabilities for up to {num_dice} amount of {value_dice} sided dice to succeed at least one with a minimum roll of {target} are:\r\n" + response
    return response

def calculate_and_display_probability_repeated_success(dice, target):
    """Calculate the probability of multiple dice meeting or surpassing the target result
    and return the message to display to the user."""
    percentages = probability_repeated_success(dice, target)
    response_parts = []
    for i, percentage in enumerate(percentages, start=1):
        response_parts.append(f"{i}: {percentage:.2f}%")

    response = "\r\n".join(response_parts)
    num_dice, value_dice = dice.split('d')
    response = f"Probabilities for up to {num_dice} amount of {value_dice} sided dice to all meet a minimum roll of {target} are:\r\n" + response
    return response

def calculate_and_display_damage_per_round(modifier, proficiency, additional_bonus, ac, damage_formula, attacks_per_turn, advantage, bonus_attacks_data):
    """Wrapper for damage_per_round that formats the result into a message."""
    try:
        hit_chance, critical_chance, average_damage, average_critical_damage, bonus_attack_dpr_list, dpr = damage_per_round(
            modifier, proficiency, additional_bonus, ac, damage_formula, attacks_per_turn, advantage, bonus_attacks_data
        )
    except Exception as e:
        return f"An error occurred during the calculation: {str(e)}"

    # Build response
    response = (f"Hit Chance: {hit_chance:.2f}%\n"
                f"Critical Chance: {critical_chance * 100:.2f}%\n"
                f"Average Damage: {average_damage}\n"
                f"Average Critical Damage: {average_critical_damage}\n"
                f"Attacks Per Turn: {attacks_per_turn}\n"
                f"Base Attack DPR: {dpr - sum(bonus_attack_dpr_list):.2f}\n")

    # Add bonus attack details
    for i, (bonus_attack, bonus_dpr) in enumerate(zip(bonus_attacks_data, bonus_attack_dpr_list), start=1):
        response += (f"  Bonus Attack {i}:\n"
                     f"    Damage Formula: {bonus_attack['damage_formula']}\n"
                     f"    Hit Modifier: {bonus_attack['hit_modifier']}\n"
                     f"    Advantage: {'Yes' if bonus_attack['advantage'] else 'No'}\n"
                     f"    DPR: {bonus_dpr:.2f}\n")

    # Total DPR
    response += f"Total Damage Per Round (DPR): {dpr:.2f}"

    return response