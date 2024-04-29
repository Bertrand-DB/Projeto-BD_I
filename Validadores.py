class Validadores():

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
    
    def digitos(self, entrada):
        return entrada.isdigit() or entrada == ""
    
    def ponto_decimal(self, entrada):
        # verificar se o valor é uma string vazia, apenas dígitos ou um número com um ponto decimal
        valores = entrada.split(".")

        if len(valores)>2:
            return False
        
        for parte in valores:
            if not self.digitos(parte):
                return False
            
        return True

    def string(self, entrada):
        caracteres_permitidos = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ -áàâãéèêíìîóòôõúùûçÁÀÂÃÉÈÊÍÌÎÓÒÔÕÚÙÛÇ'
        
        # Verifica se os caracteres não estão na lista de caracteres permitidos
        for char in entrada:
            if char not in caracteres_permitidos:
                return False

        return True
