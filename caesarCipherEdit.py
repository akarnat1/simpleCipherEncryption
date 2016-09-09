'''
Anthony Karnati
akarnat1@binghamton.edu
4/2/14
A55-CS110
Assignment 9
'''

"""
Analysis:
This program will encrypt plain
text or decrypt cipher text as
long as the user inputs it

Output to monitor:
confirm or deny input data(bool)
encrypted/decrypted message (str)

Input from keyboard:
message-message to en/decrypt(str)
opStr-operation e/E or d/D(str)
rotation Key (int)

Tasks allocated to functions:
operationValidated-validate operation (encrypt or decrypt)
rotationKeyValidated-(validate rotation key)
convertRotationKey-take key and convert it depending on 'e' or 'd'
processMessage-take data and convert it to new, converted str and
keep in bounds
"""    


import os.path

# Mapping of valid operations to rotationKey factor
OPERATIONS = {'e':[1,"Encrypted"], 'd':[-1,"Decrypted"]}
# Min and limit ordinals of printable ASCII
PRINTABLE_ASCII_MIN = 32
PRINTABLE_ASCII_LIMIT = 127
# Allowable rotationKey prefixes
KEY_PREFIXES = "-+"
# Required file extension
FILE_EXT = ".txt"
# File processing modes
READ_MODE = 'r'
WRITE_MODE = 'w'
ZERO=0
ONE=1
TOTAL_PRINTABLE=95

# Checks that file exists and that extension is .txt
# param name (str) - file name
# invoke isFile() from module os.path and endswith()
# return True when valid, False otherwise (bool)
def fileNameValidated(name):
  return os.path.isfile(name) and name.endswith(FILE_EXT)


# Generates output file name from input file name, 
#   operation requested and rotation key
# param fileName (str) - input file name
# param operation (str)
# param rotationKey (int) - converted key
# invoke str.split(), str.replace() and str.join()
# return output file name (str)
def makeName(fileName, operation, rotationKey):
  nameList = fileName.split(".")
  nameList[0] = nameList[0].replace(OPERATIONS['e'][1], "")
  nameList[0] = nameList[0].replace(OPERATIONS['d'][1], "")
  nameList[0] += (OPERATIONS[operation][1] + str(rotationKey))
  return ".".join(nameList)

# Check that requested operation is valid
# param opStr (str) - operation requested
# return  True when valid, False otherwise (bool)
def operationValidated(opStr):
      return opStr=='E' or opStr=='e' or opStr=='D' or opStr=='d'

# Check that rotation key is of form <digits> or -<digits> or +<digits>
# param rotationKeyStr (str)
# invoke str.isdigit() 
# returns:  True when valid, False otherwise (bool)
def rotationKeyValidated(rotationKeyStr):
      if rotationKeyStr[0]=='-' or rotationKeyStr[0]=='+':
        numKeyStr=rotationKeyStr[1: ]
        validKey=str.isdigit(rotationKeyStr)

      else:
        validKey=str.isdigit(rotationKeyStr)
      return validKey

# Convert rotation key to value usable for requested operation
# param  op (str) - operation requested 
# param  rotationKeyStr (str)
# invoke int()
# return encryption or decryption rotation key (int)
def convertRotationKey(op, rotationKeyStr):
      newKey=int(rotationKeyStr)
      return newKey*(OPERATIONS[op][0])

def keepInBounds(ordin):
  if ordin>=PRINTABLE_ASCII_LIMIT:
    while ordin>=PRINTABLE_ASCII_LIMIT:
      ordin-=TOTAL_PRINTABLE
  else:
    while ordin<PRINTABLE_ASCII_MIN:
      ordin+=TOTAL_PRINTABLE
  return ordin
# Encrypt or decrypt message using rotationKey and keeps in bounds
# param message (str)
# param rotationKey (int)
#invoke keepInBounds()
# return processedMessage (str)
def processMessage(message, rotationKey):
      rotationKeyInt=int(rotationKey)
      newStr=''
      for char in message:
        ordinal=ord(char)+rotationKeyInt
        if ordinal>=PRINTABLE_ASCII_MIN and ordinal<PRINTABLE_ASCII_LIMIT:
          newStr+=chr(ordinal)
        else:
          validOrd=keepInBounds(ordinal)
          newStr+=chr(validOrd)
      return newStr
