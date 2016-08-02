import random

class Mia():

	def __init__(self):
		numOfVariables = 1
		# Randomize variables to prevent bias.
		beta1 = random.randint(-100, 100)
		weightArray = [random.randint(-100, 100) for x in range(0, numOfVariables)] # the betas


	def train(y, trainingData):
		alpha = 0.05

		# Find the gradiant of the cost function for each dg/dx for each x in training data.
		# Cost function: g(x1, x2, x3... , y) = (y - (Beta1 + x1*weight1 + x2*weight2...))^2
		weightGradiants = [-2 * trainingData[x] * (y - (beta1 + sum([weightArray[y] * trainingData[y]]  for y in range(0, numOfVariables))))  for x in range(0, numOfVariables)]
		# Do the same for the first beta variable. 
		# NOTE: beta1 is really the first weight. It is just not multiplied by an x variable so it is treated separately. This also shows how the algorithm works.
		beta1_gradiant = -2 * (y - (beta1 + sum([weightArray[y] * trainingData[y]]  for y in range(0, numOfVariables))))

		# Adjust the variables based on gradiant, which point in the direction of maximum increase.
		beta1 += beta1_gradiant * alpha
		for x in range(0, numOfVariables):
			weightArray[x] += weightGradiants[x] * alpha


	def test(testingData):
		return (beta1 + sum([weightGradiants[x] * trainingData[x]  for x in range(0, numOfVariables)]) )