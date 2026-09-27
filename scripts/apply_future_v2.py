from pathlib import Path

p=Path("index.html")
s=p.read_text(encoding="utf-8")
marker="ABEL_FUTURE_DESIGN_V2"
if marker in s:
    raise SystemExit("V2 já aplicado")

css=r"""
<!-- ABEL_FUTURE_DESIGN_V2 -->
<style>
:root{--neo-bg:#06111d;--neo-card:#0b1826;--neo-card2:#0d1c2c;--neo-line:rgba(91,214,255,.18);--neo-cyan:#49dcff;--neo-green:#43e3a3;--neo-text:#f2f7fb;--neo-muted:#8e9aaa}
html,body{background:#06111d!important}
body{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;color:var(--neo-text)!important;letter-spacing:.005em}
body:before{opacity:.22!important;background-size:28px 28px!important;background-image:linear-gradient(rgba(73,220,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(73,220,255,.035) 1px,transparent 1px)!important}
.font-serif{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif!important;font-weight:750!important;letter-spacing:-.025em!important}
header{background:linear-gradient(180deg,rgba(5,15,26,.98),rgba(6,17,29,.94))!important;border-bottom:1px solid rgba(73,220,255,.12)!important;box-shadow:0 12px 40px rgba(0,0,0,.22)}
header h1,header .font-serif{font-family:Inter,ui-sans-serif,system-ui!important;font-weight:800!important;letter-spacing:-.035em!important}
nav{background:rgba(5,15,26,.78)!important;border-color:rgba(73,220,255,.10)!important}
nav button,nav a{font-weight:750!important;letter-spacing:.10em!important}
main{position:relative}
[class*="bg-[#1B2129]"],[class*="bg-[#161B22]"],[class*="bg-[#151B23]"],[class*="bg-[#111820]"],[class*="bg-[#12171E]"],[class*="bg-[#101720]"],[class*="bg-[#0F141B]"]{background:linear-gradient(145deg,rgba(13,28,44,.94),rgba(7,18,30,.96))!important}
[class*="border-[#2A313C]"],[class*="border-[#28313C]"],[class*="border-[#2B313B]"],[class*="border-[#303844]"]{border-color:rgba(91,214,255,.16)!important}
.rounded-xl,.rounded-2xl{border-radius:20px!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.025),0 16px 42px rgba(0,0,0,.22)!important}
button{border-radius:14px!important}
input,select,textarea,.input-cls{border-radius:12px!important;background:#07131f!important;border-color:rgba(91,214,255,.16)!important}
.text-\[\#EDE6D8\]{color:#f2f7fb!important}.text-\[\#8A8F98\],.text-\[\#8A929E\]{color:#8e9aaa!important}
.text-\[\#C9A24B\],.text-\[\#D5A928\]{color:#49dcff!important}
.text-\[\#7C8FD9\],.text-\[\#5BA3D0\]{color:#68dfff!important}
.ai-border-glow{background:linear-gradient(#0b1826,#0b1826) padding-box,linear-gradient(120deg,#49dcff,#6f8cff,#43e3a3) border-box!important}
.ai-fab{background:linear-gradient(135deg,#49dcff,#6f8cff)!important;box-shadow:0 0 28px rgba(73,220,255,.28)!important}
.jarvis-hud{background:radial-gradient(circle at 50% 0%,rgba(73,220,255,.10),transparent 42%),linear-gradient(145deg,#0d1c2c,#07131f)!important}
@media(max-width:767px){
 header{padding-left:18px!important;padding-right:18px!important}
 header h1,header .font-serif{font-size:1.55rem!important;line-height:1.08!important}
 main{padding-left:14px!important;padding-right:14px!important}
 .rounded-xl,.rounded-2xl{border-radius:18px!important}
 nav button,nav a{min-height:48px!important}
}
</style>
"""
if "</head>" not in s: raise SystemExit("head não encontrado")
s=s.replace("</head>",css+"\n</head>",1)
p.write_text(s,encoding="utf-8")
print("Redesign futurista V2 aplicado")