#param lst (str)
def processList(lst, rotationKey):
      newLst=[]
      for index in lst:
        messageConvert=processMessage(index, rotationKey)
        newLst.append(messageConvert)
      return newLst

def writeToFile(fileName, processedLst):
      for index in processedLst:
            index+='\n'
            fileName.write(index)



def main():

      print('This program encrypts or decrypts .txt files using a Caesar cipher (make sure to include .txt after filename)')
      fileName=input("Input the name of a file to be processed\
or press <Enter> to quit: ")
      while fileName:
            while not fileNameValidated(fileName):
                  print ("That file name does not appear to be valid, please try again")
                  fileName=input("Input the name of a file to be processed\
or press <Enter> to quit: ")
            while fileNameValidated(fileName):

                  cryption=input("Do you want to encrypt or decrypt?\
(Enter E for encrypt or D for decrypt): ")
                
                  while not operationValidated(cryption):
                        print("That operation isn't valid, please\
try again")
                        cryption=input('Do you want to encrypt or decrypt?\
(Enter E for encrypt or D for decrypt): ')
      

                  encryptionKey=input('Enter the rotation key to be used for\
encryption OR the key that was used for encryption: ')
                  while not (str.isdigit(encryptionKey) or (encryptionKey[0]=='-' \
                              and encryptionKey[1: ].isdigit()) or\
                              (encryptionKey[0]=='+' and\
                              encryptionKey[1: ].isdigit())):
                        encryptionKey=input('Enter the rotation key to be used for\
encryption OR the key that was used for encryption: ')
                  encryptionKey=convertRotationKey(cryption, encryptionKey)
                        
                  try: # outer try for infile open
                      inFileObj = open(fileName, READ_MODE)

                      try: # inner try for processing infile
                        fullLst = inFileObj.read()
                        fullLst.strip()
                        stripList=fullLst.split('\n')
                        finalName=makeName(fileName, cryption, encryptionKey)
                        newLst=[]
                        for line in stripList:
                          newLst.append(line)
                        newLst=processList(newLst, encryptionKey)
                        try:
                          finalName=open(finalName, WRITE_MODE)
                          try:
                            writeToFile(finalName,newLst)
##              print(line)

                          except IOError as err: # inner exception handler for outfile processing
                            print("\nProblem writing data: \n" + str(err))
                          except TypeError as err:  # inner exception handler for outfile processing
                            print("\nProblem writing data, wrong format or corrupted?  \n" + str(err) + '\n')
                          except Exception as err: # inner exception handler for outfile processing
                            print("\nData cannot be written to file: \n" + str(err) + '\n')
                          finally:# will close file whether or not exception has been raised
                            finalName.close()

                        except IOError as err: # "outer" exception handler for outfile open
                          print("\nExecption raised during open of output file, no write performed: \n" + str(err) + '\n')
                        except Exception as err: # outer exception handler for outfile processing
                          print("\nData cannot be read:  \n" + str(err) + '\n')  

                      except IOError as err: # inner exception handler for infile processing
                        print("\nProblem reading data: \n" + str(err))
                      except ValueError as err: # inner exception handler for infile processing
                        print("\nProblem processing data, wrong format or corrupted? \n" + str(err) + '\n')
                      except Exception as err: # inner exception handler for infile processing
                        print("\nData cannot be read:  \n" + str(err) + '\n')        
                      finally:# will close file whether or not exception has been raised
                        inFileObj.close()

              #   No FileNotFoundError in version 3.2.3        
              ##    except FileNotFoundError as err:  # outer exception handler for infile open
              ##      print("\nFile not found:  deleted or in wrong folder?  \n" + str(err) + '\n')
                  except IOError as err: # outer exception handler for infile open
                    print("\nException raised during open of input file, try a different file: \n" + str(err) + '\n')
                  except Exception as err: # outer exception handler for infile open
                    print("\nData cannot be read:  \n" + str(err) + '\n')

      
                  fileName = input("Input a filename:  ")


main()
