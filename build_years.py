import re,sys
B={'so':('Sold out','Ausverkauft'),'2nd':('2nd place','2. Platz'),'adv':('Advanced','Weitergekommen'),'head':('Headline show','Headliner-Show')}
C={'Köln':('Cologne','Köln'),'München':('Munich','München')}
D={
2026:[('04.10.','Rocktober','Essen-Kettwig',[]),('13.09.','Pannekaukenfest','Schwerte',[]),('30.08.','Bass &amp; Büdchen Festival','Köln',[]),('29.08.',('Private event','Private Veranstaltung'),'Dortmund',[]),('22.08.','Zeltfestival Ruhr','Bochum',[]),('04.07.','Bochum Total','Bochum',[]),('29.05.','Mayhem','Dortmund',[]),('16.05.','Herdecker Maiwoche','Herdecke',[]),('28.02.','Hüweg · Once Upon A Time','Essen',['head','so'])],
2025:[('12.12.','Bochum Soundz','Bochum',[]),('29.11.','Kulturtandem 2025','Essen',[]),('18.10.','Rocktober','Dortmund',[]),('18.10.',('Private event','Private Veranstaltung'),'',[]),('11.10.','Zirkus','Hückelhoven',[]),('27.09.','Nacht der Jugendkultur','Herdecke',[]),('13.09.','Pannekaukenfest','Schwerte',[]),('16.08.','Ruhrorter Hafenfest','Duisburg',[])],
2024:[('29.11.','Kulturtandem 2024','Duisburg',[]),('22.11.','Acoustic Jam','Düsseldorf',[]),('02.10.','Duisburger Spätschicht XXL','Duisburg',[]),('28.09.','Nacht der Jugendkultur','Herdecke',[]),('31.08.','The Aris Valentino Show','Essen',['head','so']),('27.08.','zakk Straßenfest','Düsseldorf',[]),('25.08.','Bochumer Musiksommer','Bochum',[]),('12.08.','Acoustic Jam','Düsseldorf',[]),('06.07.','Essendiese Projekt','Essen-Rüttenscheid',[]),('05.07.','Bochum Total','Bochum',[]),('05.07.','Duisburger Kirmes','Duisburg',[]),('02.07.','TUNIX Open Air','München',[]),('24.06.','Kessel-Festival','Stuttgart',[]),('18.05.','zakk','Düsseldorf',[]),('11.05.','Herdecker Maiwoche','Herdecke',[]),('10.05.','Mayhem','Dortmund',[]),('16.03.',('Warehouse Stage · online live stream','Warehouse Stage · Online-Livestream'),'Online',[]),('03.02.','The Aris Valentino Show','Essen',['head','so'])],
2023:[('03.11.','Falkenzentrum Süd','Essen',[]),('27.10.',('Open Deck Cologne Bus · Cologne Music Week','Open Deck Cologne Bus · Cologne Music Week'),'Köln',[]),('29.09.','Zirkus','Hückelhoven',[]),('24.09.','Nacht der Jugendkultur','Herdecke',[]),('05.07.',('Ruhrcomer band contest · final','Ruhrcomer Bandcontest · Finale'),'Ruhrgebiet',['2nd']),('17.06.',"Rock'n'Pop Spirit",'Düsseldorf',[]),('09.06.',('Ruhrcomer band contest · preliminary round','Ruhrcomer Bandcontest · Vorrunde'),'Ruhrgebiet',['adv']),('27.05.','Radio Dogs Festival','Ahaus',[]),('13.05.','Good Festival · Centro','Oberhausen',[]),('06.05.','Mayhem','Dortmund',[]),('28.04.',('Hüweg · support for Farbklang','Hüweg · Vorband von Farbklang'),'Essen',[]),('21.04.','Acoustic Jam','Düsseldorf',[]),('18.02.','Jetzt oder nie','Essen',[])],
2022:[('10.12.','KultOnTour','Essen',[]),('04.12.',('Citybeats final','Citybeats Finale'),'Düsseldorf',['2nd']),('28.10.','Hüweg','Essen',[])],
}
def bi(v,tag='span',cls=''):
    c=f' class="{cls}"' if cls else ''
    if isinstance(v,tuple): return f'<{tag}{c} data-en="{v[0]}" data-de="{v[1]}">{v[0]}</{tag}>'
    return f'<{tag}{c}>{v}</{tag}>'
out=['<div class="years">']
for y in sorted(D,reverse=True):
    g=D[y]; n=len(g)
    out.append(f'        <details class="year">\n          <summary><span class="y">{y}</span><span class="mono" data-en="{n} show{"s" if n>1 else ""}" data-de="{n} Show{"s" if n>1 else ""}">{n} show{"s" if n>1 else ""}</span><span class="chev" aria-hidden="true">+</span></summary>\n          <ul class="gigs">')
    for d,e,c,bs in g:
        badges=''.join(bi(B[b],'span','badge') for b in bs)
        city=bi(C[c]) if c in C else c
        out.append(f'            <li class="gig"><span class="d">{d}{str(y)[2:]}</span><span class="e">{bi(e)}{badges}</span><span class="w">{city}</span></li>')
    out.append('          </ul>\n        </details>')
out.append('      </div>')
new='\n'.join(out)
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
s2,k=re.subn(r'<div class="years">.*?\n      </div>(?=\n    </div>\n  </section>)',lambda m:new,s,count=1,flags=re.S)
assert k==1
open(p,'w',encoding='utf-8').write(s2); print('ok', sum(len(v) for v in D.values()))
