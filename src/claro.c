/*
 * CLARO - Programming for Everyone
 * An accessible scripting language for people with learning disabilities
 *
 * Design principles:
 * - CAPITALIZED keywords for clarity
 * - Natural English-like syntax
 * - Helpful error messages
 * - Visual feedback with colors
 * - Game development ready
 * - Portable ANSI C
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <time.h>
#ifdef _WIN32
  #define strcasecmp _stricmp
#else
  #include <strings.h>
#endif

/* ============================================================================
 * CONFIGURATION
 * ============================================================================ */

#define MAX_LINE_LENGTH  512
#define MAX_VARIABLES    200
#define MAX_FUNCTIONS    100
#define MAX_CODE_LINES  2000
#define MAX_PARAMS        10
#define MAX_SPRITES       50

/* ANSI color codes */
#define COLOR_RESET   "\x1b[0m"
#define COLOR_GREEN   "\x1b[32m"
#define COLOR_RED     "\x1b[31m"
#define COLOR_YELLOW  "\x1b[33m"
#define COLOR_BLUE    "\x1b[34m"
#define COLOR_MAGENTA "\x1b[35m"
#define COLOR_CYAN    "\x1b[36m"

/* High contrast mode */
#define HC_RESET  "\x1b[0m"
#define HC_GREEN  "\x1b[97;42m"
#define HC_RED    "\x1b[97;41m"
#define HC_YELLOW "\x1b[30;43m"

/* ============================================================================
 * DATA STRUCTURES
 * ============================================================================ */

typedef enum {
    TYPE_NUMBER,
    TYPE_TEXT,
    TYPE_YES_NO   /* Boolean - friendlier for beginners */
} VarType;

typedef struct {
    char name[MAX_LINE_LENGTH];
    VarType type;
    union {
        double number;
        char   text[MAX_LINE_LENGTH];
        int    yes_no;   /* 1 = YES, 0 = NO */
    } value;
} Variable;

typedef struct {
    char name[MAX_LINE_LENGTH];
    char params[MAX_PARAMS][MAX_LINE_LENGTH];
    int  param_count;
    char code[MAX_CODE_LINES][MAX_LINE_LENGTH];
    int  code_line_count;
} Function;

typedef struct {
    char name[MAX_LINE_LENGTH];
    int  x, y;
    int  width, height;
    int  visible;
    char image[MAX_LINE_LENGTH];
} Sprite;

typedef struct {
    Variable vars[MAX_VARIABLES];
    int      var_count;

    Function funcs[MAX_FUNCTIONS];
    int      func_count;

    Sprite   sprites[MAX_SPRITES];
    int      sprite_count;

    int      high_contrast;
    int      line_number;
    int      in_function;
    double   return_value;
    int      should_return;


    VarType  return_type;
    char     return_text[MAX_LINE_LENGTH];
    char     current_function[MAX_LINE_LENGTH];
    int      call_depth;
    /* Debug / step mode */
    int      debug_mode;
} Runtime;

static Runtime runtime;

/* ============================================================================
 * UTILITY FUNCTIONS
 * ============================================================================ */

char *trim(char *str) {
    char *end;
    while (isspace((unsigned char)*str)) str++;
    if (*str == 0) return str;
    end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) end--;
    end[1] = '\0';
    return str;
}

void to_upper(char *str) {
    for (; *str; ++str) *str = toupper((unsigned char)*str);
}

void print_colored(const char *color, const char *msg) {
    if (runtime.high_contrast) {
        if      (strcmp(color, COLOR_RED)    == 0) printf("%s%s%s", HC_RED,    msg, HC_RESET);
        else if (strcmp(color, COLOR_GREEN)  == 0) printf("%s%s%s", HC_GREEN,  msg, HC_RESET);
        else if (strcmp(color, COLOR_YELLOW) == 0) printf("%s%s%s", HC_YELLOW, msg, HC_RESET);
        else                                        printf("%s",     msg);
    } else {
        printf("%s%s%s", color, msg, COLOR_RESET);
    }
}

/* ============================================================================
 * ERROR HANDLING
 * ============================================================================ */

void error_message(const char *message, const char *help) {
    print_colored(COLOR_RED, "\n*** OOPS! ***\n");
    printf("Line %d: %s\n", runtime.line_number, message);
    if (runtime.call_depth > 0 && strlen(runtime.current_function) > 0) {
        print_colored(COLOR_MAGENTA, "In function: ");
        printf("%s\n", runtime.current_function);
    }
    if (help && strlen(help) > 0) {
        print_colored(COLOR_YELLOW, "Tip: ");
        printf("%s\n\n", help);
    }
}


/* ============================================================================
 * SPELL-CHECK / "DID YOU MEAN?" HELPER
 * ============================================================================ */

static int levenshtein(const char *s1, const char *s2) {
    int l1 = (int)strlen(s1), l2 = (int)strlen(s2);
    int dp[l1+1][l2+1];
    for (int i = 0; i <= l1; i++) dp[i][0] = i;
    for (int j = 0; j <= l2; j++) dp[0][j] = j;
    for (int i = 1; i <= l1; i++)
        for (int j = 1; j <= l2; j++) {
            int cost = (toupper(s1[i-1]) == toupper(s2[j-1])) ? 0 : 1;
            dp[i][j] = dp[i-1][j]+1;
            if (dp[i][j-1]+1   < dp[i][j]) dp[i][j] = dp[i][j-1]+1;
            if (dp[i-1][j-1]+cost < dp[i][j]) dp[i][j] = dp[i-1][j-1]+cost;
        }
    return dp[l1][l2];
}

void suggest_command(const char *bad_cmd) {
    static const char *commands[] = {
        "SAY","SET","ASK","IF","ELSE","ENDIF",
        "REPEAT","UNTIL","DO","TIMES","DONE",
        "TEACH","LEARNED","CALL","RETURN",
        "WAIT","HELP","EXIT","VARS","DEBUG",
        "CREATE","MOVE","SHOW","HIDE",
        NULL
    };
    int   best_dist  = 999;
    const char *best = NULL;
    char upper[MAX_LINE_LENGTH];
    strncpy(upper, bad_cmd, MAX_LINE_LENGTH-1);
    to_upper(upper);
    for (int i = 0; commands[i]; i++) {
        int d = levenshtein(upper, commands[i]);
        if (d < best_dist && d <= 2) { best_dist = d; best = commands[i]; }
    }
    if (best) {
        print_colored(COLOR_YELLOW, "Did you mean: ");
        print_colored(COLOR_GREEN, best);
        printf("?\n");
    }
}

/* ============================================================================
 * VARIABLE STORE
 * ============================================================================ */

Variable *find_var(const char *name) {
    for (int i = 0; i < runtime.var_count; i++)
        if (strcasecmp(runtime.vars[i].name, name) == 0)
            return &runtime.vars[i];
    return NULL;
}

