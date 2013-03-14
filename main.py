    # Basic for handling a .str subtitles
    # Works up to 99h files (its enought, i think..)

import sys

# Auxilia a pular qualquer texto que esteja antes da primeira legenda. 
# Depois basta ir procurando pela linha em braco.
def is_this_k(s,k):
	try:
		x=int(s)
		if x==k:
			return True
		return False
	except ValueError:
		return False

# Talvez fazer uma verificao se o arquivo em questao nao tem nada em comum com um arquivo de legenda?
# File - Arquivo aberto || Time - Tempo de delay || Saveas - Destino
def delay_srt(file, time):
	result=[]
	counter = 1 				# legenda atual. Eh realmente necessario marcar isso?
	t1, t2 = sub_time(), sub_time()
	
	if not file:				# caso onde arquivo esta vazio
		return result
	
	# Procura a primeira legenda (pula espacos em branco iniciais)
	while True:
		s= file.pop(0)
		if (not s) or (is_this_k(s,1) == True):
			break

	while True:
		result.append(s)		# grava o numero da legenda
		
		if file:
			s= file.pop(0)		# carrega os tempos

		# Faz a conversao de F.Pereire
		counter += 1
		t1.set_time(int(s[0:2]), int(s[3:5]), int(s[6:8]), int(s[9:12])) 
		t2.set_time(int(s[17:19]), int(s[20:22]), int(s[23:25]), int(s[26:29]))

		t1.add_ms(time)
		t2.add_ms(time)

		# Cria e grava a string de novo tempo
		str_time = t1.format_print() + " --> " + t2.format_print() + "\n"

		result.append(str_time)

		# Le e grava ate encontrar uma linha em branco ou a lista do arquivo acabar
		while s.strip() and file:
			s= file.pop(0)
			result.append(s)
			
		if file:		# Le o numero da legenda, se houver
			s= file.pop(0)
		
		else: 			# se nao houver
			print ('DONE!')
			break
   
	return result
	

# Funcaoo para salvar o resultado final em um arquivo.
# lines - Vetor de strings que representam o arquivo final || saveas - destino.
def save_file(lines, saveas) :
	draft = open(saveas, 'w')
	for x in lines:
		draft.write(x)
		
# Funcao para carregar o estado inicial de um dado arquivo de legenda (que pode vir a nao ser .srt no futuro). 
# path - caminho do arquivo. || linhas - lista com vetor resultante.
def load_file(path): 
	file_open = open(path, 'r')
	lines = file_open.readlines()			#Lista de linhas do arquivo
	return lines
	

# Adiciona uma legenda "lines" nova na posicao "pos" do arquivo "subfile" com tempo inicial "ti" e tempo final "tf". Arruma as legendas seguintes.
# subfile -> lista de string || line -> string || pos -> int || ti = sub_time() || tf = sub_time() || retorna Mod, lista com as strings
def add_sub(subfile, lines, pos, ti, tf):
	Mod = []
	print("addsub")
	
	while True:					# pula bobagens
		s=subfile.pop(0)
		if (not s) or (is_this_k(s,1) == True):
			break
			
	while True and (not pos==1):						# pula ate a pos-1 legenda. pos-1 pois precisa tratar o caso onde eh a ultima legenda. 
		if subfile and not (is_this_k(s,pos-1)):		# verifica se a legenda acabou ou se chegou a pos-1 (o (not pos==1) conserta na primeira legenda)
			print("isnotthisk")
			print(s)
			print(pos-1)
			Mod.append(s)
			
		elif not s:
			return []			# Nao tem pelo menos pos-1 legendas
			
		else:					# Se chegou aqui a legenda de pos-1 existe
			Mod.append(s)		# append do numero pos-1
			s=subfile.pop(0)	# pop do tempo do numero pos-1
			Mod.append(s)		# append do tempo
			
			s=subfile.pop(0)	# pega trecho da legenda
			while s.strip() and subfile:
				Mod.append(s)	# vai passando ate acabar
				s=subfile.pop(0)
			
			Mod.append("\n") 	# insere a blank line
			
			break
			
		s=subfile.pop(0)
	
	# Neste ponto, foi colocado a legenda pos-1.
	counter = pos+1
	Mod.append(str(pos))		# Adiciona a posicao
	str_time = ti.format_print() + " --> " + tf.format_print() + "\n"
	Mod.append(str_time)
	for w in lines:				# Adiciona as linhas
		Mod.append(w)
	Mod.append("\n")
	
	while subfile:				# Coloca o resto, respeitando a nova contagem
		s=subfile.pop(0)
		if not s:				# Resumo: Sai pegando todo mundo ate acabar, troca o numero por counter
			break
		Mod.append(str(counter))
		counter=counter+1		# e atualiza o counter para cada legenda
		s=subfile.pop(0)
		while s.strip() and subfile:
			Mod.append(s)
			s=subfile.pop(0)
		Mod.append(s)

	return Mod					# retorna a lista modificada
	
	
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

	def format_print(self):	
		Tempo = self.strh()+":"+self.strm()+":"+self.strs()+","+self.strms()
		return Tempo

	def printt(self):
		print ("h:%d - m:%d - s:%d - ms:%d" % (self.__h, self.__m, self.__s, self.__ms)) 




    ####################### MAIN
if __name__ == "__main__":

    # argument style: ./sub file.str <delay|...> <+|->time <ms|s>
															# Novo formato de funcoes, veja:
	file_variable = load_file(sys.argv[1])					# carrega o arquivo atraves da funcaozinha.
	
	t1, t2 = sub_time(), sub_time()							# tempos para exemplo do add_sub
	t1.set_time(1,1,1,1)			
	t2.set_time(2,2,2,2)
	
	nova = ["caramba", "caramba2"]							# linha de legenda que sera adicionada
	
	adicionou=add_sub(file_variable,nova, 1, t1, t2)		# chama e retorna na variavel, como tem que ser \o
	print(adicionou)										# printa pra ver. Sucesso?

	if sys.argv[2] == 'delay':

		time = int(sys.argv[3]) #Get time
		if sys.argv[4] == 's':
			time *= 1000

		delayed=delay_srt(file_variable, time)				# Faz o delay
		save_file(delayed, sys.argv[1])						# Salva arquivo
		
    # else if blalbla :
