from pathlib import Path
import csv, json, re, collections
ROOT=Path(__file__).resolve().parents[1]/'guia'
META={
'H1':('Circuitos eléctricos y electrónica','h1','openstax,electronics,digital',22),
'H2':('Arquitectura de computadoras y su organización','h2','intel,architecture',22),
'H3':('Sistemas embebidos','h3','avr,arduino,sensors',27),
'H4':('Automatización y control de procesos','h4','control,signals,pid',29),
'R1':('Diseño de redes','r1','rfc8200,rfc4632,networks,vlan',27),
'R2':('Administración de redes','r2','rfc2131,rfc1034,rfc9293,networks',32),
'R3':('Seguridad y evaluación en redes','r3','nistsecurity,owasp,aes,tls',41),
'S1':('Ingeniería de software','s1','scrum,swebok',32),
'S2':('Programación y software base','s2','ostep,cppreference,compiler',26),
'S3':('Manejo de datos y algoritmos','s3','algorithms,postgres,ai',42),
'L1':('Comprensión lectora: ámbito de estudio','l1','ceneval,reading',12),
'L2':('Comprensión lectora: ámbito literario','l2','ceneval,reading',12),
'L3':('Comprensión lectora: participación social','l3','ceneval,reading',6),
'E1':('Redacción indirecta: ámbito de estudio','e1','rae,writing',15),
'E2':('Redacción indirecta: participación social','e2','rae,writing',15)}
def tex(s):
 parts=re.split(r'(\\\(.*?\\\))',s)
 def esc(x):
  return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','\\':r'\textbackslash{}'}.get(c,c) for c in x)
 return ''.join(p if p.startswith('\\(') else esc(p) for p in parts)
rows=[]
for f in sorted((ROOT/'datos').glob('*.tsv')):
 for n,line in enumerate(f.read_text().splitlines(),1):
  if not line.strip() or line.startswith('#'): continue
  c=line.split('|')
  assert len(c) in (8,9),(f,n,len(c),line[:70])
  group,stem,correct,w1,w2,reason,d1,d2=c[:8]
  assert group in META,(f,n,group)
  rows.append(dict(group=group,stem=stem,options=[correct,w1,w2],reasons=[reason,d1,d2],sources=c[8] if len(c)==9 else META[group][2]))
counts=collections.Counter(q['group'] for q in rows)
for g,meta in META.items(): assert counts[g]==meta[3],(g,counts[g],meta[3])
seen=set(); seq=collections.Counter(); levels=collections.Counter()
# Per-subarea quotas sum to 30/50/20 in each disciplinary area.
QUOTAS={'H1':(7,11),'H2':(7,11),'H3':(8,13),'H4':(8,15),'R1':(8,14),'R2':(10,16),'R3':(12,20),'S1':(10,16),'S2':(8,13),'S3':(12,21)}
questions=[]; solutions=[]; keys=[]
for group,meta in META.items():
 name,label,sources,expected=meta
 qs=[q for q in rows if q['group']==group]
 questions.append('\\section{'+tex(name)+'}')
 solutions.append('\\section{'+tex(name)+'}')
 if group.startswith('L'):
  questions.append('\\input{capitulos/textos-'+group.lower()+'}')
 for i,q in enumerate(qs,1):
  area=group[0]; seq[area]+=1; ident=f'{area}-{seq[area]:03d}'
  assert q['stem'] not in seen,ident
  seen.add(q['stem'])
  a,b=QUOTAS.get(group,(4,6))
  level='Fundamentos' if i<=a else ('Aplicación' if i<=a+b else 'Integración')
  levels[(area,level)]+=1
  # Rotate correct position deterministically; no fixed answer across subsections.
  k=(seq[area]*7+ord(group[0])+i//3)%3
  opts=q['options'][-k:]+q['options'][:-k] if k else q['options'][:]
  reasons=q['reasons'][-k:]+q['reasons'][:-k] if k else q['reasons'][:]
  answer='ABC'[k]
  typ=('Ordenamiento' if q['stem'].startswith('Ordene') else 'Relación de elementos' if q['stem'].startswith('Relacione') else 'Completamiento' if q['stem'].startswith('Complete') else 'Cuestionamiento directo')
  q.update(id=ident,answer=answer,level=level,type=typ,display_options=opts)
  questions.append(r'\noindent\begin{minipage}{\linewidth}\setlength{\parskip}{4pt}\reactivo{'+ident+'}{'+level+'}{'+typ+r'}\label{q:'+ident+'}\n'+tex(q['stem'])+'\n'+r'\begin{enumerate}[label=\Alph*),nosep]'+ '\n'+'\n'.join(r'\item '+tex(o) for o in opts)+'\n'+r'\end{enumerate}\end{minipage}\par\medskip')
  solutions.append(r'\subsection*{'+ident+r' \quad Respuesta '+answer+r'}\label{s:'+ident+'}\n'+r'\textbf{Razonamiento.} '+tex(q['reasons'][0])+'\n\n'+ '\n\n'.join(r'\textbf{'+ 'ABC'[j]+r') '+('Correcta. ' if j==k else 'Distractor. ')+r'}'+tex(reasons[j]) for j in range(3) if j!=k)+'\n\n'+r'\textbf{Repaso:} \hyperref[sec:'+label+']{'+tex(name)+r'}. \textbf{Fuentes:} \cite{'+q['sources']+r'}. \hyperref[q:'+ident+r']{Volver al reactivo}.\par\medskip')
  keys.append(ident+' & '+answer+r' \\')
(ROOT/'capitulos/reactivos.tex').write_text('\n\n'.join(questions))
(ROOT/'capitulos/soluciones.tex').write_text('\n\n'.join(solutions))
(ROOT/'capitulos/claves.tex').write_text('\n'.join(r'\noindent\hyperref[q:'+q['id']+']{'+q['id']+r'}\hfill\textbf{'+q['answer']+r'}\par' for q in rows))
(ROOT/'datos/reactivos.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for area in 'HRS':
 assert [levels[(area,l)] for l in ['Fundamentos','Aplicación','Integración']]==[30,50,20],(area,levels)
print('Reactivos:',len(rows),'Subáreas:',dict(counts))
print('Niveles:',dict(levels))
