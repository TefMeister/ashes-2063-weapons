"""Minimal driver for the GZDoomVR window (copied from unreal-gold-vr ugdrive.py): foreground, BitBlt capture, scancode input.

Deliberately BitBlt from the screen DC, not PrintWindow -- PrintWindow serves a
stale DWM-cached frame the moment the game stops presenting (menus, pauses),
which is exactly when the picture matters (game-mod-rules / lm primitives).
Arrow keys need KEYEVENTF_EXTENDEDKEY or the scancode reads as a numpad key.
"""
import ctypes, ctypes.wintypes as w, sys, time

u32, g32 = ctypes.windll.user32, ctypes.windll.gdi32
u32.SetProcessDPIAware()

def find():
    out = []
    @ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
    def cb(h, _):
        if not u32.IsWindowVisible(h): return True
        n = u32.GetWindowTextLengthW(h)
        if n:
            b = ctypes.create_unicode_buffer(n + 1)
            u32.GetWindowTextW(h, b, n + 1)
            if b.value.strip().lower().startswith(TITLE):
                out.append((h, b.value))
        return True
    u32.EnumWindows(cb, 0)
    return out

def fg(h):
    u32.ShowWindow(h, 9); u32.SetForegroundWindow(h); time.sleep(0.35)
    return u32.GetForegroundWindow() == h

def rect(h):
    r = w.RECT(); u32.GetClientRect(h, ctypes.byref(r))
    p = w.POINT(0, 0); u32.ClientToScreen(h, ctypes.byref(p))
    return p.x, p.y, r.right, r.bottom

def shot(h, path):
    x, y, cw, ch = rect(h)
    sdc = u32.GetDC(0); mdc = g32.CreateCompatibleDC(sdc)
    bmp = g32.CreateCompatibleBitmap(sdc, cw, ch); g32.SelectObject(mdc, bmp)
    g32.BitBlt(mdc, 0, 0, cw, ch, sdc, x, y, 0x00CC0020)
    class BI(ctypes.Structure):
        _fields_ = [("biSize", w.DWORD), ("biWidth", w.LONG), ("biHeight", w.LONG),
                    ("biPlanes", w.WORD), ("biBitCount", w.WORD), ("biCompression", w.DWORD),
                    ("biSizeImage", w.DWORD), ("biXPelsPerMeter", w.LONG), ("biYPelsPerMeter", w.LONG),
                    ("biClrUsed", w.DWORD), ("biClrImportant", w.DWORD)]
    bi = BI(); bi.biSize = ctypes.sizeof(BI); bi.biWidth = cw; bi.biHeight = -ch
    bi.biPlanes = 1; bi.biBitCount = 24; bi.biCompression = 0
    stride = (cw * 3 + 3) & ~3
    buf = ctypes.create_string_buffer(stride * ch)
    g32.GetDIBits(mdc, bmp, 0, ch, buf, ctypes.byref(bi), 0)
    hdr = b'BM' + (14 + 40 + len(buf)).to_bytes(4, 'little') + b'\0' * 4 + (54).to_bytes(4, 'little')
    hdr += bytes(bi)
    open(path, 'wb').write(hdr + buf.raw)
    g32.DeleteObject(bmp); g32.DeleteDC(mdc); u32.ReleaseDC(0, sdc)
    return cw, ch

# --- scancode input -------------------------------------------------------
class KI(ctypes.Structure):
    _fields_ = [("wVk", w.WORD), ("wScan", w.WORD), ("dwFlags", w.DWORD),
                ("time", w.DWORD), ("dwExtraInfo", ctypes.POINTER(w.ULONG))]
class IU(ctypes.Union):   _fields_ = [("ki", KI), ("pad", ctypes.c_ubyte * 32)]
class INP(ctypes.Structure): _fields_ = [("type", w.DWORD), ("u", IU)]
KEYDOWN, SCAN, KEYUP, EXT = 0x0, 0x0008, 0x0002, 0x0001

SC = {'tilde':0x29,'enter':0x1C,'esc':0x01,'space':0x39,'up':0x48,'down':0x50,
      'left':0x4B,'right':0x4D,'w':0x11,'a':0x1E,'s':0x1F,'d':0x20,'y':0x15,
      '0':0x0B,'1':0x02,'2':0x03,'3':0x04,'backspace':0x0E,'f1':0x3B}
for i,c in enumerate("qwertyuiop"): SC.setdefault(c, 0x10+i)
for i,c in enumerate("asdfghjkl"):  SC.setdefault(c, 0x1E+i)
for i,c in enumerate("zxcvbnm"):    SC.setdefault(c, 0x2C+i)
for i,c in enumerate("1234567890"): SC.setdefault(c, 0x02+i)
SC[' '] = 0x39

