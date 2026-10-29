/*
 * enum_k12.c -- exhaustive enumeration of orientable neighborly triangulations
 * of the genus-6 surface with 12 vertices (triangular embeddings of K12),
 * up to combinatorial isomorphism (relabelling, orientation reversal allowed).
 *
 * Model.  An orientable triangulation with edge graph K12 is the same thing as a
 * rotation system on K12 in which every face is a triangle ("rule Delta"):
 *     succ[v][a] = b   <=>   oriented triangle (v,a,b)
 *                     <=>   succ[a][b] = v  and  succ[b][v] = a.
 * Every directed edge v->a lies in exactly one oriented triangle; each succ[v]
 * must be a single cyclic permutation (11-cycle) of the other 11 vertices.
 * (Then the complex is automatically simplicial and chi = 12-66+44 = -10.)
 *
 * Normalisation (WLOG by relabelling): rotation of vertex 0 is (1 2 ... 11).
 * Search: backtracking over directed edges with no triangle yet, branching on
 * the third vertex; MRV (directed edge with fewest consistent completions),
 * forbidding premature closing of a cycle in any vertex rotation.
 *
 * Isomorph rejection: every solution is mapped to its canonical code
 * = lexicographic minimum over all 12*11*2 = 264 "flag labellings"
 * (vertex v -> 0, neighbour a -> 1, rotation of v read forward or backward
 * -> 2..11, orientation chosen accordingly).  This equals the lex-min over all
 * relabellings and both orientations of the code
 *     code = rot(0) | rot(1) | ... | rot(11),
 * rot(x) = neighbours of x in positive cyclic order starting at the smallest.
 * Orbit-stabiliser check: #labelled solutions in a class = 264 / |Aut|.
 *
 * Usage: enum_k12 [first_only]   (prints classes to stdout, progress to stderr)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define N 12
#define NF 44
#define CODELEN (N * (N - 1))

static int succ[N][N], pred[N][N];
static int nfaces;
static int stk[NF + 4][3];
static int sp;
static long long nodes = 0, nsol = 0;
static int first_only = 0;
static clock_t t0;

typedef struct {
    unsigned char code[CODELEN];
    long long hits;     /* labelled solutions (rot(0) fixed) in this class */
    int aut, aut_op;    /* |Aut| incl. orientation reversing; orientation preserving */
} cls_t;

static cls_t *classes = NULL;
static int ncls = 0, capcls = 0;

static int closes_short(int x, int p, int q)
{
    /* linking p -> q in rotation of x (p has no succ, q has no pred) */
    int cur = q, len = 1;
    while (succ[x][cur] != -1) { cur = succ[x][cur]; len++; }
    if (cur == p) return len != N - 1;
    return 0;
}

static int valid(int v, int a, int b)
{
    if (b == v || b == a) return 0;
    if (pred[v][b] != -1) return 0;
    if (succ[a][b] != -1 || pred[a][v] != -1) return 0;
    if (succ[b][v] != -1 || pred[b][a] != -1) return 0;
    if (closes_short(v, a, b)) return 0;
    if (closes_short(a, b, v)) return 0;
    if (closes_short(b, v, a)) return 0;
    return 1;
}

static void assign(int v, int a, int b)
{
    succ[v][a] = b; pred[v][b] = a;
    succ[a][b] = v; pred[a][v] = b;
    succ[b][v] = a; pred[b][a] = v;
    stk[sp][0] = v; stk[sp][1] = a; stk[sp][2] = b; sp++;
    nfaces++;
}

static void unassign(void)
{
    sp--;
    int v = stk[sp][0], a = stk[sp][1], b = stk[sp][2];
    succ[v][a] = -1; pred[v][b] = -1;
    succ[a][b] = -1; pred[a][v] = -1;
    succ[b][v] = -1; pred[b][a] = -1;
    nfaces--;
}

/* code of the labelling given by flag (v, a, dir); dir=+1 forward, -1 backward */
static void flag_code(int S[N][N], int P[N][N], int v, int a, int dir, unsigned char *out)
{
    int L[N], inv[N];
    L[v] = 0; inv[0] = v;
    int cur = a;
    for (int k = 1; k < N; k++) {
        L[cur] = k; inv[k] = cur;
        cur = (dir > 0) ? S[v][cur] : P[v][cur];
    }
    int pos = 0;
    for (int xn = 0; xn < N; xn++) {
        int x = inv[xn];
        int start = (xn == 0) ? 1 : 0;      /* smallest new label among neighbours */
        int y = inv[start];
        for (int k = 0; k < N - 1; k++) {
            out[pos++] = (unsigned char)L[y];
            y = (dir > 0) ? S[x][y] : P[x][y];
        }
    }
}

static int find_class(const unsigned char *code)
{
    for (int i = 0; i < ncls; i++)
        if (memcmp(classes[i].code, code, CODELEN) == 0) return i;
    return -1;
}

