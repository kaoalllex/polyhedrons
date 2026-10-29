/*
 * enum2_k12.c -- second, independent enumerator (cross-check of enum_k12.c).
 *
 * Different algorithm: works with UNORIENTED triangle sets.
 *   - WLOG link(0) is the unoriented cycle 1-2-...-11-1 (triangles {0,i,i+1}).
 *   - Branch on the lexicographically smallest edge {a,b} lying in < 2 triangles,
 *     choosing the third vertex c.
 *   - Constraints: every edge in <= 2 triangles; for every vertex v the link graph
 *     (edges {x,y} for triangles {v,x,y}) has max degree 2 and no cycle shorter
 *     than 11.
 *   - Orientability (mode "orient"): union-find with parity over triangles, every
 *     shared edge forces "opposite induced directions"; a parity conflict = a
 *     Moebius strip in the partial complex = prune.
 *     Mode "all": no orientability pruning; orientable / non-orientable solutions
 *     are counted separately (checked at the end by BFS).
 *   - No isomorph rejection here: every labelled solution is printed as a line of
 *     44 sorted triples (mode orient) and classified afterwards in Python.
 *
 * Usage: enum2_k12 orient|all [print]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define N 12
#define NF 44

static int tri[NF][3];
static int ntri = 0;
static int edeg[N][N];          /* # triangles on edge */
static int etri[N][N][2];       /* triangle ids on edge */
static int lnb[N][N][2];        /* link(v): neighbours of x */
static int ldeg[N][N];
static int orient_mode = 1, print_mode = 0;
static long long nodes = 0, nsol = 0, nsol_or = 0, nsol_nonor = 0;
static clock_t t0;

/* union-find with parity, union by size, no path compression (undoable) */
static int uf_par[NF], uf_rel[NF], uf_sz[NF];
static int uf_stack[NF * 3], uf_sp = 0;

static int uf_find(int x, int *p)
{
    int r = 0;
    while (uf_par[x] != x) { r ^= uf_rel[x]; x = uf_par[x]; }
    *p = r;
    return x;
}

/* require parity(x) xor parity(y) == d; return 0 on conflict */
static int uf_union(int x, int y, int d)
{
    int px, py;
    int rx = uf_find(x, &px), ry = uf_find(y, &py);
    if (rx == ry) return ((px ^ py) == d);
    if (uf_sz[rx] < uf_sz[ry]) { int t = rx; rx = ry; ry = t; }
    uf_par[ry] = rx; uf_rel[ry] = px ^ py ^ d; uf_sz[rx] += uf_sz[ry];
    uf_stack[uf_sp++] = ry;
    return 1;
}

static void uf_undo_to(int mark)
{
    while (uf_sp > mark) {
        int ry = uf_stack[--uf_sp];
        int rx = uf_par[ry];
        uf_sz[rx] -= uf_sz[ry];
        uf_par[ry] = ry; uf_rel[ry] = 0;
    }
}

/* sign of edge {x,y} (x<y) in sorted triangle a<b<c with reference orientation (a,b,c) */
static int esign(const int *t, int x, int y)
{
    (void)y;
    if (x == t[0] && y == t[2]) return 1;  /* traversed c->a : reversed */
    return 0;                              /* a->b or b->c : forward */
}

/* would adding link edge x-y in link(v) be legal? */
static int link_ok(int v, int x, int y)
{
    if (ldeg[v][x] >= 2 || ldeg[v][y] >= 2) return 0;
    if (ldeg[v][x] == 0 || ldeg[v][y] == 0) return 1;
    /* both endpoints of paths: walk from x */
    int prev = -1, cur = x, len = 1;
    for (;;) {
        int nx = -1;
        for (int k = 0; k < ldeg[v][cur]; k++)
            if (lnb[v][cur][k] != prev) { nx = lnb[v][cur][k]; break; }
        if (nx == -1) break;
        prev = cur; cur = nx; len++;
    }
    if (cur == y) return len == N - 1;
    return 1;
}

static void link_add(int v, int x, int y)
{
    lnb[v][x][ldeg[v][x]++] = y;
    lnb[v][y][ldeg[v][y]++] = x;
}

static void link_del(int v, int x, int y)
{
    ldeg[v][x]--; ldeg[v][y]--;   /* LIFO: last added is last slot */
    (void)x; (void)y;
}

static int add_tri(int a, int b, int c)
{
    /* a<b<c assumed; returns 0 if orientation conflict (state then partially changed:
       caller must call del_tri anyway) */
    int id = ntri++;
    tri[id][0] = a; tri[id][1] = b; tri[id][2] = c;
    uf_par[id] = id; uf_rel[id] = 0; uf_sz[id] = 1;
    int ok = 1;
    int E[3][2] = {{a, b}, {b, c}, {a, c}};
    for (int k = 0; k < 3; k++) {
        int x = E[k][0], y = E[k][1];
        if (edeg[x][y] == 1) {
            int o = etri[x][y][0];
            /* coherent: induced directions opposite: o_t ^ o_o == 1 ^ s_t ^ s_o */
            int d = 1 ^ esign(tri[id], x, y) ^ esign(tri[o], x, y);
            if (!uf_union(id, o, d)) ok = 0;
        }
        etri[x][y][edeg[x][y]] = id;
        edeg[x][y]++; edeg[y][x]++;
    }
    link_add(a, b, c); link_add(b, a, c); link_add(c, a, b);
    return ok;
}

