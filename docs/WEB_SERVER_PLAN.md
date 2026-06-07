# Claro Web Server Plan

Current release: **Claro v1.18.26**

Claro currently has beginner HTTP client commands and offline `claro://` test URLs. A web server API is not complete yet.

## Ready now

- `HTTP CHECK`
- `HTTP GET`
- `HTTP SAVE`
- offline `claro://hello` and related lesson/test URLs
- `LASTHTTP`
- real `http://` and `https://` requests through `curl` when available

## Web server goals

A beginner web server should make tiny local apps possible without exposing learners to unsafe network defaults.

Desired properties:
- localhost-only by default
- readable route syntax
- simple request/response values
- friendly port-in-use errors
- easy stop behavior
- examples that work offline

## Possible future syntax sketch

```claro
WEB START LOCAL PORT 8080

WHEN GET "/"
    WEB SAY "Hello from Claro"
END

WEB WAIT
```

This is a sketch, not a committed syntax.

## Needed before implementation

- route syntax decision
- request value model
- response helpers
- safe defaults for host/port
- tests for port conflicts and malformed requests
- docs explaining localhost vs public internet

See also:
- `V1_17_NETWORKING.md`
- `CURRENT_STATUS.md`
- `ROADMAP.md`