Variable *get_or_create_var(const char *name) {
    Variable *v = find_var(name);
    if (v) return v;
    if (runtime.var_count >= MAX_VARIABLES) {
        error_message("Too many variables!", "Remove some variables you no longer need.");
        return NULL;
    }
    v = &runtime.vars[runtime.var_count++];
    memset(v, 0, sizeof(Variable));
    strncpy(v->name, name, MAX_LINE_LENGTH-1);
    return v;
}

void set_number(const char *name, double val) {
    Variable *v = get_or_create_var(name);
    if (!v) return;
    v->type          = TYPE_NUMBER;
    v->value.number  = val;
}

void set_text(const char *name, const char *val) {
    Variable *v = get_or_create_var(name);
    if (!v) return;
    v->type = TYPE_TEXT;
    strncpy(v->value.text, val, MAX_LINE_LENGTH-1);
}

void set_yes_no(const char *name, int val) {
    Variable *v = get_or_create_var(name);
    if (!v) return;
    v->type         = TYPE_YES_NO;
    v->value.yes_no = val;
}

/* ============================================================================
 * EXPRESSION EVALUATOR
 * ============================================================================ */

/* -------------------------------------------------
 * Number expressions
 * Supports:
 *   - +, -, *, / with normal precedence
 *   - parentheses: ( ... )
 *   - variables (NUMBER / YES-NO treated as 0/1)
 *   - functions: SQRT(x), ABS(x), ROUND(x), FLOOR(x), CEIL(x)
 *   - RANDOM n   (1..n)
 * ------------------------------------------------- */

typedef struct {
    const char *s;
    int pos;
    int had_error;
} NumParser;

static void np_skip_ws(NumParser *p) {
    while (p->s[p->pos] && isspace((unsigned char)p->s[p->pos])) p->pos++;
}

static int np_peek(NumParser *p) {
    np_skip_ws(p);
    return (unsigned char)p->s[p->pos];
}

static int np_match(NumParser *p, char c) {
    np_skip_ws(p);
    if (p->s[p->pos] == c) { p->pos++; return 1; }
    return 0;
}

static void np_set_error(NumParser *p, const char *msg, const char *tip) {
    if (!p->had_error) {
        error_message(msg, tip);
        p->had_error = 1;
    }
}

static double np_parse_expr(NumParser *p);  /* forward */

static int np_parse_identifier(NumParser *p, char out[MAX_LINE_LENGTH]) {
    np_skip_ws(p);
    int i = 0;
    if (!isalpha((unsigned char)p->s[p->pos]) && p->s[p->pos] != '_') return 0;
    while (p->s[p->pos] && (isalnum((unsigned char)p->s[p->pos]) || p->s[p->pos] == '_')) {
        if (i < MAX_LINE_LENGTH-1) out[i++] = p->s[p->pos];
        p->pos++;
    }
    out[i] = '\0';
    return 1;
}

static double np_parse_factor(NumParser *p) {
    np_skip_ws(p);

    /* unary + / - */
    if (np_match(p, '+')) return np_parse_factor(p);
    if (np_match(p, '-')) return -np_parse_factor(p);

    /* parenthesis */
    if (np_match(p, '(')) {
        double v = np_parse_expr(p);
        if (!np_match(p, ')')) {
            np_set_error(p, "Missing ) in math", "Check your parentheses, like: (2 + 3) * 4");
        }
        return v;
    }

    /* number literal */
    {
        np_skip_ws(p);
        char *endptr = NULL;
        double v = strtod(p->s + p->pos, &endptr);
        if (endptr && endptr != (p->s + p->pos)) {
            p->pos = (int)(endptr - p->s);
            return v;
        }
    }

    /* identifier: variable or function */
    char name[MAX_LINE_LENGTH];
    if (np_parse_identifier(p, name)) {
        char upper[MAX_LINE_LENGTH];
        strncpy(upper, name, MAX_LINE_LENGTH-1);
        upper[MAX_LINE_LENGTH-1] = '\0';
        to_upper(upper);

        /* RANDOM n  (space separated) */
        if (strcmp(upper, "RANDOM") == 0) {
            double n = np_parse_factor(p);
            if (n <= 0) { np_set_error(p, "RANDOM needs a positive number", "Try: RANDOM 10"); return 0; }
            return (double)(rand() % (int)n) + 1;
        }

        /* function call NAME(expr) */
        if (np_match(p, '(')) {
            double a = np_parse_expr(p);
            if (!np_match(p, ')')) {
                np_set_error(p, "Missing ) after function", "Example: SQRT(16)");
            }
            if (strcmp(upper,"SQRT")  == 0) return sqrt(a);
            if (strcmp(upper,"ABS")   == 0) return fabs(a);
            if (strcmp(upper,"ROUND") == 0) return round(a);
            if (strcmp(upper,"FLOOR") == 0) return floor(a);
            if (strcmp(upper,"CEIL")  == 0) return ceil(a);

            np_set_error(p, "Unknown math function", "Try: SQRT(x), ABS(x), ROUND(x), FLOOR(x), CEIL(x)");
            return 0;
        }

        /* variable lookup */
        Variable *v = find_var(name);
        if (v) {
            if (v->type == TYPE_NUMBER) return v->value.number;
            if (v->type == TYPE_YES_NO) return v->value.yes_no;
            np_set_error(p, "That value is not a number", "Use a NUMBER variable in math, like: SET score TO 10");
            return 0;
        }

        np_set_error(p, "Unknown number or variable", "Tip: Use VARS to see your variables");
        return 0;
    }

    /* nothing matched */
    np_set_error(p, "I couldn't understand that math", "Example: 2 + 3 * 4  or  (2 + 3) * 4");
    return 0;
}

static double np_parse_term(NumParser *p) {
    double v = np_parse_factor(p);
    for (;;) {
        if (np_match(p, '*')) {
            v *= np_parse_factor(p);
        } else if (np_match(p, '/')) {
            double r = np_parse_factor(p);
            if (r == 0) {
                np_set_error(p, "Divide by zero", "Make sure the right side is not 0");
                return 0;
            }
            v /= r;
        } else {
            break;
        }
    }
    return v;
}

static double np_parse_expr(NumParser *p) {
    double v = np_parse_term(p);
    for (;;) {
        if (np_match(p, '+')) {
            v += np_parse_term(p);
        } else if (np_match(p, '-')) {
            v -= np_parse_term(p);
        } else {
            break;
        }
    }
    return v;
}

double eval_number_expr(const char *expr_in) {
    NumParser p = { expr_in, 0, 0 };
    double v = np_parse_expr(&p);
    np_skip_ws(&p);
    if (!p.had_error && p.s[p.pos] != '\0') {
        error_message("Extra text in math", "Tip: check for extra words or symbols");
        return 0;
    }
    return v;
}

