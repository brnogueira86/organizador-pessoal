from pathlib import Path

p = Path('index.html')
t = p.read_text(encoding='utf-8')
marker = '// ABEL_EXTRA_SHIFT_UNITS_V1'
if marker in t:
    raise SystemExit('Extra shift units patch already applied')

needle = '''          const monthShiftsNormal = monthShifts.filter(s => s.extra !== "sim");
          const monthShiftsExtra = monthShifts.filter(s => s.extra === "sim");
          const monthTotal = monthShifts.reduce((sum, s) => sum + Number(s.valor || 0), 0);'''
replacement = '''          const monthShiftsNormal = monthShifts.filter(s => s.extra !== "sim");
          const monthShiftsExtra = monthShifts.filter(s => s.extra === "sim");
          // ABEL_EXTRA_SHIFT_UNITS_V1
          const shiftHours = (s) => {
            const [ih, im] = String(s.inicio || "00:00").split(":").map(Number);
            const [fh, fm] = String(s.fim || "00:00").split(":").map(Number);
            let minutes = (fh * 60 + fm) - (ih * 60 + im);
            if (minutes <= 0) minutes += 24 * 60;
            return minutes / 60;
          };
          const extraShiftUnits = monthShiftsExtra.reduce((sum, s) => sum + (shiftHours(s) / 12), 0);
          const formatShiftUnits = (n) => Number.isInteger(n) ? String(n) : String(Number(n.toFixed(2))).replace(".", ",");
          const monthTotal = monthShifts.reduce((sum, s) => sum + Number(s.valor || 0), 0);'''

if t.count(needle) != 1:
    raise SystemExit(f'Expected summary calculation block once, found {t.count(needle)}')
t = t.replace(needle, replacement, 1)

old = '''${monthShiftsNormal.length} plantão(ões) · ${monthShiftsExtra.length} extra(s) · ${monthAppointments.length} compromisso(s)'''
new = '''${monthShiftsNormal.length} plantão(ões) · ${formatShiftUnits(extraShiftUnits)} extra(s) · ${monthAppointments.length} compromisso(s)'''
if t.count(old) != 1:
    raise SystemExit(f'Expected visible extra counter once, found {t.count(old)}')
t = t.replace(old, new, 1)

p.write_text(t, encoding='utf-8')
