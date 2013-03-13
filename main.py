    # Basic for handling a .str subtitles
    # Works up to 99h files (its enought, i think..)

import sys

# Auxilia a pular qualquer texto que esteja antes da primeira legenda. 
# Depois basta ir procurando pela linha em braco.
def is_one(s):
	try:
		x=int(s)
		if x==1:
			return True
		return False
	except ValueError:
		return False

# Talvez fazer uma verificao se o arquivo em questao nao tem nada em comum com um arquivo de legenda?
def delay_srt(file, time, saveas):
	draft = open(saveas, 'w')
	counter = 1 #current subtitle
	t1, t2 = sub_time(), sub_time()
	
	# Procura a primeira legenda (pula espacos em branco iniciais)
	while True:
		s= file.pop(0)
		if (not s) or (is_one(s) == True):
			break

	while True:
		draft.write(s)			# grava o numero da legenda
		
		if file:
			s= file.pop(0)		# carrega os tempos

		# Faz a conversao de F.Pereire
		counter += 1
		t1.set_time(int(s[0:2]), int(s[3:5]), int(s[6:8]), int(s[9:12])) 
		t2.set_time(int(s[17:19]), int(s[20:22]), int(s[23:25]), int(s[26:29]))

		t1.add_ms(time)
		t2.add_ms(time)

		# Cria e grava a string de novo tempo
		str_time = t1.strh()+":"+t1.strm()+":"+t1.strs()+","+t1.strms()+" --> " +\
			t2.strh()+":"+t2.strm()+":"+t2.strs()+","+t2.strms()+"\n"

		draft.write(str_time)

		# Le e grava ate encontrar uma linha em branco ou a lista do arquivo acabar
		while s.strip() and file:
			s= file.pop(0)
			draft.write(s)
			
		# Le o numero da legenda, se houver
		if file:
			s= file.pop(0)
		#s = file.readline()
	
		# Verifica se acabou
		if not file:
			print ('DONE!')
			break
   
	draft.close()

class sub_time:
    def __init__(self):
        self.__h = 0
        self.__m = 0
        self.__s = 0
        self.__ms = 0

    def set_time(self, h, m, s, ms):
        self.__h = h
        self.__m = m
        self.__s = s
        self.__ms = ms
        return

    def add_ms(self, ms):
        self.__ms += ms
        if self.__ms < 0:
            self.__h -= 1
            self.__m += 59
            self.__s += 59
            self.__ms += 1000
        
        self.__s += self.__ms//1000
        self.__m += self.__s//60
        self.__h += self.__m//60

        self.__ms %= 1000
        self.__s %= 60
        self.__m %= 60
        return
        
    def get_time(self):
        return [self.__h,self.__m,self.__s,self.__ms]
            
    def strh(self):
        if self.__h < 10:
            return '0'+str(int(self.__h))
        return str(self.__h)

    def strm(self):
        if self.__m < 10:
            return '0'+str(int(self.__m))
        return str(self.__m)

    def strs(self):
        if self.__s < 10:
            return '0'+str(int(self.__s))
        return str(self.__s)

    def strms(self):
        if self.__ms < 10:
            return '00'+str(int(self.__ms))
        elif self.__ms < 100:
            return '0'+str(int(self.__ms))

        return str(int(self.__ms))

    def printt(self):
        print ("h:%d - m:%d - s:%d - ms:%d" % (self.__h, self.__m, self.__s, self.__ms)) 


    
    ####################### MAIN
if __name__ == "__main__":

    # argument style: ./sub file.str <delay|...> <+|->time <ms|s>

	file_open = open(sys.argv[1], 'r')
	file_variable = file_open.readlines()			#Lista de linhas do arquivo

	if sys.argv[2] == 'delay':

		time = int(sys.argv[3]) #Get time
		if sys.argv[4] == 's':
			time *= 1000

		delay_srt(file_variable, time, sys.argv[1])
    # else if blalbla :