int eval_yes_no_expr(const char *expr_in) {
    char expr[MAX_LINE_LENGTH];
    strncpy(expr, expr_in, MAX_LINE_LENGTH-1);
    char *e = trim(expr);

    if (strcasecmp(e,"YES")==0 || strcasecmp(e,"TRUE")==0)  return 1;
    if (strcasecmp(e,"NO")==0  || strcasecmp(e,"FALSE")==0) return 0;

    Variable *v = find_var(e);
    if (v && v->type == TYPE_YES_NO) return v->value.yes_no;

    char left[MAX_LINE_LENGTH], op[MAX_LINE_LENGTH], right[MAX_LINE_LENGTH];
    /* Try "left OP right" */
    if (sscanf(e, "%s %s %[^\n]", left, op, right) == 3) {
        to_upper(op);
        if (strcmp(op,"IS")==0 || strcmp(op,"EQUALS")==0) {
            /* String comparison */
            Variable *lv = find_var(left);
            if (lv && lv->type == TYPE_TEXT) {
                char rstr[MAX_LINE_LENGTH];
                strncpy(rstr, right, MAX_LINE_LENGTH-1);
                if (rstr[0]=='"') { memmove(rstr,rstr+1,strlen(rstr)); }
                size_t rl = strlen(rstr);
                if (rl>0 && rstr[rl-1]=='"') rstr[rl-1]='\0';
                return strcasecmp(lv->value.text, rstr) == 0;
            }
            return fabs(eval_number_expr(left) - eval_number_expr(right)) < 0.0001;
        }
        if (strcmp(op,"BIGGER")==0 || strcmp(op,"GREATER")==0)
            return eval_number_expr(left) > eval_number_expr(right);
        if (strcmp(op,"SMALLER")==0 || strcmp(op,"LESS")==0)
            return eval_number_expr(left) < eval_number_expr(right);
        if (strcmp(op,"NOT")==0 && (strcmp(right,"IS")==0 || strcmp(right,"EQUALS")==0)) {
            /* "x NOT IS y" -> not equal */
            char r2[MAX_LINE_LENGTH];
            sscanf(e, "%*s %*s %*s %[^\n]", r2);
            return fabs(eval_number_expr(left) - eval_number_expr(r2)) >= 0.0001;
        }
    }

    /* If it's just a variable holding a number, treat nonzero as YES */
    if (v && v->type == TYPE_NUMBER) return v->value.number != 0;

    return 0;
}

/* ============================================================================
 * COMMAND IMPLEMENTATIONS
 * ============================================================================ */

void execute_line(char *line);
void execute_code(char code[][MAX_LINE_LENGTH], int line_count);
void execute_block(char code[][MAX_LINE_LENGTH], int line_count, int start, int end);


/* SAY */
void cmd_say(char *args) {
    args = trim(args);
    /* Strip surrounding quotes */
    if ((args[0]=='"' || args[0]=='\'') ) {
        size_t len = strlen(args);
        if (len>1 && (args[len-1]=='"' || args[len-1]=='\'')) {
            args[len-1] = '\0';
            args++;
        }
    }
    Variable *v = find_var(args);
    if (v) {
        if (v->type == TYPE_NUMBER) {
            if (floor(v->value.number) == v->value.number)
                printf("%.0f\n", v->value.number);
            else
                printf("%g\n",   v->value.number);
        } else if (v->type == TYPE_TEXT) {
            printf("%s\n", v->value.text);
        } else {
            printf("%s\n", v->value.yes_no ? "YES" : "NO");
        }
    } else {
        printf("%s\n", args);
    }
}

/* SET */
void cmd_set(char *args) {
    char name[MAX_LINE_LENGTH];
    char value[MAX_LINE_LENGTH];

    /* Accept "SET name TO value" (case-insensitive TO) */
    char *to_pos = NULL;
    char upper_args[MAX_LINE_LENGTH];
    strncpy(upper_args, args, MAX_LINE_LENGTH-1);
    to_upper(upper_args);
    to_pos = strstr(upper_args, " TO ");
    if (!to_pos) {
        error_message("Could not understand SET command",
                      "Try: SET score TO 100");
        return;
    }
    int name_len = (int)(to_pos - upper_args);
    strncpy(name, args, name_len);
    name[name_len] = '\0';
    trim(name);
    strncpy(value, args + name_len + 4, MAX_LINE_LENGTH-1);
    trim(value);

    /* Quoted string? */
    if (value[0]=='"' || value[0]=='\'') {
        size_t len = strlen(value);
        if (len>1 && (value[len-1]=='"' || value[len-1]=='\'')) {
            value[len-1] = '\0';
            set_text(name, value+1);
            return;
        }
    }
    /* YES/NO */
    if (strcasecmp(value,"YES")==0 || strcasecmp(value,"TRUE")==0)  { set_yes_no(name,1); return; }
    if (strcasecmp(value,"NO")==0  || strcasecmp(value,"FALSE")==0) { set_yes_no(name,0); return; }
    /* Number / expression */
    set_number(name, eval_number_expr(value));
}

/* ASK */
void cmd_ask(char *args) {
    char name[MAX_LINE_LENGTH], prompt[MAX_LINE_LENGTH];
    if (sscanf(args, "%s %[^\n]", name, prompt) >= 1) {
        if (strlen(prompt) > 0)
            printf("%s ", prompt);
        char input[MAX_LINE_LENGTH];
        if (fgets(input, sizeof(input), stdin)) {
            input[strcspn(input,"\n")] = 0;
            trim(input);
            char *endptr;
            double num = strtod(input, &endptr);
            if (*endptr == '\0')
                set_number(name, num);
            else
                set_text(name, input);
        }
    } else {
        error_message("Could not understand ASK command",
                      "Try: ASK name What is your name?");
    }
}

/* WAIT */
void cmd_wait(char *args) {
    double seconds = eval_number_expr(args);
    if (seconds > 0) {
        clock_t start = clock();
        while ((double)(clock()-start)/CLOCKS_PER_SEC < seconds);
    }
}

/* VARS - display all variables */
void cmd_vars(void) {
    if (runtime.var_count == 0) {
        printf("No variables set yet.\n");
        return;
    }
    print_colored(COLOR_CYAN, "=== Variables ===\n");
    for (int i = 0; i < runtime.var_count; i++) {
        Variable *v = &runtime.vars[i];
        printf("  %-20s = ", v->name);
        if (v->type == TYPE_NUMBER) {
            if (floor(v->value.number)==v->value.number)
                printf("%.0f\n", v->value.number);
            else
                printf("%g\n",   v->value.number);
        } else if (v->type == TYPE_TEXT) {
            printf("\"%s\"\n", v->value.text);
        } else {
            printf("%s\n", v->value.yes_no ? "YES" : "NO");
        }
    }
}

