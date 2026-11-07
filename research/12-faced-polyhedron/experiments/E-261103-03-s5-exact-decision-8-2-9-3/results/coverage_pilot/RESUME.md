# Same-path pilot resume check

After the source-697e3e5 pilot completed, the same activated-environment command was invoked
again, before the post-pilot inheritance changes:

```bash
bash research/12-faced-polyhedron/experiments/E-261103-03-s5-exact-decision-8-2-9-3/run.sh coverage-pilot
```

It exited 0 and printed `no pending units; recorded units skipped`. Status still reported the
same two TIMEOUT records. No new attempt directory or target solver call was created. The
sandbox printed `nice: setpriority: Operation not permitted` on both invocations; the short
pilot continued at default priority. These notes transcribe the tool output after execution;
they are not an additional measured run manifest. Original attempt files are unchanged.

Current-source regression checks rebuild both saved CNFs and validate checkpoint inheritance
without repeating their solver calls. Source identity deliberately blocks resuming a run after
a source change; production is a new registered output root and imports this completed pilot.
