from pathlib import Path
import re

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Remove qualquer link TRAINER que tenha sido inserido dentro do template repetido do menu.
s = re.sub(r'<!-- ABEL_TRAINER_NAV_V[12] --><a href="\./trainer\.html"[^>]*><span aria-hidden="true">⚡</span><span>TRAINER</span></a>', '', s)

needle = 'navContainer.innerHTML = TABS.map(t => {'
replacement = '''navContainer.innerHTML = `<!-- ABEL_TRAINER_NAV_V3 --><a href="./trainer.html" class="flex items-center gap-2 px-4 py-3 text-xs tracking-[0.12em] whitespace-nowrap text-[#47E6FF] hover:text-white transition-colors shrink-0" title="Trainer"><span aria-hidden="true">⚡</span><span>TRAINER</span></a>` + TABS.map(t => {'''

if needle not in s:
    raise SystemExit('Renderizador do menu não encontrado')

s = s.replace(needle, replacement, 1)
p.write_text(s, encoding='utf-8')
print('Trainer corrigido para aparecer uma única vez no menu')
