import matplotlib.pyplot as plt
# import matplotlib.colors as mcolors
import numpy as np
import os


class Target:
	def __init__(self, pointRange, pointDisplayDir=3, totalSize=1):
		# Org pointRange order: [low, ..., high]
		self.pointRange = pointRange
		self.pointRange.reverse()
		# New pointRange order: [high, ..., low]

		self.pointDisplayDir = pointDisplayDir # The direction of ring point text (1-12)
		self.totalSize = totalSize
		
		self.wedgeNr = 0
		self.cmap = plt.get_cmap("Set1") # Set colormap
		self.ringColorNr = [5, 0, 1, 2, 3, 4, 6, 7] # Set color order from center to outer ring
		self.neutralNr = 8 # The "Off" color

	def func(self, vals):
		if (self.wedgeNr+self.pointDisplayDir) % len(vals) == 0:
			self.wedgeNr +=1
			return "{:d}".format(vals[0]) # If correct segment -> display point number
		else:
			self.wedgeNr +=1 # If not correct segment -> display nothing
			return ""

	def getRingColor(self, ring): # @param "ring" - index from center to outer ring
		return np.array(self.cmap(self.ringColorNr[ring]))
	
	def getNeutralColor(self, array_size):
		return self.cmap(np.full(array_size, self.neutralNr))
	
	def getTColor(self):
		return [0, 0, 0, 0.9]

	def getOutColor(self):
		return [0, 0, 1, 0.9]

	def getMissColor(self):
		return [0.8, 0, 0, 0.9]

	# Create full target plot
	def targetHit(self, point, dir=None):
		self.fig, self.ax = plt.subplots()

		totalSize = self.totalSize

		# Set outer clock numbers
		self.ax.pie(np.full(12, 1), radius=totalSize, wedgeprops=dict(width=0), startangle=75,
		labels=[' 12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2','1'])

		# Create normal target display
		if point in self.pointRange:
			size = totalSize/len(self.pointRange) # "Thicness" of each ring
			for i in range(len(self.pointRange)): # Loop through every ring
				startangle = 75

				val = np.full(12, self.pointRange[i]) # Set array of 12 elements, all with the ring value for even segentation
				color = self.getNeutralColor(12) # Default all segents to "Off"
				self.wedgeNr = 0 # Reset wedge/segment counter
				textOffset = (size*(i+1)+0.05)/(size+(size*(i+1))) # Text offset for ring point number
				
				# Create center
				if i == 0:
					val = np.array([self.pointRange[i]]) # No segmentation - To get only one segment in the center ring
					textOffset = 0 # To get bullseye number in the exact center
				
				# If the ring is hit
				if self.pointRange[i] == point:
					if dir == None: # If no direction selected
						color = [self.getRingColor(i)] # Set to correct ring color
						val = np.array([self.pointRange[i]]) # No segmentation
						startangle = 90 + self.pointDisplayDir*(360/12) # To get the number in the right place
					else:
						color[-int(dir) % 12] = self.getRingColor(i) # Set hit segment color "On" | Typecast is only there to remove linting warning, does nothing
				
				# Create the ring
				self.ax.pie(val, radius=size*(i+1), colors=color, autopct=lambda txt: self.func(val),
				wedgeprops=dict(width=size, edgecolor='black'), startangle=startangle,
				pctdistance=textOffset)

		# Create "Träff" target display
		elif point in ["T", "t"]:
			# if dir == None:
			# 	print("Error - Enter direction")
			# 	return
			color = self.getNeutralColor(4)
			if dir == None:
				color[:] = self.getTColor()
			else:
				color[-round(dir/3) % 4] = self.getTColor()
			self.ax.pie(np.full(4, 1), radius=totalSize, colors=color,
			wedgeprops=dict(width=totalSize, edgecolor='black'), startangle=45)

		# Create "Träff i figur" target display
		elif point in ["o", "O", 0, "0"]:
			# if dir == None:
			# 	print("Error - Enter direction")
			# 	return
			color = self.getNeutralColor(4)
			if dir == None:
				color[:] = self.getOutColor()
			else:
				color[-round(dir/3) % 4] = self.getOutColor()
			self.ax.pie(np.full(4, 1), radius=totalSize, colors=color,
			wedgeprops=dict(width=totalSize, edgecolor='black'), startangle=45)

		# Create "Miss / Bom" target display
		elif point in ["Miss", "x", "X"]:
			self.ax.pie([1], radius=totalSize, colors=[self.getMissColor()], 
			wedgeprops=dict(width=totalSize, edgecolor='black'), startangle=45,
			autopct=lambda txt: "Miss", pctdistance=0, textprops=dict(color='white', size='xx-large'))
	

	# Only for first image
	def default(self):
		self.fig, self.ax = plt.subplots()

		totalSize = self.totalSize

		self.ax.pie(np.full(12, 1), radius=totalSize, wedgeprops=dict(width=0), startangle=75,
		labels=[' 12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2','1'])

		size = totalSize/len(self.pointRange)
		for i in range(len(self.pointRange)):
				val = np.full(12, self.pointRange[i])
				color = self.getNeutralColor(12)
				self.wedgeNr = 0
				textOffset = (size*(i+1)+0.05)/(size+(size*(i+1)))
				
				if i == 0:
					val = np.array([self.pointRange[i]])
					textOffset = 0

				self.ax.pie(val, radius=size*(i+1), colors=color, autopct=lambda txt: self.func(val),
				wedgeprops=dict(width=size, edgecolor='black'), startangle=75,
				pctdistance=textOffset)


	def showFullscreen(self):
		self.ax.set(aspect="equal") # To get undistorted circle
		figManager = plt.get_current_fig_manager()
		figManager.full_screen_toggle()
		plt.show() # Display all figures
	
	def saveFigure(self, dpi=100):
		self.ax.set(aspect="equal")
		my_path = os.path.dirname(os.path.abspath(__file__))
		my_file = 'image.png'
		self.fig.savefig(os.path.join(my_path, my_file) , dpi=dpi)
		# self.fig.savefig('C:/Users/marcu/Desktop/Python Projects/L-O/GUI/test.png', dpi=100)
		# plt.pause(100)
		plt.close('all')


if __name__ == "__main__":
	target = Target([1, 2, 3, 4, 5, 51])
	target1 = Target([3, 4, 5, 51])

	# Colormap too small, this causes error
	# target2 = Target([1,2,3,4,5,6,7,8,9,10,11])
	# target2.targetHit(2)
	# target2.showFullscreen()
	# -------------------------------------

	# target.default(1.4)
	# target.targetHit(4, totalSize=1.4)
	# target.targetHit(3,2, totalSize=1.4)
	# target.targetHit(4,8)
	# target.targetHit("T",3)
	# target.targetHit("0",12)
	target.targetHit("X",2, totalSize=1.4)

	# target1.showFullscreen()
	target.saveFigure(170)
	# target.showFullscreen()
	# target1.targetHit("x")
	# target.showFullscreen()
	# target1.saveFigure()
	# target.saveFigure()
	print("Done")
