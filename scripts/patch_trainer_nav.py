from pathlib import Path
p=Path('index.html'); s=p.read_text(encoding='utf-8')
if 'ABEL_TRAINER_NAV_V1' in s:
 print('Trainer já está no menu'); raise SystemExit(0)
needle='LEMBRETES'
pos=s.find(needle)
if pos<0: raise SystemExit('Menu LEMBRETES não encontrado')
# Insere antes do item Lembretes, preservando toda a navegação existente.
start=s.rfind('<button',0,pos)
if start<0: start=s.rfind('<a',0,pos)
if start<0: raise SystemExit('Início do item de menu não encontrado')
link='''<!-- ABEL_TRAINER_NAV_V1 --><a href="./trainer.html" class="flex items-center gap-2 px-4 py-3 text-xs tracking-[0.12em] whitespace-nowrap text-[#47E6FF] hover:text-white transition-colors" title="Trainer"><span aria-hidden="true">⚡</span><span>TRAINER</span></a>'''
s=s[:start]+link+s[start:]
p.write_text(s,encoding='utf-8')
print('Acesso Trainer adicionado ao menu')
