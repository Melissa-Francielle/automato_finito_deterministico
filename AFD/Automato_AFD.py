import json 
import csv
import time 
import sys 

class AutomatoDFA:
    def __init__(self, file_aut):
        #inicia os paramentros recebendo uma lista com string com nome dos estados dentro do arquivo json 
        self._initial_states = file_aut["initial"] #estado inicial 
        self._final_states = file_aut["final"] #estado final
        self._transitions = file_aut["transitions"] #e as transições aceitas
        self.result = []

    def operation (self, str_in_input): #uma função para executar o automato. a partir de uma entrada 
        current = self._initial_states #estado atual que seria o inicial, para começar o automato 
        for word in str_in_input: #passa interando em entrada que é (Str_entrada)
            current = self._get_next (current, word) #a partir de uma variavel proximo_estado é pego o método proximo_estado privado e coloca como atributos a palavra e o estado atual            
            if current is None: # Adiciona esta condição para interromper a execução se não houver transição para a palavra lida
                break
        if current in self._final_states: #caso o proximo estado esteja vázio após percorrer a palavra e não levar ao estado final desejado 
            return 'Accepted'
        else:
            return 'Rejected'   
    
    def _get_next (self, current, word): #o método chamado logo acima, que pega o estado e tem os mesmos parametros usado acima
        current = current[0] if isinstance(current, list) else current  # Convertendo o estado atual para um número inteiro
        for transition in self._transitions:
            if transition["from"] == current and transition["read"] == word: #caso a transição from, no caso o arquivo dentro do json
                #for == ao estado atual que no método acima foi colocado como proximo, e for lido uma palavra ou seja lido um vazio
                return transition["to"] #então retonar para qual proximo estado vai
        return None

    def manipulating (self, string):
        self.result = [] # Limpa os resultados anteriores antes de executar o autômato
        self.result = self.operation(string)
        result = self.result
        if 'Accepted' in result:
            return 1
        elif 'Rejected' in result:  # Corrigido para verificar 'Rejected'
            return 0

            
def automata_file(file_path): #uma função fora da class para ler o arquivo json
    with open(file_path) as file:
        return json.load(file)
    
def cases (file_path):
    test = []
    with open (file_path, 'r', newline='') as file:
        reader = csv.reader (file, delimiter=';')
        next(reader)
        for line in reader:
            if len(line) >= 2:
                test.append((line[0], int(line[1])))
    return test
    
def main (file_aut_path, file_teste_path, file_out_path):
    automata = AutomatoDFA(automata_file(file_aut_path))
    case_test = cases(file_teste_path)

    with open (file_out_path, 'w', newline='') as csv_file:
        writing = csv.writer(csv_file, delimiter=';')
        writing.writerow(["Palavra de entrada; ""Resultado esperado; ""Resultado Obtido; ""Tempo; "])
        
        for testing in case_test:
            str_in_input, expected_result = testing
            start_time = time.perf_counter()
            result = automata.manipulating(str_in_input)
            end_time = time.perf_counter()

            execution_time = "{:.5f}".format(end_time - start_time)  # Formatação com cinco casas decimais
            writing.writerow([str_in_input, expected_result, result, execution_time])
            csv_file.flush()

if __name__ == "__main__":
    if len(sys.argv) !=4:
        print("Ordem para acessar o arquivo: python arquivo tipo ->(.py) arquivo tipo ->(.aut) arquivo do tipo-> (.csv) nome do arquivo de saida tipo -> (.out)")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
