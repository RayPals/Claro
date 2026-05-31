# Claro v1.17.26 Networking Reliability

Claro v1.17.26 hardens the beginner networking foundation without making the language harder to read.

The goal is simple plain-text commands:

```claro
HTTP GET "claro://hello" AS page
SAY page
```

## Offline-safe learning URLs

Claro includes built-in `claro://` network test URLs. These do not need the internet, so lessons and tests work offline.

```claro
HTTP GET "claro://hello" AS page STATUS status
SAY page
SAY status
```

Expected output:

```text
Hello from Claro networking.
200
```

Available built-in test URLs:

```text
claro://hello
claro://json
claro://empty
claro://missing
```

## Check a URL

```claro
HTTP CHECK "claro://hello" AS safe
SAY safe
```

This returns `YES` for safe `http://`, `https://`, or `claro://` URLs and `NO` for unsafe strings.

## Get a page

```claro
HTTP GET "claro://hello" AS page
SAY page
```

To also store the status code:

```claro
HTTP GET "claro://hello" AS page STATUS status
SAY status
```

Claro also stores the latest HTTP status in:

```claro
LASTHTTP
```

## Get only the status

```claro
HTTP STATUS "claro://hello" AS code
SAY code
```

## Save a response to a file

```claro
HTTP SAVE "claro://json" TO "data.json" AS code
SAY code
```

## Safety rules

Claro accepts only simple, safe network URL forms:

```text
http://...
https://...
claro://...
```

Dangerous shell characters are rejected before calling external tools. This keeps the command beginner-friendly and safer.

Real `http://` and `https://` requests use `curl` when available. The `claro://` URLs always work offline.
