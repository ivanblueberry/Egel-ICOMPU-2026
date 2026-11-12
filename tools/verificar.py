from pathlib import Path
import json,re,collections,math,ipaddress,sqlite3
REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'guia'
qs=json.loads((ROOT/'datos/reactivos.json').read_text())
def find(term):
 found=[q for q in qs if term in q['stem']]
 assert len(found)==1,(term,len(found))
 return found[0]
assert len(qs)==360
assert len({q['id'] for q in qs})==360
for q in qs:
 assert len(set(q['options']))==3,q['id']
 assert q['display_options']['ABC'.index(q['answer'])]==q['options'][0],q['id']
 assert len(q['reasons'])==3 and all(q['reasons']),q['id']
 assert q['sources'],q['id']
 assert len(q['stem'])>15,q['id']
# Regresiones editoriales: no prometer O(log n) al devolver k elementos;
# no inferir mayoria sin conocer el total de solicitudes.
assert 'localizar el inicio' in find('Se debe escoger una estructura')['stem'],'S-100: costo de salida no delimitado'
assert 'El registro muestra dos solicitudes pendientes' in find('Todos fueron atendidos')['options'][0],'E-029: mayoria sin total'
checks=[]
def check(term,expected):
 q=find(term); assert q['options'][0]==expected,(q['id'],q['options'][0],expected)
 checks.append(q['id'])
check('resistor de 3 kΩ',f'{12/3000*1000:g} mA')
check('6 kΩ y 3 kΩ',f'{6*3/(6+3):g} kΩ')
check('entran 8 mA',f'{8-3} mA')
check('2 kΩ arriba',f'{9*4/(2+4):g} V')
check('resistor de 100 Ω',f'{0.2**2*100:g} W')
check('R=10 kΩ',f'{10000*10e-6:g} s')
check('Rf=30 kΩ',f'{1+30/10:g}')
check('limitar un LED',f'{(5-2)/.01:g} Ω')
check('de 0 a 100 inclusive',str(math.ceil(math.log2(101))))
check('fuente de 10 V',f'{10*1/(1+1):g} V')
check('101101 binario',str(int('101101',2)))
check('16 bits de dirección',f'{2**16//1024} KiB')
check('2 millones de instrucciones',f'{2e6*3/1e9*1000:g} ms')
check('caché tarda 2 ns',f'{2+.05*80:g} ns')
check('palabra 0x12345678','0x'+(0x12345678).to_bytes(4,'little').hex()[:2].upper())
check('contiene 250',str((250+10)%256))
check('16 líneas y bloques',str(16-4-4))
check('periodo 2 ms',f'{.5/2*100:g}%')
check('recibe 1 MHz',f'{1000/1e6*1000:g} ms')
check('Kp=3',f'{3*2} unidades de salida')
check('4–20 mA',f'{(12-4)/(20-4)*100:g} °C')
check('muestrea a 100 Hz',f'{1/100*1000:g} ms')
check('media móvil de tres',f'{sum([3,6,9])/3:g}')
check('al menos 50 hosts','/'+str(32-math.ceil(math.log2(50+2))))
n=ipaddress.ip_network('192.168.10.77/26',strict=False)
check('red de 192.168.10.77',str(n.network_address))
check('cuál es el broadcast',str(n.broadcast_address))
check('tiene una subred IPv4 /29',str(ipaddress.ip_network('192.0.2.0/29').num_addresses-2))
check('resumirse exactamente',str(list(ipaddress.collapse_addresses([ipaddress.ip_network('10.0.0.0/24'),ipaddress.ip_network('10.0.1.0/24')]))[0]))
check('10 millones de bits',f'{10e6/100e6:g} s')
check('promedio 250 Mbit/s',f'{250/1000*100:g}%')
check('990 de 1000',f'{990/1000*100:g}%')
check('200 horas a 300',f'{200*300+10000} pesos')
check('otra de 3 depende',f'{5+3} días')
x=3;x+=2;x*=4
check('int x=3',str(x))
check('s=0; para i=1',str(sum(range(1,5))))
check('FCFS ejecuta A','3 ms')
check('Round robin usa quantum','En t=3 ms')
check('página mide 4 KiB',str(int(math.log2(4*1024))))
check('pila vacía recibe','7')
check('Una cola recibe','B')
check('1024 elementos',str(int(math.log2(1024))))
check('Cuánto vale factorial(4)',str(math.factorial(4)))
# SQL ejecutable: las operaciones usadas tienen semántica compartida aquí
# por SQLite y PostgreSQL. No se simula aislamiento de PostgreSQL en SQLite.
db=sqlite3.connect(':memory:')
db.executescript('CREATE TABLE v(id INTEGER,importe INTEGER); INSERT INTO v VALUES(1,10),(2,20),(3,NULL); CREATE TABLE clientes(id INTEGER PRIMARY KEY); INSERT INTO clientes VALUES(1),(2); CREATE TABLE pedidos(id INTEGER,cliente INTEGER); INSERT INTO pedidos VALUES(1,1),(2,1),(3,1); CREATE TABLE ventas(cliente TEXT,total INTEGER); INSERT INTO ventas VALUES("A",60),("A",50),("B",20);')
check('V(id,importe)',str(db.execute('SELECT SUM(importe) FROM v').fetchone()[0]))
check('Clientes contiene dos filas',str(db.execute('SELECT COUNT(*) FROM clientes c JOIN pedidos p ON c.id=p.cliente').fetchone()[0]))
assert db.execute('SELECT cliente,SUM(total) FROM ventas GROUP BY cliente HAVING SUM(total)>100').fetchall()==[('A',110)]
assert db.execute('SELECT COUNT(*) FROM v WHERE importe IS NULL').fetchone()[0]==1
check('90 de 100 ejemplos',f'{90/100*100:g}%')
check('20 positivos reales',f'{15/20*100:g}%')
# Identidades booleanas y complemento a dos.
for a in [0,1]:
 for b in [0,1]:
  assert (not(a and b))==((not a)or(not b))
  assert ((a and not b)or(a and b))==bool(a)
