'''
Computer Organization Project-1

Group Member 1:
Himanshu Raj
2018038
Group Member 2:
Ishaan Arora
2018041

A 12 bit two-pass assembler using Python. You need to store your assembly code in a text file
input.txt. After executing this python file, it will produce a file named machinecode.txt which
contains machine code. Also, it produces a symbol.txt file for the info of all the symbols used
in the  assembly code.
'''
class Assembler:
	symbol={}
	error=False
	'''
	RETURN TYPE- String
	This function returns an opcode string for the respective instructions.
	It builds a dictionary first which contains instructions as keys and their
	opcode as values and then returns desireable opcode string.
	'''
	def extract_opcode(self,line):
		s=line.split()
		opcode={}
		opcode["CLA"]="0000"
		opcode["LAC"]="0001"
		opcode["SAC"]="0010"
		opcode["ADD"]="0011"
		opcode["SUB"]="0100"
		opcode["BRZ"]="0101"
		opcode["BRN"]="0110"
		opcode["BRP"]="0111"
		opcode["INP"]="1000"
		opcode["DSP"]="1001"
		opcode["MUL"]="1010"
		opcode["DIV"]="1011"
		opcode["STP"]="1100"
		l=list(opcode.keys())
		if(s[0] in l):
			return opcode[s[0]]
	'''
	RETURN TYPE- Boolean
	This function returns True if the string passed is one of the instruction.
	And returns False if the passed string is not an instruction.
	It basically builds a list containing all the instructions and then checks whether the string is present in the list or not.
	'''
	def check_for_opcode(self,s):
		l=['CLA', 'LAC', 'SAC', 'ADD', 'SUB', 'BRZ', 'BRN', 'BRP', 'INP', 'DSP', 'MUL', 'DIV', 'STP']
		if(s in l):
			return True
		else:
			return False

	'''
	RETURN TYPE- int
	This function returns an integer value which is basically the count of all opcodes in the given line. It uses check_for_opcode()
	function for checking of opcode. 
	'''

	def check_for_number_of_opcode_in_a_line(self,s):
		h=s.split()
		c=0
		for i in h:
			if(self.check_for_opcode(i)):
				c+=1
		return c

	'''
	RETURN TYPE- void
	This function first reads the file input.txt and iterate over its lines. Through iterating it checks for various errors and reports
	it as soon as its caught. It updates dictionary symbol for storing various symbols as key and their address as value. It also sets
	the flag named error to True if any error is caught which will help us to stop the execution of second pass.
	'''

	def first_pass(self):					#first pass
		f=open("input.txt","r")				#open the file
		lines=list(f.readlines())			#reading the file content line by line
		ll=len(lines)
		loc_ctr=0
		j=0
		for i in lines:
			if("\n" in i):
				i=i[:-1]
			#print(i)
			j+=1
			cmnt=i.find('//')				#looking for commented line
			if(cmnt!=-1):
				i=i[:cmnt]
			curr_line=list(i.split())
			if(len(curr_line)==0):			#means whole line is commented out
				ll=ll-1
				continue
			else:
				s=i.split()
				if(i=='STP'):				#stop the process
					break
				no=self.check_for_number_of_opcode_in_a_line(i)
				if(no==0):
					print("ERROR on Line "+str(j)+": No instruction given in this line.")				#If no instruction is given in line
					self.error=True
					continue
				elif(no>1):
					print("ERROR on Line "+str(j)+": Multiple Instructions given in a line.")			#If multiple instructions are given, then its invalid.
					self.error=True
					continue
				if(len(s)==1):
					if(s[0]!='CLA' and s[0]!='STP'):													#Only STP and CLA instructions are called without any operand
						print("ERROR on Line "+str(j)+": Insufficient variable/label provided.")
						self.error=True
						continue
				elif(len(s)==2):
					if(self.check_for_opcode(s[0])==False and self.check_for_opcode(s[1])==True and s[1]!='CLA' and s[1]!='STP'):
						print("ERROR on Line "+str(j)+": Formatting Error.")							#if in the form of label: INS 
						self.error=True
						continue
				for k in range(len(s)):
					if(self.check_for_opcode(s[k])):
						if(len(s)-k-1>=2):
							print("ERROR on Line "+str(j)+": More than one variable/label provided.")	#If more than required variables are provided
							self.error=True	
							continue
				if(len(s)>=3):
					if(self.check_for_opcode(s[0])==False and self.check_for_opcode(s[1])==False):		#If no instruction is passed
						print("ERROR on Line "+str(j)+": Formatting Error.")
						self.error=True
						continue
				if(':' in i):												#It means label is defined in this line
					sym=i[:i.index(':')]
					sym=sym.strip()
					if('STP' in i):
						break												#break if stopped after branching
					if(self.check_for_opcode(sym)):
						print("ERROR on Line "+str(j)+": symbol name can not be an instruction.")
						self.error=True										#symbol name cannot be same as the instruction name
						continue
					if(sym in self.symbol):
						if(self.symbol[sym]==-1):
							print("ERROR on Line "+str(j)+": Variable with same name is already declared.")
							self.error=True									#cannot declare a label with the name of already declared variable
							continue
						elif(self.symbol[sym]==-2):
							print("ERROR on Line "+str(j)+": Label is already declared with same name.") 
							self.error=True									#cannot declare same label twice
							continue
					i=i[i.index(':')+1:]
					i=i.strip()
					self.symbol[sym]=loc_ctr
				elif('BRZ' in i or 'BRP' in i or 'BRN' in i):
					sym=s[1]
					if(self.check_for_opcode(sym)):
						print("ERROR on Line "+str(j)+": symbol name can not be an instruction.")
						self.error=True										#self explanatory
						continue
					if(sym in self.symbol):
						if(self.symbol[sym]==-1):
							print("ERROR on Line "+str(j)+": Cannot branch to a variable.")
							self.error=True									#example BRZ A where A is a variable
							continue
						else:
							continue
					else:
						self.symbol[sym]=loc_ctr
				elif('INP' in i):
					if(self.check_for_opcode(s[1])):
						print("ERROR on Line "+str(j)+": symbol name can not be an instruction.")
						self.error=True										#Example INP SAC
						continue
					elif(s[1] in self.symbol):
						if(self.symbol[s[1]]!=-1):
							print("ERROR on Line "+str(j)+": "+s[1]+" is a label type symbol.")
							self.error=True
							continue
					self.symbol[s[1]]=-1
				elif('SAC' in i):
					if(check_for_opcode(s[1])):
						print("ERROR on Line "+str(j)+": symbol name can not be an instruction.")
						self.error=True										#same as above
						continue
					if(self.symbol[s[1]]!=-1):
						print("ERROR on Line "+str(j)+": "+s[1]+" is a label type symbol.")
						self.error=True
						continue
					self.symbol[s[1]]=-1
				loc_ctr+=1
		ss=list(self.symbol.keys())
		for i in range(len(ss)):											#checking whether forward refrencing happened or not.
			if(self.symbol[ss[i]]==-1):
				ll+=1
				self.symbol[ss[i]]=ll
			elif(self.symbol[ss[i]]==-2):
				print("ERROR: Label "+ss[2]+" not defined.")
				self.error=True
		if(ll>255):															#can only store upto 256 addresses (0-255)
			print("ERROR: Address Overflow due to more number of instructions and symbols(LIMIT-255).")

	'''
	RETURN TYPE- void
	If no error is caught then only it will run. This function makes a new file named MachineCode.txt which stores
	the correct Machine Code for the given assembly code. It also converts instructions to opcode and integer addresses 
	to their binary equivalent and then write it to the file.
	'''
	def second_pass(self):
		for i in self.symbol.keys():							#converting addresses to their binary equivalent
			x=self.symbol[i]
			b=bin(x)[2:]
			p='0'*(8-len(b))+b
			self.symbol[i]=p
		file=open("MachineCode.txt","w")						#open a new file in write mode
		arr=[]
		f=open("input.txt","r")
		lines=list(f.readlines())								#reading lines (second pass) for writing the machine code
		ll=len(lines)
		for i in lines:
			if('\n' in i):
				i=i[:-1]
			cmnt=i.find('//')									#if commented then skip it
			if(cmnt!=-1):
				i=i[:cmnt]
			curr_line=list(i.split())
			if(len(curr_line)==0):								#means whole line is commented out
				ll-=1
				continue
			if(':' in i):
				i=i[i.index(':')+1:]
			s=i.split()
			if(len(s)==1):
				arr.append(self.extract_opcode(s[0])+" 00000000")		#if an instruction doesn't have any symbol attached it will add 8 0s in front
			else:
				arr.append(self.extract_opcode(s[0])+" "+self.symbol[s[1]])	#concatenating opcode and address together 
			file.write(arr[-1])											#and then adding it to file
			file.write("\n")
		file.close()
		file=open("SymbolTable.txt",'w')								#It makes a file for storing all the info of symbols used in code
		arr=[]
		file.write("SYMBOL\t\tTYPE\t\tADDRESS")
		file.write('\n')
		for i in self.symbol.keys():
			if(int(self.symbol[i],2)<=ll):
				arr.append(str(i)+'\t\t'+"Label"+'\t\t'+self.symbol[i])
			else:
				arr.append(str(i)+'\t\t'+"Variable"+'\t'+self.symbol[i])
			file.write(arr[-1])											#writing the info to file
			file.write('\n')
		file.close()

if __name__ == "__main__":
	my_assembler=Assembler()											#Makes an Assembler object
	my_assembler.first_pass()
	if(my_assembler.error):												#Only run when no error is encountered in first pass.
		exit()
	my_assembler.second_pass()											#Runs and produces file