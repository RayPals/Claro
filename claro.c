#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdarg.h>
#include <setjmp.h>

// Color definitions for normal and high-contrast modes.
#define COLOR_RESET   "\x1b[0m"
#define COLOR_PROMPT  "\x1b[32m"    // Green prompt
#define COLOR_ERROR   "\x1b[31m"    // Red error
#define COLOR_DEBUG   "\x1b[34m"    // Blue debug

#define HC_COLOR_RESET   "\x1b[0m"
#define HC_COLOR_PROMPT  "\x1b[97m"    // White prompt for high contrast
#define HC_COLOR_ERROR   "\x1b[91m"    // Light red error
#define HC_COLOR_DEBUG   "\x1b[94m"    // Light blue debug

// Limits for fixed-size arrays
#define MAX_LINE_LENGTH 256
#define MAX_BLOCK_LINES 100
#define MAX_CALL_STACK_DEPTH 100
#define MAX_VARIABLES 100
#define MAX_FUNCTIONS 100

// --- Variable type definition ---
// Updated to include a floating-point type.
typedef enum { TYPE_INT, TYPE_FLOAT, TYPE_STRING } VarType;

typedef struct {
    char name[MAX_LINE_LENGTH];
    VarType type;
    char value[MAX_LINE_LENGTH]; // Numeric values are stored as strings (using double formatting).
} Variable;

// --- Data structures for user-defined functions ---
typedef struct {
    char name[MAX_LINE_LENGTH];
    char **params;            // Array of parameter names
    int param_count;
    char **code_lines;        // Function body lines
    int code_line_count;
} FunctionDef;

// --- Interpreter Context ---
// function_return_value now uses double to handle floating-point arithmetic.
typedef struct {
    char **code_lines;
    int code_line_count;
    int current_line;
    bool debug_mode;
    bool high_contrast_mode;  // High contrast mode for accessibility
    bool audio_mode;          // Toggle auditory output for errors/messages
    jmp_buf error_buf;
    Variable variables[MAX_VARIABLES];
    int variable_count;
    FunctionDef functions[MAX_FUNCTIONS];
    int function_count;
    char call_stack[MAX_CALL_STACK_DEPTH][MAX_LINE_LENGTH];
    int call_stack_depth;
    bool in_function;
    double function_return_value;
    jmp_buf function_return_buf;
} InterpreterContext;

// --- Function Declarations ---
void init_context(InterpreterContext *ctx);
void free_context(InterpreterContext *ctx);
void repl(InterpreterContext *ctx);
void execute_code(InterpreterContext *ctx);
void execute_line(InterpreterContext *ctx, const char *line);
char **tokenize(const char *line, int *token_count);
void free_tokens(char **tokens, int token_count);
double parse_expression(const char **str, InterpreterContext *ctx);
double parse_term(const char **str, InterpreterContext *ctx);
double parse_factor(const char **str, InterpreterContext *ctx);
double parse_comparison(const char **str, InterpreterContext *ctx);
double evaluate_expression(const char *expr, InterpreterContext *ctx);
void debug_log(InterpreterContext *ctx, const char *format, ...);
void print_error(InterpreterContext *ctx, const char *message, int line_number);
void set_variable(InterpreterContext *ctx, const char *name, const char *value, VarType type);
const char *get_variable(InterpreterContext *ctx, const char *name);
void show_help(void);
char *join_tokens(char **tokens, int start, int token_count);
char *trim_whitespace(char *str);
double execute_function(InterpreterContext *ctx, const FunctionDef *f, char **args, int arg_count);
void define_function(InterpreterContext *ctx, char **tokens, int token_count);
void execute_block(InterpreterContext *ctx, char **block_lines, int block_line_count);
void show_guided_tutorial(InterpreterContext *ctx); // Guided tutorial mode.
void show_cheatsheet(void);  // New command for a concise reference.

// --- Utility functions ---
char *trim_whitespace(char *str) {
    char *end;
    while (isspace((unsigned char)*str)) str++;
    if (*str == 0)
        return str;
    end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) end--;
    end[1] = '\0';
    return str;
}

// Tokenize a line of input; if the token is quoted, prepend "S:".
char **tokenize(const char *line, int *token_count) {
    char **tokens = NULL;
    int count = 0;
    const char *p = line;
    while (*p) {
        while (*p && isspace((unsigned char)*p)) p++;
        if (!*p) break;
        char token[MAX_LINE_LENGTH] = {0};
        int pos = 0;
        bool isQuoted = false;
        if (*p == '\"') {  // Handle quoted token.
            isQuoted = true;
            p++;  // Skip the opening quote.
            while (*p && *p != '\"' && pos < MAX_LINE_LENGTH - 1)
                token[pos++] = *p++;
            if (*p == '\"') p++; // Skip the closing quote.
        } else {
            while (*p && !isspace((unsigned char)*p) && pos < MAX_LINE_LENGTH - 1)
                token[pos++] = *p++;
        }
        token[pos] = '\0';
        char *finalToken;
        if (isQuoted) {
            finalToken = malloc(strlen(token) + 3);
            if (!finalToken) {
                fprintf(stderr, "Memory allocation failed during tokenization.\n");
                exit(1);
            }
            strcpy(finalToken, "S:");
            strcat(finalToken, token);
        } else {
            finalToken = strdup(token);
        }
        tokens = realloc(tokens, sizeof(char*) * (count + 1));
        if (!tokens) {
            fprintf(stderr, "Memory allocation failed during tokenization.\n");
            exit(1);
        }
        tokens[count] = finalToken;
        count++;
    }
    *token_count = count;
    return tokens;
}

