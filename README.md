Como utilizar o sistema
=======================

## 1. Obtendo o cógido fonte

Clone o repositório:

	$ git clone https://github.com/rafasgj/tchelinux-system.git

## 2. Crie o formulário de _Call For Papers_

Crie um formulário no Google Docs com os campos das palestras na
seguinte ordem:

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

O campo **Timestamp** deve armazenar o horário da palestra (normalmente,
o Google Docs adiciona o _timestamp_ do momento que a palestra foi
submetida); o campo **Sala** deve conter o número da sala na qual a palestra
será realizada, porém não é o número da sala no evento, mas o índice da
sala (1, 2, 3, ...) na lista de salas.

Os campos *Tema da Palestra*, *Email do Palestrante*, e *Telefone do
Palestrante*, ainda não são utilizados, mas devem manter esta ordem para
permitir futuras extensões.

Devem ser adicionadas descrições para a abertura e encerramento do evento,
assim como intervalo de almoço e _coffe break_. A abertura do evento deve
ter **abertura** como _Palavra-chave_, e o encerramento deve ter
**encerramento**. Isto faz com que o palestrante do encerramento seja
adicionado como **moderador**. A palavra-chave **intervalo** deve ser
utilizada para os intervalos de almoço e _coffe break_.

Para facilitar a criação das entradas gerais do evento, apenas os campos
_Timestamp_ e _Titulo da Palestra_ são obrigatórios. Sugere-se que nenhum
campo desnecessário seja preenchido.

Os nomes dos campos não são relevantes para o sistema, mas auxiliam na
edição e verificação dos dados, portanto, sugere-se utilizar a mesma
nomenclatura.

## 3. Edite a configuração do evento

Altere o arquivo "data/config.json" com as informações do evento.

## 4. Atualize o repositório

**TODO**

Para gerar os arquivos "CNAME" e "index.html", execute o script:

	$ tchelinux-event.py

## 5. Após o _Call For Papers_ terminar

Após finalizar o _call for papers_, defina as palestras a serem inseridas
programação ajustando o seu horário no campo "Timestamp".

Faça _download_ das palestras no formato CSV (deixe que o Google Docs formate
para você) e armazene o arquivo no diretório "data" com o nome "palestras.csv".

Para gerar os arquivos "CNAME" e "index.html", execute o script:

	$ tchelinux-event.py
