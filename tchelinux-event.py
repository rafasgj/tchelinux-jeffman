#!/usr/bin/env python3

from datetime import datetime, timedelta
from collections import namedtuple
from operator import itemgetter
import json
import csv
import string

import locale
locale.setlocale(locale.LC_TIME,'pt_BR')

indexpage = open('index.html','w+')

import sys

class Lecture(namedtuple('Lecture','room author title abstract keywords level resume')):
    pass

def include_file(filename):
    with open('includes/'+filename+'.inc','r') as f:
        return f.read()


def load_lectures(eventfile):
    lectures = None
    try:
        with open('data/%s.csv'%eventfile) as csvfile:
            lectures = {}
            for row in csv.reader(csvfile):
                if not row[0].strip() or len(set(row[0]) & set(string.ascii_letters)) > 0:
                    continue
                p = Lecture(*row[1:8])
                lectures.setdefault(row[0],[]).append(p)
    except Exception as e:
        # Really, there's nothinng to do, but show it.
        print("Não encontrados dados de palestras para",eventfile,file=sys.stderr)
        # TODO: test if call for papers is still open.
        print("Assumindo que a submissão de palestras não encerrou.",file=sys.stderr)
    return lectures

def inscricoes(event):
    date = event['date']
    fix_date('enrollment:deadline',date-timedelta(days=1),event)
    fix_date('enrollment:start',date-timedelta(days=20),event)
    texto = """
        <p> O evento tem <b>entrada franca</b>, por&eacute;m os
        participantes s&atilde;o encorajados a doar 2kg de alimentos
        n&atilde;o perec&iacute;veis (exceto sal), que ser&atilde;o
        doados a institui&ccedil;&otilde;es de caridade da
        regi&atilde;o.</p>
        <p>Os alimentos ser&atilde;o recebidos no momento do
        credenciamento.</p>
    """
    before = """
        <p>As inscri&ccedil;&otilde;es para participação no evento
        estarão abertas a partir do dia <b>{enrollment[start_str]}</b>,
        até o dia <b>{enrollment[deadline_str]}</b>. Serão
        disponibilizadas <b>{enrollment[availability]}</b> vagas para o
        evento.</p>
    """
    opened = """
        <p>As inscri&ccedil;&otilde;es para o evento estarão abertas até
        o dia <b>{enrollment[deadline_str]}</b>, ou até se esgotarem as
        <b>{enrollment[availability]}</b> vagas.</p>
        <p><b><a href='{enrollment[url]}'>Inscreva-se agora!</a><b></p>
        """
    after = """
        <p>Cerca de <b>{result[attendants]}</b> participantes
        atenderam ao evento, onde foram arrecadados mais de
        <b>{result[donations]} Kg</b> de alimentos.</p>"""
    closed="""
        <p><b>As inscri&ccedil;&otilde;es pelo site foram encerradas.
        Interessados poder&atilde;o fazer sua inscri&ccedil;&atilde;o no
        dia e local do evento, mediante disponibilidade de vagas.</b>
        </p>
        """
    start_date = event['enrollment']['start']
    end_date = event['enrollment']['deadline']
    encerradas = event['enrollment'].get('closed', False)
    tdy = datetime.today()
    if date > datetime.today(): # se evento ainda nao se realizou...
        event['titulo_inscricoes'] = "Inscri&ccedil;&otilde;es"
        if tdy < start_date:
            event['texto_inscricoes'] = texto + before.format(**event)
        elif start_date <= tdy and end_date >= tdy and not encerradas:
            event['texto_inscricoes'] = texto + opened.format(**event)
        else:
            event['texto_inscricoes'] = texto + closed.format(**event)
    else: # evento já realizado..
        event['titulo_inscricoes'] = "Resultados"
        event['texto_inscricoes'] = texto + after.format(**event)

def format_date(date):
    if type(date) != datetime:
        date = datetime.strptime(date,'%Y-%m-%d')
    return date, date.strftime("%d de %B de %Y")

def fix_date(path, default_date, event):
    l = path.split(":")
    d = event
    for i in [ l[x] for x in range(len(l)-1) ]:
        d = d.setdefault(i,{})
    f = l[-1]
    fd = d.setdefault(f, default_date)
    d[f], d[f+"_str"] = format_date(fd)
    return d[f]

def texto_cursos(event):
    cursos = event['institution'].get('courses',None)
    if cursos:
        if len(cursos) == 1:
            cursos_text = "o curso "
        else:
            cursos_text = "os cursos "
        virgula = ""
        for curso in cursos:
            if 'url' in curso:
                cursos_text += virgula + '<a href="{url}">{name}</a>'.format(**curso)
            else:
                cursos_text += curso['name']
            virgula = ", e "
    else:
        cursos_text = 'a'
    event['cursos'] = cursos_text + ", da"

def load_config(eventfile):
    with open('data/'+eventfile+'.json','r') as config:
        event = json.load(config)
        date = fix_date('date', datetime.today()+timedelta(days=60),event)
        event['ano'] = date.year
        event['mes'] = date.month
        event['dia'] = date.day
        event['institution'].setdefault('short_name',event['institution']['long_name'])
        if event['institution'].setdefault('diretorio',''):
            event['institution']['artigo'] = 'o'
            event['institution']['diretorio'] += ' da '
        else:
            event['institution']['artigo'] = 'a'
        if event['institution'].get('local_map',None):
            event['local_map'] = """
                <div id="local_map">
                    <h4>Mapa da {institution[short_name]}</h4>
                    <img src="images/{institution[local_map]}" alt="{institution[short_name]}" class="photo"/>
                </div>""".format(**event)
        else:
            event['local_map'] = ''

        fix_date('callForPapers:start',date-timedelta(days=30),event)
        fix_date('callForPapers:deadline',date-timedelta(days=15),event)
        ddate = event['callForPapers']['deadline']
        fix_date('callForPapers:notification',ddate+timedelta(days=3),event)
        inscricoes(event)
        texto_cursos(event)
    return event

