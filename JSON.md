Editando a configuração do evento
=================================

# Introdução

Para criar um novo evento utlizando o script de geração do _hotsite_
padrão do Tchelinux, você deve criar um novo arquivo de configuração
utilizando o formato JSON, com as informações descritas neste documento.

# Informações Básicas

As informações básicas do evento são o identificador do evento, que é o
mesmo utilizado na URL do evento, a data de quando ocorrerá o evento, e
a cidade onde o evento será sediado. Todas estas informações são
obrigatórias.

Estas informações estão na raiz do arquivo de configuração:

```json
{
    "id": "nh",
    "date": "2017-08-12",
    "city": "Novo Hamburgo",
}
```

O **id** deve ter o mesmo valor do **codinome** atribuído ao evento. O
formato da data deve ser _YYYY-mm-dd_. E a cidade deve conter o nome
completo da cidade (por exemplo, Porto Alegre é "Porto Alegre", e não
"Poa", "Portinho" ou "Porto" -- mas seria muito legal fazer um evento
além-mar, na cidade de Porto, Portugal).

# Informações sobre a Instituição

As informações relativas à instituição que sediará o evento devem ser
inseridas no objeto **instituicao**. Os campos deste objeto são todos
obrigatórios, a não ser que seja especificado o contrário.

long_name
: Nome completo da instituição.

short_name
: Sigla, ou nome popular da instituição. Utilize um nome mais curto que
seja oficial, e com a grafia correta. Este campo é opcional.

address
: Endereço oficial da instituição.

url
: URL oficial da instituição. Caso seja uma instituição com varios
campi, se houver uma URL específica para o campus onde o evento irá
ocorrer, utilize a URL específica, e não a URL geral da instituição.

logo
: Nome do arquivo contendo a imagem do logotipo da instituição. Utilize
o loogtipo oficial, e armazene a imagem no diretório _images_.