/* HELP */
void cmd_help(char *topic) {
    topic = trim(topic);
    to_upper(topic);

    if (strlen(topic) == 0 || strcmp(topic,"ALL")==0) {
        print_colored(COLOR_GREEN, "\n=== CLARO Commands ===\n\n");
        printf("Showing / Asking:\n");
        printf("  SAY \"text\"          - Show a message\n");
        printf("  SAY variable        - Show a variable's value\n");
        printf("  ASK var What?       - Ask the user a question\n\n");
        printf("Variables:\n");
        printf("  SET var TO value    - Remember something\n");
        printf("  VARS                - Show all variables\n\n");
        printf("Making Decisions:\n");
        printf("  IF condition        - Check something\n");
        printf("    ...\n");
        printf("  ELSE                - Otherwise\n");
        printf("    ...\n");
        printf("  ENDIF               - End the IF block\n\n");
        printf("Repeating:\n");
        printf("  DO 5 TIMES          - Repeat 5 times\n");
        printf("    ...\n");
        printf("  DONE\n\n");
        printf("  REPEAT 5            - Old-style (still works)\n");
        printf("    ...\n");
        printf("  UNTIL\n\n");
        printf("Functions (Reusable Blocks):\n");
        printf("  TEACH name TAKES a, b  - Teach CLARO a new skill\n");
        printf("    ...\n");
        printf("  RETURN value           - Send a value back\n");
        printf("  LEARNED                - End the TEACH block\n\n");
        printf("  CALL name WITH a, b    - Use a function (stores RESULT)\n\n");
        printf("Sprites (Game Objects):\n");
        printf("  CREATE SPRITE name  - Create a game character\n");
        printf("  MOVE SPRITE name TO x y\n");
        printf("  SHOW SPRITE name\n");
        printf("  HIDE SPRITE name\n\n");
        printf("Other:\n");
        printf("  WAIT 2              - Pause for 2 seconds\n");
        printf("  DEBUG ON/OFF        - Toggle debug mode\n");
        printf("  HELP SAY            - Help on a specific command\n");
        printf("  EXIT / QUIT         - Exit CLARO\n\n");
        printf("Comparisons in IF:\n");
        printf("  IS / EQUALS         - Equal?\n");
        printf("  BIGGER / GREATER    - First one larger?\n");
        printf("  SMALLER / LESS      - First one smaller?\n\n");
    } else if (strcmp(topic,"SAY")==0) {
        printf("\nSAY - Show a message or variable\n");
        printf("  SAY \"Hello!\"\n");
        printf("  SAY score\n");
    } else if (strcmp(topic,"SET")==0) {
        printf("\nSET - Store a value in a variable\n");
        printf("  SET score TO 100\n");
        printf("  SET name TO \"Alice\"\n");
        printf("  SET score TO score + 10\n");
    } else if (strcmp(topic,"ASK")==0) {
        printf("\nASK - Get input from the user\n");
        printf("  ASK name What is your name?\n");
        printf("  ASK age How old are you?\n");
    } else if (strcmp(topic,"IF")==0) {
        printf("\nIF - Make a decision\n");
        printf("  IF score IS 100\n");
        printf("      SAY \"Perfect!\"\n");
        printf("  ELSE\n");
        printf("      SAY \"Try again!\"\n");
        printf("  ENDIF\n");
    } else if (strcmp(topic,"REPEAT")==0 || strcmp(topic,"DO")==0) {
        printf("\nDO / REPEAT - Repeat a block\n");
        printf("  DO 5 TIMES\n");
        printf("      SAY \"Hello!\"\n");
        printf("  DONE\n");
    } else if (strcmp(topic,"TEACH")==0) {
        printf("\nTEACH - Define a reusable function\n");
        printf("  TEACH greet TAKES name\n");
        printf("      SAY \"Hello \"\n");
        printf("      SAY name\n");
        printf("      RETURN 1\n");
        printf("  LEARNED\n");
    } else if (strcmp(topic,"CALL")==0) {
        printf("\nCALL - Run a function you taught CLARO\n");
        printf("  CALL greet WITH \"Sam\"\n");
        printf("  SAY RESULT\n");
        printf("\nTip: If you have more than one value, separate them with commas.\n");
    } else if (strcmp(topic,"RETURN")==0) {
        printf("\nRETURN - Send a value back from a function\n");
        printf("  RETURN 42\n");
        printf("  RETURN \"Done!\"\n");
        printf("  RETURN YES\n");
    } else {
        printf("No help found for '%s'. Type HELP for all commands.\n", topic);
    }
}

/* SPRITE commands */
Sprite *find_sprite(const char *name) {
    for (int i = 0; i < runtime.sprite_count; i++)
        if (strcasecmp(runtime.sprites[i].name, name) == 0)
            return &runtime.sprites[i];
    return NULL;
}

void cmd_create_sprite(char *args) {
    char name[MAX_LINE_LENGTH];
    sscanf(args, "%s", name);
    if (find_sprite(name)) {
        printf("Sprite '%s' already exists.\n", name); return;
    }
    if (runtime.sprite_count >= MAX_SPRITES) {
        error_message("Too many sprites!", "Remove some sprites first."); return;
    }
    Sprite *s = &runtime.sprites[runtime.sprite_count++];
    memset(s, 0, sizeof(Sprite));
    strncpy(s->name, name, MAX_LINE_LENGTH-1);
    s->visible = 1; s->width = 32; s->height = 32;
    printf("Sprite '%s' created.\n", name);
}

void cmd_move_sprite(char *args) {
    /* MOVE SPRITE name TO x y */
    char name[MAX_LINE_LENGTH]; int x, y;
    if (sscanf(args, "%s TO %d %d", name, &x, &y) == 3 ||
        sscanf(args, "%s to %d %d", name, &x, &y) == 3) {
        Sprite *s = find_sprite(name);
        if (!s) { error_message("Sprite not found", "Use CREATE SPRITE first"); return; }
        s->x = x; s->y = y;
        printf("Moved '%s' to (%d, %d)\n", name, x, y);
    } else {
        error_message("Could not understand MOVE SPRITE",
                      "Try: MOVE SPRITE player TO 100 200");
    }
}

void cmd_show_sprite(char *args) {
    char name[MAX_LINE_LENGTH]; sscanf(args, "%s", name);
    Sprite *s = find_sprite(name);
    if (!s) { error_message("Sprite not found","Use CREATE SPRITE first"); return; }
    s->visible = 1; printf("Sprite '%s' is now visible.\n", name);
}

