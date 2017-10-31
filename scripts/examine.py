import sys
import shapefile

from shapetype import SHAPETYPE

if __name__ == '__main__':

	if len(sys.argv) == 1:
		print('usage: %s shapename' % __file__)
		sys.exit()

	sf = shapefile.Reader(sys.argv[1])
	print('Type %s ShapeRecords #%d' % (sf.shapeType, sf.numRecords))
	
	for index, sr in enumerate(sf.shapeRecords()):
		shape = sr.shape
		record = sr.record
		print('Shape #%d Parts #%d Points #%d Record %s' % (index, len(shape.parts), len(shape.points), record))