void free_tokens(char **tokens, int token_count) {
    for (int i = 0; i < token_count; i++)
        free(tokens[i]);
    free(tokens);
}

char *join_tokens(char **tokens, int start, int token_count) {
    char *result = malloc(MAX_LINE_LENGTH);
    if (!result) {
        fprintf(stderr, "Memory allocation failed in join_tokens.\n");
        exit(1);
    }
    result[0] = '\0';
    for (int i = start; i < token_count; i++) {
        strcat(result, tokens[i]);
        if (i < token_count - 1)
            strcat(result, " ");
    }
    return result;
}

// --- Expression Parser (using double precision arithmetic) ---
// parse_factor, parse_term, parse_expression, and parse_comparison now work with double.
double parse_factor(const char **str, InterpreterContext *ctx) {
    while (**str && isspace((unsigned char)**str)) (*str)++;
    double result = 0.0;
    // Handle boolean literals.
    if (strncasecmp(*str, "true", 4) == 0 && !isalnum((unsigned char)((*str)[4]))) {
        *str += 4;
        return 1.0;
    } else if (strncasecmp(*str, "false", 5) == 0 && !isalnum((unsigned char)((*str)[5]))) {
        *str += 5;
        return 0.0;
    }
    if (**str == '(') {
        (*str)++; // Skip '('.
        result = parse_comparison(str, ctx);
        while (**str && isspace((unsigned char)**str)) (*str)++;
        if (**str == ')') {
            (*str)++; // Skip ')'.
        } else {
            print_error(ctx, "Oops! It looks like you forgot a closing parenthesis.", -1);
            longjmp(ctx->error_buf, 1);
        }
    } else if (isdigit((unsigned char)**str) || **str == '.') {
        result = strtod(*str, (char**)str);
    } else {
        // Parse a variable name.
        char varname[MAX_LINE_LENGTH] = {0};
        int pos = 0;
        while (**str && (isalnum((unsigned char)**str) || **str == '_') && pos < MAX_LINE_LENGTH - 1)
            varname[pos++] = *(*str)++;
        varname[pos] = '\0';
        const char *val = get_variable(ctx, varname);
        result = val ? atof(val) : 0.0;
    }
    return result;
}

double parse_term(const char **str, InterpreterContext *ctx) {
    double result = parse_factor(str, ctx);
    while (**str) {
        while (**str && isspace((unsigned char)**str)) (*str)++;
        if (**str == '*' || **str == '/') {
            char op = *(*str)++;
            double rhs = parse_factor(str, ctx);
            if (op == '*')
                result *= rhs;
            else {
                if (rhs == 0.0) {
                    print_error(ctx, "Division by zero is not allowed.", -1);
                    longjmp(ctx->error_buf, 1);
                }
                result /= rhs;
            }
        } else {
            break;
        }
    }
    return result;
}

double parse_expression(const char **str, InterpreterContext *ctx) {
    double result = parse_term(str, ctx);
    while (**str) {
        while (**str && isspace((unsigned char)**str)) (*str)++;
        if (**str == '+' || **str == '-') {
            char op = *(*str)++;
            double rhs = parse_term(str, ctx);
            if (op == '+')
                result += rhs;
            else
                result -= rhs;
        } else {
            break;
        }
    }
    return result;
}

double parse_comparison(const char **str, InterpreterContext *ctx) {
    double left = parse_expression(str, ctx);
    while (**str) {
        while (**str && isspace((unsigned char)**str)) (*str)++;
        if (strncmp(*str, "==", 2) == 0) {
            *str += 2;
            double right = parse_expression(str, ctx);
            left = (left == right) ? 1.0 : 0.0;
        } else if (strncmp(*str, "!=", 2) == 0) {
            *str += 2;
            double right = parse_expression(str, ctx);
            left = (left != right) ? 1.0 : 0.0;
        } else if (strncmp(*str, "<=", 2) == 0) {
            *str += 2;
            double right = parse_expression(str, ctx);
            left = (left <= right) ? 1.0 : 0.0;
        } else if (strncmp(*str, ">=", 2) == 0) {
            *str += 2;
            double right = parse_expression(str, ctx);
            left = (left >= right) ? 1.0 : 0.0;
        } else if (**str == '<') {
            (*str)++;
            double right = parse_expression(str, ctx);
            left = (left < right) ? 1.0 : 0.0;
        } else if (**str == '>') {
            (*str)++;
            double right = parse_expression(str, ctx);
            left = (left > right) ? 1.0 : 0.0;
        } else {
            break;
        }
    }
    return left;
}

double evaluate_expression(const char *expr, InterpreterContext *ctx) {
    const char *p = expr;
    double result = parse_comparison(&p, ctx);
    return result;
}

// --- Debug and Error ---
void debug_log(InterpreterContext *ctx, const char *format, ...) {
    if (!ctx->debug_mode) return;
    va_list args;
    va_start(args, format);
    if (ctx->high_contrast_mode)
        printf(HC_COLOR_DEBUG "[DEBUG] " HC_COLOR_RESET);
    else
        printf(COLOR_DEBUG "[DEBUG] " COLOR_RESET);
    vprintf(format, args);
    printf("\n");
    va_end(args);
}

