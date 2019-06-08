# DESCRIÇÃO DO PROJETO:

Solução para determinar posições e estatísticas em corridas de pilotos.

## LIMITAÇÕES DO PROGRAMA:

* O arquivo de log de corrida só tem horários, não dias. Por conta disso, fica difícil determinar
se um horário depois das 0 horas é consecutivo a um das 23, passa-se a ter que usar heurística.
Assume-se no algoritmo que a corrida é toda dada em um dia, interamente assumiu-se o dia primeiro
de janeiro de 2019 (que nunca é mostrado). Caso os horários passem da zero hora, o programa deixa
de funcionar.

* Ele não funciona se um piloto ainda não contabilizado aparecer no final da lista começando com
um número de volta maior que 1.

## CONTORNOS E TESTES EXISTENTES:

* O programa faz algumas verificações básicas de consistência, como se as voltas de um determinado
piloto são consecutivas ou se o arquivo de entrada existe.

* O programa usa o módulo doctest de python para testes, onde os testes são usados inline em forma
de comentários. Infelizmente, doctest não funciona tão bem para classes e métodos de objetos
porque estes constroem em cima de dados internos existentes. Mesmo assim, de 13 métodos foram
feitos testes para 8. O programa pode ser testado com:

`python3 -m doctest corrida.py`

## COMO EXECUTAR
* Coloque o programa, `corrida.py`, no mesmo diretório do arquivo de log, `corrida.log`. Rode usando
python3:

`python3 corrida.py corrida.log`

Se preferir, o arquivo `corrida.log` pode estar em diretório diferente, bastante especificar o caminho
completo.

## DIRETIVAS DE COMO FOI DESENVOLVIDO O PROGRAMA

* Procurou-se usar o PEP8 (espaços entre atribuições, nomes de funções, métodos e variáveis), mas nem
todas as diretivas foram seguidas (por exemplo: entende-se que o tamanho máximo de linha de 72 caracteres
é anacrônico para os displays de hoje).

* Somente módulos internos da própria linguagem python foram usados.

* Python 3 foi escolhido ao invés de 2 não só por ser mais novo, mas também por ter menos problemas com
unicode. O nosso arquivo de entrada pode ter nomes em japonês ou hindi, não é?

* Todos os comentários no programa e todos os commit no github foram feitos em inglês, pra preparar o
programa para times internacionais (nos próprios requisitos do trabalho estão o conhecimento de inglês)

* Foi usado paradigma procedural para o loop principal com os dados encapsulados em formatos de objetos,
com métodos próprios. Diretivas de orientação a objeto como variáveis protegidas, getters e métodos de
classe foram usados.

* Todos os objetivos opcionais ("bônus") foram alcançados.

* Várias condições de contorno e até "pegadinhas" foram evitadas pela estrutura de código, como os
pilotos que saem da prova antes de terminar. O programa funciona ok mesmo com esses casos.

* O programa permite mudar o número de voltas de uma corrida com a variável de classe _maximum_lap,
mas ela não pode ser igual a 1.
