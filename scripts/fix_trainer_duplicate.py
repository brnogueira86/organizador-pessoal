from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove qualquer acesso Trainer inserido anteriormente no menu.
s = re.sub(r'<!--\s*ABEL_TRAINER_NAV_V1\s*-->\s*<a\b[^>]*href=["\']\./trainer\.html["\'][^>]*>.*?</a>', '', s, flags=re.I|re.S)
s = re.sub(r'<a\b[^>]*href=["\']\./trainer\.html["\'][^>]*>.*?</a>', '', s, flags=re.I|re.S)

# Insere uma única aba Trainer antes de LEMBRETES.
needle = 'LEMBRETES'
pos = s.find(needle)
if pos < 0:
    raise SystemExit('Menu LEMBRETES não encontrado')
start = s.rfind('<button', 0, pos)
if start < 0:
    start = s.rfind('<a', 0, pos)
if start < 0:
    raise SystemExit('Início do item Lembretes não encontrado')

link = '''<!-- ABEL_TRAINER_NAV_V2 --><a href="./trainer.html" class="flex items-center gap-2 px-4 py-3 text-xs tracking-[0.12em] whitespace-nowrap text-[#47E6FF] hover:text-white transition-colors" title="Trainer"><span aria-hidden="true">⚡</span><span>TRAINER</span></a>'''
s = s[:start] + link + s[start:]

p.write_text(s, encoding='utf-8')
print('Menu corrigido: apenas uma aba Trainer.')
