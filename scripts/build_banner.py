#!/usr/bin/env python3
"""Generate the animated profile hero banners (dark.svg / light.svg).

Pure SVG + SMIL, no JavaScript. Both themes come from the same layout code so
they never drift apart.

    python3 scripts/build_banner.py                   # procedural ASCII bust
    python3 scripts/build_banner.py --photo me.jpg    # ASCII from a real photo (needs Pillow)
"""
import argparse
import math
import os
import random

W, H, R = 1180, 610, 28

THEMES = {
    "dark": dict(
        bg="#030712", panel="#0F172A", text="#E2E8F0", muted="#64748B", soft="#94A3B8",
        a1="#7C3AED", a2="#22D3EE", a3="#10B981",
        key="#A78BFA", string="#34D399", punct="#475569",
        hair="rgba(255,255,255,0.08)", grid="rgba(148,163,184,0.07)",
        blob=0.42, panel_alpha=0.66, sheen=0.07, scan="rgba(2,6,23,0.55)",
        pill_fill="#0B1222", shadow=0.55, noise=0.05, particle=0.9,
    ),
    "light": dict(
        bg="#FFFFFF", panel="#F8FAFC", text="#0F172A", muted="#64748B", soft="#475569",
        a1="#2563EB", a2="#06B6D4", a3="#10B981",
        key="#2563EB", string="#059669", punct="#94A3B8",
        hair="rgba(15,23,42,0.09)", grid="rgba(15,23,42,0.05)",
        blob=0.20, panel_alpha=0.78, sheen=0.55, scan="rgba(255,255,255,0.55)",
        pill_fill="#FFFFFF", shadow=0.10, noise=0.025, particle=0.55,
    ),
}

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono','DejaVu Sans Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
ADV = 0.6  # monospace advance in em; textLength pins every typed line to this grid

# ── layout ────────────────────────────────────────────────────────────────
LX, LY, LW, LH = 28, 28, 420, 554          # left panel (≈38%)
RX, RY, RW, RH = 468, 28, 684, 554         # terminal
COLS, ROWS = 52, 36
AX, AY, AW, AH = 48, 86, 380, 432          # ascii box
LINE = AH / ROWS
TX = RX + 32                               # terminal text x

SUBTITLES = ["RPA Engineer", "Automation Developer", "Full Stack Builder", "Enterprise Web Automation"]
SKILLS = ["Java", "Python", "PostgreSQL", "AutomationEdge", "Git", "REST APIs"]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


# ── ASCII portrait ────────────────────────────────────────────────────────
RAMP = " .:-=+*#%@"


def _hash(c, r):
    return (math.sin(c * 12.9898 + r * 78.233) * 43758.5453) % 1.0


def procedural_ascii():
    """Shaded head-and-shoulders bust with a rim light — reads as a portrait at 52 columns."""
    L = (-0.5, -0.55, 0.67)

    def ellipsoid(dx, dy):
        nz = math.sqrt(max(0.0, 1 - dx * dx - dy * dy))
        lit = max(0.0, dx * L[0] + dy * L[1] + nz * L[2])
        rim = (1 - nz) ** 3 * max(0.0, dx) * 1.6
        return min(1.0, 0.16 + 0.8 * lit + rim)

    rows = []
    for r in range(ROWS):
        line = []
        for c in range(COLS):
            X = (c + 0.5) / COLS * AW - AW / 2
            Y = (r + 0.5) / ROWS * AH - AH / 2
            b = 0.0
            # torso
            sx, sy = X / 185, (Y - 272) / 200
            if sx * sx + sy * sy < 1:
                b = ellipsoid(sx, sy) * 0.85
                v = 36 - (Y - 72) * 0.5                             # v-neck
                if abs(X) < v:
                    b = 0.3 + 0.3 * max(0.0, -X / 40)
                elif abs(X) < v + 7:
                    b = 0.97
            # neck
            if abs(X) < 34 + max(0.0, Y - 52) * 0.4 and 20 < Y < 84 and b < 0.97:
                b = max(b, 0.2 + 0.35 * max(0.0, -X / 34))
            # ears
            for ex in (-84, 84):
                if ((X - ex) / 12) ** 2 + ((Y + 42) / 22) ** 2 < 1:
                    b = ellipsoid((X - ex) / 12, (Y + 42) / 22) * 0.8
            # head
            hx, hy = X / 82, (Y + 50) / 100
            if hx * hx + hy * hy < 1:
                b = 0.12 + 0.72 * ellipsoid(hx, hy)
                for ex in (-30, 30):                                # soft eye sockets
                    if ((X - ex) / 16) ** 2 + ((Y + 44) / 7) ** 2 < 1:
                        b *= 0.35
                if abs(X) < 22 and 11 < Y < 23:                      # mouth line
                    b *= 0.45
            # hair
            gx, gy = X / 90, (Y + 64) / 102
            if gx * gx + gy * gy < 1 and Y < -112 + 0.02 * X * X:
                b = -1.0
            # orbit ring + dust
            d = math.hypot(X, (Y + 20) * 0.95)
            if b == 0 and abs(d - 168) < 4 and _hash(c, r) > 0.3:
                b = 0.14
            if b == 0 and _hash(c * 3, r * 7) > 0.985:
                b = 0.12
            if b < 0:                                               # hair strands
                line.append("@" if _hash(c, r) > 0.8 else ("/" if X < 0 else "\\"))
            else:
                line.append(RAMP[0] if b == 0 else RAMP[min(9, max(1, int(b * 9.99)))])
        rows.append("".join(line))
    return rows


