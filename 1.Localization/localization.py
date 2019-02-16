# The function localize takes the following arguments:
#
# colors:
#        2D list, each entry either 'R' (for red cell) or 'G' (for green cell)
#
# measurements:
#        list of measurements taken by the robot, each entry either 'R' or 'G'
#
# motions:
#        list of actions taken by the robot, each entry of the form [dy,dx],
#        where dx refers to the change in the x-direction (positive meaning
#        movement to the right) and dy refers to the change in the y-direction
#        (positive meaning movement downward)
#        NOTE: the *first* coordinate is change in y; the *second* coordinate is
#              change in x
#
# sensor_right:
#        float between 0 and 1, giving the probability that any given
#        measurement is correct; the probability that the measurement is
#        incorrect is 1-sensor_right
#
# p_move:
#        float between 0 and 1, giving the probability that any given movement
#        command takes place; the probability that the movement command fails
#        (and the robot remains still) is 1-p_move; the robot will NOT overshoot
#        its destination in this exercise
#
# The function should RETURN (not just show or print) a 2D list (of the same
# dimensions as colors) that gives the probabilities that the robot occupies
# each cell in the world.
#
# Compute the probabilities by assuming the robot initially has a uniform
# probability of being in any cell.
#
# Also assume that at each step, the robot:
# 1) first makes a movement,
# 2) then takes a measurement.
#
# Motion:
#  [0,0] - stay
#  [0,1] - right
#  [0,-1] - left
#  [1,0] - down
#  [-1,0] - up

def sense(p, colors, measurement, sensor_right):
	q = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]
	s = 0.0

	for i in range(len(p)):
		for j in range(len(p[i])):
			hit = (colors[i][j] == measurement)
			# posterior = measurement_probability * prior
			q[i][j] = (hit*sensor_right + (1-hit)*(1-sensor_right)) * p[i][j]
			s += q[i][j]
	for i in range(len(q)):
		for j in range(len(q[i])):
			q[i][j] = q[i][j] / s

	return q


def move(p, motion, p_move):
	q = [[0.0 for row in range(len(p[0]))] for col in range(len(p))]

	for i in range(len(p)):
		for j in range(len(p[i])):
			# probability_after_motion = probability_before_motion * transition_probability
			q[i][j] = p[(i-motion[0])%len(p)][(j-motion[1])%len(p[i])] + ((1-p_move)*p[i][j]) * p_move

	return q


def localize(colors, measurements, motions, sensor_right, p_move):
	pinit = 1.0 / (float(len(colors)) * float(len(colors[0])))
	p = [[pinit for row in range(len(colors[0]))] for col in range(len(colors))]

	for k in range(len(measurements)):
		p = move(p, motions[k], p_move)
		p = sense(p, colors, measurements[k], sensor_right)

	return p


def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print('[' + ',\n '.join(rows) + ']')


colors = [['R','G','G','R','R'],
		  ['R','R','G','R','R'],
		  ['R','R','G','G','R'],
		  ['R','R','R','R','R']]
measurements = ['G','G','G','G','G']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
sensor_right = 0.7
P_move = 0.8

p = localize(colors, measurements, motions, sensor_right = 0.7, p_move = 0.8)

show(p)

#-------------------------------------------------------------
# For 1-D case (sense and move functions)

# def sense(p, Z):
#     q=[]
#     for i in range(len(p)):
#         hit = (Z == world[i]) 
#         q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
#     s = sum(q)
#     for i in range(len(q)):
#         q[i] = q[i] / s
#     return q

# def move(p, U):
#     q = []
#     for i in range(len(p)):
#         s = pExact * p[(i-U) % len(p)]
#         s = s + pOvershoot * p[(i-U-1) % len(p)]
#         s = s + pUndershoot * p[(i-U+1) % len(p)]
#         q.append(s)
#     return q
#---------------------------------------------------------------

# Additional Test Cases

# # test 1
# colors = [['G', 'G', 'G'],
#           ['G', 'R', 'G'],
#           ['G', 'G', 'G']]
# measurements = ['R']
# motions = [[0,0]]
# sensor_right = 1.0
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)
# correct_answer = (
#     [[0.0, 0.0, 0.0],
#      [0.0, 1.0, 0.0],
#      [0.0, 0.0, 0.0]])

# # test 2
# colors = [['G', 'G', 'G'],
#           ['G', 'R', 'R'],
#           ['G', 'G', 'G']]
# measurements = ['R']
# motions = [[0,0]]
# sensor_right = 1.0
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)
# correct_answer = (
#     [[0.0, 0.0, 0.0],
#      [0.0, 0.5, 0.5],
#      [0.0, 0.0, 0.0]])

# # test 3
# colors = [['G', 'G', 'G'],
#           ['G', 'R', 'R'],
#           ['G', 'G', 'G']]
# measurements = ['R']
# motions = [[0,0]]
# sensor_right = 0.8
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)
# correct_answer = (
#     [[0.06666666666, 0.06666666666, 0.06666666666],
#      [0.06666666666, 0.26666666666, 0.26666666666],
#      [0.06666666666, 0.06666666666, 0.06666666666]])

# # test 4
# colors = [['G', 'G', 'G'],
#           ['G', 'R', 'R'],
#           ['G', 'G', 'G']]
# measurements = ['R', 'R']
# motions = [[0,0], [0,1]]
# sensor_right = 0.8
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)
# correct_answer = (
#     [[0.03333333333, 0.03333333333, 0.03333333333],
#      [0.13333333333, 0.13333333333, 0.53333333333],
#      [0.03333333333, 0.03333333333, 0.03333333333]])

# # test 5
# colors = [['G', 'G', 'G'],
#           ['G', 'R', 'R'],
#           ['G', 'G', 'G']]
# measurements = ['R', 'R']
# motions = [[0,0], [0,1]]
# sensor_right = 1.0
# p_move = 1.0
# p = localize(colors,measurements,motions,sensor_right,p_move)
# correct_answer = (
#     [[0.0, 0.0, 0.0],
#      [0.0, 0.0, 1.0],
#      [0.0, 0.0, 0.0]])

# # test 6
# colors = [['G', 'G', 'G'],
#           ['G', 'R', 'R'],
#           ['G', 'G', 'G']]
# measurements = ['R', 'R']
# motions = [[0,0], [0,1]]
# sensor_right = 0.8
# p_move = 0.5
# p = localize(colors,measurements,motions,sensor_right,p_move)
# correct_answer = (
#     [[0.0289855072, 0.0289855072, 0.0289855072],
#      [0.0724637681, 0.2898550724, 0.4637681159],
#      [0.0289855072, 0.0289855072, 0.0289855072]])

# # test 7
# colors = [['G', 'G', 'G'],
#           ['G', 'R', 'R'],
#           ['G', 'G', 'G']]
# measurements = ['R', 'R']
# motions = [[0,0], [0,1]]
# sensor_right = 1.0
# p_move = 0.5
# p = localize(colors,measurements,motions,sensor_right,p_move)
# correct_answer = (
#     [[0.0, 0.0, 0.0],
#      [0.0, 0.33333333, 0.66666666],
#      [0.0, 0.0, 0.0]])