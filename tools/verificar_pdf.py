from pathlib import Path
from pypdf import PdfReader
import re,json
REPO=Path(__file__).resolve().parents[1]
R=REPO/'guia'
r=PdfReader(R/'main.pdf')
texts=[p.extract_text() for p in r.pages]
aux=(R/'main.aux').read_text();log=(R/'main.log').read_text()
qs=json.loads((R/'datos/reactivos.json').read_text())
assert not re.search(r'Overfull|Missing character|Citation .+ undefined|Reference .+ undefined|LaTeX Error',log)
assert 'Warning--' not in (R/'main.blg').read_text()
# Todas las etiquetas apuntan a destinos diferentes y existentes.
dests=r.named_destinations
qanchors=[];sanchors=[]
for q in qs:
 for prefix,arr in [('q',qanchors),('s',sanchors)]:
  pattern=r'\\newlabel\{'+prefix+':'+q['id']+r'\}\{\{.*?\}\{.*?\}\{.*?\}\{([^}]+)\}'
  m=re.search(pattern,aux);assert m,(prefix,q['id'])
  a=m[1];assert a in dests,(prefix,q['id'],a)
  arr.append(a)
  pi=r.get_destination_page_number(dests[a])
  assert q['id'] in texts[pi],(prefix,q['id'],pi)
  if prefix=='q':
   part=texts[pi].split(q['id'],1)[1]
   nxt=re.search(r'\b[HRSLE]-\d{3}\b',part)
   if nxt:part=part[:nxt.start()]
   for letter in 'ABC':assert letter+')' in part,(q['id'],'opción fuera de página',letter)
assert len(set(qanchors))==360 and len(set(sanchors))==360
assert set(qanchors).isdisjoint(sanchors)
assert all('\ufffd' not in t for t in texts)
assert not r.is_encrypted
links=sum(len(p.get('/Annots').get_object()) if p.get('/Annots') else 0 for p in r.pages)
outline=[]
def visit(items):
 for item in items:
  if isinstance(item,list):visit(item)
  else:outline.append(item.title)
visit(r.outline)
report={'paginas':len(r.pages),'enlaces_pdf':links,'marcadores':len(outline),'preguntas_con_tres_opciones_en_una_pagina':360,'destinos_de_preguntas_y_soluciones_unicos':720,'compilacion':'sin errores, citas indefinidas, desbordamientos ni glifos faltantes','pdf':'texto seleccionable, sin cifrado'}
(REPO/'checks/pdf.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
