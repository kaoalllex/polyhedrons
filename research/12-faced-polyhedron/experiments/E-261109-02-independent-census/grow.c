/* Leaf emitter for the independent census: same growth algorithm as enum_growth.py (see its docstring).
   usage: grow F g  -> prints one line per labelled leaf: "t0a t0b t0c ... | partner(t,i) as t*3+i ..." */
#include <stdio.h>
#include <stdlib.h>
#define MAXT 64
static int F, G, T, E_, extra;
static int tr[MAXT][3], pt[MAXT][3];          /* pt = partner side index t*3+i, -1 open */
static int corners[16], present;
static int nt, nv, closedc[16][16], openc[16][16], excess;
static long long nodes, leaves;

static int val(int u, int v) {
    int a = openc[u][v], b = openc[v][u], m = a > b ? a : b, c = closedc[u][v];
    return c + m;
}
static int contrib(int u, int v) { int x = val(u, v); return x > 0 ? x - 1 : 0; }
static void chg_open(int u, int v, int d) {
    int b = val(u, v) > 0; excess -= contrib(u, v); openc[u][v] += d; excess += contrib(u, v);
    present += (val(u, v) > 0) - b;
}
static void chg_closed(int u, int v, int d) {
    int b = val(u, v) > 0; excess -= contrib(u, v); closedc[u][v] += d; closedc[v][u] += d; excess += contrib(u, v);
    present += (val(u, v) > 0) - b;
}

static int isclosed[16];
static int distinct(int x) { int n = 0; for (int y = 0; y < F; y++) if (y != x && val(x, y) > 0) n++; return n; }
/* 1 = vertex of corner (t,i) has a closed link that is inconsistent; sets *closed when its link is a full cycle */
static int walk_bad(int t, int i, int *closed) {
    int ct = t, ci = i, n = 0, x = tr[t][i];
    *closed = 0;
    do {
        int p = pt[ct][ci];
        if (p < 0) return 0;
        n++; ct = p / 3; ci = (p % 3 + 1) % 3;
    } while (ct != t || ci != i);
    *closed = 1;
    return n != corners[x] || distinct(x) != F - 1;
}

static void finish(void) {
    int cnt[16] = {0};
    if (nv != F) return;
    for (int u = 0; u < F; u++) for (int v = u + 1; v < F; v++)
        if (closedc[u][v] == 0) return;
    for (int t = 0; t < T; t++) for (int i = 0; i < 3; i++) cnt[tr[t][i]]++;
    static char seen[MAXT][3];
    for (int t = 0; t < T; t++) for (int i = 0; i < 3; i++) seen[t][i] = 0;
    for (int t = 0; t < T; t++) for (int i = 0; i < 3; i++) {
        if (seen[t][i]) continue;
        int ct = t, ci = i, n = 0;
        while (!seen[ct][ci]) {
            seen[ct][ci] = 1; n++;
            int p = pt[ct][ci]; ct = p / 3; ci = (p % 3 + 1) % 3;
        }
        if (ct != t || ci != i || n != cnt[tr[t][i]]) return;
    }
    leaves++;
    for (int t = 0; t < T; t++) printf("%d %d %d ", tr[t][0], tr[t][1], tr[t][2]);
    printf("|");
    for (int t = 0; t < T; t++) for (int i = 0; i < 3; i++) printf(" %d", pt[t][i]);
    printf("\n");
}

static void rec(void) {
    nodes++;
    int ot = -1, oi = -1, nopen = 0;
    for (int t = 0; t < nt; t++) for (int i = 0; i < 3; i++)
        if (pt[t][i] < 0) { if (ot < 0) { ot = t; oi = i; } nopen++; }
    if (ot < 0) { if (nt == T) finish(); return; }
    if ((nopen + (T - nt)) & 1) return;
    int u = tr[ot][oi], v = tr[ot][(oi + 1) % 3];
    for (int t = 0; t < nt; t++) for (int i = 0; i < 3; i++) {
        if (pt[t][i] >= 0 || (t == ot && i == oi)) continue;
        if (tr[t][i] != v || tr[t][(i + 1) % 3] != u) continue;
        pt[ot][oi] = t * 3 + i; pt[t][i] = ot * 3 + oi;
        chg_open(u, v, -1); chg_open(v, u, -1); chg_closed(u, v, 1);
        int c1, c2, bad = walk_bad(ot, oi, &c1) || walk_bad(ot, (oi + 1) % 3, &c2);
        if (!bad && excess <= extra) { isclosed[u] += c1; isclosed[v] += c2; rec(); isclosed[u] -= c1; isclosed[v] -= c2; }
        chg_closed(u, v, -1); chg_open(u, v, 1); chg_open(v, u, 1);
        pt[ot][oi] = -1; pt[t][i] = -1;
    }
    if (nt < T) {
        int lim = nv + 1 < F ? nv + 1 : F, oldnv = nv;
        for (int w = 0; w < lim; w++) {
            if (w == u || w == v) continue;
            int k = nt++;
            tr[k][0] = v; tr[k][1] = u; tr[k][2] = w;
            pt[k][0] = ot * 3 + oi; pt[ot][oi] = k * 3; pt[k][1] = pt[k][2] = -1;
            if (w == nv) nv++;
            corners[u]++; corners[v]++; corners[w]++;
            chg_open(u, v, -1); chg_closed(u, v, 1); chg_open(u, w, 1); chg_open(w, v, 1);
            int c1, c2, bad = isclosed[w] || isclosed[u] || isclosed[v]
                || walk_bad(ot, oi, &c1) || walk_bad(ot, (oi + 1) % 3, &c2);
            if (!bad && excess <= extra && F * (F - 1) / 2 - present <= 2 * (T - nt) && corners[u] <= F - 1 + extra && corners[v] <= F - 1 + extra
                && corners[w] <= F - 1 + extra) { isclosed[u] += c1; isclosed[v] += c2; rec(); isclosed[u] -= c1; isclosed[v] -= c2; }
            corners[u]--; corners[v]--; corners[w]--;
            chg_open(w, v, -1); chg_open(u, w, -1); chg_closed(u, v, -1); chg_open(u, v, 1);
            nv = oldnv; pt[ot][oi] = -1; nt--;
        }
    }
}

int main(int argc, char **argv) {
    F = atoi(argv[1]); G = atoi(argv[2]);
    T = 2 * (F + 2 * G - 2); E_ = 3 * T / 2; extra = E_ - F * (F - 1) / 2;
    tr[0][0] = 0; tr[0][1] = 1; tr[0][2] = 2; nt = 1; nv = 3; corners[0] = corners[1] = corners[2] = 1;
    for (int i = 0; i < 3; i++) pt[0][i] = -1;
    for (int i = 0; i < 3; i++) chg_open(tr[0][i], tr[0][(i + 1) % 3], 1);
    rec();
    fprintf(stderr, "nodes %lld leaves %lld\n", nodes, leaves);
    return 0;
}
