# Claro v1.18.26 - Packages and Projects

Claro v1.18.26 makes projects and packages safer and more useful while keeping the beginner syntax simple.

## Create a project

```bash
claro new MyProject
cd MyProject
claro run
```

A new project contains:

```text
main.claro
claro.project
claro.lock
packages/
README.md
```

## Project file

`claro.project` is intentionally plain text:

```text
manifest-version: 1
name: MyProject
main: main.claro
version: v1.18.26
packages:
package: text
package: net_tools
```

## Package commands

```bash
claro package init
claro package add text
claro package remove text
claro package list
claro package doctor
claro package lock
```

`claro package add NAME` creates a local folder:

```text
packages/NAME/
  claro.package
  README.md
```

Each `claro.package` file includes a tiny manifest and checksum:

```text
manifest-version: 1
name: text
version: 1
source: local
checksum: 1234abcd
```

`claro.lock` records the release version, lock format, packages, and checksums so future registry work has a stable safety foundation.

## Project-name safety

`claro new NAME` checks the project name before creating folders. Project names may use only letters, numbers, dash, and underscore, and they must be 64 characters or fewer.

This keeps mistakes like `../bad` from creating a project outside the folder where the learner is working.

## Package-name safety

Package names may use only:

```text
letters
numbers
dash
underscore
```

Package names must be 64 characters or fewer so Claro can create predictable local package folders and metadata paths.

This means simple names like these are allowed:

```text
text
sdl
net_tools
my-package
```

Unsafe names are rejected:

```text
../bad
folder/name
bad name
```

If an unsafe package name somehow gets into `claro.project`, package maintenance commands should not quietly continue. `claro package doctor` points out the bad name, `claro package lock` refuses to write lockfile data for it, and `claro package remove NAME` exits with an error if the lockfile refresh still sees an unsafe package name after the removal. Learners can still recover by removing the exact unsafe entry, such as `claro package remove ../bad`; Claro rewrites the project file and lockfile without using that unsafe name as a folder path.

## Why this matters

Packages are important for Claro's future, but the workflow must stay friendly:

```text
make a project
add a package
run the project
check the project
```

No complicated setup should be needed for a beginner.