static void del_tri(void)
{
    int id = --ntri;
    int a = tri[id][0], b = tri[id][1], c = tri[id][2];
    link_del(c, a, b); link_del(b, a, c); link_del(a, b, c);
    int E[3][2] = {{a, b}, {b, c}, {a, c}};
    for (int k = 0; k < 3; k++) {
        int x = E[k][0], y = E[k][1];
        edeg[x][y]--; edeg[y][x]--;
    }
}

static int tri_exists(int a, int b, int c)
{
    for (int k = 0; k < edeg[a][b]; k++) {
        int t = etri[a][b][k];
        if (tri[t][0] == a && tri[t][1] == b && tri[t][2] == c) return 1;
    }
    return 0;
}

static int orientable_bfs(void)
{
    /* independent end check: propagate orientations by BFS over shared edges */
    int o[NF], q[NF], h = 0, tl = 0;
    for (int i = 0; i < NF; i++) o[i] = -1;
    o[0] = 0; q[tl++] = 0;
    while (h < tl) {
        int t = q[h++];
        int a = tri[t][0], b = tri[t][1], c = tri[t][2];
        int E[3][2] = {{a, b}, {b, c}, {a, c}};
        for (int k = 0; k < 3; k++) {
            int x = E[k][0], y = E[k][1];
            for (int m = 0; m < 2; m++) {
                int u = etri[x][y][m];
                if (u == t) continue;
                int want = o[t] ^ 1 ^ esign(tri[t], x, y) ^ esign(tri[u], x, y);
                if (o[u] == -1) { o[u] = want; q[tl++] = u; }
                else if (o[u] != want) return 0;
            }
        }
    }
    return tl == NF;
}

static void solution(void)
{
    nsol++;
    int orr = orientable_bfs();
    if (orr) nsol_or++; else nsol_nonor++;
    if (print_mode && orr) {
        for (int i = 0; i < NF; i++)
            printf("%d,%d,%d%s", tri[i][0], tri[i][1], tri[i][2], i < NF - 1 ? " " : "\n");
    }
}

static void search(void)
{
    nodes++;
    if ((nodes & 0x3FFFFF) == 0) {
        fprintf(stderr, "  nodes=%lld sols=%lld (or %lld, nonor %lld) t=%.1fs\n", nodes, nsol,
                nsol_or, nsol_nonor, (double)(clock() - t0) / CLOCKS_PER_SEC);
        fflush(stderr);
    }
    if (ntri == NF) { solution(); return; }
    int a = -1, b = -1;
    for (int x = 0; x < N && a < 0; x++)
        for (int y = x + 1; y < N; y++)
            if (edeg[x][y] < 2) { a = x; b = y; break; }
    if (a < 0) return;   /* cannot happen: 66 edges * 2 = 132 = 3*44 */
    for (int c = 0; c < N; c++) {
        if (c == a || c == b) continue;
        if (edeg[a][c] >= 2 || edeg[b][c] >= 2) continue;
        int s[3] = {a, b, c};
        /* sort */
        if (s[0] > s[1]) { int t = s[0]; s[0] = s[1]; s[1] = t; }
        if (s[1] > s[2]) { int t = s[1]; s[1] = s[2]; s[2] = t; }
        if (s[0] > s[1]) { int t = s[0]; s[0] = s[1]; s[1] = t; }
        if (tri_exists(s[0], s[1], s[2])) continue;
        if (!link_ok(a, b, c) || !link_ok(b, a, c) || !link_ok(c, a, b)) continue;
        int mark = uf_sp;
        int ok = add_tri(s[0], s[1], s[2]);
        if (ok || !orient_mode) search();
        del_tri();
        uf_undo_to(mark);
    }
}

int main(int argc, char **argv)
{
    if (argc > 1 && strcmp(argv[1], "all") == 0) orient_mode = 0;
    if (argc > 2 && strcmp(argv[2], "print") == 0) print_mode = 1;
    t0 = clock();
    for (int i = 1; i <= N - 1; i++) {
        int j = (i == N - 1) ? 1 : i + 1;
        int x = i < j ? i : j, y = i < j ? j : i;
        if (!add_tri(0, x, y)) { fprintf(stderr, "init conflict\n"); return 1; }
    }
    search();
    fprintf(stderr, "# mode=%s nodes %lld solutions %lld orientable %lld nonorientable %lld time %.2f s\n",
            orient_mode ? "orient" : "all", nodes, nsol, nsol_or, nsol_nonor,
            (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}
