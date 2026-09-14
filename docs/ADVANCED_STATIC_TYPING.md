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

## Nested container values

A typed list can contain a typed map. `claro typecheck` keeps the map's own type metadata while checking the outer list:

```claro
SET people AS LIST OF MAP TO LIST
SET person AS MAP OF TEXT TO MAP
PUT person KEY "name" VALUE "Ada"
ADD person TO people
```

This is accepted with `Type check OK`. More complex nested container operations and full key/value inference remain future work.

## Complete conditional returns

### Return expressions that need more information

When a typed function or method returns a name or expression whose type the focused checker cannot infer yet, `claro typecheck` reports that clearly instead of silently accepting it:

```claro
TEACH square amount RETURNS NUMBER
    RETURN missing
END
```

```text
Function square's return value could not be understood yet. Use a NUMBER expression after RETURN.
```

Use a known typed value, such as a parameter checked with `CHECK TYPE`, while broader expression inference remains future work.

Known NUMBER parameters can also be used in arithmetic return expressions. Numeric division is accepted when both operands are known numbers:

```claro
TEACH halve amount RETURNS NUMBER
    CHECK TYPE amount IS NUMBER
    RETURN amount / 2
END
```

This valid division case is included in the focused typecheck validation matrix beside the diagnostic for using a TEXT operand in division.

Subtraction follows the same rule:

```claro
TEACH difference amount RETURNS NUMBER
    CHECK TYPE amount IS NUMBER
    RETURN amount - 2
END
```

The focused validator checks this positive function case as well as the matching subtraction diagnostic for a TEXT operand.

The same protection applies to object methods. A checked NUMBER parameter can be divided by a number and returned as NUMBER:

```claro
CLASS Player
    TEACH total amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN amount / 2
    END
END
```

This valid method-division case is included in the focused typecheck validation matrix beside the method diagnostic for using a TEXT operand in division.

Return declarations accept the same case-insensitive keyword style as the rest of Claro. For example, `returns NUMBER` still enables return checking:

```claro
TEACH square amount returns NUMBER
    RETURN "oops"
END
```

This reports a normal return mismatch naming `NUMBER` and `TEXT`; capitalization style does not disable the safety check.

The same case-insensitive return declaration rule applies to compatibility methods. A lowercase `returns` still checks the method's `RETURN` value:

```claro
CLASS Player
    TEACH score TAKES amount returns NUMBER
        RETURN "oops"
    LEARNED
END
```

`claro typecheck` reports:

```text
Type mismatch for return from Player.score: expected NUMBER, but this value looks like TEXT.
```

A correct compatibility call also remains valid when the declaration uses lowercase `returns`:

```claro
NEW Player player
CALL player.score WITH 4
```

This success path is included in the focused typecheck validation matrix.

Compatibility methods also keep arithmetic return checks when they use the older
`TAKES` / `LEARNED` spelling. For example, this checked division remains a valid
NUMBER return:

```claro
CLASS Player
    TEACH score TAKES amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN amount / 2
    LEARNED
ENDCLASS
```

This matching `CALL player.score WITH 4` path is included in focused validation.

The same compatibility method return check explains an addition mistake instead of
falling back to a generic return error:

```claro
CLASS Player
    TEACH total TAKES amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN amount + "oops"
    LEARNED
ENDCLASS
```

`claro typecheck` reports:

```text
Type mismatch for return from Player.total: addition needs NUMBER values, but "oops" looks like TEXT.
```

This negative compatibility fixture is part of focused release validation.

Compatibility methods support numeric subtraction in the same focused way:

```claro
CLASS Player
    TEACH score TAKES amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN amount - 2
    LEARNED
ENDCLASS
```

The matching `CALL player.score WITH 4` success path is included in focused validation alongside the modern method subtraction case.

Compatibility methods also keep numeric multiplication return checks. This older
`TAKES` / `LEARNED` spelling accepts a checked NUMBER parameter multiplied by a
number and returned as NUMBER:

```claro
CLASS Player
    TEACH score TAKES amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN amount * 2
    LEARNED
ENDCLASS
```

The matching `CALL player.score WITH 4` success path is included in focused validation.

