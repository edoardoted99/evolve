#include <cmath>
#include <cstdlib>
#include <cstring>
#include <iostream>

static const int W = 60;
static const int H = 40;
static char canvas[H][W];

static void clear_canvas() { std::memset(canvas, '.', sizeof(canvas)); }

static void put(int x, int y, char c) {
    if (x >= 0 && x < W && y >= 0 && y < H) canvas[y][x] = c;
}

// Bresenham line
static void line(int x0, int y0, int x1, int y1, char c) {
    int dx = std::abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
    int dy = -std::abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
    int err = dx + dy;
    while (true) {
        put(x0, y0, c);
        if (x0 == x1 && y0 == y1) break;
        int e2 = 2 * err;
        if (e2 >= dy) { err += dy; x0 += sx; }
        if (e2 <= dx) { err += dx; y0 += sy; }
    }
}

static void print_canvas() {
    for (int y = 0; y < H; ++y) {
        for (int x = 0; x < W; ++x) std::cout << canvas[y][x];
        std::cout << '\n';
    }
}

int main(int argc, char* argv[]) {
    if (argc != 9) {
        std::cerr << "Usage: ./quad x1 y1 x2 y2 x3 y3 x4 y4\n";
        return 1;
    }

    int v[8];
    for (int i = 0; i < 8; ++i) v[i] = std::atoi(argv[i + 1]);

    clear_canvas();

    // disegna i 4 lati: 1->2, 2->3, 3->4, 4->1
    for (int i = 0; i < 4; ++i) {
        int next = (i + 1) % 4;
        line(v[2 * i], v[2 * i + 1], v[2 * next], v[2 * next + 1], '#');
    }

    // segna i vertici
    for (int i = 0; i < 4; ++i)
        put(v[2 * i], v[2 * i + 1], 'A' + i);

    print_canvas();
    return 0;
}
