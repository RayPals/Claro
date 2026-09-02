# Advanced Static Typing

Claro v1.18.26 adds the first advanced static-typing foundation: typed containers checked by `claro typecheck`.

## Typed lists

```claro
SET names AS LIST OF TEXT TO LIST
ADD "Ada" TO names
ADD "Grace" TO names
```

The type checker now rejects wrong item types:

```claro
SET names AS LIST OF TEXT TO LIST
ADD 123 TO names
```

Output:

```text
Type mismatch for list names: expected TEXT item, but this value looks like NUMBER.
```

## Typed maps

```claro
SET scores AS MAP OF NUMBER TO MAP
PUT scores KEY "math" VALUE 98
```

The type checker rejects wrong value types:

```claro
SET scores AS MAP OF NUMBER TO MAP
PUT scores KEY "oops" VALUE "high"
```

Output:

```text
Type mismatch for map scores: expected NUMBER value, but this value looks like TEXT.
```

## Function parameter checks

Claro now has a small static-checking foundation for function arguments. Keep the beginner-friendly function syntax, then put the expected type inside the function with `CHECK TYPE`:

```claro
TEACH square amount
    CHECK TYPE amount IS NUMBER
    SAY amount
END

DO square 4
```

If a learner calls the function with the wrong kind of value, `claro typecheck` explains which parameter needs which type:

```claro
TEACH square amount
    CHECK TYPE amount IS NUMBER
    SAY amount
END

DO square "oops"
```

Output:

```text
Type mismatch for function square: parameter amount needs NUMBER, but this argument looks like TEXT.
```

If the learner forgets a checked argument, `claro typecheck` now names the missing parameter and expected type:

```claro
TEACH square amount
    CHECK TYPE amount IS NUMBER
    SAY amount
END

DO square
```

Output:

```text
Function square needs argument amount as NUMBER, but this call does not provide it.
```

Multiple checked parameters are reported separately, so a learner can fix each argument one at a time:

```claro
TEACH label TAKES name, age
    CHECK TYPE name IS TEXT
    CHECK TYPE age IS NUMBER
    SAY name
    SAY age
END

CALL label WITH 7, "old"
```

Output:

```text
Type mismatch for function label: parameter name needs TEXT, but this argument looks like NUMBER.
Type mismatch for function label: parameter age needs NUMBER, but this argument looks like TEXT.
```

If a learner mistypes a modern `DO` function name, `claro typecheck` now names the unknown function and suggests either checking the spelling or adding a matching `TEACH` block:

```claro
TEACH square amount
    CHECK TYPE amount IS NUMBER
    SAY amount
END

DO squre 4
```

Output:

```text
Function squre is not known yet. Check the function name or add TEACH squre before calling it.
```

## Object method parameter checks

Claro also checks simple object method arguments when the method body names a parameter with `CHECK TYPE`. This keeps the method syntax beginner-readable while giving a clearer error before the program runs:

```claro
CLASS Player
    HAS score NUMBER

    TEACH add points
        CHECK TYPE points IS NUMBER
        SET score score + points
    END
END

NEW Player player
DO player.add 5
```

If the learner passes text where the method expects a number:

```claro
DO player.add "five"
```

Output:

```text
Type mismatch for method Player.add: parameter points needs NUMBER, but this argument looks like TEXT.
```

If the learner forgets a checked method argument, `claro typecheck` also names the missing method parameter and expected type:

```claro
DO player.add
```

Output:

```text
Method Player.add needs argument points as NUMBER, but this call does not provide it.
```

If the learner gives too many arguments to a simple checked method, `claro typecheck` now points to the extra argument instead of silently accepting it:

```claro
DO player.add 5, 6
```

Output:

```text
Method Player.add only accepts 1 argument, but this call gives 2. Remove the extra argument.
```

Both sides of this narrow method foundation are covered by validation: `tests/typecheck_method_good.claro` checks that `DO player.add 5` is accepted, `tests/typecheck_method_bad.claro` checks the friendly wrong-type diagnostic, `tests/typecheck_method_missing_arg_bad.claro` checks the missing checked-argument diagnostic, and `tests/typecheck_method_extra_arg_bad.claro` checks the extra-argument diagnostic.

If the method call comes before the object is created, the type checker now gives the learner the missing setup step. The modern `DO` form and the older compatibility `CALL ... WITH` form both get this guidance, even when the method name is also a typo:

