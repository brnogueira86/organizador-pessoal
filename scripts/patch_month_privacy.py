from pathlib import Path
p=Path("index.html")
s=p.read_text(encoding="utf-8")
marker="ABEL_MONTH_VALUE_PRIVACY_V1"
if marker in s:
    print("already patched")
    raise SystemExit(0)
old='<span style="color: ${accent}">${brl(monthTotal)}</span>'
new='''<!-- ABEL_MONTH_VALUE_PRIVACY_V1 -->
                  <span class="inline-flex items-center gap-2" style="color: ${accent}">
                    <span id="abel-month-value" aria-live="polite" data-amount="${brl(monthTotal)}">R$ ••••••</span>
                    <button type="button" onclick="window.toggleAbelMonthValue(this)" aria-label="Mostrar valor a receber" title="Mostrar valor a receber" aria-pressed="false" class="p-1.5 rounded-lg border border-[#2A313C] text-[#8A8F98] hover:text-cyan-300" style="color:inherit">
                      <i data-lucide="eye" class="w-4 h-4"></i>
                    </button>
                  </span>'''
if s.count(old)!=1: raise SystemExit("Target mismatch: "+str(s.count(old)))
s=s.replace(old,new,1)
hook='''<script>
window.toggleAbelMonthValue = function(button) {
  const amount = document.getElementById("abel-month-value");
  if (!amount) return;
  const visible = button.getAttribute("aria-pressed") === "true";
  amount.textContent = visible ? "R$ ••••••" : amount.dataset.amount;
  button.setAttribute("aria-pressed", String(!visible));
  button.setAttribute("aria-label", visible ? "Mostrar valor a receber" : "Ocultar valor a receber");
  button.setAttribute("title", visible ? "Mostrar valor a receber" : "Ocultar valor a receber");
  const icon = button.querySelector("i");
  if (icon) {
    icon.setAttribute("data-lucide", visible ? "eye" : "eye-off");
    if (window.lucide && window.lucide.createIcons) window.lucide.createIcons();
  }
};
</script>
'''
s=s.replace("</body>",hook+"</body>",1)
p.write_text(s,encoding="utf-8")
print("monthly amount privacy added")