Compatibility method division mistakes receive the same operation-specific guidance:

```claro
CLASS Player
    TEACH total TAKES amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN amount / "oops"
    LEARNED
ENDCLASS
```

`claro typecheck` reports:

```text
Type mismatch for return from Player.total: division needs NUMBER values, but "oops" looks like TEXT.
```

This negative compatibility fixture is part of focused release validation.

When a function declares a return type, `claro typecheck` accepts nested conditionals when every branch returns a value of that type:

```claro
TEACH choose flag RETURNS NUMBER
    IF flag
        IF flag
            RETURN 1
        ELSE
            RETURN 2
        END
    ELSE
        RETURN 3
    END
END
```

An incomplete branch still produces a missing-return diagnostic. Deeper control-flow analysis through loops and more complex conditions remains planned.

## Object aliases and field checks

When a simple object is assigned to another variable, `claro typecheck` preserves its class for direct field assignments:

```claro
NEW Player player
SET alias player
SET alias.score 10
```

If the value has the wrong type, the diagnostic names the alias and the expected class field type:

```text
Type mismatch for field alias.score: expected NUMBER, but this value looks like TEXT.
```

This is intentionally limited to simple aliases. Broader object-flow analysis through branches, loops, and complex expressions remains planned.

The same field-assignment check follows a second simple alias. This lets a learner use a more descriptive name without losing the class field type:

```claro
SET backup alias
SET backup.score "ten"
```

Output:

```text
Type mismatch for field backup.score: expected NUMBER, but this value looks like TEXT.
```

This remains limited to direct assignments through simple alias chains; control-flow and complex object-flow analysis are still planned.

Text operands are also identified when they appear in arithmetic expressions assigned to NUMBER fields. The diagnostic names the operator and the text operand, which catches a common beginner mistake such as adding a text field to a number field:

```claro
SET player.score player.name + 1
```

```text
Type mismatch for field player.score: addition needs NUMBER values, but player.name looks like TEXT.
```

Subtraction, multiplication, and division use the same beginner-facing guidance:

```claro
SET player.score player.score - player.name
```

```text
Type mismatch for field player.score: subtraction needs NUMBER values, but player.name looks like TEXT.
```

The same learner-facing result is preserved for multiplication, so the checker does not lose the useful `TEXT` type when the invalid expression uses `*`:

```claro
SET player.score player.score * player.name
```

```text
Type mismatch for field player.score: multiplication needs NUMBER values, but player.name looks like TEXT.
```

Division is covered in the same way:

```claro
SET player.score player.score / player.name
```

```text
Type mismatch for field player.score: division needs NUMBER values, but player.name looks like TEXT.
```

Numeric division remains accepted in a NUMBER field, so the type checker protects both sides of this operator without rejecting a valid beginner expression:

```claro
SET player.score 10
SET player.score player.score / 2
```

This example is included in the focused typecheck validation matrix.

Numeric multiplication is accepted in a NUMBER field as well:

```claro
SET player.score player.score * 2
```

The focused validation matrix keeps this valid arithmetic case beside the multiplication text-operand diagnostic, so a useful expression is not confused with the nearby beginner mistake.

The expression checker now gives operator-specific guidance for known TEXT operands in subtraction, multiplication, and division, including typed method return expressions. Broader expression inference remains future work.

Compatibility methods use the same arithmetic return checks as modern methods. This older spelling is accepted when a checked NUMBER parameter is used in a numeric addition:

```claro
CLASS Player
    TEACH score TAKES amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN amount + 2
    LEARNED
ENDCLASS

NEW Player player
CALL player.score WITH 4
```

The focused validation matrix covers this positive compatibility example alongside subtraction, multiplication, and division.

The same operator-specific diagnostic is covered for older compatibility methods:

```claro
CLASS Player
    TEACH total TAKES amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN amount - "oops"
    LEARNED
ENDCLASS
```

Claro reports:

```text
Type mismatch for return from Player.total: subtraction needs NUMBER values, but "oops" looks like TEXT.
```

This keeps `TAKES` / `LEARNED` lessons aligned with the modern method syntax.

