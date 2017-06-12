#!/usr/bin/env python3

from datetime import datetime
from collections import namedtuple
from operator import itemgetter
import json
import csv

import locale
locale.setlocale(locale.LC_TIME,'pt_BR')

import sys

class Lecture(namedtuple('Lecture','room author title abstract keywords level resume')):
    pass

def load_lectures():
    lectures = {}
    with open('data/palestras.csv') as csvfile:
        for row in csv.reader(csvfile):
            if 'Timestamp' == row[0]: continue
            p = Lecture(*row[1:8])
            lectures.setdefault(row[0],[]).append(p)
    return lectures

def inscricoes(event):
    always = """
        <p> O evento tem <b>entrada franca</b>, por&eacute;m os participantes
        s&atilde;o encorajados a doar 2kg de alimentos n&atilde;o
        perec&iacute;veis (exceto sal), que ser&atilde;o doados a
        institui&ccedil;&otilde;es de caridade da regi&atilde;o.</p>
        <p>Os alimentos ser&atilde;o recebidos no momento do credenciamento.</p>
    """
    before = """
        <p>As inscri&ccedil;&otilde;es para o evento estarão abertas até
        o dia <b>{inscricoes[data]}</b>, ou até se esgotarem as
        <b>{inscricoes[vagas]}</b> vagas.</p>
        <p><b><a href='{inscricoes[url]}'>Inscreva-se agora!</a><b></p>
        """
    after = """
        <p>Cerca de <b>{resultado[participantes]}</b> participantes atenderam
        ao evento, onde foram arrecadados mais de <b>{resultado[alimentos]}</b>
        Kg de alimentos.</p>"""
    closed="""
        <p><b>As inscri&ccedil;&otilde;es pelo site foram encerradas. Interessados
        poder&atilde;o fazer sua inscri&ccedil;&atildee;o no dia e local do evento,
        mediante disponibilidade de vagas.</b></p>
        """
    if event['date'] > datetime.today():
        event['titulo_inscricoes'] = "Inscri&ccedil;&otilde;es"
        closed = event['inscricoes'].get('encerradas', False) or \
                    event['inscricoes']['date'] > datetime.today()
        if closed:
            event['texto_inscricoes'] = always + closed
        else:
            event['texto_inscricoes'] = always + before.format(**event)
    else:
        event['titulo_inscricoes'] = "Resultados"
        event['texto_inscricoes'] = always + after.format(**event)

def load_config():
    with open('data/config.json','r') as config:
        event = json.load(config)
        date = datetime.strptime(event['data'],'%Y-%m-%d')
        event['date'] = date
        event['data'] = date.strftime("%d de %B de %Y")
        event['ano'] = date.year
        event['mes'] = date.month
        event['dia'] = date.day
        date = datetime.strptime(event['inscricoes'].get('deadline', event['data']),'%Y-%m-%d')
        event['inscricoes']['date'] = date
        event['inscricoes']['data'] = date.strftime("%d de %B de %Y")
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
    rooms = event['salas']
    roomcount = len(rooms)
    for sala in event['salas']:
        print ('<th class="schedule-slot" colspan="1" style="text-align:center">Sala {numero}</th>'.format(**sala))
    print('</tr>\n</thead>\n<tbody>')

    template_other = """
        <tr class="schedule-other">
            <td class="schedule-time">{time}</td>
            <td class="schedule-slot" colspan="{span}" style="text-align:center">
                {title}<br/>
                {label}<br/>
                <span class="speaker">{author}</span>
            </td>
        </tr>
        """
    template_lecture = """
        <td class="schedule-slot" colspan="1" rowspan="1">
            <a href="#speech-{count}">
                <span class="description">{title}<br/></span>
            </a>
            {label}
            <span class="speaker">{author}</span>
        </td>
    """
    speech = 1
    for k in sorted(lectures):
        slot = lectures[k]
        if len(slot) == 1:
            kn = slot[0]
            label = ''
            author = kn.author
            if kn.keywords == "abertura":
                label = labels['all']
            elif kn.keywords == "encerramento":
                label = labels['all']
                author = 'Moderador: ' + author
            print (template_other.format(time=k,span=roomcount,
                                         label=label, **kn._asdict()))
        else:
            slot.sort(key=itemgetter(0))
            print('<tr class="schedule-other">')
            print('<td class="schedule-time">{time}</td>'.format(time=k))
            for entry in slot:
                print(template_lecture.format(**entry._asdict(),count=speech,
                                              label=labels[entry.level]))
                speech += 1
            print("</tr>")
    print ("</tbody>\n</table>\n</div>\n</div>\n</section>")

def process_abstracts(event,lectures):
    template = """
    <div id="speech-{count}" class=speech-container>
        <span class="speech-time">{time}</span>
        <div class="speech-info">
        <h3 class="speech-title">{title}
        <!-- TODO: generate liks for SLIDES and CODE
        <a href="#">
            <span class="label label-default slides">SLIDES</span>
        </a>
        -->
        </h3>
        <span class="speech-description">{abstract}</span>
        <h3 class="speaker-name">{author}</h3>
        <span class="speaker-bio">{resume}</span>
    </div>
    """

    print ("""
        <section id="palestras">
            <div class="container">
                <h2 class="subtitle">Palestras</h2>
    """)
    speech = 1
    for k in sorted(lectures):
        slot = lectures[k]
        if len(slot) == 1: continue
        for kn in slot:
            print(template.format(**kn._asdict(),count=speech,time=k))
            speech += 1
    print("</div>\n</section>")

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
    process_abstracts(event,lectures)
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
