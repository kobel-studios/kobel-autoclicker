"""Verify what interval the app ACTUALLY uses for various milliseconds inputs.

No clicking happens. This drives the real parsing/normalization logic with a
hidden Tk root, exactly as start_clicking() does (click-off + start).
"""

import tkinter as tk

import autoclicker_hub as app


def main():
    root = tk.Tk()
    root.withdraw()

    h = object.__new__(app.AutoClickerHub)
    h.root = root
    h.minutes_var = tk.StringVar(value="0")
    h.seconds_var = tk.StringVar(value="0")
    h.millis_var = tk.StringVar(value="0")

    def trial(ms, mins="0", secs="0"):
        h.minutes_var.set(mins)
        h.seconds_var.set(secs)
        h.millis_var.set(ms)
        # Same normalization start_clicking() applies (and field click-off).
        h._fill_zero_if_empty(h.minutes_var)
        h._fill_zero_if_empty(h.seconds_var)
        h._normalize_millis(h.millis_var)
        shown = h.millis_var.get()
        try:
            interval = h._get_interval_seconds()
        except ValueError as exc:
            print(f"  typed={ms!r:>9} -> field shows {shown!r:>5}  REJECTED ({exc})")
            return
        ms_eff = interval * 1000.0
        rate = "MAX SPEED (no delay)" if interval == 0 else f"{1/interval:.1f} clicks/sec"
        print(f"  typed={ms!r:>9} -> field shows {shown!r:>5}  actual interval={ms_eff:.4f} ms  ({rate})")

    print("NORMAL MODE (minutes=0, seconds=0):")
    for ms in ["0.0001", "0.5", "0.9", "1", "1.5", "2", "0"]:
        trial(ms)

    print("\nWITH seconds=1 and a sub-1 ms entry:")
    trial("0.5", secs="1")

    print("\nCODE WORD:")
    trial("kobel")

    root.destroy()


if __name__ == "__main__":
    main()