Text concatenation is also accepted when the result is assigned to a TEXT field. This keeps a common beginner pattern type-safe without treating every `+` expression as numeric:

```claro
SET player.name player.name + " Lovelace"
```

The focused typecheck validation matrix covers this positive case beside the existing numeric-expression and text-operand checks.

The same rule works when the literal comes first:

```claro
SET player.name "Ada " + player.name
```

This reverse-order concatenation is also covered by focused validation, so learners can build text from either side without losing the declared `TEXT` field type.

Two TEXT fields can be combined as well:

```claro
SET player.name player.name + player.nickname
```

The focused validation matrix covers this field-to-field form so a learner can build text from named object fields without losing the declared `TEXT` type.

`CHECK TYPE` also preserves TEXT field metadata through the same chained aliases:

```claro
CLASS Player
    HAS name TEXT
END

NEW Player player
SET alias player
SET backup alias
SET player.name "Ada"
CHECK TYPE backup.name IS TEXT
```

This confirms the declared field type without requiring the learner to repeat the original object variable name. The broader limits are unchanged: aliases created through branches, loops, or complex expressions are still planned.

`CHECK TYPE` also follows simple aliases for direct field metadata checks. This includes a second alias, so learners can give an object a more descriptive local name without losing the class field information:

```claro
NEW Player player
SET alias player
SET alias.score 10
CHECK TYPE alias.score IS NUMBER
```

```claro
SET backup alias
CHECK TYPE backup.score IS NUMBER
```

If the requested type is wrong, the diagnostic names the alias and the declared field type:

```text
Type check failed: expected TEXT, but alias.score looks like NUMBER.
```

The same diagnostic remains specific after the second alias:

```claro
SET backup alias
CHECK TYPE backup.score IS TEXT
```

```text
Type check failed: expected TEXT, but backup.score looks like NUMBER.
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

If a learner mistypes a function name, `claro typecheck` now names the unknown function and suggests either checking the spelling or adding a matching `TEACH` block. This is covered for both modern `DO` and older compatibility `CALL ... WITH` calls:

```claro
TEACH square amount
    CHECK TYPE amount IS NUMBER
    SAY amount
END

DO squre 4
CALL squre WITH 4
```

Each form reports the same beginner-facing fix:

```text
Function squre is not known yet. Check the function name or add TEACH squre before calling it.
```

## Function and method return checks

Simple functions and object methods can declare a return type with `RETURNS TYPE`. `claro typecheck` checks each simple `RETURN` expression before the program runs:

```claro
CLASS Player
    TEACH score amount RETURNS NUMBER
        RETURN amount
    END
END

NEW Player player
DO player.score 4
```

Returning text from this method produces a learner-facing diagnostic that names the class and method:

```text
Type mismatch for return from Player.score: expected NUMBER, but this value looks like TEXT.
```

If a method's return expression is not understood yet, the diagnostic names the method and gives the promised type so the learner knows what to replace:

```claro
CLASS Player
    TEACH square amount RETURNS NUMBER
        CHECK TYPE amount IS NUMBER
        RETURN missing
    END
