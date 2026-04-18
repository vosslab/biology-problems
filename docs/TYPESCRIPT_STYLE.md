# TYPESCRIPT_STYLE.md

Language Model guide to Neil TypeScript programming

## TypeScript version

* I like using a recent stable version of TypeScript, but not the absolute newest on day one.
* Prefer modern TypeScript with strict type checking enabled.

## FILENAMES
* Prefer snake_case for TypeScript filenames.
* Avoid CamelCase in filenames. Reserve CamelCase for class names, type names, and interface names.
* Keep filenames descriptive, and consistent with the primary thing the file provides.
* Use only lowercase letters, numbers, and underscores in filenames.

## CODE STRUCTURE

* Use small, single-task functions rather than one large function.
* Prefer explicit named functions over deeply nested inline callbacks.
* Keep top-level code minimal.
* Prefer clear data flow with explicit parameters and return values.
* Avoid hidden shared state when possible.
* For scripts, use a `main()` function and call it at the bottom.
* For library code, export small focused functions.
* Use `async` and `await` rather than raw promise chains when possible.
* Avoid broad `try/catch` blocks when possible. I find they often hide bugs.
* Use `try/catch` rarely, and keep the scope small.
* Throw `Error` objects rather than returning silent failure values.
* Return statements should be simple and should not build large objects or long strings inline. Store computed values first, then return the variable.
* Add comments within the code to describe what different lines are doing, especially for complex lines.
* Please only use ASCII characters in the script. If special characters are needed in output, escape them when appropriate.

## STRICT TYPES

* Use TypeScript because the type system is useful, so use it.
* Prefer explicit parameter types and return types for exported functions.
* Add type annotations when they improve clarity.
* Avoid `any` whenever possible.
* Prefer narrow types over loose types.
* Prefer `unknown` over `any` when the type is truly unknown.
* Prefer simple inline object types or named `type` aliases.
* Use `interface` only when it clearly improves readability or extension.

### Good

```ts
function greaterThan(a: number, b: number): boolean {
	return a > b;
}
```

### Avoid

```ts
function processData(data: any): any {
	return data;
}
```

## CONST, LET, AND VAR

* Never use `var`.
* Prefer `const` by default.
* Use `let` only when reassignment is actually needed.

## FUNCTIONS

* Prefer `function name()` for most named functions.
* Be conservative with arrow functions.
* Arrow functions are fine for short callbacks when the logic is obvious.
* If the callback is doing real work, give it a name with `function`.
* If a function would be hard to understand without a comment, rewrite it more clearly.

### Allowed

```ts
const valuesSorted = values.sort((a, b) => a.count - b.count);
```

### Preferred rewrite for more complex logic

```ts
function compareCounts(a: Item, b: Item): number {
	const diff = a.count - b.count;
	return diff;
}

const valuesSorted = values.sort(compareCounts);
```

## CLASSES

* Use classes only when they clearly match the problem.
* Prefer plain functions and plain objects for simple scripts and data transformations.
* Do not introduce classes just to look object-oriented.

## OBJECTS AND DATA

* Prefer plain objects for structured data.
* Keep object shapes consistent.
* Avoid adding properties to objects far away from where the objects are created.
* Prefer building a complete object in one place when practical.

## NULL AND UNDEFINED

* Be explicit about optional values.
* Use `undefined` consistently for missing values unless there is a strong reason to use `null`.
* Do not mix both without a clear reason.

## STRINGS

* Use template strings when interpolation helps readability.
* Prefer simple string assembly over overly clever helpers.
* Keep multiline text readable, but avoid unnecessary complexity.

## QUOTING

* Avoid backslash escaping quotes inside strings when possible.
* Prefer alternating quote styles instead.
* Use double quotes on the outside with single quotes inside.
* Or use single quotes on the outside with double quotes inside.
* This is especially useful for HTML like `"<span style='color: red'>text</span>"`.

## ARRAYS

* Prefer array methods when they improve clarity.
* Do not chain too many methods if it hurts readability.
* If `map().filter().reduce()` becomes hard to read, break it into steps.

## ASYNC CODE

* Prefer `async` and `await`.
* Keep async flow easy to follow.
* Avoid mixing `await` with `.then()` in the same block unless there is a clear reason.
* For network requests, be polite to servers. Add a small delay when appropriate unless the official API says otherwise.

## IMPORTS

* Never use wildcard imports.
* Prefer explicit imports.
* Keep imports grouped and ordered.
* Standard library or platform imports first, then external packages, then local modules.
* Within each group, keep the order consistent and easy to scan.

### Example

```ts
import fs from "node:fs";
import path from "node:path";

import yaml from "js-yaml";

import { readConfig } from "./read_config";
import { writeReport } from "./write_report";
```

## EXPORTS

* Prefer named exports over default exports.
* Named exports are easier to track and refactor.

## ERROR HANDLING

* Do not swallow errors.
* If an error matters, raise it clearly.
* Keep `try/catch` blocks narrow.
* Add useful context to thrown errors when needed.

## COMMENTING

* Use comments to explain why, not to restate obvious code.
* Visually separate major functions with a comment of only equal signs when it helps readability. For example:

```ts
//============================================
```

* Keep line lengths less than 100 characters.
* Comments should be on a line of their own before the code they are commenting.
* No emoji or special characters in comments, only ASCII characters.

## TESTING

* I like to test the code.
* For small utility functions, a short simple test is good.
* For real projects, use a normal test framework and keep tests in a `tests/` folder.
* Keep tests small and deterministic.
* Avoid network calls, random behavior, and time-based logic unless mocked.

## FORMATTERS AND LINTERS

* Use Prettier for formatting. Let Prettier own whitespace, semicolons, and line breaks.
* Use ESLint for catching real bugs: unused variables, implicit `any`, unreachable code.
* Do not fight Prettier on style choices. If Prettier formats it, that is the style.
* ESLint rules should catch problems, not enforce cosmetic preferences that Prettier already handles.
* Strict typing is preferred. Enable `noImplicitAny` and `strict` in `tsconfig.json`.

## CONFIGURATION

* The program should not require custom environment variables to function.
* Configuration must be explicit and visible via config files or command line arguments.
* Environment variables may be read only when they are standard OS or ecosystem variables, not variables invented to control program behavior.

## ARGUMENT PARSING

* Be conservative. Only add arguments users frequently need to change between runs.
* Good candidates:
  - Input and output file paths
  - Mode switches
  - Behavior toggles
* Hardcode minor internal settings instead of turning everything into a flag.
* If a script needs CLI parsing, keep it small and readable.

## DATA FILES

* YAML favorite, readable, editable
* CSV spreadsheet input and output
* JSON good for larger structured data
* PNG images, graphics, figures, pixel data

## GENERAL STYLE

* Prefer plain language in names and comments.
* Keep the code easy to scan.
* Avoid clever code when a direct version is easier to read.
* I want code that is easy to maintain later, not code that tries to impress people.