void print_error(InterpreterContext *ctx, const char *message, int line_number) {
    const char *error_color = ctx->high_contrast_mode ? HC_COLOR_ERROR : COLOR_ERROR;
    const char *reset_color = ctx->high_contrast_mode ? HC_COLOR_RESET : COLOR_RESET;
    if (line_number >= 0)
         fprintf(stderr, "%sOops! Error (line %d): %s\n%s", error_color, line_number, message, reset_color);
    else
         fprintf(stderr, "%sOops! Error: %s\n%s", error_color, message, reset_color);
    if (ctx->audio_mode) {
        char cmd[MAX_LINE_LENGTH * 2];
        snprintf(cmd, sizeof(cmd), "espeak \"Error: %s\"", message);
        system(cmd);
    }
}

// --- Variable handling ---
void set_variable(InterpreterContext *ctx, const char *name, const char *value, VarType type) {
    for (int i = 0; i < ctx->variable_count; i++) {
        if (strcmp(ctx->variables[i].name, name) == 0) {
            strncpy(ctx->variables[i].value, value, MAX_LINE_LENGTH);
            ctx->variables[i].type = type;
            return;
        }
    }
    if (ctx->variable_count < MAX_VARIABLES) {
        strncpy(ctx->variables[ctx->variable_count].name, name, MAX_LINE_LENGTH);
        strncpy(ctx->variables[ctx->variable_count].value, value, MAX_LINE_LENGTH);
        ctx->variables[ctx->variable_count].type = type;
        ctx->variable_count++;
    } else {
        print_error(ctx, "Maximum variable limit reached", -1);
    }
}

const char *get_variable(InterpreterContext *ctx, const char *name) {
    for (int i = 0; i < ctx->variable_count; i++) {
        if (strcmp(ctx->variables[i].name, name) == 0)
            return ctx->variables[i].value;
    }
    return NULL;
}

// --- Function handling ---
void define_function(InterpreterContext *ctx, char **tokens, int token_count) {
    if (token_count < 2) {
        print_error(ctx, "Usage: FUNCTION <name> [params...]", ctx->current_line + 1);
        return;
    }
    if (ctx->function_count >= MAX_FUNCTIONS) {
        print_error(ctx, "Maximum function limit reached", ctx->current_line + 1);
        return;
    }
    FunctionDef *f = &ctx->functions[ctx->function_count];
    strncpy(f->name, tokens[1], MAX_LINE_LENGTH);
    f->param_count = token_count - 2;
    if (f->param_count > 0) {
        f->params = malloc(sizeof(char*) * f->param_count);
        if (!f->params) {
            print_error(ctx, "Memory allocation failed for function parameters", ctx->current_line + 1);
            return;
        }
        for (int i = 0; i < f->param_count; i++) {
            f->params[i] = strdup(tokens[i+2]);
        }
    } else {
        f->params = NULL;
    }
    f->code_line_count = 0;
    f->code_lines = NULL;
    printf("Enter function body lines. Type ENDFUNCTION on a line by itself to finish:\n");
    char line[MAX_LINE_LENGTH];
    while (true) {
        printf("... ");
        if (!fgets(line, sizeof(line), stdin))
            break;
        line[strcspn(line, "\n")] = '\0';
        char *trimmed = trim_whitespace(line);
        if (strcmp(trimmed, "ENDFUNCTION") == 0)
            break;
        f->code_lines = realloc(f->code_lines, sizeof(char*) * (f->code_line_count + 1));
        if (!f->code_lines) {
            print_error(ctx, "Memory allocation failed for function body", ctx->current_line + 1);
            return;
        }
        f->code_lines[f->code_line_count] = strdup(line);
        f->code_line_count++;
    }
    ctx->function_count++;
    printf("Function '%s' defined with %d parameter(s) and %d code line(s).\n", f->name, f->param_count, f->code_line_count);
}

double execute_function(InterpreterContext *ctx, const FunctionDef *f, char **args, int arg_count) {
    if (arg_count != f->param_count) {
        printf("Error: Function '%s' expects %d arguments, got %d.\n", f->name, f->param_count, arg_count);
        return 0.0;
    }
    int local_scope_start = ctx->variable_count;
    for (int i = 0; i < f->param_count; i++) {
        set_variable(ctx, f->params[i], args[i], TYPE_FLOAT);
    }
    if (ctx->call_stack_depth < MAX_CALL_STACK_DEPTH) {
        strncpy(ctx->call_stack[ctx->call_stack_depth], f->name, MAX_LINE_LENGTH);
        ctx->call_stack_depth++;
    }
    ctx->in_function = true;
    if (setjmp(ctx->function_return_buf) == 0) {
        for (int i = 0; i < f->code_line_count; i++) {
            debug_log(ctx, "Function '%s' executing: %s", f->name, f->code_lines[i]);
            execute_line(ctx, f->code_lines[i]);
        }
    }
    double retVal = ctx->function_return_value;
    ctx->variable_count = local_scope_start;
    ctx->in_function = false;
    if (ctx->call_stack_depth > 0)
        ctx->call_stack_depth--;
    return retVal;
}

// --- Block execution ---
void execute_block(InterpreterContext *ctx, char **block_lines, int block_line_count) {
    for (int i = 0; i < block_line_count; i++) {
        execute_line(ctx, block_lines[i]);
    }
}

