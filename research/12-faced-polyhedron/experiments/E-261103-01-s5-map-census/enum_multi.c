/* Exhaustive triangular rotations of K_n plus identified parallel edges.
 * Triangle assignment, MRV and short-cycle pruning follow code/enum_k12.c.
 * Input: n g k patterns, then k endpoint pairs for each extra-edge pattern.
 * Output: canonical dart codes as JSONL, followed by an explicit completion record.
 */
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXN 12
#define MAXD 180
static int n, nd, degree[MAXN], extra_degree[MAXN];
static int tail[MAXD], head[MAXD], succ[MAXD], pred[MAXD];
static int arc[MAXN][MAXN][MAXN], mult[MAXN][MAXN];
static int root_darts[MAXD], root_order[MAXD], root_used[MAXD];
static long long nodes, leaves, roots;
static int timed_out;
static double limit;
static struct timespec start;
typedef struct { unsigned char code[2 * MAXD]; } Class;
static Class *classes;
static int nclasses, capacity;

static double elapsed(void)
{
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);
    return now.tv_sec - start.tv_sec + (now.tv_nsec - start.tv_nsec) / 1e9;
}

static int stopped(void)
{
    if (!timed_out && elapsed() >= limit) timed_out = 1;
    return timed_out;
}

static int short_cycle(int a, int b)
{
    int cur = b, len = 1;
    while (succ[cur] != -1) { cur = succ[cur]; len++; }
    return cur == a && len != degree[tail[a]];
}

static int valid(int e, int f, int g)
{
    if (succ[e] != -1 || succ[f] != -1 || succ[g] != -1) return 0;
    if (pred[e ^ 1] != -1 || pred[f ^ 1] != -1 || pred[g ^ 1] != -1) return 0;
    return !short_cycle(e, g ^ 1) && !short_cycle(f, e ^ 1) && !short_cycle(g, f ^ 1);
}

static void assign(int e, int f, int g)
{
    succ[e] = g ^ 1; pred[g ^ 1] = e;
    succ[f] = e ^ 1; pred[e ^ 1] = f;
    succ[g] = f ^ 1; pred[f ^ 1] = g;
}

static void unassign(int e, int f, int g)
{
    succ[e] = succ[f] = succ[g] = -1;
    pred[e ^ 1] = pred[f ^ 1] = pred[g ^ 1] = -1;
}

static void flag_code(int root, int mirror, unsigned char *code)
{
    int label[MAXD], order[MAXD], count = 1;
    for (int d = 0; d < nd; d++) label[d] = -1;
    label[root] = 0; order[0] = root;
    for (int i = 0; i < count; i++) {
        int d = order[i];
        int step = mirror ? (succ[d] ^ 1) : pred[d ^ 1];
        int neighbors[2] = {step, d ^ 1};
        for (int j = 0; j < 2; j++) {
            int e = neighbors[j];
            if (label[e] == -1) { label[e] = count; order[count++] = e; }
            code[2 * i + j] = (unsigned char)label[e];
        }
    }
    if (count != nd) { fprintf(stderr, "disconnected completed map\n"); exit(2); }
}

static void report(void)
{
    leaves++;
    unsigned char best[2 * MAXD], code[2 * MAXD];
    int have = 0;
    for (int mirror = 0; mirror < 2; mirror++)
        for (int d = 0; d < nd; d++) {
            flag_code(d, mirror, code);
            if (!have || memcmp(code, best, 2 * nd) < 0) {
                memcpy(best, code, 2 * nd); have = 1;
            }
        }
    for (int i = 0; i < nclasses; i++)
        if (memcmp(classes[i].code, best, 2 * nd) == 0) return;
    if (nclasses == capacity) {
        capacity = capacity ? 2 * capacity : 256;
        Class *p = realloc(classes, (size_t)capacity * sizeof(Class));
        if (!p) { fprintf(stderr, "allocation failed\n"); exit(2); }
        classes = p;
    }
    memcpy(classes[nclasses++].code, best, 2 * nd);
    printf("{\"code\":[");
    for (int i = 0; i < nd; i++)
        printf("%s[%u,%u]", i ? "," : "", best[2 * i], best[2 * i + 1]);
    printf("]}\n"); fflush(stdout);
}

static void search(int remaining)
{
    nodes++;
    if ((nodes & 1023) == 0 && stopped()) return;
    if (!remaining) { report(); return; }
    int beste = -1, bestcount = MAXD * MAXD, bestf[MAXD * MAXN], bestg[MAXD * MAXN];
    for (int e = 0; e < nd && bestcount > 1; e++) {
        if (succ[e] != -1) continue;
        int v = tail[e], a = head[e], count = 0;
        int fs[MAXD * MAXN], gs[MAXD * MAXN];
        for (int b = 0; b < n; b++) {
            if (b == v || b == a) continue;
            for (int j = 0; j < mult[a][b]; j++)
                for (int k = 0; k < mult[b][v]; k++) {
                    int f = arc[a][b][j], g = arc[b][v][k];
                    if (valid(e, f, g)) { fs[count] = f; gs[count++] = g; }
                }
        }
        if (count < bestcount) {
            bestcount = count; beste = e;
            if (!count) return;
            memcpy(bestf, fs, sizeof(int) * count);
            memcpy(bestg, gs, sizeof(int) * count);
        }
    }
    for (int i = 0; i < bestcount && !timed_out; i++) {
        assign(beste, bestf[i], bestg[i]);
        search(remaining - 3);
        unassign(beste, bestf[i], bestg[i]);
    }
}