void cmd_hide_sprite(char *args) {
    char name[MAX_LINE_LENGTH]; sscanf(args, "%s", name);
    Sprite *s = find_sprite(name);
    if (!s) { error_message("Sprite not found","Use CREATE SPRITE first"); return; }
    s->visible = 0; printf("Sprite '%s' is now hidden.\n", name);
}


/* ============================================================================
 * USER FUNCTIONS (TEACH / CALL / RETURN)
 * ============================================================================ */

Function *find_func(const char *name) {
    for (int i = 0; i < runtime.func_count; i++)
        if (strcasecmp(runtime.funcs[i].name, name) == 0)
            return &runtime.funcs[i];
    return NULL;
}

static void clear_function(Function *f) {
    memset(f, 0, sizeof(Function));
}

static void upsert_function(const Function *src) {
    Function *existing = find_func(src->name);
    if (existing) {
        *existing = *src;
        return;
    }
    if (runtime.func_count >= MAX_FUNCTIONS) {
        error_message("Too many functions!", "Tip: keep your program small, or reuse functions you already have.");
        return;
    }
    runtime.funcs[runtime.func_count++] = *src;
}

static int is_word(const char *w, const char *kw) { return strcasecmp(w, kw) == 0; }

/* Parse: TEACH name [TAKES a, b, c] */
static void parse_teach_header(const char *rest, Function *out) {
    clear_function(out);

    char tmp[MAX_LINE_LENGTH];
    strncpy(tmp, rest, MAX_LINE_LENGTH-1);
    tmp[MAX_LINE_LENGTH-1] = '\0';

    char *p = trim(tmp);

    /* name */
    char name[MAX_LINE_LENGTH] = {0};
    sscanf(p, "%s", name);
    strncpy(out->name, name, MAX_LINE_LENGTH-1);

    /* move past name */
    p = p + strlen(name);
    p = trim(p);

    out->param_count = 0;

    if (*p == 0) return;

    char kw[MAX_LINE_LENGTH] = {0};
    sscanf(p, "%s", kw);
    if (!is_word(kw, "TAKES") && !is_word(kw, "WITH")) return;

    p = trim(p + strlen(kw));
    if (*p == 0) return;

    /* split by commas, otherwise treat as space-separated simple names */
    if (strchr(p, ',')) {
        for (char *tok = strtok(p, ",");
             tok && out->param_count < MAX_PARAMS;
             tok = strtok(NULL, ",")) {
            tok = trim(tok);
            if (*tok == 0) continue;
            /* take first word as param name */
            char param[MAX_LINE_LENGTH] = {0};
            sscanf(tok, "%s", param);
            strncpy(out->params[out->param_count++], param, MAX_LINE_LENGTH-1);
        }
    } else {
        /* space-separated */
        for (char *tok = strtok(p, " \t");
             tok && out->param_count < MAX_PARAMS;
             tok = strtok(NULL, " \t")) {
            tok = trim(tok);
            if (*tok == 0) continue;
            strncpy(out->params[out->param_count++], tok, MAX_LINE_LENGTH-1);
        }
    }
}

/* Scan a code buffer and register any TEACH blocks (functions). */
void parse_functions(char code[][MAX_LINE_LENGTH], int line_count) {
    for (int i = 0; i < line_count; i++) {
        char line_copy[MAX_LINE_LENGTH];
        strncpy(line_copy, code[i], MAX_LINE_LENGTH-1);
        line_copy[MAX_LINE_LENGTH-1] = '\0';
        char *l = trim(line_copy);

        if (strlen(l)==0 || l[0]=='#') continue;

        char cmd[MAX_LINE_LENGTH];
        sscanf(l, "%s", cmd);
        to_upper(cmd);

        if (strcmp(cmd, "TEACH") != 0) continue;

        Function f;
        char *rest = trim(l + strlen(cmd));
        parse_teach_header(rest, &f);

        if (strlen(f.name) == 0) {
            runtime.line_number = i + 1;
            error_message("TEACH needs a function name", "Try: TEACH greet TAKES name");
            continue;
        }

        /* collect lines until LEARNED */
        int start = i + 1;
        int end = start;
        while (end < line_count) {
            char w[MAX_LINE_LENGTH]; w[0] = '\0';
            sscanf(trim(code[end]), "%s", w);
            to_upper(w);
            if (strcmp(w, "LEARNED") == 0) break;
            end++;
        }
        if (end >= line_count) {
            runtime.line_number = i + 1;
            error_message("TEACH without LEARNED", "Add LEARNED at the end of your TEACH block");
            continue;
        }

        f.code_line_count = 0;
        for (int j = start; j < end && f.code_line_count < MAX_CODE_LINES; j++) {
            strncpy(f.code[f.code_line_count], code[j], MAX_LINE_LENGTH-1);
            f.code[f.code_line_count][MAX_LINE_LENGTH-1] = '\0';
            f.code_line_count++;
        }

        upsert_function(&f);

        /* skip past this function block */
        i = end;
    }
}

static void set_result_from_return(void) {
    if (runtime.return_type == TYPE_TEXT) {
        set_text("RESULT", runtime.return_text);
    } else if (runtime.return_type == TYPE_YES_NO) {
        set_yes_no("RESULT", runtime.return_value != 0.0);
    } else {
        set_number("RESULT", runtime.return_value);
    }
}

static void parse_value(const char *expr, VarType *out_type, double *out_num, char *out_text) {
    char tmp[MAX_LINE_LENGTH];
    strncpy(tmp, expr, MAX_LINE_LENGTH-1);
    tmp[MAX_LINE_LENGTH-1] = '\0';
    char *t = trim(tmp);

    if (strlen(t) == 0) { *out_type = TYPE_NUMBER; *out_num = 0; out_text[0] = '\0'; return; }

    /* quoted text */
    if ((t[0] == '"' && t[strlen(t)-1] == '"') || (t[0] == '\'' && t[strlen(t)-1] == '\'')) {
        *out_type = TYPE_TEXT;
        t[strlen(t)-1] = '\0';
        strncpy(out_text, t+1, MAX_LINE_LENGTH-1);
        out_text[MAX_LINE_LENGTH-1] = '\0';
        return;
    }

    /* YES/NO */
    char up[MAX_LINE_LENGTH];
    strncpy(up, t, MAX_LINE_LENGTH-1);
    up[MAX_LINE_LENGTH-1] = '\0';
    to_upper(up);
    if (strcmp(up, "YES") == 0 || strcmp(up, "NO") == 0) {
        *out_type = TYPE_YES_NO;
        *out_num = (strcmp(up, "YES") == 0) ? 1.0 : 0.0;
        out_text[0] = '\0';
        return;
    }

    /* variable reference (text/bool) */
    Variable *v = find_var(t);
    if (v && v->type == TYPE_TEXT) {
        *out_type = TYPE_TEXT;
        strncpy(out_text, v->value.text, MAX_LINE_LENGTH-1);
        out_text[MAX_LINE_LENGTH-1] = '\0';
        return;
    }
    if (v && v->type == TYPE_YES_NO) {
        *out_type = TYPE_YES_NO;
        *out_num = v->value.yes_no ? 1.0 : 0.0;
        out_text[0] = '\0';
        return;
    }

    /* fallback: number expression */
    *out_type = TYPE_NUMBER;
    *out_num = eval_number_expr(t);
    out_text[0] = '\0';
}

