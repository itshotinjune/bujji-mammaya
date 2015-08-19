import ConfigParser
import random
from random import randint
import shutil
import fileinput
import sys

randomSSNs = range(900000001, 900699999) + range(999900000, 999999999+1)

targetLastNames = []

targetFirstName_male = []
targetFirstName_female = []
commonFirstNames = []
Alphabets = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
Numbers = ['0','1','2','3','4','5','6','7','8','9']


def getrandomSSN(length):
	randomSSN =  str(randomSSNs.pop())
	randomSSN = randomSSN.ljust(length)
	return randomSSN

def getrandomLastName(length):
	return (random.choice(targetLastNames)).ljust(length)

def getrandomFirstName(sourceName, length):
	sourceName = (sourceName.rstrip()).lower()

	if (sourceName not in targetFirstName_male and sourceName not in targetFirstName_female) or (sourceName in targetFirstName_male and sourceName in targetFirstName_female):
		return (random.choice(commonFirstNames)).ljust(length)
	elif (sourceName in targetFirstName_male):
		return (random.choice(targetFirstName_male)).ljust(length)
	elif (sourceName in targetFirstName_female):
		return (random.choice(targetFirstName_female)).ljust(length)

def getRandomAccountNumber(sourceNumber, length):
	sourceNumber = sourceNumber.rstrip()
	sourceNumber = list(sourceNumber)
	for i, c in enumerate(sourceNumber):
		if c.isalpha():
			sourceNumber[i] = random.choice(Alphabets)
		elif c.isdigit():
			sourceNumber[i] = random.choice(Numbers)

	sourceNumber = "".join(sourceNumber)
	return sourceNumber.ljust(length)

def getRandomPhoneNumber(sourceNumber, length):
	return ('5555555555'.ljust(length))

def getRandomInstitutionAddress(length):
	return ' '*length



def Mask(section, SegmentName, startPosition, endPosition):

	length = endPosition - startPosition + 1
	fileName = Config.get(section, "filename")

	if section == 'SSN':
		for line in fileinput.input("maskedData.txt", inplace=1):
			if line.startswith(SegmentName):
				maskedSSN = getrandomSSN(length)
				line = line.replace(line[startPosition-1:endPosition], maskedSSN)
			sys.stdout.write(line)
		

	elif section == 'LastName':
		for line in fileinput.input("maskedData.txt",inplace=1):
			if line.startswith(SegmentName) and  (not line[startPosition-1:endPosition].isspace()):
				maskedLastName = getrandomLastName(length)	
				line = line.replace(line[startPosition-1:endPosition], maskedLastName)
			sys.stdout.write(line)

	elif section == 'FirstName' or section == 'MiddleName':
		for line in fileinput.input("maskedData.txt",inplace=1):
			if line.startswith(SegmentName) and  (not line[startPosition-1:endPosition].isspace()):
				maskedFirstName = getrandomFirstName(line[startPosition-1:endPosition], length)
				line = line.replace(line[startPosition-1:endPosition], maskedFirstName)
			sys.stdout.write(line)

	elif section == 'AccountNumber':
		for line in fileinput.input("maskedData.txt",inplace=1):
			if line.startswith(SegmentName) and  (not line[startPosition-1:endPosition].isspace()):
				maskedAccountNumber = getRandomAccountNumber(line[startPosition-1:endPosition], length)
				line = line.replace(line[startPosition-1:endPosition], maskedAccountNumber)
			sys.stdout.write(line)

	elif section == 'PhoneNumber':
		for line in fileinput.input("maskedData.txt",inplace=1):
			if line.startswith(SegmentName) and  (not line[startPosition-1:endPosition].isspace()):
				maskedPhoneNumber = getRandomPhoneNumber(line[startPosition-1:endPosition], length)
				line = line.replace(line[startPosition-1:endPosition], maskedPhoneNumber)
			sys.stdout.write(line)

	elif section == 'InstitutionAddress' or section == 'EmailAddress' or section == 'TitleInformation' or section == 'InterviewerName' or section == 'AlternateName' or section == 'PASEmployerAddress':
		for line in fileinput.input("maskedData.txt",inplace=1):
				if line.startswith(SegmentName) and  (not line[startPosition-1:endPosition].isspace()):
					maskedInstitutionAddress = getRandomInstitutionAddress(length)
					line = line.replace(line[startPosition-1:endPosition], maskedInstitutionAddress)
				sys.stdout.write(line)


with open('dist.all.last.txt',"r") as f:
	targetLastNames = [(r.split()[0]).lower() for r in f]

with open('dist.male.first.txt',"r") as f:
    targetFirstName_male = [(r.split()[0]).lower() for r in f]

with open('dist.female.first.txt',"r") as f:
    targetFirstName_female = [(r.split()[0]).lower() for r in f]

commonFirstNames = list(set(targetFirstName_male) & set(targetFirstName_female))

#print FirstName_female


shutil.copy('Data.txt','maskedData.txt')
Config = ConfigParser.ConfigParser()
Config.read("config.ini")
Sections = Config.sections()
random.shuffle(randomSSNs)

for section in Sections:
	masks = Config.get(section,"segments")
	masks = masks.splitlines();
	#print masks
	for mask in masks:
		mask = [x.strip() for x in mask.split(',')]
		SegmentName = mask[0]
		startPosition = int(mask[1])
		endPosition = int(mask[2])
		Mask(section, SegmentName, startPosition, endPosition)