from pathlib import Path

p = Path('index.html')
t = p.read_text(encoding='utf-8')

old_remove = '''        window.removeShift = (id) => {
          const s = state.shifts.find(s => s.id === id);
          if (!s) return;
          if (s.serieId) {
            const excluirSerie = window.confirm("Este plantão faz parte de uma série recorrente.\\n\\nOK = excluir toda a série\\nCancelar = excluir somente este plantão");
            state.shifts = excluirSerie
              ? state.shifts.filter(item => item.serieId !== s.serieId)
              : state.shifts.filter(item => item.id !== id);
          } else {
            state.shifts = state.shifts.filter(item => item.id !== id);
          }
          persistData();
          render();
        };'''

new_remove = '''        window.removeShift = (id) => {
          const s = state.shifts.find(s => s.id === id);
          if (!s) return;
          if (s.serieId) {
            const excluirSerie = window.confirm("Este plantão faz parte de uma série recorrente.\\n\\nOK = excluir toda a série\\nCancelar = escolher outra opção");
            if (excluirSerie) {
              state.shifts = state.shifts.filter(item => item.serieId !== s.serieId);
            } else {
              const excluirSomenteEste = window.confirm("Excluir somente este plantão da série?\\n\\nOK = excluir somente este\\nCancelar = não excluir nada");
              if (!excluirSomenteEste) return;
              state.shifts = state.shifts.filter(item => item.id !== id);
            }
          } else {
            if (!window.confirm("Excluir este plantão?")) return;
            state.shifts = state.shifts.filter(item => item.id !== id);
          }
          persistData();
          render();
        };'''

if t.count(old_remove) != 1:
    raise SystemExit('current removeShift block not found exactly once')
t = t.replace(old_remove, new_remove, 1)

old_start = '''            const dataInicial = data || state.selectedDay;

if (repetir === "nenhum" || !repetirAte) {'''
new_start = '''            const dataInicial = data || state.selectedDay;

            if (repetir !== "nenhum" && repetirAte && repetirAte < dataInicial) {
              window.alert("A data final da repetição não pode ser anterior à data inicial.");
              return;
            }

if (repetir === "nenhum" || !repetirAte) {'''
if t.count(old_start) != 1:
    raise SystemExit('recurrence start block not found exactly once')
t = t.replace(old_start, new_start, 1)

old_loop_start = '''    let atual = new Date(dataInicial + "T12:00:00");
    const limite = new Date(repetirAte + "T12:00:00");

    while (atual <= limite) {'''
new_loop_start = '''    let atual = new Date(dataInicial + "T12:00:00");
    const limite = new Date(repetirAte + "T12:00:00");
    const diaBaseMensal = atual.getDate();

    while (atual <= limite) {'''
if t.count(old_loop_start) != 1:
    raise SystemExit('recurrence loop start not found exactly once')
t = t.replace(old_loop_start, new_loop_start, 1)

old_month = '''        } else if (repetir === "mensal") {
            atual.setMonth(atual.getMonth() + 1);
        } else {'''
new_month = '''        } else if (repetir === "mensal") {
            const primeiroDoProximoMes = new Date(atual.getFullYear(), atual.getMonth() + 1, 1, 12, 0, 0);
            const ultimoDiaDoProximoMes = new Date(
              primeiroDoProximoMes.getFullYear(),
              primeiroDoProximoMes.getMonth() + 1,
              0,
              12,
              0,
              0
            ).getDate();
            atual = new Date(
              primeiroDoProximoMes.getFullYear(),
              primeiroDoProximoMes.getMonth(),
              Math.min(diaBaseMensal, ultimoDiaDoProximoMes),
              12,
              0,
              0
            );
        } else {'''
if t.count(old_month) != 1:
    raise SystemExit('monthly recurrence block not found exactly once')
t = t.replace(old_month, new_month, 1)

p.write_text(t, encoding='utf-8')
