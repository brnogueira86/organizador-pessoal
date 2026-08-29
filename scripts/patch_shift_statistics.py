from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

if 'ABEL_SHIFT_STATS_V1' in s:
    print('Painel estatístico já aplicado.')
    raise SystemExit(0)

needle = '${monthShiftsNormal.length} plantão(ões) · ${formatShiftUnits(extraShiftUnits)} extra(s) · ${monthAppointments.length} compromisso(s)'
pos = s.find(needle)
if pos < 0:
    raise SystemExit('Resumo mensal não encontrado')

# Insert calculation block before monthTotal, reusing the existing shiftHours helper.
calc_needle = 'const monthTotal = monthShifts.reduce((sum, s) => sum + Number(s.valor || 0), 0);'
calc = '''// ABEL_SHIFT_STATS_V1\nconst todayShiftStats = new Date();\ntodayShiftStats.setHours(23, 59, 59, 999);\nconst completedShifts = state.shifts.filter(s => {\n  if (!s.data) return false;\n  const d = new Date(`${s.data}T00:00:00`);\n  return !Number.isNaN(d.getTime()) && d <= todayShiftStats;\n});\nconst completedShiftHours = completedShifts.reduce((sum, s) => sum + shiftHours(s), 0);\nconst completedExtraUnits = completedShifts\n  .filter(s => s.extra === "sim")\n  .reduce((sum, s) => sum + (shiftHours(s) / 12), 0);\nconst completedMonths = completedShifts.reduce((acc, s) => {\n  const key = String(s.data || "").slice(0, 7);\n  if (!key) return acc;\n  if (!acc[key]) acc[key] = { shifts: 0, hours: 0 };\n  acc[key].shifts += 1;\n  acc[key].hours += shiftHours(s);\n  return acc;\n}, {});\nconst completedMonthEntries = Object.entries(completedMonths);\nconst activeMonthCount = completedMonthEntries.length;\nconst avgShiftsPerMonth = activeMonthCount ? completedShifts.length / activeMonthCount : 0;\nconst avgHoursPerMonth = activeMonthCount ? completedShiftHours / activeMonthCount : 0;\nconst busiestMonthEntry = completedMonthEntries.sort((a, b) => b[1].shifts - a[1].shifts)[0];\nconst formatStatNumber = (n) => Number.isInteger(n) ? String(n) : String(Number(n.toFixed(1))).replace(".", ",");\nconst formatMonthLabel = (key) => {\n  if (!key) return "—";\n  const [yy, mm] = key.split("-").map(Number);\n  return new Intl.DateTimeFormat("pt-BR", { month: "short", year: "numeric" }).format(new Date(yy, mm - 1, 1)).replace(" de ", "/");\n};\n''' + calc_needle
if calc_needle not in s:
    raise SystemExit('Ponto de cálculo não encontrado')
s = s.replace(calc_needle, calc, 1)

# Insert stats panel immediately after the monthly summary container by locating its nearby closing structure.
# Use a robust anchor: the summary text followed by the monthTotal currency expression; then find the next </div> pair.
summary_pos = s.find(needle)
end1 = s.find('</div>', summary_pos)
if end1 < 0: raise SystemExit('Fechamento do resumo não encontrado')
insert_at = end1 + len('</div>')

panel = '''\n<div class="mt-4 pt-4 border-t border-[#2A313B]">\n  <div class="flex items-center justify-between gap-3 mb-3">\n    <div>\n      <div class="text-[11px] uppercase tracking-[0.16em] text-[#D5A928] font-semibold">Estatísticas de Plantões</div>\n      <div class="text-[11px] text-[#747C88] mt-1">Histórico de plantões realizados até hoje</div>\n    </div>\n  </div>\n  <div class="grid grid-cols-2 md:grid-cols-3 gap-2.5">\n    <div class="rounded-xl border border-[#28313C] bg-[#111820] p-3">\n      <div class="text-xl font-semibold text-[#F2F0EA]">${completedShifts.length}</div>\n      <div class="text-[11px] text-[#8A929E] mt-1">Plantões realizados</div>\n    </div>\n    <div class="rounded-xl border border-[#28313C] bg-[#111820] p-3">\n      <div class="text-xl font-semibold text-[#F2F0EA]">${formatStatNumber(completedShiftHours)} h</div>\n      <div class="text-[11px] text-[#8A929E] mt-1">Horas trabalhadas</div>\n    </div>\n    <div class="rounded-xl border border-[#28313C] bg-[#111820] p-3">\n      <div class="text-xl font-semibold text-[#F2F0EA]">${formatShiftUnits(completedExtraUnits)}</div>\n      <div class="text-[11px] text-[#8A929E] mt-1">Extras realizados</div>\n    </div>\n    <div class="rounded-xl border border-[#28313C] bg-[#111820] p-3">\n      <div class="text-xl font-semibold text-[#F2F0EA]">${formatStatNumber(avgShiftsPerMonth)}</div>\n      <div class="text-[11px] text-[#8A929E] mt-1">Média de plantões/mês</div>\n    </div>\n    <div class="rounded-xl border border-[#28313C] bg-[#111820] p-3">\n      <div class="text-xl font-semibold text-[#F2F0EA]">${formatStatNumber(avgHoursPerMonth)} h</div>\n      <div class="text-[11px] text-[#8A929E] mt-1">Média de horas/mês</div>\n    </div>\n    <div class="rounded-xl border border-[#28313C] bg-[#111820] p-3">\n      <div class="text-base font-semibold text-[#F2F0EA]">${busiestMonthEntry ? formatMonthLabel(busiestMonthEntry[0]) : "—"}</div>\n      <div class="text-[11px] text-[#8A929E] mt-1">Mês com mais plantões${busiestMonthEntry ? ` · ${busiestMonthEntry[1].shifts}` : ""}</div>\n    </div>\n  </div>\n</div>'''
s = s[:insert_at] + panel + s[insert_at:]
p.write_text(s, encoding='utf-8')
print('Painel estatístico aplicado.')