static void canon(int S[N][N], int P[N][N], unsigned char *best, int *aut, int *aut_op)
{
    unsigned char c[CODELEN];
    int have = 0, cnt = 0, cnt_op = 0, bestdir = 0;
    for (int v = 0; v < N; v++)
        for (int a = 0; a < N; a++) {
            if (a == v) continue;
            for (int dir = 1; dir >= -1; dir -= 2) {
                flag_code(S, P, v, a, dir, c);
                int r = have ? memcmp(c, best, CODELEN) : -1;
                if (r < 0) {
                    memcpy(best, c, CODELEN); have = 1; cnt = 1; bestdir = dir;
                    cnt_op = 1;
                } else if (r == 0) {
                    cnt++;
                    if (dir == bestdir) cnt_op++;
                }
            }
        }
    *aut = cnt; *aut_op = cnt_op;
}

static void print_rot(FILE *f, int S[N][N])
{
    for (int x = 0; x < N; x++) {
        int y = (x == 0) ? 1 : 0;
        for (int k = 0; k < N - 1; k++) { fprintf(f, "%d%s", y, k < N - 2 ? " " : ""); y = S[x][y]; }
        fprintf(f, "%s", x < N - 1 ? " | " : "\n");
    }
}

static void report(void)
{
    nsol++;
    if (first_only) {
        printf("ROT ");
        print_rot(stdout, succ);
        fflush(stdout);
        fprintf(stderr, "first solution after %lld nodes, %.3f s\n", nodes,
                (double)(clock() - t0) / CLOCKS_PER_SEC);
        exit(0);
    }
    unsigned char best[CODELEN];
    int aut, aut_op;
    canon(succ, pred, best, &aut, &aut_op);
    int i = find_class(best);
    if (i < 0) {
        if (ncls == capcls) {
            capcls = capcls ? 2 * capcls : 128;
            classes = realloc(classes, capcls * sizeof(cls_t));
        }
        i = ncls++;
        memcpy(classes[i].code, best, CODELEN);
        classes[i].hits = 0;
        classes[i].aut = aut;
        classes[i].aut_op = aut_op;
    }
    classes[i].hits++;
}

static void search(void)
{
    nodes++;
    if ((nodes & 0xFFFFF) == 0)
        fprintf(stderr, "  nodes=%lld sols=%lld classes=%d t=%.1fs\n", nodes, nsol, ncls,
                (double)(clock() - t0) / CLOCKS_PER_SEC);
    if (nfaces == NF) { report(); return; }
    int bestv = -1, besta = -1, bestc = 100, bc[N], cc[N];
    for (int v = 0; v < N && bestc > 1; v++)
        for (int a = 0; a < N && bestc > 1; a++) {
            if (a == v || succ[v][a] != -1) continue;
            int c = 0;
            for (int b = 0; b < N; b++)
                if (valid(v, a, b)) cc[c++] = b;
            if (c < bestc) {
                bestc = c; bestv = v; besta = a;
                memcpy(bc, cc, sizeof(int) * c);
                if (c == 0) return;
            }
        }
    for (int i = 0; i < bestc; i++) {
        assign(bestv, besta, bc[i]);
        search();
        unassign();
    }
}

static int cmpcls(const void *x, const void *y)
{
    return memcmp(((const cls_t *)x)->code, ((const cls_t *)y)->code, CODELEN);
}

int main(int argc, char **argv)
{
    if (argc > 1 && strcmp(argv[1], "first_only") == 0) first_only = 1;
    memset(succ, -1, sizeof succ);
    memset(pred, -1, sizeof pred);
    t0 = clock();
    /* rotation of 0 = (1 2 ... 11): triangles (0,i,i+1) */
    for (int i = 1; i <= N - 1; i++) {
        int j = (i == N - 1) ? 1 : i + 1;
        assign(0, i, j);
    }
    search();
    double t = (double)(clock() - t0) / CLOCKS_PER_SEC;
    qsort(classes, ncls, sizeof(cls_t), cmpcls);
    long long check = 0;
    int bad = 0;
    for (int i = 0; i < ncls; i++) {
        check += classes[i].hits;
        if (classes[i].hits * classes[i].aut != 2 * N * (N - 1)) bad++;
    }
    printf("# nodes %lld solutions %lld classes %d time %.2f s orbit_stabiliser_failures %d\n",
           nodes, nsol, ncls, t, bad);
    for (int i = 0; i < ncls; i++) {
        printf("CLASS %d aut %d aut_op %d hits %lld code ", i, classes[i].aut, classes[i].aut_op,
               classes[i].hits);
        for (int k = 0; k < CODELEN; k++) printf("%x", classes[i].code[k]);
        printf("\n");
    }
    return 0;
}