assert ((~13+1)&255)==243 and 243-256==-13
assert math.isclose(1/(.4+.6/4),1.8181818181818181)
assert math.isclose(5/1024*1000,4.8828125)
assert math.isclose(10/9600*1000,1.0416666666666667)
assert math.isclose(1-math.exp(-1),.6321205588285577)
assert (16/20-12/20)*100>19.999
# El esquema del divisor incluye fuente y no une ambos polos por un cable.
hardware=(ROOT/'capitulos/hardware.tex').read_text()
assert r'\draw (0,0.6) circle' in hardware
assert r'\draw (0,0)--(0,1.7)' not in hardware
# Bibliografía y enlaces internos.
bib=(ROOT/'referencias.bib').read_text()
bibkeys=set(re.findall(r'@\w+\{([^,]+),',bib))
for q in qs:
 assert set(q['sources'].split(','))<=bibkeys,(q['id'],q['sources'])
tex='\n'.join(p.read_text() for p in (ROOT/'capitulos').glob('*.tex'))
for group in ['h1','h2','h3','h4','r1','r2','r3','s1','s2','s3','l1','l2','l3','e1','e2']:
 assert '\\label{sec:'+group+'}' in tex,group
for q in qs:
 assert '\\label{q:'+q['id']+'}' in tex and '\\label{s:'+q['id']+'}' in tex,q['id']
for p in (ROOT/'capitulos').glob('*.tex'):
 for cite in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',p.read_text()):
  assert set(cite.split(','))<=bibkeys,(p,cite)
report={'reactivos':len(qs),'por_grupo':dict(collections.Counter(q['group'] for q in qs)),'distribucion_claves':dict(collections.Counter(q['answer'] for q in qs)),'calculos_vinculados_a_reactivos':len(checks),'ids_calculados':checks,'sql':'SUM, IS NULL, JOIN y GROUP BY/HAVING comprobados','regresiones_editoriales':['S-100 costo de devolver resultados delimitado','E-029 no inferir mayoría sin total'],'estructura':'360 IDs únicos, tres opciones distintas, solución y fuente para cada reactivo; enlaces y claves consistentes'}
(REPO/'checks/comprobaciones.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
