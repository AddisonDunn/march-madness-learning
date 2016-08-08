import random

class Mia(object):

	def __init__(self):
		self.numOfVariables = 1
		# Randomize variables to prevent bias.
		self.beta1 = random.randint(-100, 100)
		self.weightArray = [random.random() for x in range(0, self.numOfVariables)] # the betas

	def train(self, y, trainingData):
		alpha = 0.01


		# Find the gradiant of the cost function for each dg/dx for each x in training data.
		# Cost function: g(x1, x2, x3... , y) = (y - (Beta1 + x1*weight1 + x2*weight2...))^2
		weightGradiants = [-2 * trainingData[x] * (y - (self.beta1 + sum(self.weightArray[y] * trainingData[y]  for y in range(0, self.numOfVariables))))  for x in range(0, self.numOfVariables)] 
		# Do the same for the first beta variable. 
		# NOTE: beta1 is really the first weight. It is just not multiplied by an x variable so it is treated separately. This also shows how the algorithm works.
		beta1_gradiant = -2 * (y - (self.beta1 + sum(self.weightArray[y] * trainingData[y]  for y in range(0, self.numOfVariables))))

		# Adjust the variables based on gradiant, which point in the direction of maximum increase.
		self.beta1 += beta1_gradiant * alpha
		for x in range(0, self.numOfVariables):
			self.weightArray[x] += weightGradiants[x] * alpha


	def test(self, testingData):
		return (self.beta1 + sum([weightGradiants[x] * trainingData[x]  for x in range(0, self.numOfVariables)]) )