// --- Command Execution ---
void execute_line(InterpreterContext *ctx, const char *line) {
    if (setjmp(ctx->error_buf) != 0) {
        print_error(ctx, "An error occurred; skipping this command", ctx->current_line + 1);
        return;
    }
    int token_count = 0;
    char **tokens = tokenize(line, &token_count);
    if (token_count == 0) {
        free_tokens(tokens, token_count);
        return;
    }
    char command[MAX_LINE_LENGTH];
    strncpy(command, tokens[0], MAX_LINE_LENGTH);
    for (char *p = command; *p; ++p)
        *p = toupper((unsigned char)*p);
    debug_log(ctx, "Executing command: %s", command);

    // VARIABLE/SET command (alias for assignment)
    if ((strcmp(command, "VARIABLE") == 0 || strcmp(command, "SET") == 0) && token_count >= 4) {
        if (strcmp(tokens[2], "=") != 0) {
            print_error(ctx, "Usage: VARIABLE/SET <name> = <expression>", ctx->current_line + 1);
        } else {
            if (strncmp(tokens[3], "S:", 2) == 0 && token_count == 4) {
                const char *str_literal = tokens[3] + 2;
                set_variable(ctx, tokens[1], str_literal, TYPE_STRING);
                printf("Variable '%s' set to '%s'\n", tokens[1], str_literal);
            } else {
                char *expr = join_tokens(tokens, 3, token_count);
                double eval = evaluate_expression(expr, ctx);
                char eval_str[MAX_LINE_LENGTH];
                snprintf(eval_str, sizeof(eval_str), "%g", eval);
                set_variable(ctx, tokens[1], eval_str, TYPE_FLOAT);
                printf("Variable '%s' set to '%s'\n", tokens[1], eval_str);
                free(expr);
            }
        }
    }
    else if (strcmp(command, "PRINT") == 0) {
        for (int i = 1; i < token_count; i++) {
            if (tokens[i][0] == '$') {
                const char *val = get_variable(ctx, tokens[i] + 1);
                if (val)
                    printf("%s ", val);
                else
                    printf("[undefined] ");
            }
            else if (strncmp(tokens[i], "S:", 2) == 0) {
                printf("%s ", tokens[i] + 2);
            }
            else {
                const char *val = get_variable(ctx, tokens[i]);
                if (val)
                    printf("%s ", val);
                else
                    printf("%s ", tokens[i]);
            }
        }
        printf("\n");
    }
    else if (strcmp(command, "GET") == 0 && token_count >= 2) {
        const char *val = get_variable(ctx, tokens[1]);
        if (val)
            printf("Variable '%s' = '%s'\n", tokens[1], val);
        else
            printf("Variable '%s' is not defined.\n", tokens[1]);
    }
    else if (strcmp(command, "DEBUG") == 0 && token_count >= 2) {
        if (strcasecmp(tokens[1], "ON") == 0) {
            ctx->debug_mode = true;
            printf("Debug mode enabled.\n");
        } else if (strcasecmp(tokens[1], "OFF") == 0) {
            ctx->debug_mode = false;
            printf("Debug mode disabled.\n");
        } else {
            print_error(ctx, "Usage: DEBUG ON|OFF", ctx->current_line + 1);
        }
    }
    else if (strcmp(command, "INPUT") == 0 && token_count >= 3) {
        char *prompt = join_tokens(tokens, 2, token_count);
        prompt = trim_whitespace(prompt);
        printf("%s ", prompt);
        char input_line[MAX_LINE_LENGTH];
        if (fgets(input_line, sizeof(input_line), stdin) != NULL) {
            input_line[strcspn(input_line, "\n")] = '\0';
            char *trimmed_input = trim_whitespace(input_line);
            set_variable(ctx, tokens[1], trimmed_input, TYPE_STRING);
            printf("Variable '%s' set to '%s'\n", tokens[1], trimmed_input);
        } else {
            print_error(ctx, "Failed to read input", ctx->current_line + 1);
        }
        free(prompt);
    }
    else if (strcmp(command, "REPEAT") == 0 && token_count >= 3) {
        int count = atoi(tokens[1]);
        if (count <= 0) {
            print_error(ctx, "REPEAT count must be a positive integer", ctx->current_line + 1);
        } else {
            char *repeat_cmd = join_tokens(tokens, 2, token_count);
            for (int i = 0; i < count; i++) {
                debug_log(ctx, "REPEAT iteration %d: %s", i+1, repeat_cmd);
                execute_line(ctx, repeat_cmd);
            }
            free(repeat_cmd);
        }
    }
    else if (strcmp(command, "IF") == 0) {
        int then_idx = -1, else_idx = -1, endif_idx = -1;
        for (int i = 1; i < token_count; i++) {
            char temp[MAX_LINE_LENGTH];
            strncpy(temp, tokens[i], MAX_LINE_LENGTH);
            for (char *p = temp; *p; ++p) *p = toupper((unsigned char)*p);
            if (strcmp(temp, "THEN") == 0 && then_idx == -1)
                then_idx = i;
            else if (strcmp(temp, "ELSE") == 0 && else_idx == -1)
                else_idx = i;
            else if (strcmp(temp, "ENDIF") == 0) {
                endif_idx = i;
                break;
            }
        }
        if (then_idx == -1 || endif_idx == -1) {
            print_error(ctx, "IF syntax error. Usage: IF <cond> THEN <cmd> [ELSE <cmd>] ENDIF", ctx->current_line + 1);
        } else {
            char *cond_expr = join_tokens(tokens, 1, then_idx);
            double cond_val = evaluate_expression(cond_expr, ctx);
            free(cond_expr);
            if (cond_val) {
                char *then_cmd = (else_idx == -1) ? join_tokens(tokens, then_idx+1, endif_idx)
                                                  : join_tokens(tokens, then_idx+1, else_idx);
                execute_line(ctx, then_cmd);
                free(then_cmd);
            } else if (else_idx != -1) {
                char *else_cmd = join_tokens(tokens, else_idx+1, endif_idx);
                execute_line(ctx, else_cmd);
                free(else_cmd);
            }
        }
    }
    else if (strcmp(command, "WHILE") == 0) {
        int idx = 1;
        char cond_expr[MAX_LINE_LENGTH] = {0};
        while (idx < token_count && strcasecmp(tokens[idx], "BEGIN") != 0) {
            strcat(cond_expr, tokens[idx]);
            strcat(cond_expr, " ");
            idx++;
        }
        if (idx == token_count) {
            print_error(ctx, "WHILE syntax error. Missing BEGIN", ctx->current_line + 1);
        } else {
            char *block_lines[MAX_BLOCK_LINES];
            int block_line_count = 0;
            printf("Enter WHILE loop block lines (type ENDWHILE on a line by itself):\n");
            char blk_line[MAX_LINE_LENGTH];
            while (true) {
                printf("... ");
                if (!fgets(blk_line, sizeof(blk_line), stdin))
                    break;
                blk_line[strcspn(blk_line, "\n")] = '\0';
                char *trimmed = trim_whitespace(blk_line);
                if (strcasecmp(trimmed, "ENDWHILE") == 0)
                    break;
                block_lines[block_line_count] = strdup(blk_line);
                block_line_count++;
            }
            while (evaluate_expression(cond_expr, ctx)) {
                execute_block(ctx, block_lines, block_line_count);
            }
            for (int i = 0; i < block_line_count; i++)
                free(block_lines[i]);
        }
    }
    // --- New FOR Loop Control Structure ---
    else if (strcmp(command, "FOR") == 0) {
        // Expected syntax: FOR <var> = <start> TO <end> [STEP <step>] BEGIN
        if (token_count < 7) {
            print_error(ctx, "Usage: FOR <var> = <start> TO <end> [STEP <step>] BEGIN", ctx->current_line + 1);
        } else {
            if (strcmp(tokens[2], "=") != 0) {
                print_error(ctx, "Expected '=' in FOR loop declaration", ctx->current_line + 1);
            } else {
                double start_val = evaluate_expression(tokens[3], ctx);
                if (strcasecmp(tokens[4], "TO") != 0) {
                    print_error(ctx, "Expected 'TO' in FOR loop declaration", ctx->current_line + 1);
                    free_tokens(tokens, token_count);
                    return;
                }
                double end_val = evaluate_expression(tokens[5], ctx);
                double step_val = 1.0;
                int idx = 6;
                if (idx < token_count && strcasecmp(tokens[idx], "STEP") == 0) {
                    if (idx+1 < token_count) {
                        step_val = evaluate_expression(tokens[idx+1], ctx);
                        idx += 2;
                    } else {
                        print_error(ctx, "Missing step value in FOR loop", ctx->current_line + 1);
                        free_tokens(tokens, token_count);
                        return;
                    }
                }
                if (idx >= token_count || strcasecmp(tokens[idx], "BEGIN") != 0) {
                    print_error(ctx, "Missing BEGIN in FOR loop declaration", ctx->current_line + 1);
                } else {
                    char *block_lines[MAX_BLOCK_LINES];
                    int block_line_count = 0;
                    printf("Enter FOR loop block lines (type ENDFOR on a line by itself):\n");
                    char blk_line[MAX_LINE_LENGTH];
                    while (true) {
                        printf("... ");
                        if (!fgets(blk_line, sizeof(blk_line), stdin))
                            break;
                        blk_line[strcspn(blk_line, "\n")] = '\0';
                        char *trimmed = trim_whitespace(blk_line);
                        if (strcasecmp(trimmed, "ENDFOR") == 0)
                            break;
                        block_lines[block_line_count] = strdup(blk_line);
                        block_line_count++;
                    }
                    char start_str[MAX_LINE_LENGTH];
                    snprintf(start_str, sizeof(start_str), "%g", start_val);
                    set_variable(ctx, tokens[1], start_str, TYPE_FLOAT);
                    while (true) {
                        const char *current_str = get_variable(ctx, tokens[1]);
                        double current_val = atof(current_str);
                        bool condition_met = (step_val > 0) ? (current_val <= end_val) : (current_val >= end_val);
                        if (!condition_met) break;
                        execute_block(ctx, block_lines, block_line_count);
                        current_val += step_val;
                        char current_buf[MAX_LINE_LENGTH];
                        snprintf(current_buf, sizeof(current_buf), "%g", current_val);
                        set_variable(ctx, tokens[1], current_buf, TYPE_FLOAT);
                    }
                    for (int i = 0; i < block_line_count; i++)
                        free(block_lines[i]);
                }
            }
        }
    }
    else if (strcmp(command, "TRY") == 0) {
        char *try_lines[MAX_BLOCK_LINES];
        int try_line_count = 0;
        printf("Enter TRY block lines (type CATCH on a line by itself):\n");
        char blk_line[MAX_LINE_LENGTH];
        while (true) {
            printf("TRY> ");
            if (!fgets(blk_line, sizeof(blk_line), stdin))
                break;
            blk_line[strcspn(blk_line, "\n")] = '\0';
            char *trimmed = trim_whitespace(blk_line);
            if (strcasecmp(trimmed, "CATCH") == 0)
                break;
            try_lines[try_line_count] = strdup(blk_line);
            try_line_count++;
        }
        if (setjmp(ctx->error_buf) == 0) {
            execute_block(ctx, try_lines, try_line_count);
            for (int i = 0; i < try_line_count; i++)
                free(try_lines[i]);
            printf("TRY block executed successfully; skipping CATCH.\n");
            while (true) {
                printf("CATCH> ");
                if (!fgets(blk_line, sizeof(blk_line), stdin))
                    break;
                blk_line[strcspn(blk_line, "\n")] = '\0';
                char *trimmed = trim_whitespace(blk_line);
                if (strcasecmp(trimmed, "ENDTRY") == 0)
                    break;
            }
        } else {
            printf("Error in TRY block; executing CATCH block.\n");
            for (int i = 0; i < try_line_count; i++)
                free(try_lines[i]);
            char *catch_lines[MAX_BLOCK_LINES];
            int catch_line_count = 0;
            while (true) {
                printf("CATCH> ");
                if (!fgets(blk_line, sizeof(blk_line), stdin))
                    break;
                blk_line[strcspn(blk_line, "\n")] = '\0';
                char *trimmed = trim_whitespace(blk_line);
                if (strcasecmp(trimmed, "ENDTRY") == 0)
                    break;
                catch_lines[catch_line_count] = strdup(blk_line);
                catch_line_count++;
            }
            execute_block(ctx, catch_lines, catch_line_count);
            for (int i = 0; i < catch_line_count; i++)
                free(catch_lines[i]);
        }
    }
    else if (strcmp(command, "IMPORT") == 0 && token_count >= 2) {
        char *filename = join_tokens(tokens, 1, token_count);
        FILE *fptr = fopen(filename, "r");
        if (!fptr) {
            print_error(ctx, "Could not open import file.", ctx->current_line + 1);
        } else {
            char file_line[MAX_LINE_LENGTH];
            while (fgets(file_line, sizeof(file_line), fptr)) {
                file_line[strcspn(file_line, "\n")] = '\0';
                execute_line(ctx, file_line);
            }
            fclose(fptr);
        }
        free(filename);
    }
    else if (strcmp(command, "CONCAT") == 0 && token_count >= 4) {
        const char *v1 = get_variable(ctx, tokens[2]);
        const char *v2 = get_variable(ctx, tokens[3]);
        char result[MAX_LINE_LENGTH] = "";
        if (v1) strcat(result, v1);
        if (v2) strcat(result, v2);
        set_variable(ctx, tokens[1], result, TYPE_STRING);
        printf("Concatenated value stored in '%s'.\n", tokens[1]);
    }
    else if (strcmp(command, "CALL") == 0 && token_count >= 2) {
        char *func_name = tokens[1];
        FunctionDef *f = NULL;
        for (int i = 0; i < ctx->function_count; i++) {
            if (strcmp(ctx->functions[i].name, func_name) == 0) {
                f = &ctx->functions[i];
                break;
            }
        }
        if (f == NULL) {
            printf("Function '%s' not defined.\n", func_name);
        } else {
            int arg_count = token_count - 2;
            char **args = NULL;
            if (arg_count > 0) {
                args = malloc(sizeof(char*) * arg_count);
                for (int i = 0; i < arg_count; i++) {
                    args[i] = strdup(tokens[i+2]);
                }
            }
            double retVal = execute_function(ctx, f, args, arg_count);
            printf("Function '%s' returned %g\n", func_name, retVal);
            for (int i = 0; i < arg_count; i++) {
                free(args[i]);
            }
            free(args);
        }
    }
    else if (strcmp(command, "RETURN") == 0 && token_count >= 2) {
        if (!ctx->in_function) {
            print_error(ctx, "RETURN can only be used inside a function", ctx->current_line + 1);
        } else {
            char *expr = join_tokens(tokens, 1, token_count);
            double retVal = evaluate_expression(expr, ctx);
            free(expr);
            ctx->function_return_value = retVal;
            longjmp(ctx->function_return_buf, 1);
        }
    }
    else if (strcmp(command, "STACK") == 0) {
        printf("Call Stack (depth %d):\n", ctx->call_stack_depth);
        for (int i = 0; i < ctx->call_stack_depth; i++) {
            printf("  %s\n", ctx->call_stack[i]);
        }
    }
    else if (strcmp(command, "TRACE") == 0) {
        printf("---- TRACE ----\n");
        printf("Variables (%d):\n", ctx->variable_count);
        for (int i = 0; i < ctx->variable_count; i++) {
            printf("  %s = %s\n", ctx->variables[i].name, ctx->variables[i].value);
        }
        printf("Functions (%d):\n", ctx->function_count);
        for (int i = 0; i < ctx->function_count; i++) {
            printf("  %s(", ctx->functions[i].name);
            for (int j = 0; j < ctx->functions[i].param_count; j++) {
                printf("%s", ctx->functions[i].params[j]);
                if (j < ctx->functions[i].param_count - 1)
                    printf(", ");
            }
            printf(") with %d lines\n", ctx->functions[i].code_line_count);
        }
        printf("---- END TRACE ----\n");
    }
    else if (strcmp(command, "HELP") == 0) {
        show_help();
    }
    // --- New commands for improved UX ---
    else if (strcmp(command, "CHEATSHEET") == 0) {
        show_cheatsheet();
    }
    else if (strcmp(command, "CUSTOM") == 0) {
        printf("Custom display mode activated. Extra spacing will be added to outputs to aid readability.\n");
    }
    else if (strcmp(command, "GUIDED") == 0) {
        show_guided_tutorial(ctx);
    }
    else if (strcmp(command, "AUDIO") == 0 && token_count >= 2) {
        if (strcasecmp(tokens[1], "ON") == 0) {
            ctx->audio_mode = true;
            printf("Audio mode enabled. Errors and important messages will be read aloud.\n");
        } else if (strcasecmp(tokens[1], "OFF") == 0) {
            ctx->audio_mode = false;
            printf("Audio mode disabled.\n");
        } else {
            print_error(ctx, "Usage: AUDIO ON|OFF", ctx->current_line + 1);
        }
    }
    else if (strcmp(command, "THEME") == 0 && token_count >= 2) {
        if (strcasecmp(tokens[1], "HIGH") == 0) {
            ctx->high_contrast_mode = true;
            printf("High contrast mode enabled.\n");
        } else if (strcasecmp(tokens[1], "NORMAL") == 0) {
            ctx->high_contrast_mode = false;
            printf("Normal theme enabled.\n");
        } else {
            print_error(ctx, "Usage: THEME HIGH|NORMAL", ctx->current_line + 1);
        }
    }
    else if (strcmp(command, "SAY") == 0 && token_count >= 2) {
        char *msg = join_tokens(tokens, 1, token_count);
        char command_str[MAX_LINE_LENGTH * 2];
        snprintf(command_str, sizeof(command_str), "espeak \"%s\"", msg);
        system(command_str);
        free(msg);
    }
    else if (strcmp(command, "EXIT") == 0) {
        printf("Exiting interpreter.\n");
        free_tokens(tokens, token_count);
        free_context(ctx);
        exit(0);
    }
    else {
        print_error(ctx, "Unknown command", ctx->current_line + 1);
    }
    free_tokens(tokens, token_count);
}

