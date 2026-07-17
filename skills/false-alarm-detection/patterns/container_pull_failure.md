# container_pull_failure

Container image pull failure — the test never ran because the container runtime (podman/docker) could not pull the required base image.

## Key signals

- A `podman run` or `docker run` command is issued
- Immediately followed by an error from the container runtime (not from inside the container)
- The error references image pulling: `Error: initializing source docker://`, `manifest unknown`, `unauthorized`, `connection refused`, `timeout`
- The test script itself never executes — the failure is purely at the container pull stage
- A failure marker file may be touched after the pull fails

## Example log excerpt

```text
+ podman run -i --rm --userns=keep-id:uid=1001 ... quay.io/aipcc/base-images/rocm-7.14-el9.6:3.5 ./import_test.sh Authlib Authlib ...
Trying to pull quay.io/aipcc/base-images/rocm-7.14-el9.6:3.5...
Error: initializing source docker://quay.io/aipcc/base-images/rocm-7.14-el9.6:3.5: reading manifest 3.5 in quay.io/aipcc/base-images/rocm-7.14-el9.6: unauthorized: access to the requested resource is not authorized
+ touch /tmp/.../import_failed_Authlib
```

## What this is NOT

- A failure that happens inside a running container (the container started successfully but the test failed) — that is a real test failure, not this pattern.
- A network error during `pip install` or `uv install` inside the container — that is a different kind of infrastructure issue.