/* CALL name [WITH arg1, arg2, ...] */
void cmd_call(char *args) {
    char tmp[MAX_LINE_LENGTH];
    strncpy(tmp, args, MAX_LINE_LENGTH-1);
    tmp[MAX_LINE_LENGTH-1] = '\0';
    char *t = trim(tmp);

    if (strlen(t) == 0) {
        error_message("CALL needs a function name", "Try: CALL greet WITH \"Sam\"");
        return;
    }

    char fname[MAX_LINE_LENGTH] = {0};
    sscanf(t, "%s", fname);

    Function *f = find_func(fname);
    if (!f) {
        char msg[MAX_LINE_LENGTH];
        snprintf(msg, sizeof(msg), "I don't know how to '%s' yet.", fname);
        error_message(msg, "Tip: Define it first with TEACH ... LEARNED");
        return;
    }

    /* move past name */
    t = trim(t + strlen(fname));

    /* optional WITH/USING */
    char kw[MAX_LINE_LENGTH] = {0};
    char *arg_str = t;
    if (strlen(arg_str) > 0) {
        sscanf(arg_str, "%s", kw);
        to_upper(kw);
        if (strcmp(kw,"WITH")==0 || strcmp(kw,"USING")==0) {
            arg_str = trim(arg_str + strlen(kw));
        }
    }

    /* parse args */
    char argbuf[MAX_LINE_LENGTH];
    strncpy(argbuf, arg_str, MAX_LINE_LENGTH-1);
    argbuf[MAX_LINE_LENGTH-1] = '\0';
    char *ab = trim(argbuf);

    char *argv[MAX_PARAMS];
    int argc = 0;

    if (strlen(ab) == 0) {
        argc = 0;
    } else if (strchr(ab, ',')) {
        for (char *tok = strtok(ab, ",");
             tok && argc < MAX_PARAMS;
             tok = strtok(NULL, ",")) {
            tok = trim(tok);
            if (*tok == 0) continue;
            argv[argc++] = tok;
        }
    } else {
        /* single argument (may contain spaces / expressions) */
        argv[argc++] = ab;
    }

    if (argc != f->param_count) {
        char msg[MAX_LINE_LENGTH];
        snprintf(msg, sizeof(msg), "CALL %s needs %d value(s), but you gave %d.",
                 f->name, f->param_count, argc);
        error_message(msg, "Tip: Use commas: CALL name WITH a, b, \"text\"");
        return;
    }

    /* Save previous param variables so we can restore them after the call */
    Variable saved[MAX_PARAMS];
    int     had_saved[MAX_PARAMS];
    memset(saved, 0, sizeof(saved));
    memset(had_saved, 0, sizeof(had_saved));

    for (int i = 0; i < f->param_count; i++) {
        Variable *v = find_var(f->params[i]);
        if (v) { had_saved[i] = 1; saved[i] = *v; }
    }

    /* Assign params */
    for (int i = 0; i < f->param_count; i++) {
        VarType ttype;
        double  tnum;
        char    ttext[MAX_LINE_LENGTH];
        parse_value(argv[i], &ttype, &tnum, ttext);

        if (ttype == TYPE_TEXT)         set_text(f->params[i], ttext);
        else if (ttype == TYPE_YES_NO)  set_yes_no(f->params[i], (tnum != 0.0));
        else                            set_number(f->params[i], tnum);
    }

    /* Call */
    int prev_in_func = runtime.in_function;
    int prev_should_return = runtime.should_return;
    VarType prev_return_type = runtime.return_type;
    double prev_return_value = runtime.return_value;
    char prev_return_text[MAX_LINE_LENGTH];
    strncpy(prev_return_text, runtime.return_text, MAX_LINE_LENGTH-1);
    prev_return_text[MAX_LINE_LENGTH-1] = '\0';

    runtime.in_function = 1;
    runtime.should_return = 0;
    runtime.return_type = TYPE_NUMBER;
    runtime.return_value = 0;
    runtime.return_text[0] = '\0';

    runtime.call_depth++;
    strncpy(runtime.current_function, f->name, MAX_LINE_LENGTH-1);
    runtime.current_function[MAX_LINE_LENGTH-1] = '\0';

    execute_code(f->code, f->code_line_count);

    runtime.call_depth--;
    if (runtime.call_depth == 0) runtime.current_function[0] = '\0';

    /* Restore param variables */
    for (int i = 0; i < f->param_count; i++) {
        if (had_saved[i]) {
            Variable *v = get_or_create_var(saved[i].name);
            if (v) *v = saved[i];
        }
    }

    /* publish return as RESULT */
    set_result_from_return();

    /* restore caller context flags */
    runtime.in_function = prev_in_func;
    runtime.should_return = prev_should_return;

    /* keep returned value in runtime, but restore caller's return storage if nested call */
    if (runtime.call_depth > 0) {
        runtime.return_type  = prev_return_type;
        runtime.return_value = prev_return_value;
        strncpy(runtime.return_text, prev_return_text, MAX_LINE_LENGTH-1);
        runtime.return_text[MAX_LINE_LENGTH-1] = '\0';
    }
}

void cmd_return(char *expr) {
    if (!runtime.in_function) {
        error_message("RETURN can only be used inside TEACH ... LEARNED", "Tip: RETURN ends a function early.");
        return;
    }

    VarType ttype;
    double  tnum;
    char    ttext[MAX_LINE_LENGTH];
    parse_value(expr, &ttype, &tnum, ttext);

    runtime.return_type = ttype;
    if (ttype == TYPE_TEXT) {
        strncpy(runtime.return_text, ttext, MAX_LINE_LENGTH-1);
        runtime.return_text[MAX_LINE_LENGTH-1] = '\0';
        runtime.return_value = 0;
    } else {
        runtime.return_value = tnum;
        runtime.return_text[0] = '\0';
    }
    runtime.should_return = 1;

    /* also set RESULT inside the function (helpful for beginners) */
    set_result_from_return();
}

/* ============================================================================
 * IF / REPEAT / DO TIMES COMMANDS
 * ============================================================================ */