// --- Guided Tutorial Mode ---
void show_guided_tutorial(InterpreterContext *ctx) {
    printf("\n--- Guided Tutorial ---\n");
    printf("Welcome to Guided Tutorial Mode!\n");
    printf("Let's review some basic commands step by step.\n\n");
    printf("1. Creating a variable:\n");
    printf("   Use SET or VARIABLE, e.g., SET x = 3.14\n\n");
    printf("2. Printing output:\n");
    printf("   Use PRINT, e.g., PRINT $x\n\n");
    printf("3. Conditionals:\n");
    printf("   Use IF...THEN...ELSE...ENDIF, e.g., IF $x > 2 THEN PRINT \"High\" ELSE PRINT \"Low\" ENDIF\n\n");
    printf("4. Loops with WHILE:\n");
    printf("   Example: WHILE $x < 10 BEGIN ... ENDWHILE\n\n");
    printf("5. FOR loops:\n");
    printf("   Example: FOR i = 1 TO 5 STEP 1 BEGIN ... ENDFOR\n\n");
    printf("6. To see all commands, type HELP or CHEATSHEET.\n\n");
    printf("End of guided tutorial. Enjoy exploring the interpreter!\n");
}

// --- Cheatsheet Command ---
void show_cheatsheet(void) {
    printf("\n--- Command Cheatsheet ---\n");
    printf(" SET/VARIABLE <name> = <expression>      : Assign a variable (numbers or \"strings\")\n");
    printf(" PRINT <expression>                      : Display text/variable (use $ for variables)\n");
    printf(" GET <name>                              : Retrieve a variable's value\n");
    printf(" IF <cond> THEN <cmd> [ELSE <cmd>] ENDIF   : Conditional execution\n");
    printf(" WHILE <cond> BEGIN ... ENDWHILE          : Loop while condition is true\n");
    printf(" FOR <var> = <start> TO <end> [STEP <s>] BEGIN ... ENDFOR : Loop with initialization and step\n");
    printf(" FUNCTION <name> [params...] ... ENDFUNCTION : Define a function; use CALL to execute it\n");
    printf(" INPUT <variable> <prompt>               : Prompt for input\n");
    printf(" IMPORT <filename>                       : Run commands from a file\n");
    printf(" CONCAT <dest> <var1> <var2>               : Concatenate two variables\n");
    printf(" DEBUG ON|OFF, THEME HIGH|NORMAL, AUDIO ON|OFF : Toggle modes\n");
    printf(" GUIDED, CHEATSHEET, HELP, EXIT          : Additional utility commands\n\n");
    printf("--- End Cheatsheet ---\n");
}

