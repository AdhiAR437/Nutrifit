
from fitness_tools.meals.meal_maker import MakeMeal


# converting weights from kg to pounds
def weight_in_pounds(weight):
    weight = weight * 2.20462
    return weight


# make the meal to get all nutrition
def nutrition(weight, activity, goal, body):
    weight_pounds = int(weight_in_pounds(weight))
    food = MakeMeal(weight_pounds, goal=goal, activity_level=activity,
                    body_type=body)

    maximum_calories = food.daily_max_calories()

    print(maximum_calories)
    return maximum_calories