def key(name, hold=0.05):
    sc = SC[name] if name in SC else SC[name.lower()]
    ext = EXT if name in ('up','down','left','right') else 0
    for fl in (SCAN|ext, SCAN|KEYUP|ext):
        i = INP(); i.type = 1; i.u.ki = KI(0, sc, fl, 0, None)
        u32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INP))
        if fl & KEYUP: continue
        time.sleep(hold)
    time.sleep(0.05)

def typestr(s, d=0.04):
    for ch in s:
        key(ch if ch != ' ' else 'space'); time.sleep(d)

# Punctuation the console needs. '.' cost a KeyError mid-session on "VRGOLD IPD 2.85".
SC.update({'.':0x34, ',':0x33, '-':0x0C, '=':0x0D, '/':0x35, ';':0x27, "'":0x28})

# ---- GZDoomVR / Ashes 2063 additions --------------------------------------
import subprocess, os
TITLE = "ashes"            # window title prefix, lower case; checked against all visible windows
GAME = r"C:\NonSteam\Ashes 2063 VR"
# Repo-relative. This used to be an absolute path into C:\Users\TD3KX\ashes-2063-weapons, which
# stopped existing when the clone root moved to github-backups\ (2026-08-31).
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_PK3 = os.path.join(REPO, "revolver", "gzdoom", "Ashes2063_revolver3d_test.pk3")
FLAT_INI = r"gzdoomvr\ashes-flat-test.ini"   # a copy, so the VR config is never rewritten

def launch(extra_files=(TEST_PK3,), map_name="MAP01", engine="gzdoomvr", extra_args=()):
    import shutil
    flat_ini = FLAT_INI.replace("gzdoomvr", engine, 1)
    ini = os.path.join(GAME, flat_ini)
    if not os.path.exists(ini):
        shutil.copy(os.path.join(GAME, r"gzdoomvr\ashes-vr.ini"), ini)
    args = [os.path.join(GAME, engine, "gzdoomvr.exe"), "-iwad", r"Resources\freedoom-0.12.1\freedoom2.wad",
            "-file", r"Resources\AshesSAMenu.pk3", r"Resources\lightmodepatch.pk3",
            r"Resources\Ashes2063Enriched2_23.pk3", r"Resources\Ashes2063EnrichedFDPatch.pk3", *extra_files,
            "-config", flat_ini, "+vr_mode", "0", "+vid_fullscreen", "0", "+win_w", "1280", "+win_h", "720",
            "+set", "language", "enu", "-skill", "3", "+map", map_name, *extra_args]
    return subprocess.Popen(args, cwd=GAME)

def console(cmd, settle=0.4):
    key('tilde'); time.sleep(settle)
    typestr(cmd); key('enter'); time.sleep(0.2)
    key('tilde'); time.sleep(settle)

def all_windows():
    out = []
    @ctypes.WINFUNCTYPE(w.BOOL, w.HWND, w.LPARAM)
    def cb(h, _):
        if u32.IsWindowVisible(h):
            n = u32.GetWindowTextLengthW(h)
            if n:
                b = ctypes.create_unicode_buffer(n + 1); u32.GetWindowTextW(h, b, n + 1); out.append((h, b.value))
        return True
    u32.EnumWindows(cb, 0)
    return out

SHIFTED = {'+': '=', '_': '-', ':': ';', '"': "'"}

def _raw(sc, up):
    i = INP(); i.type = 1; i.u.ki = KI(0, sc, SCAN | (KEYUP if up else 0), 0, None)
    u32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INP))

def typestr(s, d=0.04):
    for ch in s:
        if ch in SHIFTED:
            _raw(0x2A, False); time.sleep(0.03); key(SHIFTED[ch]); _raw(0x2A, True)
        else:
            key(ch if ch != ' ' else 'space')
        time.sleep(d)

def fg(h):
    """Foreground the window. Windows refuses SetForegroundWindow from a background process,
    so join the input queue of whatever is in front for the call (AttachThreadInput), then verify.
    [verified-live 2026-09-17: plain SetForegroundWindow and the ALT-tap trick both failed here]"""
    k32 = ctypes.windll.kernel32
    u32.ShowWindow(h, 9)
    for _ in range(3):
        cur = u32.GetForegroundWindow()
        t_fg = u32.GetWindowThreadProcessId(cur, None)
        t_me = k32.GetCurrentThreadId()
        u32.AttachThreadInput(t_me, t_fg, True)
        u32.BringWindowToTop(h); u32.SetForegroundWindow(h); u32.SetFocus(h)
        u32.AttachThreadInput(t_me, t_fg, False)
        time.sleep(0.35)
        if u32.GetForegroundWindow() == h:
            return True
    return False
