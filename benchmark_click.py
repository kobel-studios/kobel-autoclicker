"""Measure how fast the auto-clicker can actually click.

This performs REAL mouse clicks at the current cursor position, so move your
mouse over an empty area (e.g. the desktop) before running. It mirrors the
timing logic used by autoclicker_hub.py (PAUSE=0 + sliced sleep).
"""

import os
import statistics
import time

import pyautogui


pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0  # same as the app: timing is controlled by the interval


def sliced_sleep(target_interval):
    slept = 0.0
    while slept < target_interval:
        step = min(0.02, target_interval - slept)
        time.sleep(step)
        slept += step


def bench(n, target_interval):
    per_click_ms = []
    start_all = time.perf_counter()
    for _ in range(n):
        t0 = time.perf_counter()
        pyautogui.click()
        sliced_sleep(target_interval)
        per_click_ms.append((time.perf_counter() - t0) * 1000.0)
    total = time.perf_counter() - start_all
    return {
        "n": n,
        "target_ms": target_interval * 1000.0,
        "total_s": total,
        "avg_ms": statistics.mean(per_click_ms),
        "median_ms": statistics.median(per_click_ms),
        "min_ms": min(per_click_ms),
        "max_ms": max(per_click_ms),
        "clicks_per_sec": n / total,
    }


def fmt(r):
    return (
        f"target {r['target_ms']:.0f}ms | "
        f"avg {r['avg_ms']:.2f}ms | median {r['median_ms']:.2f}ms | "
        f"min {r['min_ms']:.2f}ms | max {r['max_ms']:.2f}ms | "
        f"{r['clicks_per_sec']:.1f} clicks/sec ({r['n']} clicks in {r['total_s']:.2f}s)"
    )


def main():
    lines = ["Auto-clicker timing benchmark", "-" * 40]

    # Warm-up so the first click's overhead doesn't skew results.
    pyautogui.click()

    raw = bench(200, 0.0)
    one_ms = bench(200, 0.001)

    lines.append("Raw (no interval):   " + fmt(raw))
    lines.append("1 ms interval:       " + fmt(one_ms))
    lines.append("")
    lines.append(
        "Note: 'avg' is the real time per click including OS click overhead. "
        "True 1ms is limited by click overhead and OS timer resolution."
    )

    report = "\n".join(lines)
    print(report)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "benchmark_result.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report + "\n")


if __name__ == "__main__":
    main()