```claro
CLASS Player
    HAS score NUMBER

    TEACH add points
        CHECK TYPE points IS NUMBER
        SET score score + points
    END
END

DO player.add 5
CALL player.add WITH 5
CALL player.fly WITH 5
```

Output:

```text
Object player is not known yet. Create it with NEW ClassName player before calling player.add.
Object player is not known yet. Create it with NEW ClassName player before calling player.fly.
```

If the object exists but the class does not declare the method, Claro now names the class and suggests where to add the missing `TEACH` block:

```claro
DO player.fly 5
```

Output:

```text
Object Player has no method fly. Check the method name or add TEACH fly inside CLASS Player.
```

## Object field assignment checks

Claro also has a narrow static diagnostic for direct object-field assignments. If a class declares a typed field and a script creates a simple object with `NEW Class name`, `claro typecheck` remembers the field type:

```claro
CLASS Player
    HAS score NUMBER
END

NEW Player player
SET player.score 10
```

If a learner assigns the wrong value type directly to that known field:

```claro
SET player.score "ten"
```

Output:

```text
Type mismatch for field player.score: expected NUMBER, but this value looks like TEXT.
```

If a learner assigns to a field the class did not declare, `claro typecheck` now names the object class and suggests the matching `HAS` line:

```claro
CLASS Player
    HAS score NUMBER
END

NEW Player player
SET player.level 3
```

Output:

```text
Object Player has no field level. Check the field name or add HAS level NUMBER to the class.
```

The unknown-field hint uses the value type it can see. Text-valued and YESNO-valued typos such as `SET player.nickname "Ace"` and `SET player.ready YES` are covered separately:

```text
Object Player has no field nickname. Check the field name or add HAS nickname TEXT to the class.
Object Player has no field ready. Check the field name or add HAS ready YESNO to the class.
```

When the value is an expression whose type is not known yet, Claro now avoids the internal `ANY` placeholder and gives a plain next step instead:

```text
Object Player has no field level. Check the field name or add the field to the class with the right type.
```

Direct `CHECK TYPE` on an undeclared field uses the expected type from the check in its suggestion:

```claro
CHECK TYPE player.level IS NUMBER
```

Output:

```text
Object Player has no field level. Check the field name or add HAS level NUMBER to the class.
```

TEXT expectations use the same learner-facing pattern:

```claro
CHECK TYPE player.nickname IS TEXT
```

Output:

```text
Object Player has no field nickname. Check the field name or add HAS nickname TEXT to the class.
```

YESNO expectations are covered too:

```claro
CHECK TYPE player.enabled IS YESNO
```

Output:

```text
Object Player has no field enabled. Check the field name or add HAS enabled YESNO to the class.
```

If the object itself has not been created yet, the diagnostic points to the missing `NEW` step:

```claro
CHECK TYPE player.score IS NUMBER
```

Output:

```text
Object player is not known yet. Create it with NEW ClassName player before checking player.score.
```

Direct field assignment before `NEW` is checked with the same beginner-first guidance:

```claro
SET player.score 10
```

Output:

```text
Object player is not known yet. Create it with NEW ClassName player before setting player.score.
```

Both sides of this narrow field foundation are covered by validation: `tests/typecheck_object_field_good.claro` checks that `SET player.score 10` is accepted for a `HAS score NUMBER` field, `tests/typecheck_object_field_text_good.claro` checks that `SET player.name "Ada"` is accepted for a `HAS name TEXT` field, `tests/typecheck_object_field_yesno_good.claro` checks that `SET player.ready YES` is accepted for a `HAS ready YESNO` field, `tests/typecheck_object_field_unknown_object_bad.claro` checks that `SET player.score 10` before `NEW Player player` reports the missing-object assignment diagnostic, `tests/typecheck_object_field_check_type_unknown_object_bad.claro` checks the matching missing-object `CHECK TYPE` diagnostic, and the remaining object-field fixtures cover known-field mismatches, unknown NUMBER/TEXT/YESNO fields, and unknown-field assignments whose value type is not inferable yet.

This slice is intentionally small: it covers direct `NEW Class object` plus `SET object.field value` cases in one file. Broader object flows, aliases, method return checks, and richer object signatures remain future work.

## Status

This is currently a static checker feature. It improves `claro typecheck` and validation confidence for `DO` and compatibility `CALL ... WITH` function calls, simple `DO object.method ...` calls where the object was created with `NEW Class name`, and direct assignments to known object fields. Runtime enforcement for every container mutation and richer function/object signatures can be added later after the syntax is classroom-tested.