def photo_ascii(path):
    from PIL import Image, ImageOps
    img = ImageOps.grayscale(Image.open(path))
    img = ImageOps.fit(img, (COLS, ROWS), centering=(0.5, 0.35))
    img = ImageOps.autocontrast(img, cutoff=2)
    px = img.load()
    return ["".join(RAMP[int(px[c, r] / 256 * len(RAMP))] for c in range(COLS)) for r in range(ROWS)]


# ── SMIL helpers ──────────────────────────────────────────────────────────
def discrete(events, total):
    """events: [(t, value)] sorted; returns values/keyTimes strings over `total` secs."""
    ev = []
    for t, v in events:
        if ev and abs(ev[-1][0] - t) < 1e-6:
            ev[-1] = (t, v)
        else:
            ev.append((t, v))
    if ev[0][0] > 0:
        ev.insert(0, (0.0, ev[0][1]))
    vals = ";".join(f(v) for _, v in ev)
    kts = ";".join(f"{t / total:.4f}" for t, _ in ev)
    return vals, kts


def typed(uid, x, y, text, size, begin, step, fill, weight=400, cursor=True, theme=None, hold_cursor=0.6):
    """Text typed char-by-char via a discretely-growing clip rect plus a block cursor."""
    n = len(text)
    adv = size * ADV
    width = n * adv
    dur = (n + 1) * step
    vals = ";".join(f(k * adv) for k in range(n + 1))
    kts = ";".join(f"{k / (n + 1):.4f}" for k in range(n + 1))
    out = [
        f'<clipPath id="{uid}"><rect x="{f(x)}" y="{f(y - size)}" height="{f(size * 1.4)}" width="0">'
        f'<animate attributeName="width" calcMode="discrete" values="{vals}" keyTimes="{kts}" '
        f'dur="{f(dur)}s" begin="{f(begin)}s" fill="freeze"/></rect></clipPath>',
        f'<text x="{f(x)}" y="{f(y)}" font-family="{MONO}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" textLength="{f(width)}" lengthAdjust="spacingAndGlyphs" clip-path="url(#{uid})" '
        f'xml:space="preserve">{esc(text)}</text>',
    ]
    if cursor:
        cx_vals = ";".join(f(x + k * adv + 2) for k in range(n + 1))
        out.append(
            f'<rect x="{f(x + 2)}" y="{f(y - size * 0.82)}" width="{f(adv * 0.9)}" height="{f(size * 0.98)}" '
            f'rx="1.5" fill="{theme["a2"]}" opacity="0">'
            f'<animate attributeName="x" calcMode="discrete" values="{cx_vals}" keyTimes="{kts}" '
            f'dur="{f(dur)}s" begin="{f(begin)}s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.9" begin="{f(begin)}s" end="{f(begin + dur + hold_cursor)}s"/>'
            f'</rect>'
        )
    return "\n".join(out)


def reveal(begin, dx=-10, dur=0.45):
    return (
        f'<animate attributeName="opacity" from="0" to="1" begin="{f(begin)}s" dur="{f(dur)}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="{dx} 0" to="0 0" '
        f'begin="{f(begin)}s" dur="{f(dur)}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.2 0.8 0.2 1"/>'
    )


BLINK = '<animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1.06s" repeatCount="indefinite"/>'


