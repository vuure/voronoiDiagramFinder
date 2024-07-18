import random
import math
import numpy
import matplotlib.pyplot as plt

origin = [0, 0, 0, 0]


# Calculation of Dot Product Between Two Unit Vectors
def dot_product_of_two_vectors(vector1, vector2):
    dot_product = (vector1[0] * vector2[0]) + (vector1[1] * vector2[1])

    return round(dot_product, 3)


# Calculation of Cross Product Between Two Unit Vectors
def cross_product_two_vectors(vector1, vector2):
    cross_product = (vector1[0] * vector2[1]) - (vector1[1] * vector2[0])

    return round(cross_product, 3)


# Calculation of Unit Vector Between Two Points
def calculate_unit_vector_two_points(first_point, second_point):
    x_of_first_point, y_of_first_point = first_point[1], first_point[2]
    xOfSecondPoint, yOfSecondPoint = second_point[1], second_point[2]

    magnitude = math.sqrt(((xOfSecondPoint - x_of_first_point) ** 2) + ((yOfSecondPoint - y_of_first_point) ** 2))

    xOfUnitVector = (x_of_first_point - xOfSecondPoint) / magnitude
    yOfUnitVector = (y_of_first_point - yOfSecondPoint) / magnitude

    calculatedUnitVector = [round(xOfUnitVector, 2), round(yOfUnitVector, 2)]

    return calculatedUnitVector


# Generating Random Points and Sorting Them by Range to Origin
def generatePointsAndSortRanges():
    points = []
    for number in range(1, 21):

        r = random.uniform(2.5, 15)

        if number <= 5:
            angle = random.randint(5, 85)
        elif number <= 10:
            angle = random.randint(95, 175)
        elif number <= 15:
            angle = random.randint(195, 265)
        elif number <= 20:
            angle = random.randint(275, 355)

        XofPoint = r * math.cos(angle)
        YofPoint = r * math.sin(angle)

        distance = math.sqrt(XofPoint ** 2 + YofPoint ** 2)

        points.append([number, round(XofPoint, 2), round(YofPoint, 2), round(distance)])

    points.sort(key=lambda x: x[3])

    return points


# Finding Points That Closest and Passed the 'Dot Production' Elimination
def findingEligibleClosestPoints(points):
    closest_points = []

    unit_vectors = []

    while len(points) > 0:

        closesPoint = points[0]
        closest_points.append(closesPoint)

        unitVectorPoint = calculate_unit_vector_two_points(origin, closesPoint)
        unit_vectors.append(unitVectorPoint)

        del points[0]

        uneliminated_points = []

        for indexNumber, tryingPoint in enumerate(points):

            unitVectorTryingPoint = calculate_unit_vector_two_points(tryingPoint, closesPoint)

            dotProd = dot_product_of_two_vectors(unitVectorTryingPoint, unitVectorPoint)

            if dotProd < 0:
                pass
            else:
                uneliminated_points.append(points[indexNumber])

        points = uneliminated_points

    return [closest_points, unit_vectors]


# Calculating Mid-Points Between Eligible Closest Points and Origin
def midpointCalculation(eligiblePoints):
    midpoints = []

    for indexNumber, pointEligible in enumerate(eligiblePoints):
        desiredMidpointX, desiredMidpointY = pointEligible[1] / 2, pointEligible[2] / 2

        midpoints.append([desiredMidpointX, desiredMidpointY])

    return midpoints


# Finding Desired Angle by Dot and Cross Product Methods for Plotting
def calculateAngles_DotandCrosProduct(vectorNormal, vectorsList):
    angles = []
    for vector in vectorsList:
        anglesCalculation = numpy.degrees(
            numpy.arctan2(cross_product_two_vectors(vectorNormal, vector), dot_product_of_two_vectors(vectorNormal, vector)))
        angles.append(anglesCalculation % 360)
    return angles

#Generate Points and Define Them to Variable
points_list = generatePointsAndSortRanges()

#Use Generated Points, Find Points Fits to Elimination Criterias and Calculate Unit Vectors to Origin of That Points
pointsEligibleForMidpointCalcultion, unitVectorsOfEligiblePoints = findingEligibleClosestPoints(points_list)

#Find Mid-Points Between Eligible Points and Origin and Define Them to Variable
midpointsCalculated = midpointCalculation(pointsEligibleForMidpointCalcultion)

#Calculate Angles Required for Plotting Voronoi Cell of Origin and Define Them to Variable
angles_forPoints = calculateAngles_DotandCrosProduct(unitVectorsOfEligiblePoints[0], unitVectorsOfEligiblePoints[1:])

midpoints_sortingForPlotting = [midpointsCalculated[0]]

paired_andSorted = sorted(zip(angles_forPoints, midpointsCalculated[1:]))

for i, mid in paired_andSorted:
    midpoints_sortingForPlotting += [mid]

#Plot All Points and Origin
for pointsWillShow in points_list:
    plt.plot(pointsWillShow[1], pointsWillShow[2], "b*")

plt.plot(0, 0, "rx")

#Calculate and Plot Voronoi Cell
for indexNumber in range(len(midpoints_sortingForPlotting)):
    xValues = [midpoints_sortingForPlotting[indexNumber][0],
                midpoints_sortingForPlotting[(indexNumber + 1) % len(midpoints_sortingForPlotting)][0]]

    yValues = [midpoints_sortingForPlotting[indexNumber][1],
                midpoints_sortingForPlotting[(indexNumber + 1) % len(midpoints_sortingForPlotting)][1]]

    plt.plot(xValues, yValues, color="orange")

#Show All Plots
plt.show()
