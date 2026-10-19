from pathlib import Path
p=Path("index.html")
s=p.read_text(encoding="utf-8")
marker="ABEL_NIGHT_SHIFT_PURPLE_V1"
if marker in s: raise SystemExit("already applied")
old="""              if (item.type === 'shift') return item.extra === "sim" ? '#ef4444' : '#10b981';"""
new="""              // ABEL_NIGHT_SHIFT_PURPLE_V1: turnos noturnos aparecem em roxo, inclusive extras.
              if (item.type === 'shift') {
                const start = String(item.inicio || '').slice(0, 5);
                const end = String(item.fim || '').slice(0, 5);
                const toMin = (v) => /^\\d{2}:\\d{2}$/.test(v) ? Number(v.slice(0,2))*60 + Number(v.slice(3,5)) : null;
                const a = toMin(start), b = toMin(end);
                // Considera noturno se o plantão começa a partir das 18h, antes das 6h,
                // ou atravessa a madrugada. Não classifica 07h–19h como noturno.
                const night = a !== null && (a >= 1080 || a < 360 || (b !== null && b < a));
                if (night) return '#a855f7';
                return item.extra === "sim" ? '#ef4444' : '#10b981';
              }"""
if s.count(old)!=1: raise SystemExit("dot color target mismatch")
s=s.replace(old,new,1)
old2='''<span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-red-500"></span> Plantão Extra</span>'''
new2=old2+'''
                  <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full" style="background:#a855f7"></span> Plantão Noturno</span>'''
if s.count(old2)!=1: raise SystemExit("legend target mismatch")
s=s.replace(old2,new2,1)
p.write_text(s,encoding="utf-8")
print("night shifts colored purple")