def create_CNAME(event):
    with open('CNAME','w') as cname:
        cname.write('{id}.tchelinux.org'.format(**event))

def include(filename,**kargs):
    print(include_file(filename).format(**kargs),end='',file=indexpage)

def process_schedule(event, lectures):
    labels = {
        "all":'<span class="label label-info">Todo o Público</span>',
        "Principiante":'<span class="label label-success">Principiante</span>',
        "Iniciante":'<span class="label label-success">Principiante</span>',
        "Intermediario":'<span class="label label-warning">Intermediário</span>',
        "Intermediário":'<span class="label label-warning">Intermediário</span>',
        "Avancado":'<span class="label label-danger">Avançado</span>',
        "Avançado":'<span class="label label-danger">Avançado</span>'
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
    """, file=indexpage)
    rooms = event['rooms']
    roomcount = len(rooms)
    for sala in rooms:
        sala.setdefault('subject',"")
        print ("""
            <th class="schedule-slot" colspan="1" style="text-align:center">
                Sala {number}<br/>
                <small>{subject}</small>
            </th>""".format(**sala),file=indexpage)
    print('</tr>\n</thead>\n<tbody>',file=indexpage)

    template_other = """
        <tr class="schedule-other">
            <td class="schedule-time">{time}</td>
            <td class="schedule-slot" colspan="{span}" style="text-align:center">
                {title}<br/>
                {label}<br/>
                <span class="speaker">{effective_author}</span>
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
        if k == '': continue
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
            print (template_other.format(effective_author=author,
                                         time=k,span=roomcount,
                                         label=label, **kn._asdict()),
                                         file=indexpage)
        else:
            slot.sort(key=itemgetter(0))
            print('<tr class="schedule-other">',file=indexpage)
            print('<td class="schedule-time">{time}</td>'.format(time=k),file=indexpage)
            for entry in slot:
                level = entry.level.strip()
                print(template_lecture.format(**entry._asdict(),count=speech,
                                              label=labels[level if level else "all"]),
                                              file=indexpage)
                speech += 1
            print("</tr>",file=indexpage)
    print ("</tbody>\n</table>\n</div>\n</div>\n</section>",file=indexpage)

def process_abstracts(event,lectures):
    template = include_file('abstract')
    print ("""
        <section id="palestras">
            <div class="container">
                <h2 class="subtitle">Palestras</h2>
    """,file=indexpage)
    speech = 1
    for k in sorted(lectures):
        if k == '': continue
        slot = lectures[k]
        if len(slot) == 1: continue
        slot.sort(key=itemgetter(0))
        for kn in slot:
            if kn.room == '': continue
            try:
                print(template.format(**kn._asdict(),count=speech,time=k,
                                      number=event['rooms'][int(kn.room)-1]['number']),
                                      file=indexpage)
                speech += 1
            except:
                print(kn)
                print("Error reading JSON data.")
                raise Exception("Unexected error.")

    print("</div>\n</section>",file=indexpage)

def process_support(event):
    support_item = """
        <li class="apoio-item">
            <a href="{url}" title="{long_name}" class="apoio-logo apoio-link">
            <img src="images/{logo}" alt="{short_name}" class="photo"/>
            </a>
        </li>
    """
    with open('includes/support.inc','r') as f:
        data = f.read()
    sponsors = ""
    for s in event.get('sponsors',[]):
        sponsors += support_item.format(**s)
    if sponsors:
        sponsors = '<h4>Patrocinio</h4><ul class="apoio-list">{s}</ul>'.format(s=sponsors)
    support = ""
    for s in event.get('apoio',[]):
        support += support_item.format(**s)
    print(data.format(**event,sponsor_list=sponsors, support_list=support), file=indexpage)

def process_certificates(event):
    start = """
        <p>Serão fornecidos certificados digitais para os participantes
        do evento. Para obtê-los, você deverá utilizar o email fornecido
        na sua inscrição para o evento.</p>
    """
    finished = """
        <p>Obtenha seu certificado utilizando o email da inscrição no site
        <a href="https://certificados.tchelinux.org" target="_blank">https://certificados.tchelinux.org</a>.</p>
    """
    cert_text = start if event['date'] > datetime.today() else finished
    with open('includes/certificates.inc') as f:
        data = f.read().format(certificates=cert_text,**event)
    print(data,end='',file=indexpage)

def create_index_page(event, lectures):
    print('<!DOCTYPE html>\n<html>',file=indexpage)
    include('head', **event)
    print('<body>',file=indexpage)
    include('navbar', **event)
    include('page_header', **event)
    include('about', **event)
    include('subscription', **event)
    process_certificates(event)
    if lectures != None:
        process_schedule(event,lectures)
        process_abstracts(event,lectures)
    else:
        include('call4papers', **event)
    include('location', **event)
    process_support(event)
    include('footer',**event)
    include('load_scripts')
    print('</body>\n<html>',file=indexpage)

eventfile = 'config'
if len(sys.argv) > 1:
    eventfile = sys.argv[1]
event = load_config(eventfile)
lectures = load_lectures(eventfile)
create_CNAME(event)
create_index_page(event,lectures)
indexpage.close()