latitude
: A latitude da entrada oficial da instituição. Idealmente, você obtém
este dado a partir do [Google Maps](https://maps.google.com), pois este
dado será utilizado para obter a posição da instituição neste sistema.

longitude
: A longitude da entrada oficial da instituição. Veja as observações
para a latitude.

courses
: Uma lista, opcional, de cursos que apóiam o evento, onde cada objeto
da lista contém, obrigatoriamente, o campo _name_, representando o nome
do curso, e, opcionalmente, o campo _url_, contendo a URL que direciona
para a página com informações do curso.

local_map
: Caso exista uma imagem que mostra um mapa interno da instituição para
identificar o local do evento, adicione a imagem do mapa ao diretório
_images_, e o nome do arquivo neste campo. Este campo é opcional.

```json
{
    "instituicao": {
        "courses" : [
            { "name": "Ciência da Computação" }
        ],
        "long_name": "Universidade de Santa Cruz do Sul",
        "short_name": "UNISC",
        "address": "Av. Independência, 2293",
        "url": "http://www.unisc.br",
        "logo": "UNISC.png",
        "latitude": -29.697987,
        "longitude": -52.438431,
        "diretorio": "Diretório Acadêmico da Ciência da Computação",
        "local_map": "MAPA.png"
    }
}
```

# Apoiadores e patrocinadores

É possivel adicionar duas listas de objetos representando apoiadores, e
patrocinadores do evento. Embora as listas sejam opcionais, os campos
dos objetos são todos obrigatórios.

Para cada objeto das listas, os seguintes campos devem ser preenchidos:

name
: Nome do apoiador/patrocinador.

short_name
: Sigla ou nome mais curto do apoiador/patrocinador.

url
: A URL que leva para o site do apoiador/patrocinador.

logo
: O nome do arquivo que contem a imagem com o logotipo do apoiador ou
patrocinador. Esta imagem deve ser armazenada no diretório _images_.

```json
{
    "sponsors": [],
    "support": [
        {
            "nome": "Diretório Acadêmico da Ciência da Computação",
            "short_name": "DACOMP",
            "url": "http://dacomp.forumeiros.com/",
            "logo": "DACOMP.png"
        }
    ]
}
```

# Configuração de salas do evento

A configuração de salas do evento define quantas salas serão utilizadas
para palestras no evento. Sugere-se reservar um número de salas
suficiente para comportar entre, no mínimo, 30 participantes, e, no
máximo, 50 participantes, por sala, sem jamais superar o número máximo
de participantes que as salas do local permitem, para garantir a
segurança dos participantes no evento.

As salas reservadas devem ter projetores para os palestrantes, e não
devem ser laboratórios, para evitar danos a equipamentos das
instituiições, uma vez que a ideia das apresentações do Tchelinux são no
estilo _lecture_ e não práticas.

A ordem das salas na configuração são relevantes, e serão utilizadas
para definir, posteriormente, a programação, sendo a primeira sala a
sala de índice 1 na programação, a segunda a sala de índice 2, e assim
por diante.

O campo **number** é obrigatório, e define o número que identifica a
sala, dentro da instituição. O campo **subject**, é um campo opcional,
que normalmente será preenchido, se necessário, quando da adição da
programação ao _hotsite_.

```json
{
    "rooms" : [
        { "number": "C327", "subject": "Sysadmin e Cloud" },
        { "number": "C335", "subject": "Desenvolvimento e Marketing" },
        { "number": "C336", "subject": "Distribuições e Aplicações" },
        { "number": "C338", "subject": "Sistemas embarcados e IoT" }
    ]
}
```

# Configuração da Chamada de Trabalhos

A chamada de trabalhos de um evento do Tchelinux deve ser aberta, pelo
menos, 45 dias antes do evento. Para isso, deve ser criado um formulário
utilizando o Google Forms com um formato específico (veja o
[README](README.md)).

O objeto **callForPapers** é obrigatório, assim como o campo **url**,
onde será adicionada a URL do formulário de submissão de palestras. Os
campos **start**, **deadline** e **notice** são opcionais.

Os campos **start** e **deadline** marcam o período no qual as propostas
de palestras podem ser submetidas, e se não estiver presente, esta data
serão automaticamente definida para 30 e 15 dias antes do evento,
respectivamente.

> TODO: o campo _start_ ainda não está sendo utilizado.

O campo **notice**, também é opcional, e marca a data em que será dado
retorno aos palestrantes sobre o aceite de suas propostas de palestras.
Esta data, se não for definida no arquivo de configuração, é
automaticamente definida para 3 dias após o encerramento da submissão
de propostas.

```json
{
    "callForPapers": {
        "url": "https://goo.gl/forms/wTyrVgyrOigZ5b2E3",
        "start": "2017-07-10",
        "deadline": "2017-07-30",
        "notice": "2017-08-03"
    }
}
```

# Configuração das informações de inscrição

As inscrições para o evento são, atualmente, realizadas a partir de um
formulário criado utilizando o Google Forms, contendo apenas o nome e o
email do participante. É muito importante salientar que o _email_ será
utilizado para a obtenção do certificado digital de participação.

A configuração das inscrições para a geração do _hotsite_ do evento é
obrigatória. A **url** deve ser a URL do formulário de inscrição no
evento. O número de vagas é definido no campo **availability**. Os dois
campos são obrigatórios.

Os campos opcionais **start**, **deadline** e **closed** definem
como o _hotsite_ irá mostrar o estado das incrições. Os campos
**start** e **deadline**, cotém datas no formato _YYYY-mm-dd_, que
marcam a data de início e fim das inscrições.

O campo **closed**, contém um dos valores _true_ ou _false_, e marca
se as incrições estão fechadas (encerradas) ou não. Este campo só é
avaliado dentro do período de inscrições. Caso não seja definido, o
campo **closed** contém o valor _false_, significando que o estado
das inscrições dependem, exclusivamente, do período de inscrições
definido.

O campo **deadline**, se não definido, recebe o mesmo valor do dia
anterior ao evento. As inscrições realizadas no dia do evento devem ser
realizadas à parte. O link para as inscrições no _hotsite_ só será
exibido se o dia de geração for anterior a esta data.

O campo **start**, se não definido, recebe como valor padrão a data
relativa a 20 dias antes do evento. O link para as inscrições no
_hotsite_ só será exibido se o dia de geração for posterior a esta data.

```json
{
    "inscricoes": {
        "url": "https://goo.gl/forms/gdiu9s7bcC0faSWl2",
        "availability": 300,
        "start": "2017-07-28`",
        "deadline": "2017-05-28",
        "closed": false
    }
}
```

# Exemplo de JSON

O JSON abaixo, contém a configuração do _hotsite_ do evento realizado em
Novo Hamburgo, em 2017, quando da abertura da chamada de trabalhos.

```json
{
    "id": "nh",
    "date": "2017-08-12",
    "city": "Novo Hamburgo",
    "institution": {
        "long_name": "FTEC Faculdades de Tecnologia",
        "short_name": "FTEC",
        "address": "Rua Silveira Martins, 780",
        "url": "http://www.ftec.com.br",
        "logo": "ftec.png",
        "latitude":  -29.681352,
        "longitude": -51.125599
    },
    "sponsors": [],
    "support": [],
    "rooms" : [
        { "number": "1" },
        { "number": "2" },
        { "number": "3" },
    ],
    "callForPapers": {
        "url": "https://goo.gl/forms/wTyrVgyrOigZ5b2E3",
        "deadline": "2017-07-30",
        "notice": "2017-08-03"
    },
    "enrollment": {
        "start": "2017-07-25",
        "deadline": "2017-08-12",
        "url": "https://goo.gl/forms/UZg3GSt31G7tP5SD3",
        "availability": 250,
        "closed": false
    }
}
```
