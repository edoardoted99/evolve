import sys
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def apply_matrix(mat, pts):
    a, b, c, d = mat
    return [(a * x + b * y, c * x + d * y) for x, y in pts]


def eigen_2x2(mat):
    a, b, c, d = mat
    trace = a + d
    det = a * d - b * c
    disc = trace * trace - 4 * det

    eigenvalues = []
    eigenvectors = []

    if disc >= 0:
        sq = math.sqrt(disc)
        for l in ((trace + sq) / 2, (trace - sq) / 2):
            eigenvalues.append(l)
            if abs(b) > 1e-12:
                eigenvectors.append((b, l - a))
            elif abs(c) > 1e-12:
                eigenvectors.append((l - d, c))
            else:
                if abs(a - l) < 1e-12:
                    eigenvectors.append((1, 0))
                else:
                    eigenvectors.append((0, 1))
    else:
        re = trace / 2
        im = math.sqrt(-disc) / 2
        eigenvalues.append(complex(re, im))
        eigenvalues.append(complex(re, -im))

    return eigenvalues, eigenvectors


def main():
    if len(sys.argv) < 14:
        print("Usage: python quad.py x1 y1 x2 y2 x3 y3 x4 y4 a b c d steps",
              file=sys.stderr)
        sys.exit(1)

    args = [float(a) for a in sys.argv[1:]]
    pts = [(args[i], args[i + 1]) for i in range(0, 8, 2)]
    mat = (args[8], args[9], args[10], args[11])
    steps = int(args[12])

    eigenvalues, eigenvectors = eigen_2x2(mat)
    is_complex = any(isinstance(ev, complex) for ev in eigenvalues)

    # pre-calcola tutti gli stati
    history = [pts]
    cur = pts
    for _ in range(steps):
        cur = apply_matrix(mat, cur)
        history.append(cur)

    # limiti del plot
    all_x = [p[0] for frame in history for p in frame]
    all_y = [p[1] for frame in history for p in frame]
    margin = 5
    xmin, xmax = min(all_x) - margin, max(all_x) + margin
    ymin, ymax = min(all_y) - margin, max(all_y) + margin

    fig, ax = plt.subplots(1, 1, figsize=(10, 7))
    fig.patch.set_facecolor('#1a1a2e')
    ax.set_facecolor('#16213e')

    # disegna autovettori (fissi)
    if not is_complex:
        t_max = max(abs(xmax - xmin), abs(ymax - ymin)) * 2
        for i, (vx, vy) in enumerate(eigenvectors):
            norm = math.sqrt(vx * vx + vy * vy)
            if norm < 1e-12:
                continue
            vx, vy = vx / norm, vy / norm
            ax.plot([-vx * t_max, vx * t_max], [-vy * t_max, vy * t_max],
                    color='red', linewidth=1, linestyle='--', alpha=0.6,
                    label=f'v{i+1} (λ={eigenvalues[i]:.3f})')

    quad_line, = ax.plot([], [], color='#e94560', linewidth=2, solid_capstyle='round')
    vertices = ax.scatter([], [], c='white', s=60, zorder=5)
    labels = []
    for i in range(4):
        lbl = ax.text(0, 0, chr(ord('A') + i), color='white', fontsize=11,
                      fontweight='bold', ha='center', va='bottom')
        labels.append(lbl)

    title_text = ax.set_title('', color='white', fontsize=12, pad=10)
    eigen_text = ax.text(0.02, 0.02, '', transform=ax.transAxes, color='#ff6b6b',
                         fontsize=9, verticalalignment='bottom', family='monospace')

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.15, color='white')
    ax.tick_params(colors='#aaa')
    for spine in ax.spines.values():
        spine.set_color('#333')

    if not is_complex:
        ax.legend(loc='upper right', facecolor='#1a1a2e', edgecolor='#555',
                  labelcolor='#ff6b6b', fontsize=9)

    def update(step):
        pts = history[step]
        xs = [p[0] for p in pts] + [pts[0][0]]
        ys = [p[1] for p in pts] + [pts[0][1]]
        quad_line.set_data(xs, ys)
        vertices.set_offsets([(p[0], p[1]) for p in pts])
        for i, lbl in enumerate(labels):
            lbl.set_position((pts[i][0], pts[i][1] + 0.8))

        title_text.set_text(
            f'Step {step}  |  A = [[{mat[0]},{mat[1]}],[{mat[2]},{mat[3]}]]')

        if is_complex:
            ev = eigenvalues[0]
            mod_n = abs(ev) ** step if step > 0 else 1.0
            eigen_text.set_text(
                f'λ = {ev.real:.3f} ± {abs(ev.imag):.3f}i\n|λ|^{step} = {mod_n:.4f}')
        else:
            lines = []
            for i, ev in enumerate(eigenvalues):
                ev_n = ev ** step if step > 0 else 1.0
                lines.append(f'λ{i+1}^{step} = {ev_n:.4f}  (λ{i+1} = {ev:.3f})')
            eigen_text.set_text('\n'.join(lines))

        return quad_line, vertices, title_text, eigen_text, *labels

    ani = animation.FuncAnimation(fig, update, frames=steps + 1,
                                  interval=300, blit=False, repeat=True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
