from pathlib import Path
import struct, zlib

ROOT = Path('.')
index = ROOT / 'index.html'
t = index.read_text(encoding='utf-8')
marker = '<!-- ABEL_PWA_V1 -->'
if marker in t:
    raise SystemExit('PWA patch already applied')

head_insert = '''    <!-- ABEL_PWA_V1 -->
    <link rel="manifest" href="manifest.webmanifest">
    <meta name="theme-color" content="#070b12">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Abel Ferreira">
'''
needle = '</head>'
if t.count(needle) != 1:
    raise SystemExit(f'Expected one </head>, found {t.count(needle)}')
t = t.replace(needle, head_insert + '\n</head>', 1)

register = '''
    <script>
      if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
          navigator.serviceWorker.register('./service-worker.js').catch(err => console.error('Service Worker:', err));
        });
      }
    </script>
'''
body_needle = '</body>'
if t.count(body_needle) != 1:
    raise SystemExit(f'Expected one </body>, found {t.count(body_needle)}')
t = t.replace(body_needle, register + '\n</body>', 1)
index.write_text(t, encoding='utf-8')

icons = ROOT / 'icons'
icons.mkdir(exist_ok=True)

def png_chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)

def save_icon(path, size, maskable=False):
    # Dark navy background with simple geometric AF mark in blue/gold.
    bg = (7, 11, 18, 255)
    blue = (96, 165, 250, 255)
    gold = (214, 173, 96, 255)
    white = (232, 238, 248, 255)
    pixels = [bytearray(bg * size) for _ in range(size)]

    def rect(x0, y0, x1, y1, color):
        x0=max(0,int(x0)); y0=max(0,int(y0)); x1=min(size,int(x1)); y1=min(size,int(y1))
        for y in range(y0,y1):
            row=pixels[y]
            for x in range(x0,x1):
                i=x*4; row[i:i+4]=bytes(color)

    pad = size * (0.18 if maskable else 0.12)
    # subtle frame
    rect(pad, pad, size-pad, pad+size*.018, blue)
    rect(pad, size-pad-size*.018, size-pad, size-pad, gold)
    # A
    rect(size*.25, size*.30, size*.31, size*.72, white)
    rect(size*.45, size*.30, size*.51, size*.72, white)
    rect(size*.31, size*.30, size*.45, size*.36, white)
    rect(size*.31, size*.48, size*.45, size*.54, blue)
    # F
    rect(size*.57, size*.30, size*.63, size*.72, white)
    rect(size*.63, size*.30, size*.78, size*.36, gold)
    rect(size*.63, size*.48, size*.75, size*.54, gold)

    raw = b''.join(b'\x00' + bytes(row) for row in pixels)
    data = b'\x89PNG\r\n\x1a\n'
    data += png_chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
    data += png_chunk(b'IDAT', zlib.compress(raw, 9))
    data += png_chunk(b'IEND', b'')
    path.write_bytes(data)

save_icon(icons/'icon-192.png', 192)
save_icon(icons/'icon-512.png', 512)
save_icon(icons/'icon-maskable-512.png', 512, True)