/* Seed triangles around vertex 0 for one chosen root rotation. */
static void seed(int i)
{
    if (timed_out) return;
    if (i == degree[0]) { search(nd - 3 * degree[0]); return; }
    int e = root_order[i], next = root_order[(i + 1) % degree[0]];
    int a = head[e], b = head[next], g = next ^ 1;
    if (a == b) return;
    for (int j = 0; j < mult[a][b] && !timed_out; j++) {
        int f = arc[a][b][j];
        if (valid(e, f, g)) {
            assign(e, f, g); seed(i + 1); unassign(e, f, g);
        }
    }
}

static void rotations(int pos)
{
    if (stopped()) return;
    if (pos == degree[0]) { roots++; seed(0); return; }
    for (int j = 0; j < degree[0] && !timed_out; j++) {
        if (root_used[j]) continue;
        int d = root_darts[j], v = head[d], skip = 0;
        if (head[root_order[pos - 1]] == v) continue;
        for (int k = 0; k < j; k++)
            if (!root_used[k] && (head[root_darts[k]] == v ||
                (!extra_degree[v] && !extra_degree[head[root_darts[k]]]))) skip = 1;
        if (skip) continue;
        root_order[pos] = d; root_used[j] = 1;
        rotations(pos + 1);
        root_used[j] = 0;
    }
}

int main(int argc, char **argv)
{
    if (argc != 3) { fprintf(stderr, "usage: enum_multi input seconds\n"); return 2; }
    char *end;
    limit = strtod(argv[2], &end);
    if (*end || !(limit >= 0)) return 2;
    FILE *in = fopen(argv[1], "r");
    int genus, extras, patterns;
    if (!in || fscanf(in, "%d%d%d%d", &n, &genus, &extras, &patterns) != 4) return 2;
    if (n < 3 || n > MAXN || extras < 0 || extras > 8 || patterns < 1 ||
        2 * (n * (n - 1) / 2 + extras) > MAXD ||
        n * (n - 1) / 2 + extras != 3 * (n + 2 * genus - 2)) return 2;
    clock_gettime(CLOCK_MONOTONIC, &start);
    int done = 0;
    for (int p = 0; p < patterns && !stopped(); p++) {
        int m[MAXN][MAXN] = {{0}};
        memset(extra_degree, 0, sizeof extra_degree);
        for (int j = 0; j < extras; j++) {
            int a, b;
            if (fscanf(in, "%d%d", &a, &b) != 2 || a < 0 || b < 0 || a >= n || b >= n || a == b) return 2;
            m[a][b]++; m[b][a]++; extra_degree[a]++; extra_degree[b]++;
        }
        memset(degree, 0, sizeof degree); memset(mult, 0, sizeof mult);
        nd = 0;
        for (int a = 0; a < n; a++)
            for (int b = a + 1; b < n; b++)
                for (int j = 0; j <= m[a][b]; j++) {
                    tail[nd] = a; head[nd] = b; tail[nd + 1] = b; head[nd + 1] = a;
                    arc[a][b][mult[a][b]++] = nd; arc[b][a][mult[b][a]++] = nd + 1;
                    degree[a]++; degree[b]++; nd += 2;
                }
        for (int d = 0; d < nd; d++) succ[d] = pred[d] = -1;
        int k = 0;
        memset(root_used, 0, sizeof root_used);
        for (int d = 0; d < nd; d++) if (!tail[d]) root_darts[k++] = d;
        root_order[0] = root_darts[0]; root_used[0] = 1;
        rotations(1);
        if (!timed_out) done++;
        fprintf(stderr, "pattern %d/%d complete=%d nodes=%lld classes=%d seconds=%.3f\n",
                p + 1, patterns, !timed_out, nodes, nclasses, elapsed());
    }
    fclose(in);
    printf("{\"summary\":true,\"complete\":%s,\"stop_reason\":\"%s\","
           "\"graphs_done\":%d,\"graphs_total\":%d,\"roots\":%lld,\"nodes\":%lld,"
           "\"leaves\":%lld,\"classes\":%d,\"seconds\":%.6f}\n",
           done == patterns ? "true" : "false", done == patterns ? "exhausted" : "time_limit",
           done, patterns, roots, nodes, leaves, nclasses, elapsed());
    free(classes);
    return 0;
}
