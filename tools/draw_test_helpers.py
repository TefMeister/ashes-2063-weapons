"""Shared by the unattended flat checks (2026-11-27): find the game window by process id, as draw_test.py does (never
by title: a file window on the game folder is called "Ashes 2063 VR" too)."""
import ctypes
import ctypes.wintypes
import time

import gzdrive as g


def game_window(pid, timeout=60):
    want = ctypes.wintypes.DWORD(pid)
    for _ in range(timeout * 2):
        for h, _t in g.all_windows():
            got = ctypes.wintypes.DWORD()
            g.u32.GetWindowThreadProcessId(h, ctypes.byref(got))
            if got.value == want.value:
                return h
        time.sleep(0.5)
    return None
