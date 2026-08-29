from pathlib import Path

p = Path('index.html')
t = p.read_text(encoding='utf-8')
marker = '<!-- ABEL_DESIGN_POLISH_V1 -->'
if marker in t:
    raise SystemExit('Design polish already applied')

css = r'''
    <!-- ABEL_DESIGN_POLISH_V1 -->
    <style>
      :root {
        --abel-bg: #070b12;
        --abel-surface: rgba(15, 23, 42, 0.78);
        --abel-surface-strong: rgba(17, 24, 39, 0.94);
        --abel-border: rgba(148, 163, 184, 0.14);
        --abel-border-hover: rgba(96, 165, 250, 0.34);
        --abel-blue: #60a5fa;
        --abel-blue-soft: rgba(59, 130, 246, 0.13);
        --abel-gold: #d6ad60;
        --abel-text: #e8eef8;
        --abel-muted: #94a3b8;
        --abel-shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
      }

      html { background: var(--abel-bg); scroll-behavior: smooth; }
      body {
        background:
          radial-gradient(circle at 15% -10%, rgba(37, 99, 235, 0.14), transparent 34rem),
          radial-gradient(circle at 92% 8%, rgba(214, 173, 96, 0.07), transparent 28rem),
          linear-gradient(180deg, #080d16 0%, #070b12 44%, #060910 100%) !important;
        color: var(--abel-text);
        min-height: 100vh;
        text-rendering: optimizeLegibility;
        -webkit-font-smoothing: antialiased;
      }

      body::before {
        content: '';
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image: linear-gradient(rgba(148,163,184,.018) 1px, transparent 1px), linear-gradient(90deg, rgba(148,163,184,.018) 1px, transparent 1px);
        background-size: 34px 34px;
        mask-image: linear-gradient(to bottom, rgba(0,0,0,.55), transparent 72%);
        z-index: -1;
      }

      ::selection { background: rgba(96,165,250,.28); color: #fff; }
      * { scrollbar-width: thin; scrollbar-color: rgba(100,116,139,.55) transparent; }
      *::-webkit-scrollbar { width: 8px; height: 8px; }
      *::-webkit-scrollbar-thumb { background: rgba(100,116,139,.45); border-radius: 999px; }

      header,
      [class*="sticky"][class*="top-0"] {
        backdrop-filter: blur(18px) saturate(135%);
        -webkit-backdrop-filter: blur(18px) saturate(135%);
        border-bottom-color: rgba(148,163,184,.11) !important;
      }

      main { animation: abelFadeIn .28s ease-out both; }
      @keyframes abelFadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }

      [class*="rounded-xl"], [class*="rounded-2xl"] {
        border-color: var(--abel-border) !important;
      }

      [class*="bg-slate-900"], [class*="bg-gray-900"], [class*="bg-zinc-900"] {
        background-color: var(--abel-surface-strong) !important;
      }

      [class*="bg-slate-800"], [class*="bg-gray-800"], [class*="bg-zinc-800"] {
        background-color: var(--abel-surface) !important;
      }

      .shadow, .shadow-md, .shadow-lg, .shadow-xl, .shadow-2xl {
        box-shadow: var(--abel-shadow) !important;
      }

      button, [role="button"] {
        transition: transform .16s ease, border-color .16s ease, background-color .16s ease, box-shadow .16s ease, color .16s ease;
      }
      button:hover:not(:disabled), [role="button"]:hover { transform: translateY(-1px); }
      button:active:not(:disabled), [role="button"]:active { transform: translateY(0) scale(.985); }
      button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible {
        outline: 2px solid rgba(96,165,250,.7);
        outline-offset: 2px;
      }

      input, select, textarea {
        border-color: rgba(148,163,184,.18) !important;
        background-color: rgba(15,23,42,.72) !important;
        color: #e5edf8 !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,.015);
        transition: border-color .16s ease, box-shadow .16s ease, background-color .16s ease;
      }
      input:hover, select:hover, textarea:hover { border-color: rgba(148,163,184,.3) !important; }
      input:focus, select:focus, textarea:focus {
        border-color: rgba(96,165,250,.58) !important;
        box-shadow: 0 0 0 3px rgba(59,130,246,.10) !important;
        background-color: rgba(15,23,42,.92) !important;
      }
      input::placeholder, textarea::placeholder { color: #64748b !important; }

      table { border-collapse: separate; border-spacing: 0; }
      thead th { color: #aebdd1 !important; letter-spacing: .025em; }
      tbody tr { transition: background-color .14s ease; }
      tbody tr:hover { background: rgba(96,165,250,.035); }

      [class*="fixed"][class*="inset-0"] {
        backdrop-filter: blur(7px);
        -webkit-backdrop-filter: blur(7px);
      }

      nav button, nav a {
        white-space: nowrap;
      }

      .text-blue-400, .text-blue-300 { color: #74b4ff !important; }
      .text-amber-400, .text-yellow-400 { color: #dfbd76 !important; }

      @media (min-width: 768px) {
        main { max-width: 1600px; margin-inline: auto; }
        [class*="rounded-xl"], [class*="rounded-2xl"] { box-shadow: 0 10px 30px rgba(0,0,0,.14); }
        [class*="rounded-xl"]:hover, [class*="rounded-2xl"]:hover { border-color: rgba(148,163,184,.22) !important; }
      }

      @media (max-width: 767px) {
        body { overflow-x: hidden; }
        header { padding-top: env(safe-area-inset-top); }
        main { padding-left: 12px !important; padding-right: 12px !important; padding-bottom: calc(22px + env(safe-area-inset-bottom)); }
        nav {
          overflow-x: auto;
          overscroll-behavior-inline: contain;
          scrollbar-width: none;
          -webkit-overflow-scrolling: touch;
        }
        nav::-webkit-scrollbar { display: none; }
        nav button, nav a { min-height: 42px; }
        button { min-height: 40px; }
        input, select, textarea { font-size: 16px !important; }
        [class*="grid-cols-2"], [class*="grid-cols-3"], [class*="grid-cols-4"] { gap: .7rem !important; }
        .text-3xl { font-size: 1.55rem !important; line-height: 1.2 !important; }
        .text-2xl { font-size: 1.3rem !important; line-height: 1.25 !important; }
        [class*="p-6"] { padding: 1rem !important; }
        [class*="p-5"] { padding: .9rem !important; }
        [class*="gap-6"] { gap: 1rem !important; }
      }

      @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { scroll-behavior: auto !important; animation-duration: .01ms !important; transition-duration: .01ms !important; }
      }
    </style>
'''

needle = '</head>'
if t.count(needle) != 1:
    raise SystemExit(f'Expected one </head>, found {t.count(needle)}')
t = t.replace(needle, css + '\n</head>', 1)
p.write_text(t, encoding='utf-8')