/* Find matching ELSE and ENDIF for an IF at position start */
void find_if_structure(char code[][MAX_LINE_LENGTH], int line_count, int start,
                       int *else_line, int *endif_line) {
    int depth = 1;
    *else_line  = -1;
    *endif_line = -1;
    for (int i = start+1; i < line_count; i++) {
        char w[MAX_LINE_LENGTH]; sscanf(trim(code[i]), "%s", w); to_upper(w);
        if (strcmp(w,"IF")==0)    depth++;
        if (strcmp(w,"ENDIF")==0) { depth--; if (depth==0) { *endif_line = i; return; } }
        if (strcmp(w,"ELSE")==0 && depth==1) *else_line = i;
    }
}

void cmd_if(char *cond, char code[][MAX_LINE_LENGTH], int line_count, int *line) {
    int else_line, endif_line;
    find_if_structure(code, line_count, *line, &else_line, &endif_line);
    if (endif_line < 0) { error_message("IF without ENDIF","Add ENDIF after your IF block"); return; }

    int result = eval_yes_no_expr(cond);
    if (result) {
        int end = (else_line >= 0) ? else_line : endif_line;
        execute_block(code, line_count, *line + 1, end);
    } else if (else_line >= 0) {
        execute_block(code, line_count, else_line + 1, endif_line);
    }
    *line = endif_line;
}

void cmd_repeat(char *args, char code[][MAX_LINE_LENGTH], int line_count, int *line) {
    int count = (int)eval_number_expr(args);
    if (count <= 0) { error_message("REPEAT count must be a positive number","Try: REPEAT 5"); return; }

    int start = *line + 1;
    int end   = start;
    int depth = 1;
    while (end < line_count && depth > 0) {
        char w[MAX_LINE_LENGTH]; sscanf(trim(code[end]), "%s", w); to_upper(w);
        if (strcmp(w,"REPEAT")==0) depth++;
        if (strcmp(w,"UNTIL")==0)  depth--;
        if (depth > 0) end++;
    }

    if (depth != 0) { error_message("REPEAT without UNTIL","Add UNTIL after your REPEAT block"); return; }

    for (int i = 0; i < count; i++) {
        execute_block(code, line_count, start, end);
    }
    *line = end;
}

void cmd_do_times(char *count_str, char code[][MAX_LINE_LENGTH], int line_count, int *line) {
    int count = (int)eval_number_expr(count_str);
    if (count <= 0) { error_message("DO count must be a positive number","Try: DO 5 TIMES"); return; }

    int start = *line + 1;
    int end   = start;
    int depth = 1;
    while (end < line_count && depth > 0) {
        char w[MAX_LINE_LENGTH]; sscanf(trim(code[end]), "%s", w); to_upper(w);
        if (strcmp(w,"DO")==0)   depth++;
        if (strcmp(w,"DONE")==0) depth--;
        if (depth > 0) end++;
    }

    if (depth != 0) { error_message("DO without DONE","Add DONE after your DO block"); return; }

    for (int i = 0; i < count; i++) {
        execute_block(code, line_count, start, end);
    }
    *line = end;
}

/* ============================================================================
 * LINE EXECUTOR
 * ============================================================================ */

void execute_line(char *raw_line) {
    char line[MAX_LINE_LENGTH];
    strncpy(line, raw_line, MAX_LINE_LENGTH-1);
    char *l = trim(line);

    if (strlen(l) == 0) return;
    if (l[0] == '#')    return;   /* comment */

    /* Debug step */
    if (runtime.debug_mode) {
        print_colored(COLOR_CYAN, "[DEBUG] ");
        printf("Line %d: %s\n", runtime.line_number, l);
    }

    char cmd[MAX_LINE_LENGTH];
    sscanf(l, "%s", cmd);
    to_upper(cmd);

    char *rest = l + strlen(cmd);
    rest = trim(rest);

    /* ---- Commands ---- */
    if (strcmp(cmd,"SAY")==0)  { cmd_say(rest);  return; }
    if (strcmp(cmd,"SET")==0)  { cmd_set(rest);  return; }
    if (strcmp(cmd,"ASK")==0)  { cmd_ask(rest);  return; }
    if (strcmp(cmd,"WAIT")==0) { cmd_wait(rest); return; }
    if (strcmp(cmd,"VARS")==0) { cmd_vars();     return; }

    if (strcmp(cmd,"CALL")==0)  { cmd_call(rest);  return; }
    if (strcmp(cmd,"RETURN")==0){ cmd_return(rest); return; }

    if (strcmp(cmd,"HELP")==0) { cmd_help(rest); return; }

    if (strcmp(cmd,"EXIT")==0 || strcmp(cmd,"QUIT")==0) { exit(0); }

    if (strcmp(cmd,"DEBUG")==0) {
        to_upper(rest);
        runtime.debug_mode = (strcmp(rest,"ON")==0) ? 1 : 0;
        printf("Debug mode: %s\n", runtime.debug_mode ? "ON" : "OFF");
        return;
    }

    /* Sprite commands */
    if (strcmp(cmd,"CREATE")==0) {
        char sub[MAX_LINE_LENGTH]; sscanf(rest, "%s", sub); to_upper(sub);
        if (strcmp(sub,"SPRITE")==0) { cmd_create_sprite(rest + strlen(sub) + 1); return; }
    }
    if (strcmp(cmd,"MOVE")==0) {
        char sub[MAX_LINE_LENGTH]; sscanf(rest, "%s", sub); to_upper(sub);
        if (strcmp(sub,"SPRITE")==0) { cmd_move_sprite(rest + strlen(sub) + 1); return; }
    }
    if (strcmp(cmd,"SHOW")==0) {
        char sub[MAX_LINE_LENGTH]; sscanf(rest, "%s", sub); to_upper(sub);
        if (strcmp(sub,"SPRITE")==0) { cmd_show_sprite(rest + strlen(sub) + 1); return; }
    }
    if (strcmp(cmd,"HIDE")==0) {
        char sub[MAX_LINE_LENGTH]; sscanf(rest, "%s", sub); to_upper(sub);
        if (strcmp(sub,"SPRITE")==0) { cmd_hide_sprite(rest + strlen(sub) + 1); return; }
    }

    /* Unknown command */
    char msg[MAX_LINE_LENGTH];
    snprintf(msg, sizeof(msg), "Unknown command: %s", cmd);
    error_message(msg, "");
    suggest_command(cmd);
}

/* ============================================================================
 * MULTI-LINE EXECUTOR
 * ============================================================================ */

