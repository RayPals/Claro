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

Both sides of this narrow method foundation are covered by validation: `tests/typecheck_method_good.claro` checks that `DO player.add 5` is accepted, and `tests/typecheck_method_bad.claro` checks the friendly wrong-type diagnostic.

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

Both sides of this narrow field foundation are covered by validation: `tests/typecheck_object_field_good.claro` checks that `SET player.score 10` is accepted for a `HAS score NUMBER` field, `tests/typecheck_object_field_text_good.claro` checks that `SET player.name "Ada"` is accepted for a `HAS name TEXT` field, `tests/typecheck_object_field_yesno_good.claro` checks that `SET player.ready YES` is accepted for a `HAS ready YESNO` field, `tests/typecheck_object_field_check_type_number_good.claro` checks that direct `CHECK TYPE player.score IS NUMBER` metadata is accepted, `tests/typecheck_object_field_check_type_text_good.claro` checks the dedicated direct `CHECK TYPE player.name IS TEXT` metadata path, `tests/typecheck_object_field_check_type_text_yesno_good.claro` keeps combined TEXT/YESNO metadata checks covered, `tests/typecheck_object_field_check_type_number_bad.claro` checks that `CHECK TYPE player.score IS TEXT` reports the NUMBER metadata mismatch, `tests/typecheck_object_field_check_type_text_bad.claro` checks that `CHECK TYPE player.name IS NUMBER` reports the TEXT metadata mismatch, `tests/typecheck_object_field_check_type_yesno_bad.claro` checks that `CHECK TYPE player.ready IS TEXT` reports the YESNO metadata mismatch, `tests/typecheck_object_field_check_type_unknown_number_bad.claro` checks that `CHECK TYPE player.level IS NUMBER` reports the unknown-field metadata diagnostic, `tests/typecheck_object_field_check_type_unknown_text_bad.claro` checks that `CHECK TYPE player.nickname IS TEXT` reports the TEXT unknown-field metadata diagnostic, `tests/typecheck_object_field_check_type_unknown_yesno_bad.claro` checks that `CHECK TYPE player.enabled IS YESNO` reports the YESNO unknown-field metadata diagnostic, `tests/typecheck_object_field_check_type_unknown_object_bad.claro` checks that `CHECK TYPE player.score IS NUMBER` before `NEW Player player` reports the missing-object diagnostic, `tests/typecheck_object_field_bad.claro` checks the NUMBER wrong-type diagnostic, `tests/typecheck_object_field_text_bad.claro` checks the TEXT wrong-type diagnostic, `tests/typecheck_object_field_yesno_bad.claro` checks the YESNO wrong-type diagnostic, `tests/typecheck_object_field_unknown_bad.claro` checks a NUMBER-valued unknown-field hint, `tests/typecheck_object_field_unknown_text_bad.claro` checks a TEXT-valued unknown-field hint, `tests/typecheck_object_field_unknown_yesno_bad.claro` checks a YESNO-valued unknown-field hint, and `tests/37_object_field_types.claro` keeps the runtime object-field example passing.

This slice is intentionally small: it covers direct `NEW Class object` plus `SET object.field value` cases in one file. Broader object flows, aliases, method return checks, and richer object signatures remain future work.

## Status

This is currently a static checker feature. It improves `claro typecheck` and validation confidence for `DO` and compatibility `CALL ... WITH` function calls, simple `DO object.method ...` calls where the object was created with `NEW Class name`, and direct assignments to known object fields. Runtime enforcement for every container mutation and richer function/object signatures can be added later after the syntax is classroom-tested.
