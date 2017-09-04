 Como utilizar o sistema
=======================

## 1. Obtendo o cógido fonte

Clone o repositório:

	$ git clone https://github.com/rafasgj/tchelinux-system.git

## 2. Crie o formulário de _Call For Papers_

Crie um formulário no Google Docs com os campos das palestras na
seguinte ordem:

1	* Nome do Palestrante
	* Titulo da Palestra
	* Resumo da Palestra
	* Palavras-chave
	* Nível de Experiência Esperado
	* Mini-currículo do Palestrante
	* Tema da Palestra
	* Email do Palestrante
	* Telefone do Palestrante

Os campos *Tema da Palestra*, *Email do Palestrante*, e *Telefone do
Palestrante*, ainda não são utilizados, mas devem manter esta ordem para
permitir futuras extensões.

Os nomes dos campos não são relevantes para o sistema, mas auxiliam na
edição e verificação dos dados, portanto, sugere-se utilizar a mesma
nomenclatura. A ordem dos campos é relevante e não deve ser modificada.

## 3. Crie o formulário de inscrições

Crie um formulário de inscrições para o evento, contendo o Nome e Email
como campos obrigatórios.

## 4. Edite a configuração do evento

Copie o arquivo "data/config.json" para "data/<codinome>.json", e o
altere com as informações do evento.

A descrição do formato deste arquivo você encontra no arquivo
[JSON.md](JSON.md).

## 5. Após o encerramento do Call For Papers

Após finalizar o _call for papers_, defina as palestras a serem inseridas
programação ajustando o seu horário no campo "Timestamp".

O campo **Timestamp**, é adicionado pelo Google Forms, e deverá armazenar
o horário da palestra; o campo **Sala** deve ser adicionado após o
fechamento do _Call for Papers_ e conterá o índice da sala na qual a
palestra será realizada. Este índice não é o número real da sala no
evento, mas o índice da sala na grade (1, 2, 3, ...).

Após esta configuração, os campos devem ter a seguinte ordem:

	* Timestamp
	* Sala
	* Nome do Palestrante
	* Titulo da Palestra
	* Resumo da Palestra
	* Palavras-chave
	* Nível de Experiência Esperado
	* Mini-currículo do Palestrante
	* Tema da Palestra
	* Email do Palestrante
	* Telefone do Palestrante

Devem ser adicionadas, na lista de palestras, as descrições para a
abertura e encerramento do evento, assim como intervalo de almoço e
_coffe break_. A abertura do evento deve ter **abertura** como
_Palavra-chave_, e o encerramento deve ter **encerramento**. Isto faz
com que o palestrante do encerramento seja adicionado como **moderador**.
A palavra-chave **intervalo** deve ser utilizada para os intervalos de
almoço e _coffe break_.

Para facilitar a criação das entradas gerais do evento, apenas os campos
_Timestamp_ e _Titulo da Palestra_ são obrigatórios. Sugere-se que nenhum
campo desnecessário seja preenchido.

Faça _download_ das palestras no formato CSV (deixe que o Google Docs
formate para você) e armazene o arquivo no diretório "data" com o nome
"<codinome>.csv".

Para gerar o diretório do evento, execute:

	$ ./mkevent.sh <codinoe>
