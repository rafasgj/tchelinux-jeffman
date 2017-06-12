#!/usr/bin/env python3

from datetime import datetime
from collections import namedtuple

import json
import csv

class Lecture(namedtuple('Lecture','speaker title abstract keywords level resume')):
    pass

def load_lectures():
    lectures = {}
    with open('data/palestras.csv') as csvfile:
        for row in csv.reader(csvfile):
            if 'Timestamp' == row[0]: continue
            p = Lecture(*row[1:7])
            lectures.setdefault(row[0],[]).append(p)
    return lectures

def inscricoes(event):
    always = """
        <p> A participa&ccedil;&atilde;o no evento &eacute; <b>gratuita</b>
        por&eacute;m os participantes s&atilde;o encorajados a doar 2kg de
        alimentos n&atilde;o perec&iacute;veis (exceto sal) que ser&atilde;o
        doados a institui&ccedil;&otilde;es de caridade da região.
        </p>
        <p>Os alimentos ser&atilde;o recebidos no momento do credenciamento.</p>
    """
    before = """
        <p>As inscrições estão abertas até o dia {inscricoes[deadline]},
        ou até se esgotarem as {inscricoes[vagas]}.</p>
        <p><b><a href='{inscricoes[url]}'>Inscreva-se agora!</a><b></p>
        """
    after = """
        <p>Cerca de {resultado[participantes]} participantes atenderam
        ao evento, onde foram arrecadados mais de {resultado[alimentos]}
        Kg de alimentos.</p>"""
    closed="""
        <p><b>As inscrições pelo site foram encerradas. Interessados
        poderão fazer inscrição no local do evento, mediante
        disponibilidade de vagas.</b><p>
        """
    if event['date'] <= datetime.today():
        event['titulo_inscricoes'] = "Inscrições"
        closed = event['inscricoes'].get('encerradas', False)
        if closed:
            event['texto_inscricoes'] = always + closed
        else:
            event['texto_inscricoes'] = always + before.format(**event)
    else:
        event['titulo_inscricoes'] = "Resultados"
        event['texto_inscricoes'] = always + after.format(**event)

def load_config():
    with open('config.json','r') as config:
        event = json.load(config)
        date = datetime.strptime(event['data'],'%Y-%m-%d')
        event['date'] = date
        event['data'] = date.strftime("%d de %B de %Y")
        event['ano'] = date.year
        event['mes'] = date.month
        event['dia'] = date.day
        if event['instituicao'].get('diretorio',None):
            event['instituicao']['artigo'] = 'o'
        else:
            event['instituicao']['artigo'] = 'a'
        if event['instituicao'].get('local_map',None):
            event['local_map'] = """
                <div id="local_map">
                    <h4>Mapa da {instituicao[short_name]}</h4>
                    <img src="{instituicao[local_map]}" alt="{instituicao[short_name]}" class="photo"/>
                </div>""".format(**event)
        else:
            event['local_map'] = ''
        inscricoes(event)
    return event

def create_CNAME(event):
    with open('CNAME','w') as cname:
        cname.write('{id}.tchelinux.org'.format(**event))

def include(filename,**kargs):
    with open('includes/'+filename+".inc") as f:
        print(f.read().format(**kargs),end='')

def process_schedule(event, lectures):
    # PROGRAMACAO
    pass

def process_lectures(event, lectures):
    labels = {
        "all":'<span class="label label-info">Todo o Público</span>',
        "Principiante":'<span class="label label-success">Principiante</span>',
        "Intermediario":'<span class="label label-warning">Intermediário</span>',
        "Avancado":'<span class="label label-danger">Avançado</span>'
    }
    print("""
    <section id="programacao">
        <div class="container">
            <h2 class="subtitle">Programa&ccedil;&atilde;o</h2>
            <div class="schedule-tbl">
                <table class="table table-responsive">
                    <thead>
                        <tr>
                            <th class="schedule-time">Hor&aacute;rio</th>
    """)
    numsalas = len(event['salas'])
    for sala in event['salas']:
        print ('<th class="schedule-slot" colspan="1" style="text-align:center">Sala {numero}</th>'.format(**sala))
    print('</tr>\n</thead>\n<tbody>')

    template_other = """
        <tr class="schedule-other">
            <td class="schedule-time">{time}</td>
            <td class="schedule-slot" colspan="{span}" style="text-align:center">
                {title}<br/>
                {label}<br/>
                <span class="speaker">{speaker}</span>
            </td>
        </tr>
        """
    template_lecture = """
        <td class="schedule-slot" colspan="1" rowspan="1">
            <a href="#speech-eeeee">
                <span class="description">{title}<br/></span>
            </a>
            {label}
            <span class="speaker">{speaker}</span>
        </td>
    """
    speech = 1
    for k in sorted(lectures):
        slot = lectures[k]
        if len(slot) == 1:
            kn = slot[0]
            label = ''
            speaker = kn.speaker
            if kn.keywords == "abertura":
                label = labels['all']
            elif kn.keywords == "encerramento":
                label = labels['all']
                speaker = 'Moderador: ' + speaker
            print (template_other.format(time=k,span=numsalas,
                                         title=kn.title,label=label,
                                         speaker=speaker))
        else:
            print('<tr class="schedule-other">')
            print('<td class="schedule-time">{time}</td>'.format(time=k))
            for entry in slot:
                print(template_lecture.format(**entry._asdict(),count=speech,
                                              label=labels[entry.level]))
                speech += 1
            print("</tr>")
    print ("</tbody>\n</table>\n</div>\n</div>\n</section>")

def process_support(event):
    include('support', **event)

def create_index_page(event, lectures):
    print('<!DOCTYPE html>')
    print('<html>')
    include('head')
    print('<body>')
    include('navbar', **event)
    include('page_header', **event)
    include('about', **event)
    include('subscription', **event)
    include('certificates', **event)
    process_schedule(event,lectures)
    process_lectures(event,lectures)
    include('location', **event)
    process_support(event)
    include('footer',**event)
    include('load_scripts')
    print('</body>')
    print('</html>')

event = load_config()
lectures = load_lectures()
create_CNAME(event)
create_index_page(event,lectures)