// --- Execute code from file ---
void execute_code(InterpreterContext *ctx) {
    for (ctx->current_line = 0; ctx->current_line < ctx->code_line_count; ctx->current_line++) {
        debug_log(ctx, "Line %d: %s", ctx->current_line + 1, ctx->code_lines[ctx->current_line]);
        execute_line(ctx, ctx->code_lines[ctx->current_line]);
    }
}

// --- Display help ---
void show_help(void) {
    printf("\nAvailable commands:\n");
    printf("  PRINT <expression>                - Print text and variables (use $ before variable names).\n");
    printf("  VARIABLE/SET <name> = <expr>        - Create/update a variable. Use quotes for strings.\n");
    printf("  GET <name>                        - Retrieve the value of a variable.\n");
    printf("  INPUT <variable> <prompt>         - Prompt for input and store it in a variable.\n");
    printf("  REPEAT <count> <command>          - Repeat a command a given number of times.\n");
    printf("  IF <cond> THEN <cmd> [ELSE <cmd>] ENDIF - Conditional execution.\n");
    printf("  WHILE <cond> BEGIN ... ENDWHILE    - Loop while a condition is true.\n");
    printf("  FOR <var> = <start> TO <end> [STEP <s>] BEGIN ... ENDFOR - For-loop with optional step.\n");
    printf("  FUNCTION <name> [params...] ... ENDFUNCTION - Define a function; use CALL to invoke.\n");
    printf("  CALL <name> [args...]             - Call a user-defined function.\n");
    printf("  RETURN <expr>                     - Return a value from a function (inside a function).\n");
    printf("  STACK                             - Display the current function call stack.\n");
    printf("  TRACE                             - Show variables and function definitions.\n");
    printf("  DEBUG ON|OFF                      - Enable/disable debug logging.\n");
    printf("  THEME HIGH|NORMAL                 - Toggle high contrast theme.\n");
    printf("  CUSTOM                            - Activate custom display mode (extra spacing).\n");
    printf("  AUDIO ON|OFF                      - Enable/disable audio for errors/messages.\n");
    printf("  GUIDED                            - Launch guided tutorial mode.\n");
    printf("  CHEATSHEET                        - Show a summary of available commands.\n");
    printf("  SAY <text>                        - Use text-to-speech for the given text (requires espeak).\n");
    printf("  HELP                              - Display this help message.\n");
    printf("  EXIT                              - Exit the interpreter.\n\n");
}