# ── build ─────────────────────────────────────────────────────────────────
def build(name, t, ascii_rows):
    rnd = random.Random(7)
    o = []
    a = o.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-labelledby="title desc">')
    a('<title id="title">Ameya Ajit Kabir — Automation Developer &amp; RPA Engineer</title>')
    a('<desc id="desc">Animated terminal-style profile banner: ASCII portrait, typed introduction, '
      'location Pune, India, company AutomationEdge, and skills Java, Python, PostgreSQL, AutomationEdge, Git.</desc>')

    # styles (hover only works when the SVG is opened directly — GitHub embeds it as <img>)
    a(f'''<style>
  .pill {{ transition: transform .25s cubic-bezier(.2,.8,.2,1), filter .25s; transform-box: fill-box; transform-origin: center; cursor: default; }}
  .pill:hover {{ transform: scale(1.08); filter: drop-shadow(0 0 10px {t["a2"]}); }}
</style>''')

    # ── defs
    a("<defs>")
    a(f'<clipPath id="card"><rect width="{W}" height="{H}" rx="{R}"/></clipPath>')
    a(f'<clipPath id="clipL"><rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="20"/></clipPath>')
    a(f'<clipPath id="clipR"><rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="20"/></clipPath>')
    a(f'<clipPath id="clipA"><rect x="{AX - 8}" y="{AY - 12}" width="{AW + 16}" height="{AH + 20}" rx="10"/></clipPath>')

    # moving accent gradient (name, ascii, borders)
    a(f'<linearGradient id="accent" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="560" y2="0" spreadMethod="reflect">'
      f'<stop offset="0" stop-color="{t["a1"]}"/><stop offset="0.5" stop-color="{t["a2"]}"/>'
      f'<stop offset="1" stop-color="{t["a3"]}"/>'
      f'<animateTransform attributeName="gradientTransform" type="translate" values="0 0;560 0;0 0" '
      f'dur="9s" repeatCount="indefinite"/></linearGradient>')
    a(f'<linearGradient id="asciiGrad" gradientUnits="userSpaceOnUse" x1="{AX}" y1="{AY}" x2="{AX + AW}" y2="{AY + AH}" spreadMethod="reflect">'
      f'<stop offset="0" stop-color="{t["a1"]}"/><stop offset="0.5" stop-color="{t["a2"]}"/>'
      f'<stop offset="1" stop-color="{t["a3"]}"/>'
      f'<animateTransform attributeName="gradientTransform" type="translate" values="0 0;300 300;0 0" '
      f'dur="11s" repeatCount="indefinite"/></linearGradient>')
    a(f'<linearGradient id="border" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0" stop-color="{t["a1"]}"/><stop offset="0.5" stop-color="{t["a2"]}"/>'
      f'<stop offset="1" stop-color="{t["a3"]}"/></linearGradient>')
    a(f'<linearGradient id="sheen" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{t["sheen"]}"/>'
      f'<stop offset="0.35" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
    a(f'<linearGradient id="streak" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
      f'<stop offset="0.5" stop-color="#FFFFFF" stop-opacity="{0.06 if name == "dark" else 0.5}"/>'
      f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
    a(f'<linearGradient id="scanBand" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{t["a2"]}" stop-opacity="0"/>'
      f'<stop offset="0.5" stop-color="{t["a2"]}" stop-opacity="{0.18 if name == "dark" else 0.12}"/>'
      f'<stop offset="1" stop-color="{t["a2"]}" stop-opacity="0"/></linearGradient>')
    for i, col in enumerate((t["a1"], t["a2"], t["a3"])):
        a(f'<radialGradient id="blob{i}"><stop offset="0" stop-color="{col}" stop-opacity="{t["blob"]}"/>'
          f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
    a('<radialGradient id="fade" cx="0.5" cy="0.4" r="0.7"><stop offset="0" stop-color="#fff"/>'
      '<stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>')
    a(f'<mask id="gridMask"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>')
    a(f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
      f'<path d="M40 0H0V40" fill="none" stroke="{t["grid"]}" stroke-width="1"/></pattern>')
    a(f'<pattern id="scan" width="4" height="3" patternUnits="userSpaceOnUse">'
      f'<rect width="4" height="1" fill="{t["scan"]}"/></pattern>')

    a('<filter id="frost" x="-10%" y="-10%" width="120%" height="120%">'
      '<feGaussianBlur stdDeviation="28"/><feColorMatrix type="saturate" values="1.6"/></filter>')
    a(f'<filter id="noise" x="0" y="0" width="100%" height="100%">'
      f'<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>'
      f'<feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 {t["noise"]} 0"/></filter>')
    a('<filter id="glow" x="-20%" y="-20%" width="140%" height="140%">'
      '<feGaussianBlur stdDeviation="2.4" result="b"/>'
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>')
    a(f'<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%">'
      f'<feGaussianBlur in="SourceAlpha" stdDeviation="18"/><feOffset dy="14"/>'
      f'<feComponentTransfer><feFuncA type="linear" slope="{t["shadow"]}"/></feComponentTransfer>'
      f'<feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

    # animated aurora blobs, reused for the background and the frosted panels
    a('<g id="blobs">')
    for i, (cx, cy, r, path, dur) in enumerate((
        (260, 140, 340, "260 140;380 220;200 260;260 140", 22),
        (900, 120, 360, "900 120;780 230;960 260;900 120", 26),
        (720, 560, 320, "720 560;560 470;860 500;720 560", 19),
    )):
        xs = ";".join(p.split()[0] for p in path.split(";"))
        ys = ";".join(p.split()[1] for p in path.split(";"))
        a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#blob{i})">'
          f'<animate attributeName="cx" values="{xs}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" '
          f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1;0.4 0 0.6 1"/>'
          f'<animate attributeName="cy" values="{ys}" dur="{dur}s" repeatCount="indefinite" calcMode="spline" '
          f'keySplines="0.4 0 0.6 1;0.4 0 0.6 1;0.4 0 0.6 1"/></circle>')
    a("</g>")
    a("</defs>")

    a('<g clip-path="url(#card)">')

    # ── background
    a(f'<rect width="{W}" height="{H}" fill="{t["bg"]}"/>')
    a('<use href="#blobs"/>')
    a(f'<rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gridMask)"/>')

    # particles
    a('<g>')
    for _ in range(34):
        x = rnd.uniform(20, W - 20)
        y = rnd.uniform(60, H - 10)
        r = rnd.uniform(0.7, 2.0)
        col = rnd.choice((t["a1"], t["a2"], t["a3"]))
        dur = rnd.uniform(7, 15)
        rise = rnd.uniform(50, 120)
        drift = rnd.uniform(-14, 14)
        beg = -rnd.uniform(0, dur)
        pk = t["particle"] * rnd.uniform(0.5, 1)
        a(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{col}" opacity="0">'
          f'<animate attributeName="cy" values="{f(y)};{f(y - rise)}" dur="{f(dur)}s" begin="{f(beg)}s" repeatCount="indefinite"/>'
          f'<animate attributeName="cx" values="{f(x)};{f(x + drift)};{f(x)}" dur="{f(dur)}s" begin="{f(beg)}s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;{f(pk)};0" dur="{f(dur)}s" begin="{f(beg)}s" repeatCount="indefinite"/>'
          f'</circle>')
    a('</g>')

    # ── glass panels
    def glass(x, y, w, h, clip, delay):
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="{t["bg"]}" filter="url(#shadow)" opacity="0.9"/>')
        a(f'<g clip-path="url(#{clip})">')
        a('<use href="#blobs" filter="url(#frost)"/>')
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t["panel"]}" fill-opacity="{t["panel_alpha"]}"/>')
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#noise)"/>')
        a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sheen)"/>')
        # soft diagonal reflection sweeping across the glass
        a(f'<rect x="{x - 260}" y="{y - 40}" width="160" height="{h + 80}" fill="url(#streak)" '
          f'transform="skewX(-18)">'
          f'<animate attributeName="x" values="{x - 300};{x + w + 220}" dur="7s" begin="{delay}s" '
          f'repeatCount="indefinite" keyTimes="0;1" calcMode="spline" keySplines="0.5 0 0.3 1"/></rect>')
        a('</g>')
        a(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="19.5" fill="none" stroke="{t["hair"]}"/>')
        a(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="19.5" fill="none" '
          f'stroke="url(#border)" stroke-opacity="0.35" stroke-width="1"/>')
        # shimmer: a short bright dash orbiting the border
        a(f'<rect x="{x + 0.5}" y="{y + 0.5}" width="{w - 1}" height="{h - 1}" rx="19.5" fill="none" '
          f'stroke="url(#accent)" stroke-width="1.6" pathLength="1000" stroke-dasharray="140 860" stroke-linecap="round">'
          f'<animate attributeName="stroke-dashoffset" values="1000;0" dur="{7 + delay}s" repeatCount="indefinite"/></rect>')

    glass(LX, LY, LW, LH, "clipL", 0)
    glass(RX, RY, RW, RH, "clipR", 2)

    # ── left: ASCII portrait
    a(f'<text x="{LX + 22}" y="{LY + 32}" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{t["muted"]}">'
      f'PORTRAIT.ASCII</text>')
    a(f'<g><circle cx="{LX + LW - 64}" cy="{LY + 28}" r="3.5" fill="{t["a3"]}">'
      f'<animate attributeName="opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/></circle>'
      f'<circle cx="{LX + LW - 64}" cy="{LY + 28}" r="3.5" fill="none" stroke="{t["a3"]}">'
      f'<animate attributeName="r" values="3.5;9" dur="1.8s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="0.7;0" dur="1.8s" repeatCount="indefinite"/></circle>'
      f'<text x="{LX + LW - 52}" y="{LY + 32}" font-family="{MONO}" font-size="11" letter-spacing="2" '
      f'fill="{t["muted"]}">LIVE</text></g>')

    a('<g clip-path="url(#clipA)">')
    a('<g>')
    a('<animateTransform attributeName="transform" type="translate" values="0 0;0 -7;0 0" dur="6s" '
      'repeatCount="indefinite" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>')
    a(f'<g font-family="{MONO}" font-size="{f(LINE * 0.98)}" fill="url(#asciiGrad)" filter="url(#glow)">')
    for r, row in enumerate(ascii_rows):
        y = AY + (r + 0.8) * LINE
        a(f'<text x="{AX}" y="{f(y)}" textLength="{AW}" lengthAdjust="spacingAndGlyphs" xml:space="preserve" '
          f'style="white-space:pre">{esc(row)}</text>')
    a('</g></g>')
    # scanlines + travelling scan band
    a(f'<rect x="{AX - 8}" y="{AY - 12}" width="{AW + 16}" height="{AH + 20}" fill="url(#scan)"/>')
    a(f'<rect x="{AX - 8}" y="{AY - 80}" width="{AW + 16}" height="70" fill="url(#scanBand)">'
      f'<animate attributeName="y" values="{AY - 80};{AY + AH + 10}" dur="4.2s" repeatCount="indefinite"/></rect>')
    a('</g>')

    # corner brackets around the portrait
    br = 14
    for (cx, cy, dx, dy) in ((AX - 8, AY - 12, 1, 1), (AX + AW + 8, AY - 12, -1, 1),
                             (AX - 8, AY + AH + 8, 1, -1), (AX + AW + 8, AY + AH + 8, -1, -1)):
        a(f'<path d="M{cx} {cy + dy * br}V{cy}H{cx + dx * br}" fill="none" stroke="url(#border)" '
          f'stroke-width="1.5" stroke-linecap="round" opacity="0.8"/>')

    fy = LY + LH - 26
    a(f'<text x="{LX + 22}" y="{fy}" font-family="{MONO}" font-size="13" fill="{t["soft"]}">'
      f'<tspan fill="{t["a3"]}">&gt;</tspan> ameya.kabir</text>')
    a(f'<rect x="{LX + 22 + 13 * ADV * 13 + 4}" y="{fy - 11}" width="7.5" height="14" rx="1.5" fill="{t["a2"]}">{BLINK}</rect>')
    a(f'<text x="{LX + LW - 22}" y="{fy}" text-anchor="end" font-family="{MONO}" font-size="11" '
      f'fill="{t["muted"]}">{COLS}×{ROWS} · utf-8</text>')

    # ── right: terminal
    a(f'<line x1="{RX}" y1="{RY + 44}" x2="{RX + RW}" y2="{RY + 44}" stroke="{t["hair"]}"/>')
    for i, col in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        a(f'<circle cx="{RX + 24 + i * 20}" cy="{RY + 22}" r="6" fill="{col}"/>')
    a(f'<text x="{RX + RW / 2}" y="{RY + 26}" text-anchor="middle" font-family="{SANS}" font-size="12.5" '
      f'fill="{t["muted"]}">ameya@automationedge — ~/profile — zsh</text>')
    a(f'<text x="{RX + RW - 20}" y="{RY + 26}" text-anchor="end" font-family="{MONO}" font-size="11" '
      f'fill="{t["muted"]}">⌥ 1</text>')

    def prompt(y, begin):
        a(f'<g opacity="0">{reveal(begin, dx=0, dur=0.15)}'
          f'<text x="{TX}" y="{y}" font-family="{MONO}" font-size="14.5" fill="{t["a3"]}">➜ '
          f'<tspan fill="{t["a2"]}">~</tspan></text></g>')
        return TX + 14.5 * ADV * 4

    # 1. whoami
    cx = prompt(RY + 80, 0.25)
    a(typed("t_who", cx, RY + 80, "whoami", 14.5, 0.45, 0.07, t["text"], theme=t, hold_cursor=0.25))

    # 2. name
    a(typed("t_name", TX, RY + 132, "Hi, I'm Ameya Ajit Kabir", 36, 1.15, 0.065, "url(#accent)",
            weight=700, theme=t, hold_cursor=0.2))

    # 3. rotating subtitles
    sub_begin, step, erase, slot = 3.0, 0.055, 0.022, 3.8
    total = slot * len(SUBTITLES)
    sy, ss = RY + 172, 20
    sadv = ss * ADV
    sx = TX + sadv * 2
    a(f'<g opacity="0">{reveal(sub_begin - 0.2, dx=0, dur=0.2)}'
      f'<text x="{TX}" y="{sy}" font-family="{MONO}" font-size="{ss}" fill="{t["a1"]}">›</text></g>')
    cursor_events = {0.0: 0.0}
    for i, s in enumerate(SUBTITLES):
        n = len(s)
        t0 = i * slot
        ev = [(0.0, 0.0)] if t0 > 0 else []
        for k in range(n + 1):
            ev.append((t0 + k * step, k * sadv))
        t_erase = t0 + slot - 0.35 - n * erase
        for k in range(n, -1, -1):
            ev.append((t_erase + (n - k) * erase, k * sadv))
        for tt, w in ev:
            if tt >= t0 or t0 == 0:
                cursor_events[round(tt, 4)] = w
        vals, kts = discrete(ev, total)
        uid = f"t_sub{i}"
        a(f'<clipPath id="{uid}"><rect x="{f(sx)}" y="{f(sy - ss)}" height="{f(ss * 1.4)}" width="0">'
          f'<animate attributeName="width" calcMode="discrete" values="{vals}" keyTimes="{kts}" '
          f'dur="{f(total)}s" begin="{sub_begin}s" repeatCount="indefinite"/></rect></clipPath>')
        a(f'<text x="{f(sx)}" y="{sy}" font-family="{MONO}" font-size="{ss}" fill="{t["soft"]}" '
          f'textLength="{f(n * sadv)}" lengthAdjust="spacingAndGlyphs" clip-path="url(#{uid})" '
          f'xml:space="preserve">{esc(s)}</text>')
    cvals, ckts = discrete(sorted((tt, sx + w + 2) for tt, w in cursor_events.items()), total)
    a(f'<rect x="{f(sx + 2)}" y="{f(sy - ss * 0.82)}" width="{f(sadv * 0.9)}" height="{f(ss * 0.98)}" rx="1.5" '
      f'fill="{t["a2"]}" opacity="0">'
      f'<animate attributeName="x" calcMode="discrete" values="{cvals}" keyTimes="{ckts}" dur="{f(total)}s" '
      f'begin="{sub_begin}s" repeatCount="indefinite"/>'
      f'<set attributeName="opacity" to="0.9" begin="{sub_begin}s"/></rect>')

    # 4. cat profile.json
    fs = 14.5
    y0 = RY + 222
    cx = prompt(y0, 3.3)
    a(typed("t_cat", cx, y0, "cat profile.json", fs, 3.5, 0.045, t["text"], theme=t, hold_cursor=0.15))
    K, S, P = t["key"], t["string"], t["punct"]
    json_lines = [
        [("{", P)],
        [("  ", P), ('"location"', K), (": ", P), ('"Pune, India"', S), (",", P)],
        [("  ", P), ('"company"', K), (":  ", P), ('"AutomationEdge"', S), (",", P)],
        [("  ", P), ('"role"', K), (":     ", P), ('"Automation Developer · RPA Engineer"', S), (",", P)],
        [("  ", P), ('"focus"', K), (":    ", P), ("[", P), ('"Web Automation"', S), (", ", P),
         ('"APIs"', S), (", ", P), ('"DB Architecture"', S), ("]", P)],
        [("}", P)],
    ]
    for i, parts in enumerate(json_lines):
        y = y0 + 28 + i * 24
        spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in parts)
        a(f'<g opacity="0">{reveal(4.45 + i * 0.16)}'
          f'<text x="{TX}" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve">{spans}</text></g>')

    # 5. ls ./stack → skill pills
    y1 = y0 + 28 + 6 * 24 + 14
    cx = prompt(y1, 5.6)
    a(typed("t_ls", cx, y1, "ls ./stack", fs, 5.8, 0.045, t["text"], theme=t, hold_cursor=0.15))
    px, py, ph = TX, y1 + 18, 34
    pfs = 13
    for i, s in enumerate(SKILLS):
        pw = len(s) * pfs * ADV + 38
        ccx, ccy = px + pw / 2, py + ph / 2
        beg = 6.55 + i * 0.12
        col = (t["a1"], t["a2"], t["a3"])[i % 3]
        a(f'<g opacity="0">'
          f'<animate attributeName="opacity" from="0" to="1" begin="{f(beg)}s" dur="0.3s" fill="freeze"/>'
          f'<g transform="translate({f(ccx)} {f(ccy)})"><g>'
          f'<animateTransform attributeName="transform" type="scale" values="0.6;1.06;1" keyTimes="0;0.6;1" '
          f'begin="{f(beg)}s" dur="0.45s" fill="freeze"/>'
          f'<g transform="translate({f(-ccx)} {f(-ccy)})"><g class="pill">'
          f'<rect x="{f(px)}" y="{py}" width="{f(pw)}" height="{ph}" rx="{ph / 2}" fill="{col}" filter="url(#soft)" opacity="0.25">'
          f'<animate attributeName="opacity" values="0.15;{0.45 if name == "dark" else 0.3};0.15" dur="3.2s" '
          f'begin="{f(i * 0.45)}s" repeatCount="indefinite"/></rect>'
          f'<rect x="{f(px)}" y="{py}" width="{f(pw)}" height="{ph}" rx="{ph / 2}" fill="{t["pill_fill"]}" '
          f'stroke="url(#accent)" stroke-width="1.2"/>'
          f'<circle cx="{f(px + 16)}" cy="{f(ccy)}" r="3.5" fill="{col}"/>'
          f'<text x="{f(px + 27)}" y="{f(ccy + 4.6)}" font-family="{MONO}" font-size="{pfs}" font-weight="500" '
          f'fill="{t["text"]}">{esc(s)}</text>'
          f'</g></g></g></g></g>')
        px += pw + 10

    # 6. idle prompt
    y2 = py + ph + 38
    cx = prompt(y2, 7.5)
    a(f'<rect x="{f(cx + 2)}" y="{f(y2 - 12)}" width="8" height="14.5" rx="1.5" fill="{t["a2"]}" opacity="0">'
      f'<animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1.06s" begin="7.6s" repeatCount="indefinite"/></rect>')

    # status bar
    sb = RY + RH - 36
    a(f'<line x1="{RX}" y1="{sb}" x2="{RX + RW}" y2="{sb}" stroke="{t["hair"]}"/>')
    a(f'<circle cx="{TX + 4}" cy="{sb + 18}" r="3.5" fill="{t["a3"]}">'
      f'<animate attributeName="opacity" values="1;0.3;1" dur="2.2s" repeatCount="indefinite"/></circle>')
    a(f'<text x="{TX + 16}" y="{sb + 22}" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">'
      f'online · building automations that never sleep</text>')
    a(f'<text x="{RX + RW - 24}" y="{sb + 22}" text-anchor="end" font-family="{MONO}" font-size="11.5" '
      f'fill="{t["muted"]}">IST +05:30 · main ⎇</text>')

    a("</g>")  # card clip

    # outer card border + shimmer
    a(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="{R - 0.5}" fill="none" stroke="{t["hair"]}"/>')
    a(f'<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="{R - 0.5}" fill="none" stroke="url(#accent)" '
      f'stroke-width="1.5" pathLength="1000" stroke-dasharray="220 280" stroke-linecap="round" opacity="0.75">'
      f'<animate attributeName="stroke-dashoffset" values="0;-1000" dur="12s" repeatCount="indefinite"/></rect>')

    a("</svg>")
    return "\n".join(o) + "\n"


PW, PH = 1180, 330
STAGES = [
    ("TRIGGER", "cron · webhook", "inbox · file drop"),
    ("BOT", "AutomationEdge", "Selenium · DOM"),
    ("INTEGRATE", "REST APIs · JSON", "auth · retries"),
    ("PERSIST", "PostgreSQL", "audit trail"),
    ("WATCHDOG", "health checks", "SLA timers"),
]
ESCALATION = ["detect", "L1 · on-call", "L2 · team lead", "L3 · management", "resolved ✓"]


def build_pipeline(name, t):
    """Animated 'how my automations run' diagram: data flows through five stages, then escalates."""
    T = 10.0
    o = []
    a = o.append

    def kt(*ts):
        return ";".join(f"{x / T:.4f}" for x in ts)

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}" '
      f'role="img" aria-labelledby="ptitle pdesc">')
    a('<title id="ptitle">How my automations run</title>')
    a('<desc id="pdesc">Pipeline: trigger, bot, API integration, PostgreSQL, watchdog — failures escalate '
      'from detection through L1, L2 and L3 until resolved.</desc>')
    a("<defs>")
    a(f'<clipPath id="pcard"><rect width="{PW}" height="{PH}" rx="24"/></clipPath>')
    a(f'<linearGradient id="paccent" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0" spreadMethod="reflect">'
      f'<stop offset="0" stop-color="{t["a1"]}"/><stop offset="0.5" stop-color="{t["a2"]}"/>'
      f'<stop offset="1" stop-color="{t["a3"]}"/>'
      f'<animateTransform attributeName="gradientTransform" type="translate" values="0 0;600 0;0 0" '
      f'dur="9s" repeatCount="indefinite"/></linearGradient>')
    a(f'<linearGradient id="psheen" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="{t["sheen"]}"/>'
      f'<stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
    for i, col in enumerate((t["a1"], t["a2"], t["a3"])):
        a(f'<radialGradient id="pblob{i}"><stop offset="0" stop-color="{col}" stop-opacity="{t["blob"] * 0.8}"/>'
          f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>')
    a(f'<pattern id="pgrid" width="32" height="32" patternUnits="userSpaceOnUse">'
      f'<path d="M32 0H0V32" fill="none" stroke="{t["grid"]}"/></pattern>')
    a('<filter id="pglow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4"/></filter>')
    a("</defs>")

    a('<g clip-path="url(#pcard)">')
    a(f'<rect width="{PW}" height="{PH}" fill="{t["bg"]}"/>')
    for i, (cx, cy, r, dx, dur) in enumerate(((180, 60, 300, 120, 20), (620, 300, 320, -140, 24), (1040, 80, 300, -100, 22))):
        a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#pblob{i})">'
          f'<animate attributeName="cx" values="{cx};{cx + dx};{cx}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    a(f'<rect width="{PW}" height="{PH}" fill="url(#pgrid)"/>')

    # header
    a(f'<text x="40" y="46" font-family="{MONO}" font-size="14" fill="{t["a3"]}">➜ <tspan fill="{t["a2"]}">~/pipeline</tspan>'
      f'<tspan fill="{t["soft"]}">  how my automations run, end to end</tspan></text>')
    a(f'<circle cx="{PW - 140}" cy="41" r="3.5" fill="{t["a3"]}">'
      f'<animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/></circle>')
    a(f'<text x="{PW - 40}" y="46" text-anchor="end" font-family="{MONO}" font-size="12" fill="{t["muted"]}">'
      f'running 24/7</text>')

    # stages
    nw, nh, ny, gap = 188, 118, 74, 40
    xs = [40 + i * (nw + gap) for i in range(len(STAGES))]
    cy = ny + nh / 2
    arrive = [0.4] + [1.0 + i * 1.0 for i in range(1, len(STAGES))]

    # connectors + packets
    for i in range(len(STAGES) - 1):
        x1, x2 = xs[i] + nw, xs[i + 1]
        a(f'<line x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}" stroke="{t["hair"]}" stroke-width="2"/>')
        a(f'<line x1="{x1}" y1="{cy}" x2="{x2}" y2="{cy}" stroke="url(#paccent)" stroke-width="2" '
          f'stroke-dasharray="4 6" opacity="0.7"><animate attributeName="stroke-dashoffset" values="20;0" '
          f'dur="0.8s" repeatCount="indefinite"/></line>')
        s, e = arrive[i] + 0.15, arrive[i + 1]
        for glow in (True, False):
            a(f'<circle cx="0" cy="0" r="{6 if glow else 3.5}" fill="{t["a2"] if glow else t["text"]}" opacity="0"'
              f'{" filter=" + chr(34) + "url(#pglow)" + chr(34) if glow else ""}>'
              f'<animateMotion path="M{x1} {cy}H{x2}" keyPoints="0;0;1;1" keyTimes="{kt(0, s, e, T)}" '
              f'calcMode="linear" dur="{T}s" repeatCount="indefinite"/>'
              f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt(0, s, s + 0.05, e - 0.05, e, T)}" '
              f'dur="{T}s" repeatCount="indefinite"/></circle>')

    for i, (title, l1, l2) in enumerate(STAGES):
        x = xs[i]
        col = (t["a1"], t["a2"], t["a3"], t["a1"], t["a2"])[i]
        a(f'<rect x="{x}" y="{ny}" width="{nw}" height="{nh}" rx="16" fill="{t["panel"]}" fill-opacity="{t["panel_alpha"]}"/>')
        a(f'<rect x="{x}" y="{ny}" width="{nw}" height="{nh}" rx="16" fill="url(#psheen)"/>')
        a(f'<rect x="{x + 0.5}" y="{ny + 0.5}" width="{nw - 1}" height="{nh - 1}" rx="15.5" fill="none" stroke="{t["hair"]}"/>')
        # pulse when the packet arrives
        p = arrive[i]
        a(f'<rect x="{x + 0.5}" y="{ny + 0.5}" width="{nw - 1}" height="{nh - 1}" rx="15.5" fill="none" '
          f'stroke="url(#paccent)" stroke-width="1.6" opacity="0.15">'
          f'<animate attributeName="opacity" values="0.15;0.15;1;0.15;0.15" '
          f'keyTimes="{kt(0, p - 0.3, p, p + 0.9, T)}" dur="{T}s" repeatCount="indefinite"/></rect>')
        a(f'<text x="{x + 18}" y="{ny + 28}" font-family="{MONO}" font-size="11" fill="{t["muted"]}">0{i + 1}</text>')
        a(f'<circle cx="{x + nw - 22}" cy="{ny + 24}" r="4" fill="{col}">'
          f'<animate attributeName="r" values="4;4;6.5;4;4" keyTimes="{kt(0, p - 0.2, p, p + 0.4, T)}" '
          f'dur="{T}s" repeatCount="indefinite"/></circle>')
        a(f'<text x="{x + 18}" y="{ny + 58}" font-family="{MONO}" font-size="15" font-weight="700" '
          f'letter-spacing="1.5" fill="{t["text"]}">{title}</text>')
        a(f'<text x="{x + 18}" y="{ny + 82}" font-family="{MONO}" font-size="12" fill="{t["soft"]}">{esc(l1)}</text>')
        a(f'<text x="{x + 18}" y="{ny + 100}" font-family="{MONO}" font-size="12" fill="{t["muted"]}">{esc(l2)}</text>')

    # escalation lane
    ly = 252
    a(f'<text x="40" y="{ly + 5}" font-family="{MONO}" font-size="12" letter-spacing="1.5" fill="{t["muted"]}">'
      f'ON FAILURE ›</text>')
    lx0, lx1 = 170, PW - 40
    n = len(ESCALATION)
    cw = 156
    step = (lx1 - lx0 - cw) / (n - 1)
    chip_x = [lx0 + k * step for k in range(n)]
    lit = [4.4 + k * 0.85 for k in range(n)]
    reset = 9.4
    a(f'<line x1="{lx0 + cw / 2}" y1="{ly}" x2="{chip_x[-1] + cw / 2}" y2="{ly}" stroke="{t["hair"]}" stroke-width="2"/>')
    xs_prog = ";".join(f(v) for v in [lx0 + cw / 2, lx0 + cw / 2] + [c + cw / 2 for c in chip_x] + [chip_x[-1] + cw / 2, lx0 + cw / 2, lx0 + cw / 2])
    a(f'<line x1="{lx0 + cw / 2}" y1="{ly}" x2="{lx0 + cw / 2}" y2="{ly}" stroke="url(#paccent)" stroke-width="2">'
      f'<animate attributeName="x2" values="{xs_prog}" keyTimes="{kt(0, lit[0] - 0.4, *lit, reset, reset + 0.01)};1" '
      f'dur="{T}s" repeatCount="indefinite"/></line>')
    for k, label in enumerate(ESCALATION):
        x = chip_x[k]
        done = k == n - 1
        col = t["a3"] if done else (t["a2"] if k == 0 else t["a1"])
        a(f'<rect x="{f(x)}" y="{ly - 17}" width="{cw}" height="34" rx="17" fill="{t["pill_fill"]}" stroke="{t["hair"]}"/>')
        a(f'<g opacity="0.0"><animate attributeName="opacity" values="0;0;1;1;0;0" '
          f'keyTimes="{kt(0, lit[k] - 0.15, lit[k], reset, reset + 0.3, T)}" dur="{T}s" repeatCount="indefinite"/>'
          f'<rect x="{f(x)}" y="{ly - 17}" width="{cw}" height="34" rx="17" fill="{col}" filter="url(#pglow)" opacity="0.3"/>'
          f'<rect x="{f(x)}" y="{ly - 17}" width="{cw}" height="34" rx="17" fill="{t["pill_fill"]}" stroke="{col}" stroke-width="1.4"/>'
          f'</g>')
        a(f'<circle cx="{f(x + 18)}" cy="{ly}" r="3.5" fill="{col}"/>')
        a(f'<text x="{f(x + 30)}" y="{ly + 4.5}" font-family="{MONO}" font-size="12.5" fill="{t["text"]}">{esc(label)}</text>')

    a(f'<text x="40" y="{PH - 22}" font-family="{MONO}" font-size="11.5" fill="{t["muted"]}">'
      f'each tier gets a window to acknowledge before the next one is paged</text>')
    a("</g>")
    a(f'<rect x="0.5" y="0.5" width="{PW - 1}" height="{PH - 1}" rx="23.5" fill="none" stroke="{t["hair"]}"/>')
    a(f'<rect x="0.5" y="0.5" width="{PW - 1}" height="{PH - 1}" rx="23.5" fill="none" stroke="url(#paccent)" '
      f'stroke-width="1.4" pathLength="1000" stroke-dasharray="180 320" opacity="0.6">'
      f'<animate attributeName="stroke-dashoffset" values="0;-1000" dur="14s" repeatCount="indefinite"/></rect>')
    a("</svg>")
    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--photo", help="portrait photo to convert to ASCII (needs Pillow)")
    ap.add_argument("--out", default=os.path.join(os.path.dirname(__file__), ".."))
    args = ap.parse_args()
    rows = photo_ascii(args.photo) if args.photo else procedural_ascii()
    for name, theme in THEMES.items():
        path = os.path.join(args.out, f"{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build(name, theme, rows))
        print(f"wrote {os.path.normpath(path)} ({os.path.getsize(path) // 1024} KB)")
        path = os.path.join(args.out, f"pipeline-{name}.svg")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(build_pipeline(name, theme))
        print(f"wrote {os.path.normpath(path)} ({os.path.getsize(path) // 1024} KB)")


if __name__ == "__main__":
    main()