END
```

```text
Method Player.square's return value could not be understood yet. Use a NUMBER expression after RETURN.
```

Methods can also return a typed field declared by their class. A field is available by its simple name inside the method, so `RETURN score` is checked against `HAS score NUMBER` instead of being treated as an unknown expression. Returning that field from a method declared `RETURNS TEXT` reports the same expected-versus-found diagnostic.

This is a focused check for simple return expressions. When a parameter has a `CHECK TYPE` declaration, that known type also informs arithmetic return expressions in functions and methods, so `RETURN amount + 1` is checked against the declared return type. The `RETURNS` keyword is case-insensitive in both modern and compatibility function forms, so `returns NUMBER` keeps working while learners are still getting used to Claro's capitalization. A declared return with no `RETURN`, or with a `RETURN` only inside an `IF`, gets a beginner-facing message explaining that the function may finish without returning the promised type:

```text
Function choose declares RETURNS NUMBER but does not return a NUMBER value on every path. Add RETURN to each branch or after the conditional.
```

The focused validation matrix covers modern and compatibility syntax, method success and mismatch fixtures, unknown method return expressions, typed field returns, missing returns, and conditional-only returns. It also includes a positive nested `IF`/`ELSE` return example inside a method, so a complete nested method path is protected from regression. Full path-sensitive analysis proving that every `IF`/`ELSE` branch returns remains planned.

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

Both sides of this narrow method foundation are covered by validation: `tests/typecheck_method_good.claro` checks that `DO player.add 5` is accepted, `tests/typecheck_method_bad.claro` checks the friendly wrong-type diagnostic, `tests/typecheck_method_missing_arg_bad.claro` checks the missing checked-argument diagnostic, and `tests/typecheck_method_extra_arg_bad.claro` checks the extra-argument diagnostic. Multi-method class examples are covered too, including the extra-argument case where the checked method appears after another method in the same class. A compatibility `CALL second.add WITH 5, 6` through a two-step alias is also covered by `tests/typecheck_object_alias_method_call_extra_arg_bad.claro`, preserving the same actionable extra-argument message for older lessons.

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

If the object exists but the class does not declare the method, Claro now names the class and suggests where to add the missing `TEACH` block. This is validated for the modern `DO player.fly 5` form and the older compatibility `CALL player.fly WITH 5` form:

```claro
DO player.fly 5
CALL player.fly WITH 5
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

Simple expressions are checked too. Text joined with a number has a `TEXT` result, so this mistake is caught before running the program:

```claro
SET player.name "Ada"
SET player.score player.name + 1
```

```text
Type mismatch for field player.score: expected NUMBER, but this value looks like TEXT.
```

The reverse mismatch is checked as well. A numeric expression cannot be stored in a `TEXT` field:

```claro
SET player.score 10
SET player.name player.score + 1
```

```text
Type mismatch for field player.name: expected TEXT, but this value looks like NUMBER.
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

This slice is intentionally small: it covers direct `NEW Class object` plus `SET object.field value` cases in one file. Field declarations are collected even when a learner writes a simple method before a later `HAS` field, so the type checker can still report the field's declared type. Broader object flows, aliases, method return checks, and richer object signatures remain future work.

Simple functions also get an arity check before running. If a learner defines `TEACH greet name` and then writes `DO greet` without the `name` argument, `claro typecheck` reports:

```text
Function greet needs 1 argument, but this call gives 0. Add the missing argument.
```

The older compatibility spelling gets the same beginner-facing result when `WITH` is left empty:

```claro
CALL greet WITH
```

Output:

```text
Function greet needs 1 argument, but this call gives 0. Add the missing argument.
```

The same method-aware diagnostic is used when a method directly assigns the wrong value to a class field. For example, `SET name 123` inside `Player.rename` reports `Type mismatch for field name in Player.rename: expected TEXT, but this value looks like NUMBER.` The operator-specific form also remains available: `SET score score + name` inside `Player.add RETURNS NUMBER` reports `Type mismatch for field score in Player.add: addition needs NUMBER values, but name looks like TEXT.` YESNO fields use the same clear method context: assigning text to `HAS ready YESNO` inside `Player.toggle` reports `Type mismatch for field ready in Player.toggle: expected YESNO, but this value looks like TEXT.` Both modern `DO` and compatibility `CALL ... WITH` method forms are covered by the focused validation matrix. These focused checks cover typed method bodies; broader control-flow and object-flow analysis remains planned.

## Status

This is currently a static checker feature. It improves `claro typecheck` and validation confidence for `DO` and compatibility `CALL ... WITH` function calls, simple `DO object.method ...` calls where the object was created with `NEW Class name`, and direct assignments to known object fields. Runtime enforcement for every container mutation and richer function/object signatures can be added later after the syntax is classroom-tested.

Method-body field assignments are covered in both modern and compatibility syntax, including a valid YESNO assignment through `TEACH toggle TAKES value` and `CALL player.toggle WITH YES`. Method-body `CHECK TYPE` metadata has the same balanced coverage: a modern `DO player.toggle YES` example and the compatibility `CALL` example both verify a declared YESNO field. The focused release validator keeps these positive examples beside the wrong-type diagnostics.
