


# height /= 100
# Function to convert centimeter to meter
def cm_to_mt(height):
    height /= 100
    return height


# Function to calculate BMI and return BMI with body type
def bmi_calculator(height, weight):
    height=float(height)
    weight=float(weight)
    # Converting centimeter to meter
    height = cm_to_mt(height)

    # Calculating BMI
    bmi =(weight /(height ** 2))

    # Conditions to find out body type according to the BMI calculated
    if bmi < 18.5:
        return bmi
    elif 18.5 <= bmi <= 24.9:
        return bmi
    elif 25 <= bmi < 30:
        return bmi
    elif 30 <= bmi < 35:
        return bmi
    elif bmi >= 35:
        return bmi