void execute_block(char code[][MAX_LINE_LENGTH], int line_count, int start, int end) {
    if (start < 0) start = 0;
    if (end > line_count) end = line_count;

    for (int i = start; i < end; i++) {
        runtime.line_number = i + 1;

        char line_copy[MAX_LINE_LENGTH];
        strncpy(line_copy, code[i], MAX_LINE_LENGTH-1);
        line_copy[MAX_LINE_LENGTH-1] = '\0';

        char *l = trim(line_copy);
        if (strlen(l)==0 || l[0]=='#') continue;

        char cmd[MAX_LINE_LENGTH]; sscanf(l, "%s", cmd); to_upper(cmd);
        char *rest = trim(l + strlen(cmd));

        if (strcmp(cmd,"TEACH")==0) {
            /* Skip function definition blocks during normal execution */
            int end = i + 1;
            while (end < line_count) {
                char w[MAX_LINE_LENGTH]; w[0] = '\0';
                sscanf(trim(code[end]), "%s", w);
                to_upper(w);
                if (strcmp(w, "LEARNED") == 0) break;
                end++;
            }
            if (end >= line_count) {
                error_message("TEACH without LEARNED", "Add LEARNED at the end of your TEACH block");
                return;
            }
            i = end;
            continue;
        }

        if (strcmp(cmd,"IF")==0) {
            /* Find the THEN keyword if present, strip it */
            char cond[MAX_LINE_LENGTH]; strncpy(cond, rest, MAX_LINE_LENGTH-1);
            cond[MAX_LINE_LENGTH-1] = '\0';
            char *then = strstr(cond," THEN"); if (then) *then = '\0';
            to_upper(cond);
            cmd_if(cond, code, line_count, &i);
            continue;
        }
        if (strcmp(cmd,"ELSE")==0 || strcmp(cmd,"ENDIF")==0 ||
            strcmp(cmd,"UNTIL")==0 || strcmp(cmd,"DONE")==0 || strcmp(cmd,"LEARNED")==0)  continue;

        if (strcmp(cmd,"REPEAT")==0) { cmd_repeat(rest, code, line_count, &i); continue; }

        if (strcmp(cmd,"DO")==0) {
            /* DO n TIMES */
            char count_s[MAX_LINE_LENGTH], times_kw[MAX_LINE_LENGTH];
            count_s[0] = '\0'; times_kw[0] = '\0';
            sscanf(rest, "%s %s", count_s, times_kw);
            cmd_do_times(count_s, code, line_count, &i);
            continue;
        }

        execute_line(code[i]);
        if (runtime.should_return) return;
    }
}

void execute_code(char code[][MAX_LINE_LENGTH], int line_count) {
    /* First, learn any TEACH blocks in this code buffer */
    parse_functions(code, line_count);
    execute_block(code, line_count, 0, line_count);
}

/* ============================================================================
 * MAIN ENTRY POINTS
 * ============================================================================ */

void run_interactive(void) {
    print_colored(COLOR_GREEN, "\n=== Welcome to CLARO! ===\n\n");
    printf("A programming language designed for everyone.\n");
    printf("Type HELP for a list of commands.  Type EXIT to quit.\n");
    printf("Tip: IF/DO/REPEAT can be typed as multi-line blocks here.\n\n");

    char input[MAX_LINE_LENGTH];

    /* REPL block buffer */
    char block[MAX_CODE_LINES][MAX_LINE_LENGTH];
    int  block_count = 0;
    int  stack_depth = 0;

    while (1) {
        if (stack_depth == 0) {
            print_colored(COLOR_MAGENTA, "claro> ");
        } else {
            print_colored(COLOR_MAGENTA, "....> ");
        }

        if (!fgets(input, sizeof(input), stdin)) break;
        input[strcspn(input,"\n")] = 0;

        char tmp[MAX_LINE_LENGTH];
        strncpy(tmp, input, MAX_LINE_LENGTH-1);
        tmp[MAX_LINE_LENGTH-1] = '\0';
        char *t = trim(tmp);
        if (strlen(t) == 0) continue;

        /* If we're not currently in a block, decide whether to start one */
        if (stack_depth == 0) {
            char first[MAX_LINE_LENGTH];
            sscanf(t, "%s", first); to_upper(first);

            if (strcmp(first,"IF")==0 || strcmp(first,"DO")==0 || strcmp(first,"REPEAT")==0 || strcmp(first,"TEACH")==0) {
                block_count = 0;
                stack_depth = 0;
            } else {
                runtime.line_number = 0;
                execute_line(input);
                continue;
            }
        }

        /* Add line to block buffer */
        if (block_count >= MAX_CODE_LINES) {
            error_message("Block too long", "Tip: keep blocks shorter, or run from a file");
            block_count = 0;
            stack_depth = 0;
            continue;
        }
        strncpy(block[block_count], input, MAX_LINE_LENGTH-1);
        block[block_count][MAX_LINE_LENGTH-1] = '\0';
        block_count++;

        /* Update block nesting stack by keywords */
        char kw[MAX_LINE_LENGTH];
        kw[0] = '\0';
        sscanf(t, "%s", kw); to_upper(kw);

        if (strcmp(kw,"IF")==0)     stack_depth++;
        if (strcmp(kw,"DO")==0)     stack_depth++;
        if (strcmp(kw,"REPEAT")==0) stack_depth++;
        if (strcmp(kw,"TEACH")==0)  stack_depth++;

        if (strcmp(kw,"ENDIF")==0)  stack_depth--;
        if (strcmp(kw,"DONE")==0)   stack_depth--;
        if (strcmp(kw,"UNTIL")==0)  stack_depth--;
        if (strcmp(kw,"LEARNED")==0) stack_depth--;

        if (stack_depth < 0) {
            error_message("Unexpected block ending", "Tip: ENDIF closes IF, DONE closes DO, UNTIL closes REPEAT, LEARNED closes TEACH");
            block_count = 0;
            stack_depth = 0;
            continue;
        }

        /* If stack is empty, execute the whole collected block */
        if (stack_depth == 0) {
            runtime.line_number = 0;
            execute_code(block, block_count);
            block_count = 0;
        }
    }
}

void run_file(const char *filename) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        print_colored(COLOR_RED, "Error: ");
        printf("Could not open file '%s'\n", filename);
        return;
    }
    char code[MAX_CODE_LINES][MAX_LINE_LENGTH];
    int  count = 0;
    while (fgets(code[count], MAX_LINE_LENGTH, file) && count < MAX_CODE_LINES) {
        code[count][strcspn(code[count],"\n")] = 0;
        count++;
    }
    fclose(file);
    execute_code(code, count);
}

int main(int argc, char *argv[]) {
    memset(&runtime, 0, sizeof(Runtime));
    srand((unsigned)time(NULL));

    if (argc > 1) {
        if (strcmp(argv[1],"-h")==0 || strcmp(argv[1],"--high-contrast")==0) {
            runtime.high_contrast = 1;
            if (argc > 2) run_file(argv[2]);
            else          run_interactive();
        } else {
            run_file(argv[1]);
        }
    } else {
        run_interactive();
    }
    return 0;
}