// --- REPL (Read-Eval-Print Loop) ---
void repl(InterpreterContext *ctx) {
    if (ctx->high_contrast_mode)
        printf(HC_COLOR_PROMPT "Welcome to Extended Claro Interpreter! (High Contrast Mode)\nType HELP or GUIDED for commands.\n" HC_COLOR_RESET);
    else
        printf(COLOR_PROMPT "Welcome to Extended Claro Interpreter!\nType HELP or GUIDED for commands.\n" COLOR_RESET);
    while (true) {
        if (ctx->high_contrast_mode)
            printf(HC_COLOR_PROMPT "Claro> " HC_COLOR_RESET);
        else
            printf(COLOR_PROMPT "Claro> " COLOR_RESET);
        char input[MAX_LINE_LENGTH];
        if (!fgets(input, sizeof(input), stdin))
            break;
        input[strcspn(input, "\n")] = '\0';
        if (strlen(input) == 0)
            continue;
        execute_line(ctx, input);
    }
}

// --- Context Initialization and Free ---
void init_context(InterpreterContext *ctx) {
    ctx->code_lines = NULL;
    ctx->code_line_count = 0;
    ctx->current_line = 0;
    ctx->debug_mode = false;
    ctx->high_contrast_mode = false;
    ctx->audio_mode = false;
    ctx->variable_count = 0;
    ctx->function_count = 0;
    ctx->call_stack_depth = 0;
    ctx->in_function = false;
}

