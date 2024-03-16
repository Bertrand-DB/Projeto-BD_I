class Verificadores():

    def espaco_vazio(self, entradas):   #verifica se a(s) entradas possuem apenas espaço ou são vazias
        vazios = False
        for i in entradas:
            i = str(i)
            if i.strip() == "":
                vazios += 1
        return vazios
    
    def tem_numero(self, entradas):     #verifica se a(s) entradas possuem ao menos um caracter numero
        numeros = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        for palavra in entradas:
            for num in numeros:
                if palavra.find(num) != -1:
                    return True
        return False

    def so_numero(self, entradas):            #verifica se a entrada é um número em forma de string, int ou float
        try:        
            if type(entradas) is list:
                for palavra in entradas:
                    float(palavra)
            else:
                float(entradas) 

        except ValueError:
            return False

        return True   
