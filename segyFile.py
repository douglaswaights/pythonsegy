import struct
import collections
import pandas
import numpy
import PIL.Image
import os
import math
import argparse

class SegyFile:

	N_BYTES_TEXT_HEADER = 3200
	N_BYTES_BINARY_HEADER = 400
	N_BYTES_TRACE_HEADER = 240
	N_BYTES_HEADER = 3600

	def __init__(self, filePath):
		self._filePath = filePath
		self._bE = False
		self._traceInfoDict = None
		self._seismicInfoDict = None
		self._textHeader = None
		self._binaryHeaderDict = None
		self._scanTraceDataDict = None
		self._scanTraceHeaderDict = None

	def ebcidicHeader(self):
		if self._textHeader != None:
			return self._textHeader
		
		f = open(self._filePath, "rb")
		binTextHeader = f.read(3200)
		f.close()
		try:
			#important we try ascii first otherwise problem afterwards
			self._textHeader = binTextHeader.decode("ascii")
		except:
			self._textHeader = binTextHeader.decode("IBM500")
			self._bE = True
		return self._textHeader

	def binaryHeader(self):
		if self._binaryHeaderDict != None:
			return self._binaryHeaderDict
		bd = collections.OrderedDict()
		bd["jn"] = [3201,3204,0]
		bd["ln"] = [3205,3208,0]
		bd["rn"] = [3209,3212,0]
		bd["nte"] = [3213,3214,0]
		bd["nate"] = [3215,3216,0]
		bd["si"] = [3217,3218,0]
		bd["sio"] = [3219,3220,0]
		bd["ns"] = [3221,3222,0]
		bd["nso"] = [3223,3224,0]
		bd["dsfc"] = [3225,3226,0]
		bd["cmpf"] = [3227,3228,0]
		bd["tsc"] = [3229,3230,0]
		bd["vsc"] = [3231,3232,0]
		bd["sfs"] = [3233,3234,0]
		bd["sfe"] = [3235,3236,0]
		bd["sl"] = [3237,3238,0]
		bd["stc"] = [3239,3240,0]
		bd["tnsc"] = [3241,3242,0]
		bd["sttls"] = [3243,3244,0]
		bd["sttle"] = [3245,3246,0]
		bd["tt"] = [3247,3248,0]
		bd["cdt"] = [3249,3250,0]
		bd["bgr"] = [3251,3252,0]
		bd["arm"] = [3253,3254,0]
		bd["ms"] = [3255,3256,0]
		bd["isp"] = [3257,3258,0]
		bd["vpc"] = [3259,3260,0]
		#bd["unassigned"] = (3261,3500)
		bd["sfrn"] = [3501,3502,0]
		bd["fltf"] = [3503,3504,0]
		bd["ntfhrfbh"] = [3505,3506,0]
		#bd["unassigned"] = (3507,3600)

		f = open(self._filePath, "rb")
		head = f.read(3600)
		f.close()

		for k, v in bd.items():
			format = ""
			if self._bE:
				format = ">"
			numBytes = v[1] -v[0] + 1
			if numBytes == 2:
				format = format + "h"
			else:
				format = format + "i"
			v[2] = struct.unpack(format, head[v[0]-1:v[1]])[0]
			#print("%s=%s" % (k,v[2]))
		self._binaryHeaderDict = bd
		return self._binaryHeaderDict


	def numBytesSampleFromDsfc(self, dsfc):
		numBytes = 0
		if dsfc == 1:
			numBytes = 4 # ibm floating point
		elif dsfc == 2:
			numBytes = 4 # twos complement integer
		elif dsfc == 3:
			numBytes = 2 # twos complement integer 
		elif dsfc == 4:
			numBytes = 4 # fixed point with gain
		elif dsfc == 5:
			numBytes = 4 # IEEE floating point
		elif dsfc == 8:
			numBytes = 1 # twos complement integer
		return numBytes

	def traceHeaderDict(self):
		#assume no extended trace headers so first trace header at 3600 bytes and each trace header 240 bytes
		bd = collections.OrderedDict()
		bd["tswl"] = [1,4]
		bd["tsnwf"] = [5,8]
		bd["ofrn"] = [9,12]
		bd["tnwofr"] = [13,16]
		bd["espn"] = [17,20]
		bd["cmp"] = [21,24]
		bd["tnwe"] = [25,28]
		bd["tic"] = [29,30]
		bd["nvstyt"] = [31,32]
		bd["nhstyt"] = [33,34]
		bd["du"] = [35,36]
		bd["dcsptcrg"] = [37,40]
		bd["rge"] = [41,44]
		bd["ses"] = [45,48]
		bd["sdbs"] = [49,52]
		bd["derg"] = [53,56]
		bd["des"] = [57,60]
		bd["wds"] = [61,64]
		bd["wdg"] = [65,68]
		bd["saed"] = [69,70]
		bd["sac"] = [71,72]
		bd["scx"] = [73,76]
		bd["scy"] = [77,80]
		bd["gcx"] = [81,84]
		bd["gcy"] = [85,88]
		bd["cu"] = [89,90]
		bd["wv"] = [91,92]
		bd["swv"] = [93,94]
		bd["uhts"] = [95,96]
		bd["uhtg"] = [97,98]
		bd["ssc"] = [99,100]
		bd["gsc"] = [101,102]
		bd["tsa"] = [103,104]
		bd["lta"] = [105,106]
		bd["ltb"] = [107,108]
		bd["drt"] = [109,110]
		bd["mts"] = [111,112]
		bd["mte"] = [113,114]
		bd["nst"] = [115,116]
		bd["si"] = [117,118]
		bd["gtfi"] = [119,120]
		bd["igc"] = [121,122]
		bd["ig"] = [123,124]
		bd["c"] = [125,126]
		bd["sfs"] = [127,128]
		bd["sfe"] = [129,130]
		bd["sl"] = [131,132]
		bd["st"] = [133,134]
		bd["sttls"] = [135,136]
		bd["sttle"] = [137,138]
		bd["tt"] = [139,140]
		bd["aff"] = [141,142]
		bd["afs"] = [143,144]
		bd["nff"] = [145,146]
		bd["nfs"] = [147,148]
		bd["lcf"] = [149,150]
		bd["hcf"] = [151,152]
		bd["lcs"] = [153,154]
		bd["hcs"] = [155,156]
		bd["ydr"] = [157,158]
		bd["doy"] = [159,160]
		bd["hod"] = [161,162]
		bd["moh"] = [163,164]
		bd["som"] = [165,166]
		bd["tbc"] = [167,168]
		bd["twf"] = [169,170]
		bd["ggnorspo"] = [171,172]
		bd["ggnotnowofr"] = [173,174]
		bd["ggnoltwofr"] = [175,176]
		bd["gs"] = [177,178]
		bd["otawtabel"] = [179,180]
		bd["xcdp"] = [181,184]
		bd["ycdp"] = [185,188]
		bd["iln"] = [189,192]
		bd["xln"] = [193,196]
		bd["spn"] = [197,200]
		bd["saspn"] = [201,202]
		bd["tvmu"] = [203,204]
		bd["tcm"] = [205,208]
		bd["tcpte"] = [209,210]
		bd["tu"] = [211,212]
		bd["di"] = [213,214]
		bd["satt"] = [215,216]
		bd["sto"] = [217,218]
		#bd["sedwrtso"] = [219,224]
		#bd["sm"] = [225,230]
		bd["smu"] = [231,232]
		#bd["unassigned"] = [233,240]
		return bd

	def getTraceHeaders(self, listTraceNums):	
		bd = self.traceHeaderDict()
		traceInfoDict = self.getTraceInfoDict()
		f = open(self._filePath, "rb")
		traceDict = dict()
		for traceNum in listTraceNums:
			headerValueList = list()
			traceDict[traceNum] = headerValueList
			for k,v in bd.items():
				offset = ((traceNum -1) * traceInfoDict["numBytesForTraceIncludingHeader"]) + self.N_BYTES_HEADER
				f.seek(offset)
				bys = f.read(self.N_BYTES_TRACE_HEADER)
				format = ""
				if self._bE > 0:
					format = ">"
				numBytes = v[1] - v[0] + 1
				if numBytes == 2:
					format = format + "h"
				else:
					format = format+"i"
				val = struct.unpack(format, bys[v[0]-1:v[1]])[0]
				headerValueList.append(val)
		f.close()
		indexList = list(bd.keys())
		pandas.options.display.max_rows = 100
		df = pandas.DataFrame(traceDict, index=indexList, columns=listTraceNums)
		return df

	def traceValues(self, traceNum):
		f = open(self._filePath, "rb")
		traceInfoDict = self.getTraceInfoDict()
		offset = ((traceNum -1) * traceInfoDict["numBytesForTraceIncludingHeader"]) + self.N_BYTES_HEADER + self.N_BYTES_TRACE_HEADER
		f.seek(offset)
		mydtype = numpy.dtype(">f",numpy.int32)
		myarray = numpy.fromfile(f, dtype=mydtype, count=traceInfoDict["numSamplesTrace"], sep="")
		f.close()
		return myarray

	# calculate data min max values	
	def scanAllTraceData(self):
		if self._scanTraceDataDict != None:
			return self._scanTraceDataDict

		self._scanTraceDataDict = collections.OrderedDict()	
		f = open(self._filePath, "rb")
		traceInfoDict = self.getTraceInfoDict()
		seismicInfoDict = self.getSeismicInfoDict()
		mydtype = numpy.dtype(">f",numpy.int32)
		
		minTraceValue = numpy.NAN
		maxTraceValue = numpy.NAN
		for traceNum in range(1,seismicInfoDict["numTraces"]):
			offset = ((traceNum -1) * traceInfoDict["numBytesForTraceIncludingHeader"]) + self.N_BYTES_HEADER + self.N_BYTES_TRACE_HEADER
			f.seek(offset)
			arr = numpy.fromfile(f, dtype=mydtype, count=traceInfoDict["numSamplesTrace"], sep="")
			min = numpy.min(arr)
			max = numpy.max(arr)
			if math.isnan(minTraceValue) or min < minTraceValue:
				minTraceValue = min
			if math.isnan(maxTraceValue) or max > maxTraceValue:
				maxTraceValue = max
			
		f.close()
		self._scanTraceDataDict["minTraceValue"] = minTraceValue
		self._scanTraceDataDict["maxTraceValue"] = maxTraceValue
		return self._scanTraceDataDict

	def getValueFromHeader(self, bys, headerItem):
		format = ""
		if self._bE > 0:
			format = ">"
		numBytes = headerItem[1] - headerItem[0] + 1
		if numBytes == 2:
			format = format + "h"
		else:
			format = format+"i"
		val = struct.unpack(format, bys[headerItem[0]-1:headerItem[1]])[0]
		return val

	#cdp and sp range and x,y min max values etc	
	def scanAllTraceHeaders(self):
		if self._scanTraceHeaderDict != None:
			return self._scanTraceHeaderDict
		self._scanTraceHeaderDict = collections.OrderedDict()
		thDict = self.traceHeaderDict()
		f = open(self._filePath, "rb")
		traceInfoDict = self.getTraceInfoDict()
		seismicInfoDict = self.getSeismicInfoDict()
		minx = numpy.NAN
		maxx = numpy.NAN
		miny = numpy.NAN
		maxy = numpy.NAN
		mincmp = numpy.NAN
		maxcmp = numpy.NAN
		tswlFirstTrace = numpy.NAN
		for traceNum in range(1,seismicInfoDict["numTraces"]):
			offset = ((traceNum -1) * traceInfoDict["numBytesForTraceIncludingHeader"]) + self.N_BYTES_HEADER
			f.seek(offset)
			bys = f.read(self.N_BYTES_TRACE_HEADER)
			if traceNum == 1:
				tswlFirstTrace = self.getValueFromHeader(bys, thDict["tswl"])
			scx = self.getValueFromHeader(bys,thDict["scx"])
			scy = self.getValueFromHeader(bys,thDict["scy"])
			cdp = self.getValueFromHeader(bys,thDict["cmp"])
			if math.isnan(minx) or scx < minx:
				minx = scx
			if math.isnan(miny) or scy < miny:
				miny = scy
			if math.isnan(maxx) or scx > maxx:
				maxx = scx
			if math.isnan(maxy) or scy > maxy:
				maxy = scy
			if math.isnan(mincmp) or cdp < mincmp:
				mincmp = cdp
			if math.isnan(maxcmp) or cdp > maxcmp:
				maxcmp = cdp

		f.close()
		self._scanTraceHeaderDict["minx"] = minx
		self._scanTraceHeaderDict["maxx"] = maxx
		self._scanTraceHeaderDict["miny"] = miny
		self._scanTraceHeaderDict["maxy"] = maxy
		self._scanTraceHeaderDict["mincmp"] = mincmp
		self._scanTraceHeaderDict["maxcmp"] = maxcmp

		#calculate inline and crossline ranges etc
		bh = self.binaryHeader()
		lineNo = bh["ln"][2]
		deltaCmp = maxcmp - mincmp
		minInline = lineNo
		minCrossline = mincmp
		maxCrossline = maxcmp
		siDict = self.getSeismicInfoDict()
		numTraces = siDict["numTraces"]
		self._scanTraceHeaderDict["numTraces"] = numTraces
		numInlines = int(numTraces / (deltaCmp + 1))
		maxInline = minInline + numInlines
		self._scanTraceHeaderDict["minInline"] = minInline
		self._scanTraceHeaderDict["maxInline"] = maxInline
		self._scanTraceHeaderDict["numInlines"] = numInlines
		self._scanTraceHeaderDict["minCrossline"] = minCrossline
		self._scanTraceHeaderDict["maxCrossline"] = maxCrossline
		self._scanTraceHeaderDict["numCrosslines"] = deltaCmp + 1
		return self._scanTraceHeaderDict


	def getSeismicInfoDict(self):
		if self._seismicInfoDict != None:
			return self._seismicInfoDict
		self._seismicInfoDict = collections.OrderedDict()	
		f = open(self._filePath, "rb")
		size = os.path.getsize(self._filePath)
		traceInfo = self.getTraceInfoDict()
		traceAnDHeaderBytes = traceInfo["numBytesForTraceIncludingHeader"]
		numTraces = (size - self.N_BYTES_HEADER) / traceAnDHeaderBytes
		self._seismicInfoDict["numTraces"] = int(numTraces)
		return self._seismicInfoDict

	def getTraceInfoDict(self):
		if self._traceInfoDict != None:
			return self._traceInfoDict
		self._traceInfoDict = collections.OrderedDict()
		bd = self.traceHeaderDict()
		f = open(self._filePath, "rb")
		f.seek(self.N_BYTES_HEADER+ bd["nst"][0]-1)
		nstValBytes = f.read(2)
		format = "h"
		if self._bE:
			format = ">h"
		numSamples = struct.unpack(format, nstValBytes)[0]
		ebBinDict = self.binaryHeader()
		f.seek(ebBinDict["dsfc"][0] -1)
		dsfcBytes = f.read(2)
		dsfc = struct.unpack(format, dsfcBytes)[0]
		nbps = self.numBytesSampleFromDsfc(dsfc)
		numTraceHeaderAndDataBytes = (numSamples * nbps) + self.N_BYTES_TRACE_HEADER
		f.close()
		
		self._traceInfoDict["DataSampleFormatCode"] = dsfc
		self._traceInfoDict["numSamplesTrace"] = numSamples
		self._traceInfoDict["numBytesForTraceIncludingHeader"] = numTraceHeaderAndDataBytes
		
		return self._traceInfoDict


	def createImage(self,startTraceNum,endTraceNum):
		l = list()
		for t in range(startTraceNum,endTraceNum):
			l.append(self.traceValues(t))
		array = numpy.column_stack(l)
		im = PIL.Image.fromarray(array,mode="F")
		im.save("seismic {0} trace {1} to {2}.tiff".format(self._filePath, startTraceNum, endTraceNum))
		im.show()

	def getInline(self, inlineNum):
		allTraceHeadersInfo = self.scanAllTraceHeaders()
		numTraces = allTraceHeadersInfo["numTraces"]
		firstInline = allTraceHeadersInfo["minInline"]
		numCrosslines = allTraceHeadersInfo["numCrosslines"]
		traceStartNum = ((inlineNum - firstInline) * numCrosslines) + 1
		traceEndNum = traceStartNum + numCrosslines
		l = list()
		for trace in range(traceStartNum,traceEndNum):
			l.append(self.traceValues(trace))
		return l

	def getCrossline(self, crosslineNum):
		allTraceHeadersInfo = self.scanAllTraceHeaders()
		numTraces = allTraceHeadersInfo["numTraces"]
		firstInline = allTraceHeadersInfo["minInline"]
		lastInline = allTraceHeadersInfo["maxInline"]
		firstCrossline = allTraceHeadersInfo["minCrossline"]
		numInlines = allTraceHeadersInfo["numInlines"]
		l = list()
		for il in range(firstInline,lastInline):
			l.append(self.getTraceValuesAtInlineCrossline(il, crosslineNum))
		return l

	def getTraceValuesAtInlineCrossline(self, inline, crossline):
		allTraceHeadersInfo = self.scanAllTraceHeaders()
		inlineTraceStartNum = ((inline - allTraceHeadersInfo["minInline"]) * allTraceHeadersInfo["numCrosslines"]) + 1
		firstCrossline = allTraceHeadersInfo["minCrossline"]
		crosslineTrace = crossline - firstCrossline
		traceNum = inlineTraceStartNum + crosslineTrace
		return self.traceValues(traceNum)


	def createInlineImage(self, inlineNum, save):
		inlineLine = self.getInline(inlineNum)
		array = numpy.column_stack(inlineLine)
		im = PIL.Image.fromarray(array,mode="F")
		if save:
			im.save("seismic {0} inline {1}.tiff".format(self._filePath, inlineNum))
		im.show()

	def createCrosslineImage(self, crosslineNum, save):
		crosslineData = self.getCrossline(crosslineNum)
		array = numpy.column_stack(crosslineData)
		im = PIL.Image.fromarray(array,mode="F")
		if save:
			im.save("seismic {0} crossline {1}.tiff".format(self._filePath, crosslineNum))
		im.show()

# if __name__ == '__main__':
# 	#s = SegyFile("troll2D.Segy")
# 	s = SegyFile("mig.sgy")
# 	eh = s.ebcidicHeader()
# 	print(eh)
# 	bh =s.binaryHeader()
# 	print(bh)
# 	df = s.getTraceHeaders([1,2,221,222,223])
# 	print(df)
# 	#traceData = s.traceValues(59891)
# 	#s.createImage(1,239)#59891)
# 	ti = s.getTraceInfoDict()
# 	print(ti)
# 	si = s.getSeismicInfoDict()
# 	print(si)
# 	sci = s.scanAllTraceData()
# 	print(sci)
# 	scTh = s.scanAllTraceHeaders()
# 	print(scTh)
# 	il = s.getInline(500)
# 	#s.createInlineImage(770, True)
# 	xl = s.getCrossline(360)
# 	#s.createCrosslineImage(470, True)

parser = argparse.ArgumentParser()
parser.parse_args()