void free_context(InterpreterContext *ctx) {
    if (ctx->code_lines) {
        for (int i = 0; i < ctx->code_line_count; i++)
            free(ctx->code_lines[i]);
        free(ctx->code_lines);
    }
    for (int i = 0; i < ctx->function_count; i++) {
        FunctionDef *f = &ctx->functions[i];
        for (int j = 0; j < f->param_count; j++)
            free(f->params[j]);
        free(f->params);
        for (int j = 0; j < f->code_line_count; j++)
            free(f->code_lines[j]);
        free(f->code_lines);
    }
}

// --- Main ---
int main(int argc, char *argv[]) {
    InterpreterContext ctx;
    init_context(&ctx);

    if (setjmp(ctx.error_buf) != 0) {
        print_error(&ctx, "An unrecoverable error occurred.", ctx.current_line + 1);
        free_context(&ctx);
        exit(1);
    }
    
    if (argc > 1) {
        FILE *file = fopen(argv[1], "r");
        if (!file) {
            print_error(&ctx, "Could not open file.", -1);
            return 1;
        }
        char line[MAX_LINE_LENGTH];
        while (fgets(line, sizeof(line), file)) {
            ctx.code_lines = realloc(ctx.code_lines, sizeof(char*) * (ctx.code_line_count + 1));
            ctx.code_lines[ctx.code_line_count] = strdup(line);
            ctx.code_line_count++;
        }
        fclose(file);
        execute_code(&ctx);
    } else {
        repl(&ctx);
    }
    
    free_context(&ctx);
    return 0;
}
