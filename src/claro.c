/*
  Claro v1.18.26 - Networking Reliability Release

  A compact, buildable Claro interpreter focused on the beginner-friendly
  teaching core: readable commands, simple expressions, functions, collections,
  files, JSON, imports, TRY/CATCH, stronger beginner checking, and small standard-library
  built-ins.

  Build:
    gcc -std=c99 src/claro.c -O0 -o claro -lm
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifndef _WIN32
#include <strings.h>
#define strnicmp2 strncasecmp
#else
#define strnicmp2 _strnicmp
#endif
#include <ctype.h>
#include <stdarg.h>
#include <errno.h>
#include <math.h>
#include <time.h>
#include <sys/stat.h>
#ifndef _WIN32
FILE *popen(const char *command, const char *mode);
int pclose(FILE *stream);
#endif
#ifndef _WIN32
#include <dirent.h>
#include <unistd.h>
#else
#include <direct.h>
#include <io.h>
#ifdef __MINGW32__
#include <dirent.h>
#endif
#define access _access
#define F_OK 0
#endif

#define CLARO_VERSION "Claro v1.18.26"

static void *xmalloc(size_t n){ void *p=malloc(n?n:1); if(!p){ fprintf(stderr,"Out of memory\n"); exit(1);} return p; }
static void *xrealloc(void *p,size_t n){ void *q=realloc(p,n?n:1); if(!q){ fprintf(stderr,"Out of memory\n"); exit(1);} return q; }
static char *xstrdup(const char *s){ size_t n; char *p; if(!s) s=""; n=strlen(s); p=(char*)xmalloc(n+1); memcpy(p,s,n+1); return p; }
static int ci_cmp(const char *a,const char *b){ while(*a&&*b){ int ca=toupper((unsigned char)*a), cb=toupper((unsigned char)*b); if(ca!=cb) return ca-cb; a++; b++; } return (unsigned char)*a-(unsigned char)*b; }
static int ci_eq(const char *a,const char *b){ return ci_cmp(a,b)==0; }
static int starts_ci(const char *s,const char *p){ while(*p){ if(!*s) return 0; if(toupper((unsigned char)*s)!=toupper((unsigned char)*p)) return 0; s++; p++; } return 1; }
static char *trim_inplace(char *s){ char *e; while(*s&&isspace((unsigned char)*s)) s++; e=s+strlen(s); while(e>s&&isspace((unsigned char)e[-1])) e--; *e=0; return s; }
static void first_word(const char *s,char *out,size_t n){ size_t i=0; while(*s&&isspace((unsigned char)*s)) s++; while(*s&&!isspace((unsigned char)*s)&&i+1<n){ out[i++]=*s++; } out[i]=0; }
static void upper_copy(char *d,const char *s,size_t n){ size_t i=0; if(!n) return; while(s&&s[i]&&i+1<n){ d[i]=(char)toupper((unsigned char)s[i]); i++; } d[i]=0; }
static int is_blank_or_comment(const char *s){ while(*s&&isspace((unsigned char)*s)) s++; return *s==0 || *s=='#'; }

/* ---------- growable string ---------- */
typedef struct { char *s; size_t len, cap; } Str;
static void str_init(Str *b){ b->s=NULL; b->len=0; b->cap=0; }
static void str_need(Str *b,size_t extra){ size_t need=b->len+extra+1; if(need>b->cap){ size_t nc=b->cap?b->cap*2:64; while(nc<need) nc*=2; b->s=(char*)xrealloc(b->s,nc); b->cap=nc; } }
static void str_addn(Str *b,const char *s,size_t n){ str_need(b,n); memcpy(b->s+b->len,s,n); b->len+=n; b->s[b->len]=0; }
static void str_add(Str *b,const char *s){ if(s) str_addn(b,s,strlen(s)); }
static void str_ch(Str *b,char c){ str_need(b,1); b->s[b->len++]=c; b->s[b->len]=0; }
static char *str_take(Str *b){ char *s=b->s?b->s:xstrdup(""); b->s=NULL; b->len=b->cap=0; return s; }

/* ---------- values ---------- */
typedef struct Value Value;
typedef struct { Value *items; int count, cap; } List;
typedef struct { char **keys; Value *vals; int count, cap; } Map;
struct Value { int type; double num; int boolean; char *str; List *list; Map *map; };
enum { V_NONE, V_NUM, V_STR, V_BOOL, V_LIST, V_MAP };

static Value v_none(void){ Value v; memset(&v,0,sizeof(v)); v.type=V_NONE; return v; }
static Value v_num(double n){ Value v=v_none(); v.type=V_NUM; v.num=n; return v; }
static Value v_bool(int b){ Value v=v_none(); v.type=V_BOOL; v.boolean=b?1:0; return v; }
static Value v_str(const char *s){ Value v=v_none(); v.type=V_STR; v.str=xstrdup(s?s:""); return v; }
static List *list_new(void){ List *l=(List*)xmalloc(sizeof(List)); l->items=NULL; l->count=l->cap=0; return l; }
static Map *map_new(void){ Map *m=(Map*)xmalloc(sizeof(Map)); m->keys=NULL; m->vals=NULL; m->count=m->cap=0; return m; }
static Value v_list(void){ Value v=v_none(); v.type=V_LIST; v.list=list_new(); return v; }
static Value v_map(void){ Value v=v_none(); v.type=V_MAP; v.map=map_new(); return v; }
static Value v_copy(Value v);
static void list_add(List *l,Value v){ if(l->count>=l->cap){ l->cap=l->cap?l->cap*2:8; l->items=(Value*)xrealloc(l->items,sizeof(Value)*l->cap);} l->items[l->count++]=v_copy(v); }
static int map_index(Map *m,const char *key){ int i; for(i=0;i<m->count;i++) if(strcmp(m->keys[i],key)==0) return i; return -1; }
static void map_put(Map *m,const char *key,Value v){ int i=map_index(m,key); if(i>=0){ m->vals[i]=v_copy(v); return;} if(m->count>=m->cap){ m->cap=m->cap?m->cap*2:8; m->keys=(char**)xrealloc(m->keys,sizeof(char*)*m->cap); m->vals=(Value*)xrealloc(m->vals,sizeof(Value)*m->cap);} m->keys[m->count]=xstrdup(key); m->vals[m->count++]=v_copy(v); }
static Value map_get(Map *m,const char *key){ int i=map_index(m,key); if(i>=0) return v_copy(m->vals[i]); return v_none(); }
static Value v_copy(Value v){ Value o=v_none(); int i; o.type=v.type; o.num=v.num; o.boolean=v.boolean; if(v.type==V_STR) o.str=xstrdup(v.str); else if(v.type==V_LIST){ o=v_list(); for(i=0;i<v.list->count;i++) list_add(o.list,v.list->items[i]); } else if(v.type==V_MAP){ o=v_map(); for(i=0;i<v.map->count;i++) map_put(o.map,v.map->keys[i],v.map->vals[i]); } return o; }
static int v_truth(Value v){ if(v.type==V_BOOL) return v.boolean; if(v.type==V_NUM) return fabs(v.num)>0.0000001; if(v.type==V_STR) return v.str&&v.str[0]; if(v.type==V_LIST) return v.list&&v.list->count>0; if(v.type==V_MAP) return v.map&&v.map->count>0; return 0; }
static double v_number(Value v){ if(v.type==V_NUM) return v.num; if(v.type==V_BOOL) return v.boolean; if(v.type==V_STR) return atof(v.str?v.str:""); return 0; }
static char *v_to_string(Value v);
static char *num_to_string(double d){ char buf[80]; if(fabs(d-(long long)d)<0.0000001) snprintf(buf,sizeof(buf),"%lld",(long long)d); else snprintf(buf,sizeof(buf),"%.15g",d); return xstrdup(buf); }
static char *v_to_string(Value v){ if(v.type==V_NONE) return xstrdup(""); if(v.type==V_NUM) return num_to_string(v.num); if(v.type==V_BOOL) return xstrdup(v.boolean?"YES":"NO"); if(v.type==V_STR) return xstrdup(v.str?v.str:""); if(v.type==V_LIST) return xstrdup("[list]"); if(v.type==V_MAP) return xstrdup("[map]"); return xstrdup(""); }
static int parse_number_strict(const char *s,double *out){ char *end; double d; if(!s) return 0; while(*s&&isspace((unsigned char)*s)) s++; if(!*s) return 0; d=strtod(s,&end); if(end==s) return 0; while(end&&*end&&isspace((unsigned char)*end)) end++; if(end&&*end) return 0; if(out) *out=d; return 1; }
static int value_compare(Value a,Value b){ char *as,*bs; int r; double x,y; if((a.type==V_NUM||a.type==V_BOOL)&&(b.type==V_NUM||b.type==V_BOOL)){ x=v_number(a); y=v_number(b); if(x<y) return -1; if(x>y) return 1; return 0; }
 if(a.type==V_STR && (b.type==V_NUM||b.type==V_BOOL) && parse_number_strict(a.str,&x)){ y=v_number(b); if(x<y) return -1; if(x>y) return 1; return 0; }
 if((a.type==V_NUM||a.type==V_BOOL) && b.type==V_STR && parse_number_strict(b.str,&y)){ x=v_number(a); if(x<y) return -1; if(x>y) return 1; return 0; }
 if(a.type==V_STR && b.type==V_STR && parse_number_strict(a.str,&x) && parse_number_strict(b.str,&y)){ if(x<y) return -1; if(x>y) return 1; return 0; }
 as=v_to_string(a); bs=v_to_string(b); r=strcmp(as,bs); free(as); free(bs); return r; }

/* ---------- env/program/runtime ---------- */
typedef struct Var { char *name; Value val; struct Var *next; } Var;
typedef struct Program { char *path; char **lines; int count, cap; } Program;
typedef struct Function { char *name; char **params; int pcnt; Program *prog; int start, end; struct Function *next; } Function;
typedef struct Module { char *ns; char *kind; struct Module *next; } Module;
typedef struct FieldDef { char *name; char *type; struct FieldDef *next; } FieldDef;
typedef struct ClassDef { char *name; FieldDef *fields; struct ClassDef *next; } ClassDef;
typedef struct Runtime {
 Var *globals; Var *locals; Function *funcs; Module *modules; ClassDef *classes;
 Str captured; int capture; int trace;
 int error; char *err_msg; char *err_file; int err_line;
 int returning; Value ret;
 Program **programs; int pcount, pcap;
 char **import_stack; int import_depth;
 int script_argc; char **script_argv;
} Runtime;
static void rt_init(Runtime *rt){ memset(rt,0,sizeof(*rt)); str_init(&rt->captured); rt->ret=v_none(); srand(1); }
static Var *env_find(Var *v,const char *name){ while(v){ if(strcmp(v->name,name)==0) return v; v=v->next;} return NULL; }
static Value rt_get(Runtime *rt,const char *name){ Var *v=env_find(rt->locals,name); if(v) return v_copy(v->val); v=env_find(rt->globals,name); if(v) return v_copy(v->val); return v_none(); }
static int rt_has(Runtime *rt,const char *name){ return env_find(rt->locals,name)||env_find(rt->globals,name); }
static void rt_set(Runtime *rt,const char *name,Value val){ Var **head=rt->locals?&rt->locals:&rt->globals; Var *v=env_find(*head,name); if(!v && rt->locals) v=env_find(rt->globals,name); if(v){ v->val=v_copy(val); return;} v=(Var*)xmalloc(sizeof(Var)); v->name=xstrdup(name); v->val=v_copy(val); v->next=*head; *head=v; }
static void rt_set_global(Runtime *rt,const char *name,Value val){ Var *v=env_find(rt->globals,name); if(v){ v->val=v_copy(val); return;} v=(Var*)xmalloc(sizeof(Var)); v->name=xstrdup(name); v->val=v_copy(val); v->next=rt->globals; rt->globals=v; }

static void rt_error(Runtime *rt,const char *file,int line,const char *fmt,...);
static char *normalize_path_copy(const char *path){ char *out=xstrdup(path?path:""); char *p; for(p=out;*p;p++) if(*p=='\\') *p='/'; return out; }
static int claro_is_type_word(const char *s){ return s&&(ci_eq(s,"NUMBER")||ci_eq(s,"TEXT")||ci_eq(s,"YESNO")||ci_eq(s,"BOOL")||ci_eq(s,"BOOLEAN")||ci_eq(s,"LIST")||ci_eq(s,"MAP")||ci_eq(s,"OBJECT")||ci_eq(s,"ANY")); }
static const char *claro_value_type(Value v){ if(v.type==V_NUM) return "NUMBER"; if(v.type==V_STR) return "TEXT"; if(v.type==V_BOOL) return "YESNO"; if(v.type==V_LIST) return "LIST"; if(v.type==V_MAP) return "MAP"; return "NONE"; }
static Value claro_default_for_type(const char *type){ if(ci_eq(type,"NUMBER")) return v_num(0); if(ci_eq(type,"TEXT")) return v_str(""); if(ci_eq(type,"YESNO")||ci_eq(type,"BOOL")||ci_eq(type,"BOOLEAN")) return v_bool(0); if(ci_eq(type,"LIST")) return v_list(); if(ci_eq(type,"MAP")||ci_eq(type,"OBJECT")) return v_map(); return v_none(); }
static int claro_type_matches(const char *type,Value v){ if(!type||!*type||ci_eq(type,"ANY")) return 1; if(ci_eq(type,"NUMBER")) return v.type==V_NUM || (v.type==V_STR && parse_number_strict(v.str,NULL)); if(ci_eq(type,"TEXT")) return v.type==V_STR; if(ci_eq(type,"YESNO")||ci_eq(type,"BOOL")||ci_eq(type,"BOOLEAN")) return v.type==V_BOOL; if(ci_eq(type,"LIST")) return v.type==V_LIST; if(ci_eq(type,"MAP")||ci_eq(type,"OBJECT")) return v.type==V_MAP; return 1; }
static int claro_value_from_text(const char *type,const char *text,Value *out){ double d; if(!type||!*type||ci_eq(type,"TEXT")||ci_eq(type,"ANY")){ if(out) *out=v_str(text?text:""); return 1; } if(ci_eq(type,"NUMBER")){ if(parse_number_strict(text,&d)){ if(out) *out=v_num(d); return 1; } return 0; } if(ci_eq(type,"YESNO")||ci_eq(type,"BOOL")||ci_eq(type,"BOOLEAN")){ if(ci_eq(text,"YES")||ci_eq(text,"TRUE")||strcmp(text,"1")==0){ if(out) *out=v_bool(1); return 1; } if(ci_eq(text,"NO")||ci_eq(text,"FALSE")||strcmp(text,"0")==0){ if(out) *out=v_bool(0); return 1; } return 0; } if(ci_eq(type,"LIST")){ if(out) *out=v_list(); return 1; } if(ci_eq(type,"MAP")||ci_eq(type,"OBJECT")){ if(out) *out=v_map(); return 1; } if(out) *out=v_str(text?text:""); return 1; }
static const char *runtime_type_for(Runtime *rt,const char *name,char *buf,size_t n);
static const char *declared_type_for_expr(Runtime *rt,const char *expr,char *buf,size_t n){ char tmp[256]; const char *t=expr; size_t i=0; while(t&&*t&&isspace((unsigned char)*t)) t++; if(!t||!*t) return NULL; while(t[i]&&(isalnum((unsigned char)t[i])||t[i]=='_'||t[i]=='.')&&i+1<sizeof(tmp)){ tmp[i]=t[i]; i++; } tmp[i]=0; if(!tmp[0]) return NULL; return runtime_type_for(rt,tmp,buf,n); }
static void type_key_for(const char *name,char *out,size_t n){ snprintf(out,n,"__type_%s",name?name:""); }
static const char *runtime_type_for(Runtime *rt,const char *name,char *buf,size_t n){ Value tv; type_key_for(name,buf,n); tv=rt_get(rt,buf); if(tv.type==V_STR && tv.str && tv.str[0]) return tv.str; return NULL; }
static int rt_set_checked(Runtime *rt,const char *file,int line,const char *name,const char *type,Value val){ char key[320], oldbuf[320]; const char *oldtype=NULL; char *dot; if(!name||!*name) return 0; if(type&&*type){ type_key_for(name,key,sizeof(key)); rt_set(rt,key,v_str(type)); oldtype=type; } else oldtype=runtime_type_for(rt,name,oldbuf,sizeof(oldbuf)); if(oldtype && !claro_type_matches(oldtype,val)){ rt_error(rt,file,line,"%s must be %s, but got %s.",name,oldtype,claro_value_type(val)); return 0; } dot=strchr(name,'.'); if(dot){ char objname[256]; char field[256]; Value obj; snprintf(objname,sizeof(objname),"%.*s",(int)(dot-name),name); snprintf(field,sizeof(field),"%s",dot+1); obj=rt_get(rt,objname); if(obj.type!=V_MAP) obj=v_map(); map_put(obj.map,field,val); rt_set(rt,objname,obj); }
 rt_set(rt,name,val); return 1; }
static void graphics_note(Runtime *rt,const char *what){ (void)what; rt_set(rt,"GRAPHICS_READY",v_bool(1)); }

static void rt_error(Runtime *rt,const char *file,int line,const char *fmt,...){ va_list ap; char buf[1024]; char *nfile; if(rt->error) return; va_start(ap,fmt); vsnprintf(buf,sizeof(buf),fmt,ap); va_end(ap); nfile=normalize_path_copy(file?file:""); rt->error=1; rt->err_msg=xstrdup(buf); rt->err_file=xstrdup(nfile); rt->err_line=line; rt_set(rt,"LASTERROR",v_str(buf)); rt_set(rt,"LASTERRORFILE",v_str(nfile)); rt_set(rt,"LASTERRORLINE",v_num(line)); free(nfile); }
static void rt_clear_error(Runtime *rt){ rt->error=0; }
static void out_line(Runtime *rt,Value v){ char *s=v_to_string(v); if(rt->capture){ str_add(&rt->captured,s); str_ch(&rt->captured,'\n'); } else { printf("%s\n",s); } free(s); }
static void add_function(Runtime *rt,const char *name,char **params,int pcnt,Program *p,int start,int end){ Function *f=(Function*)xmalloc(sizeof(Function)); int i; f->name=xstrdup(name); f->pcnt=pcnt; f->params=(char**)xmalloc(sizeof(char*)*(pcnt?pcnt:1)); for(i=0;i<pcnt;i++) f->params[i]=xstrdup(params[i]); f->prog=p; f->start=start; f->end=end; f->next=rt->funcs; rt->funcs=f; }
static Function *find_function(Runtime *rt,const char *name){ Function *f=rt->funcs; while(f){ if(strcmp(f->name,name)==0) return f; f=f->next;} return NULL; }
static void add_module(Runtime *rt,const char *ns,const char *kind){ Module *m=(Module*)xmalloc(sizeof(Module)); m->ns=xstrdup(ns); m->kind=xstrdup(kind); m->next=rt->modules; rt->modules=m; }
static const char *module_kind(Runtime *rt,const char *ns){ Module *m=rt->modules; while(m){ if(strcmp(m->ns,ns)==0) return m->kind; m=m->next;} return NULL; }

static ClassDef *find_class(Runtime *rt,const char *name){ ClassDef *c=rt->classes; while(c){ if(strcmp(c->name,name)==0) return c; c=c->next; } return NULL; }
static ClassDef *add_class(Runtime *rt,const char *name){ ClassDef *c=find_class(rt,name); if(c) return c; c=(ClassDef*)xmalloc(sizeof(ClassDef)); c->name=xstrdup(name); c->fields=NULL; c->next=rt->classes; rt->classes=c; return c; }
static FieldDef *find_field(ClassDef *c,const char *name){ FieldDef *f=c?c->fields:NULL; while(f){ if(strcmp(f->name,name)==0) return f; f=f->next; } return NULL; }
static void class_add_field(ClassDef *c,const char *name,const char *type){ FieldDef *f; if(!c||!name||!*name) return; f=find_field(c,name); if(f){ free(f->type); f->type=xstrdup(type&&*type?type:"ANY"); return; } f=(FieldDef*)xmalloc(sizeof(FieldDef)); f->name=xstrdup(name); f->type=xstrdup(type&&*type?type:"ANY"); f->next=c->fields; c->fields=f; }
static const char *object_class_name(Value obj){ Value cv; if(obj.type!=V_MAP||!obj.map) return NULL; cv=map_get(obj.map,"class"); if(cv.type==V_STR && cv.str && cv.str[0]) return cv.str; return NULL; }

/* ---------- tokenization / expressions ---------- */
typedef struct { char **t; int n, cap, pos; } Tokens;
static void toks_add(Tokens *ts,const char *s,size_t n){ if(ts->n>=ts->cap){ ts->cap=ts->cap?ts->cap*2:16; ts->t=(char**)xrealloc(ts->t,sizeof(char*)*ts->cap);} ts->t[ts->n]=(char*)xmalloc(n+1); memcpy(ts->t[ts->n],s,n); ts->t[ts->n][n]=0; ts->n++; }
static Tokens tokenize(const char *s){ Tokens ts; size_t i=0; memset(&ts,0,sizeof(ts)); while(s[i]){ if(isspace((unsigned char)s[i])){ i++; continue;} if(s[i]=='"'){ Str b; Str q; str_init(&b); str_init(&q); i++; while(s[i]&&s[i]!='"'){ if(s[i]=='\\'){ i++; if(s[i]=='n') str_ch(&b,'\n'); else if(s[i]=='t') str_ch(&b,'\t'); else if(s[i]=='r') str_ch(&b,'\r'); else if(s[i]=='"') str_ch(&b,'"'); else if(s[i]=='\\') str_ch(&b,'\\'); else if(s[i]) str_ch(&b,s[i]); if(s[i]) i++; } else str_ch(&b,s[i++]); } if(s[i]=='"') i++; str_ch(&q,'\001'); str_add(&q,b.s?b.s:""); toks_add(&ts,q.s?q.s:"",strlen(q.s?q.s:"")); free(b.s); free(q.s); continue; }
  if(strchr("(),",s[i])){ toks_add(&ts,s+i,1); i++; continue; }
  if((s[i]=='!'||s[i]=='<'||s[i]=='>')&&s[i+1]=='='){ toks_add(&ts,s+i,2); i+=2; continue; }
  if(strchr("+-*/=<>",s[i])){ toks_add(&ts,s+i,1); i++; continue; }
  { size_t st=i; while(s[i]&&!isspace((unsigned char)s[i])&&!strchr("(),+-*/=<>!",s[i])) i++; toks_add(&ts,s+st,i-st); }
 }
 return ts; }
static int tok_end(Tokens *ts){ return ts->pos>=ts->n; }
static char *tok_peek(Tokens *ts){ return tok_end(ts)?NULL:ts->t[ts->pos]; }
static char *tok_next(Tokens *ts){ return tok_end(ts)?NULL:ts->t[ts->pos++]; }
static int tok_match(Tokens *ts,const char *s){ if(!tok_end(ts)&&ci_eq(ts->t[ts->pos],s)){ ts->pos++; return 1;} return 0; }
static Value parse_expr(Runtime *rt,Tokens *ts);
static Value parse_primary(Runtime *rt,Tokens *ts){ char *t=tok_next(ts); Value v; if(!t) return v_none(); if(strcmp(t,"(")==0){ v=parse_expr(rt,ts); tok_match(ts,")"); return v; } if(t[0]=='\001') return v_str(t+1); if(ci_eq(t,"YES")) return v_bool(1); if(ci_eq(t,"NO")) return v_bool(0); if(ci_eq(t,"NONE")) return v_none(); if(ci_eq(t,"LIST")) return v_list(); if(ci_eq(t,"MAP")) return v_map(); if((isdigit((unsigned char)t[0])||((t[0]=='-'||t[0]=='+')&&isdigit((unsigned char)t[1])))){ char *end=NULL; double d=strtod(t,&end); if(end&&*end==0) return v_num(d); }
 /* Because tokenizer stores string literals as raw token text, quoted and bare identifiers are ambiguous. Bare identifiers resolve to variables; unresolved become strings only when they came from quotes. We mark quoted literals by detecting tokens that contain spaces/newlines or are followed by original quotes is not possible here. To keep Claro beginner-friendly, unresolved words become variable lookup if known, otherwise plain text. */
 if(rt_has(rt,t)) return rt_get(rt,t);
 if(isalpha((unsigned char)t[0]) || strchr(t,'.')){ rt_error(rt,"",0,"I do not know the variable \"%s\" yet.",t); return v_none(); }
 return v_str(t);
}
static Value parse_unary(Runtime *rt,Tokens *ts){ if(tok_match(ts,"NOT")){ Value v=parse_unary(rt,ts); return v_bool(!v_truth(v)); } if(tok_match(ts,"-")){ Value v=parse_unary(rt,ts); return v_num(-v_number(v)); } return parse_primary(rt,ts); }
static Value parse_mul(Runtime *rt,Tokens *ts){ Value v=parse_unary(rt,ts); while(!tok_end(ts)){ char *op=tok_peek(ts); if(strcmp(op,"*")&&strcmp(op,"/")) break; tok_next(ts); Value r=parse_unary(rt,ts); if(strcmp(op,"*")==0) v=v_num(v_number(v)*v_number(r)); else v=v_num(v_number(r)==0?0:v_number(v)/v_number(r)); } return v; }
static Value parse_add(Runtime *rt,Tokens *ts){ Value v=parse_mul(rt,ts); while(!tok_end(ts)){ char *op=tok_peek(ts); if(strcmp(op,"+")&&strcmp(op,"-")) break; tok_next(ts); Value r=parse_mul(rt,ts); if(strcmp(op,"+")==0){ double x,y; int vn=0,rn=0; if(v.type==V_NUM||v.type==V_BOOL){ x=v_number(v); vn=1; } else if(v.type==V_STR && parse_number_strict(v.str,&x)) vn=1; if(r.type==V_NUM||r.type==V_BOOL){ y=v_number(r); rn=1; } else if(r.type==V_STR && parse_number_strict(r.str,&y)) rn=1; if(vn&&rn) v=v_num(x+y); else if(v.type==V_STR||r.type==V_STR){ char *a=v_to_string(v), *b=v_to_string(r); Str s; str_init(&s); str_add(&s,a); str_add(&s,b); v=v_str(s.s?s.s:""); free(a); free(b); free(s.s); } else v=v_num(v_number(v)+v_number(r)); } else v=v_num(v_number(v)-v_number(r)); } return v; }
static Value parse_cmp(Runtime *rt,Tokens *ts){ Value v=parse_add(rt,ts); while(!tok_end(ts)){ char *op=tok_peek(ts); int c; if(!(ci_eq(op,"IS")||!strcmp(op,"=")||!strcmp(op,"!=")||!strcmp(op,"<")||!strcmp(op,"<=")||!strcmp(op,">")||!strcmp(op,">="))) break; tok_next(ts); Value r=parse_add(rt,ts); c=value_compare(v,r); if(ci_eq(op,"IS")||!strcmp(op,"=")) v=v_bool(c==0); else if(!strcmp(op,"!=")) v=v_bool(c!=0); else if(!strcmp(op,"<")) v=v_bool(c<0); else if(!strcmp(op,"<=")) v=v_bool(c<=0); else if(!strcmp(op,">")) v=v_bool(c>0); else v=v_bool(c>=0); } return v; }
static Value parse_and(Runtime *rt,Tokens *ts){ Value v=parse_cmp(rt,ts); while(tok_match(ts,"AND")){ Value r=parse_cmp(rt,ts); v=v_bool(v_truth(v)&&v_truth(r)); } return v; }
static Value parse_expr(Runtime *rt,Tokens *ts){ Value v=parse_and(rt,ts); while(tok_match(ts,"OR")){ Value r=parse_and(rt,ts); v=v_bool(v_truth(v)||v_truth(r)); } return v; }
static Value eval_expr(Runtime *rt,const char *expr){ Tokens ts=tokenize(expr); Value v=parse_expr(rt,&ts); return v; }

/* Better string token parsing helpers for commands. */
static char *unquote_token(const char **ps){ const char *s=*ps; Str b; str_init(&b); while(*s&&isspace((unsigned char)*s)) s++; if(*s=='"'){ s++; while(*s&&*s!='"'){ if(*s=='\\'){ s++; if(*s=='n') str_ch(&b,'\n'); else if(*s=='t') str_ch(&b,'\t'); else if(*s=='r') str_ch(&b,'\r'); else if(*s=='"') str_ch(&b,'"'); else if(*s=='\\') str_ch(&b,'\\'); else if(*s) str_ch(&b,*s); if(*s) s++; } else str_ch(&b,*s++); } if(*s=='"') s++; } else { while(*s&&!isspace((unsigned char)*s)) str_ch(&b,*s++); } *ps=s; return str_take(&b); }
static char *expr_after_word(const char *line,const char *word){ const char *p=line; while(*p&&isspace((unsigned char)*p)) p++; while(*p&&!isspace((unsigned char)*p)) p++; while(*p&&isspace((unsigned char)*p)) p++; (void)word; return xstrdup(p); }
static char *substr(const char *a,const char *b){ if(b<a) b=a; char *s=(char*)xmalloc((size_t)(b-a)+1); memcpy(s,a,(size_t)(b-a)); s[b-a]=0; return s; }
static const char *find_word_ci(const char *s,const char *word){ size_t n=strlen(word); int inq=0, depth=0; const char *p=s; while(*p){ if(*p=='"'&&(p==s||p[-1]!='\\')) inq=!inq; if(!inq){ if(*p=='(') depth++; else if(*p==')') depth--; if(depth==0 && (p==s||isspace((unsigned char)p[-1])) && strnicmp2(p,word,n)==0 && (p[n]==0||isspace((unsigned char)p[n]))) return p; } p++; } return NULL; }
static int split_args(const char *s,char ***out){ int count=0, cap=0; char **arr=NULL; int inq=0, depth=0; const char *st=s,*p=s; while(1){ char c=*p; if(c=='"'&&(p==s||p[-1]!='\\')) inq=!inq; if(!inq){ if(c=='(') depth++; else if(c==')') depth--; if((c==','&&depth==0)||c==0){ char *part=substr(st,p); char *t=trim_inplace(part); if(count>=cap){ cap=cap?cap*2:4; arr=(char**)xrealloc(arr,sizeof(char*)*cap);} arr[count++]=xstrdup(t); free(part); if(c==0) break; st=p+1; } } p++; } *out=arr; return count; }

static int is_word_token(const char *s){ if(!s||!*s) return 0; if(!(isalpha((unsigned char)s[0])||s[0]=='_')) return 0; for(s++;*s;s++) if(!(isalnum((unsigned char)*s)||*s=='_')) return 0; return 1; }
static char *text_upper_copy(const char *s){ char *o=xstrdup(s?s:""); int i; for(i=0;o[i];i++) o[i]=(char)toupper((unsigned char)o[i]); return o; }
static char *text_lower_copy(const char *s){ char *o=xstrdup(s?s:""); int i; for(i=0;o[i];i++) o[i]=(char)tolower((unsigned char)o[i]); return o; }
static char *text_trim_copy(const char *s){ char *o=xstrdup(s?s:""); char *t=trim_inplace(o); char *r=xstrdup(t); free(o); return r; }
static int str_starts_with(const char *s,const char *prefix){ size_t n=strlen(prefix?prefix:""); return strncmp(s?s:"",prefix?prefix:"",n)==0; }
static int str_ends_with(const char *s,const char *suffix){ size_t a=strlen(s?s:""), b=strlen(suffix?suffix:""); return b<=a && strcmp((s?s:"")+a-b,suffix?suffix:"")==0; }
static char *capture_command_output(const char *cmd,int *exit_code){
 Str out; char buf[512]; FILE *fp; str_init(&out);
#ifdef _WIN32
 fp=_popen(cmd,"r");
#else
 fp=popen(cmd,"r");
#endif
 if(!fp){ if(exit_code) *exit_code=-1; return xstrdup(""); }
 while(fgets(buf,sizeof(buf),fp)) str_add(&out,buf);
#ifdef _WIN32
 if(exit_code) *exit_code=_pclose(fp);
#else
 if(exit_code) *exit_code=pclose(fp);
#endif
 return str_take(&out);
}

static int claro_url_is_safe(const char *url){
 int i;
 if(!url||!*url) return 0;
 if(!(starts_ci(url,"http://")||starts_ci(url,"https://")||starts_ci(url,"claro://"))) return 0;
 for(i=0;url[i];i++){
  unsigned char c=(unsigned char)url[i];
  if(c<32||c>126) return 0;
  if(url[i]=='"'||url[i]=='\''||url[i]=='`'||url[i]=='$'||url[i]=='\\'||url[i]=='|'||url[i]=='<'||url[i]=='>') return 0;
 }
 return 1;
}
static char *claro_mock_http(const char *url,int *status){
 if(starts_ci(url,"claro://hello")){ if(status) *status=200; return xstrdup("Hello from Claro networking."); }
 if(starts_ci(url,"claro://json")){ if(status) *status=200; return xstrdup("{\"message\":\"Hello from Claro\",\"ok\":true}"); }
 if(starts_ci(url,"claro://empty")){ if(status) *status=204; return xstrdup(""); }
 if(status) *status=404; return xstrdup("Claro mock URL was not found.");
}
static char *claro_http_get_text(const char *url,int *http_status,int *exit_code){
 char cmd[2300]; char *raw,*mark,*body; const char *marker="\n__CLARO_HTTP_STATUS__";
 if(http_status) *http_status=0;
 if(exit_code) *exit_code=0;
 if(starts_ci(url,"claro://")) return claro_mock_http(url,http_status);
 snprintf(cmd,sizeof(cmd),"curl -L -s -m 15 -w \"\\n__CLARO_HTTP_STATUS__%%{http_code}\" \"%s\"",url);
 raw=capture_command_output(cmd,exit_code);
 mark=strstr(raw,marker);
 if(mark){ *mark=0; if(http_status) *http_status=atoi(mark+strlen(marker)); body=xstrdup(raw); free(raw); return body; }
 if(http_status) *http_status=0;
 return raw;
}
static int write_text_bytes(const char *path,const char *text){ FILE *f=fopen(path,"wb"); if(!f) return 0; fwrite(text?text:"",1,strlen(text?text:""),f); fclose(f); return 1; }

static int copy_file_bytes(const char *src,const char *dst){ FILE *a=fopen(src,"rb"), *b; char buf[8192]; size_t n; if(!a) return 0; b=fopen(dst,"wb"); if(!b){ fclose(a); return 0; } while((n=fread(buf,1,sizeof(buf),a))>0) fwrite(buf,1,n,b); fclose(a); fclose(b); return 1; }
static int make_folder(const char *path){
#ifdef _WIN32
 return _mkdir(path)==0 || errno==EEXIST;
#else
 return mkdir(path,0777)==0 || errno==EEXIST;
#endif
}
static int remove_folder(const char *path){
#ifdef _WIN32
 return _rmdir(path)==0;
#else
 return rmdir(path)==0;
#endif
}
static Value list_folder_value(const char *path){ Value arr=v_list();
#if defined(_WIN32) && !defined(__MINGW32__)
 (void)path;
#else
 DIR *d=opendir(path); struct dirent *de; if(!d) return arr; while((de=readdir(d))){ if(strcmp(de->d_name,".")&&strcmp(de->d_name,"..")) list_add(arr.list,v_str(de->d_name)); } closedir(d);
#endif
 return arr; }
static void value_list_sort(Value v){ int i,j; if(v.type!=V_LIST||!v.list) return; for(i=0;i<v.list->count;i++) for(j=i+1;j<v.list->count;j++){ char *a=v_to_string(v.list->items[i]); char *b=v_to_string(v.list->items[j]); if(strcmp(a,b)>0){ Value tmp=v.list->items[i]; v.list->items[i]=v.list->items[j]; v.list->items[j]=tmp; } free(a); free(b); } }
static void value_list_reverse(Value v){ int i; if(v.type!=V_LIST||!v.list) return; for(i=0;i<v.list->count/2;i++){ Value tmp=v.list->items[i]; v.list->items[i]=v.list->items[v.list->count-1-i]; v.list->items[v.list->count-1-i]=tmp; } }


/* ---------- program loading / blocks ---------- */
static Program *load_program(Runtime *rt,const char *path){ FILE *f; char buf[4096]; Program *p; int i; for(i=0;i<rt->pcount;i++) if(strcmp(rt->programs[i]->path,path)==0) return rt->programs[i]; f=fopen(path,"rb"); if(!f) return NULL; p=(Program*)xmalloc(sizeof(Program)); p->path=xstrdup(path); p->lines=NULL; p->count=p->cap=0; while(fgets(buf,sizeof(buf),f)){ size_t n=strlen(buf); while(n&& (buf[n-1]=='\n'||buf[n-1]=='\r')) buf[--n]=0; if(p->count>=p->cap){ p->cap=p->cap?p->cap*2:32; p->lines=(char**)xrealloc(p->lines,sizeof(char*)*p->cap);} p->lines[p->count++]=xstrdup(buf); } fclose(f); if(rt->pcount>=rt->pcap){ rt->pcap=rt->pcap?rt->pcap*2:16; rt->programs=(Program**)xrealloc(rt->programs,sizeof(Program*)*rt->pcap);} rt->programs[rt->pcount++]=p; return p; }
static void scan_functions(Runtime *rt,Program *p,const char *prefix);
static void line_word(Program *p,int i,char *up,size_t n){ char tmp[512],w[128]; strncpy(tmp,p->lines[i],sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; first_word(trim_inplace(tmp),w,sizeof(w)); upper_copy(up,w,n); }
static int line_is_block_opener(Program *p,int i,const char *up){ char *t; char tmp[512]; if(ci_eq(up,"IF")||ci_eq(up,"FOR")||ci_eq(up,"REPEAT")||ci_eq(up,"TEACH")||ci_eq(up,"TRY")||ci_eq(up,"COMMENT")||ci_eq(up,"CLASS")) return 1; if(ci_eq(up,"DO")){ strncpy(tmp,p->lines[i],sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); return find_word_ci(t,"TIMES")!=NULL; } if(ci_eq(up,"START")){ strncpy(tmp,p->lines[i],sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); return starts_ci(t+5," TASK"); } return 0; }
static int line_is_block_closer(const char *up){ return ci_eq(up,"END")||ci_eq(up,"ENDIF")||ci_eq(up,"DONE")||ci_eq(up,"UNTIL")||ci_eq(up,"LEARNED")||ci_eq(up,"ENDTRY")||ci_eq(up,"ENDCOMMENT")||ci_eq(up,"ENDCLASS")||ci_eq(up,"ENDTASK"); }
static int match_block(Program *p,int start,const char *open,const char *close,const char *mid,int *midpos){ int depth=0,i; char up[64]; if(midpos) *midpos=-1; for(i=start;i<p->count;i++){ line_word(p,i,up,sizeof(up)); if(line_is_block_opener(p,i,up)){ depth++; continue; } if(mid&&ci_eq(up,mid)&&depth==1){ if(midpos&&*midpos<0) *midpos=i; continue; } if(depth>1 && line_is_block_closer(up)){ depth--; continue; } if(depth==1 && (ci_eq(up,close)||ci_eq(up,"END"))) { depth--; if(depth==0) return i; } } return -1; }
static int find_done(Program *p,int start){ int depth=0,i; char up[64]; for(i=start;i<p->count;i++){ line_word(p,i,up,sizeof(up)); if(line_is_block_opener(p,i,up)){ depth++; continue; } if(line_is_block_closer(up)){ depth--; if(depth==0) return i; } } return -1; }

/* ---------- JSON ---------- */
typedef struct { const char *s; } JsonP;
static void jp_ws(JsonP *j){ while(*j->s&&isspace((unsigned char)*j->s)) j->s++; }
static char *jp_string(JsonP *j){ Str b; str_init(&b); jp_ws(j); if(*j->s!='"') return xstrdup(""); j->s++; while(*j->s&&*j->s!='"'){ if(*j->s=='\\'){ j->s++; if(*j->s=='n') str_ch(&b,'\n'); else if(*j->s=='t') str_ch(&b,'\t'); else if(*j->s=='r') str_ch(&b,'\r'); else if(*j->s) str_ch(&b,*j->s); if(*j->s) j->s++; } else str_ch(&b,*j->s++); } if(*j->s=='"') j->s++; return str_take(&b); }
static Value jp_value(JsonP *j);
static Value jp_array(JsonP *j){ Value arr=v_list(); jp_ws(j); if(*j->s=='[') j->s++; jp_ws(j); if(*j->s==']'){ j->s++; return arr; } while(*j->s){ Value v=jp_value(j); list_add(arr.list,v); jp_ws(j); if(*j->s==','){ j->s++; continue;} if(*j->s==']'){ j->s++; break;} } return arr; }
static Value jp_object(JsonP *j){ Value obj=v_map(); jp_ws(j); if(*j->s=='{') j->s++; jp_ws(j); if(*j->s=='}'){ j->s++; return obj; } while(*j->s){ char *k=jp_string(j); jp_ws(j); if(*j->s==':') j->s++; Value v=jp_value(j); map_put(obj.map,k,v); free(k); jp_ws(j); if(*j->s==','){ j->s++; continue;} if(*j->s=='}'){ j->s++; break;} } return obj; }
static Value jp_value(JsonP *j){ char *end; jp_ws(j); if(*j->s=='"'){ char *s=jp_string(j); Value v=v_str(s); free(s); return v;} if(*j->s=='{') return jp_object(j); if(*j->s=='[') return jp_array(j); if(!strncmp(j->s,"true",4)){ j->s+=4; return v_bool(1);} if(!strncmp(j->s,"false",5)){ j->s+=5; return v_bool(0);} if(!strncmp(j->s,"null",4)){ j->s+=4; return v_none();} end=NULL; { double d=strtod(j->s,&end); if(end&&end!=j->s){ j->s=end; return v_num(d);} } return v_none(); }
static Value parse_json_text(const char *s){ JsonP j; j.s=s; return jp_value(&j); }
static void json_escape(Str *b,const char *s){ str_ch(b,'"'); while(s&&*s){ if(*s=='"'){ str_add(b,"\\\""); } else if(*s=='\\'){ str_add(b,"\\\\"); } else if(*s=='\n'){ str_add(b,"\\n"); } else str_ch(b,*s); s++; } str_ch(b,'"'); }
static void json_write(Str *b,Value v,int pretty,int indent);
static void indent_add(Str *b,int n){ int i; for(i=0;i<n;i++) str_ch(b,' '); }
static void json_write(Str *b,Value v,int pretty,int indent){ int i; char *s; if(v.type==V_STR){ json_escape(b,v.str); } else if(v.type==V_NUM){ s=num_to_string(v.num); str_add(b,s); free(s); } else if(v.type==V_BOOL){ str_add(b,v.boolean?"true":"false"); } else if(v.type==V_NONE){ str_add(b,"null"); } else if(v.type==V_LIST){ str_ch(b,'['); if(pretty&&v.list->count) str_ch(b,'\n'); for(i=0;i<v.list->count;i++){ if(pretty) indent_add(b,indent+2); json_write(b,v.list->items[i],pretty,indent+2); if(i+1<v.list->count) str_ch(b,','); if(pretty) str_ch(b,'\n'); } if(pretty&&v.list->count) indent_add(b,indent); str_ch(b,']'); } else if(v.type==V_MAP){ str_ch(b,'{'); if(pretty&&v.map->count) str_ch(b,'\n'); for(i=0;i<v.map->count;i++){ if(pretty) indent_add(b,indent+2); json_escape(b,v.map->keys[i]); str_ch(b,':'); if(pretty) str_ch(b,' '); json_write(b,v.map->vals[i],pretty,indent+2); if(i+1<v.map->count) str_ch(b,','); if(pretty) str_ch(b,'\n'); } if(pretty&&v.map->count) indent_add(b,indent); str_ch(b,'}'); } }
static char *make_json(Value v,int pretty){ Str b; str_init(&b); json_write(&b,v,pretty,0); return str_take(&b); }

/* ---------- stdlib built-ins ---------- */
static Value builtin_call(Runtime *rt,const char *name,Value *args,int argc,int *handled){ char ns[128], fn[128]; const char *dot=strrchr(name,'.'); const char *kind=NULL; *handled=0; if(!dot) return v_none(); snprintf(ns,sizeof(ns),"%.*s",(int)(dot-name),name); snprintf(fn,sizeof(fn),"%s",dot+1); kind=module_kind(rt,ns); if(!kind) return v_none(); *handled=1;
 if(strcmp(kind,"text")==0){ char *a=argc>0?v_to_string(args[0]):xstrdup(""); char *b=argc>1?v_to_string(args[1]):xstrdup(""); int i; if(strcmp(fn,"upper")==0){ for(i=0;a[i];i++) a[i]=(char)toupper((unsigned char)a[i]); Value r=v_str(a); free(a); free(b); return r; } if(strcmp(fn,"lower")==0){ for(i=0;a[i];i++) a[i]=(char)tolower((unsigned char)a[i]); Value r=v_str(a); free(a); free(b); return r; } if(strcmp(fn,"contains")==0){ Value r=v_bool(strstr(a,b)!=NULL); free(a); free(b); return r; } if(strcmp(fn,"endswith")==0){ size_t la=strlen(a), lb=strlen(b); Value r=v_bool(lb<=la && strcmp(a+la-lb,b)==0); free(a); free(b); return r; } if(strcmp(fn,"split2")==0){ char *pos=strstr(a,b); Value arr=v_list(); if(pos){ char *left=substr(a,pos); list_add(arr.list,v_str(left)); list_add(arr.list,v_str(pos+strlen(b))); free(left); } else list_add(arr.list,v_str(a)); free(a); free(b); return arr; } free(a); free(b); }
 if(strcmp(kind,"math")==0){ if(strcmp(fn,"abs")==0) return v_num(fabs(v_number(args[0]))); if(strcmp(fn,"clamp")==0){ double x=v_number(args[0]), lo=v_number(args[1]), hi=v_number(args[2]); if(x<lo)x=lo; if(x>hi)x=hi; return v_num(x); } }
 if(strcmp(kind,"random")==0){ if(strcmp(fn,"seed")==0){ srand((unsigned)v_number(args[0])); return v_none(); } if(strcmp(fn,"int")==0){ int a=(int)v_number(args[0]), b=(int)v_number(args[1]); int r=a + (rand() % (b-a+1)); return v_num(r); } }
 if(strcmp(kind,"csv")==0){ if(strcmp(fn,"read")==0){ char *txt=argc>0?v_to_string(args[0]):xstrdup(""); char *del=argc>1?v_to_string(args[1]):xstrdup(","); char d=del[0]?del[0]:','; Value rows=v_list(); const char *p=txt; while(*p){ Value row=v_list(); Str field; str_init(&field); int inq=0; while(*p&&*p!='\n'&&*p!='\r'){ if(*p=='"'){ if(inq&&p[1]=='"'){ str_ch(&field,'"'); p+=2; continue;} inq=!inq; p++; continue;} if(!inq&&*p==d){ list_add(row.list,v_str(field.s?field.s:"")); field.len=0; if(field.s) field.s[0]=0; p++; continue;} str_ch(&field,*p++); } list_add(row.list,v_str(field.s?field.s:"")); free(field.s); list_add(rows.list,row); while(*p=='\r'||*p=='\n') p++; } free(txt); free(del); return rows; }
  if(strcmp(fn,"write")==0){ char *del=argc>1?v_to_string(args[1]):xstrdup(","); char d=del[0]?del[0]:','; Str out; str_init(&out); int i,j; if(argc>0&&args[0].type==V_LIST){ for(i=0;i<args[0].list->count;i++){ Value row=args[0].list->items[i]; if(row.type==V_LIST){ for(j=0;j<row.list->count;j++){ char *f=v_to_string(row.list->items[j]); int quote=strchr(f,d)||strchr(f,'\n')||strchr(f,'"'); if(j) str_ch(&out,d); if(quote){ const char *q=f; str_ch(&out,'"'); while(*q){ if(*q=='"') str_add(&out,"\"\""); else str_ch(&out,*q); q++; } str_ch(&out,'"'); } else str_add(&out,f); free(f); } } str_ch(&out,'\n'); } } free(del); return v_str(out.s?out.s:""); } }
 return v_none(); }

/* ---------- execution ---------- */
static void exec_range(Runtime *rt,Program *p,int start,int end);
static int parse_params(char *s,char ***out){ char **arr=NULL; int cnt=0,cap=0; char *tok=strtok(s,","); while(tok){ char *t=trim_inplace(tok); if(*t){ if(cnt>=cap){cap=cap?cap*2:4; arr=(char**)xrealloc(arr,sizeof(char*)*cap);} arr[cnt++]=xstrdup(t);} tok=strtok(NULL,","); } *out=arr; return cnt; }
static void parse_teach_parts(char *t,char **name_out,char ***params_out,int *pcnt_out){ char *name,*takes; char **params=NULL; int pcnt=0; t+=5; while(*t&&isspace((unsigned char)*t)) t++; name=t; while(*t&&!isspace((unsigned char)*t)) t++; if(*t) *t++=0; takes=strstr(t,"TAKES"); if(takes){ takes+=5; pcnt=parse_params(takes,&params); } else { char *simple=trim_inplace(t); if(*simple) pcnt=parse_params(simple,&params); } *name_out=name; *params_out=params; *pcnt_out=pcnt; }
static void scan_functions(Runtime *rt,Program *p,const char *prefix){ int i; for(i=0;i<p->count;i++){ char tmp[1024],up[64],w[128]; char *t; strncpy(tmp,p->lines[i],sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); first_word(t,w,sizeof(w)); upper_copy(up,w,sizeof(up));
 if(strcmp(up,"CLASS")==0){ const char *pcur=t+5; char *cls=unquote_token(&pcur); char *cn=trim_inplace(cls); int end=match_block(p,i,"CLASS","ENDCLASS",NULL,NULL); ClassDef *c=NULL; int j; if(*cn) c=add_class(rt,cn); for(j=i+1;j<(end<0?p->count:end);j++){ char itmp[1024],iup[64],iw[128]; char *it; strncpy(itmp,p->lines[j],sizeof(itmp)-1); itmp[sizeof(itmp)-1]=0; it=trim_inplace(itmp); first_word(it,iw,sizeof(iw)); upper_copy(iup,iw,sizeof(iup)); if(strcmp(iup,"HAS")==0){ const char *fp=it+3; char *fn=unquote_token(&fp); char *ft=unquote_token(&fp); char *ftt=trim_inplace(ft); if(c) class_add_field(c,trim_inplace(fn),*ftt?ftt:"ANY"); free(fn); free(ft); } else if(strcmp(iup,"TEACH")==0){ char *mname; char **params=NULL; int pcnt=0; char fname[256]; int mend=match_block(p,j,"TEACH","LEARNED",NULL,NULL); parse_teach_parts(it,&mname,&params,&pcnt); if(c&&*mname){ snprintf(fname,sizeof(fname),"%s.%s",c->name,mname); if(!find_function(rt,fname)) add_function(rt,fname,params,pcnt,p,j+1,mend<0?(end<0?p->count:end):mend); } if(mend>=0) j=mend; } } free(cls); if(end>=0) i=end; continue; }
 if(strcmp(up,"TEACH")==0){ char *name; char **params=NULL; int pcnt=0; char fname[256]; int end=match_block(p,i,"TEACH","LEARNED",NULL,NULL); parse_teach_parts(t,&name,&params,&pcnt); snprintf(fname,sizeof(fname),"%s%s",prefix?prefix:"",name); if(!find_function(rt,fname)) add_function(rt,fname,params,pcnt,p,i+1,end<0?p->count:end); if(end>=0) i=end; } } }
static int call_object_method(Runtime *rt,const char *name,Value *args,int argc){ const char *dot=strchr(name,'.'); char objname[128],method[128],fname[256],fieldname[256]; Value obj,cv; ClassDef *c; Function *f; Var *old; FieldDef *fd; int i; if(!dot) return 0; snprintf(objname,sizeof(objname),"%.*s",(int)(dot-name),name); snprintf(method,sizeof(method),"%s",dot+1); obj=rt_get(rt,objname); if(obj.type!=V_MAP || !obj.map) return 0; cv=map_get(obj.map,"class"); if(cv.type!=V_STR || !cv.str || !cv.str[0]) return 0; snprintf(fname,sizeof(fname),"%s.%s",cv.str,method); f=find_function(rt,fname); if(!f){ rt_error(rt,"",0,"%s does not know how to do %s yet.",cv.str,method); return 1; } c=find_class(rt,cv.str); old=rt->locals; rt->locals=NULL; rt_set(rt,"self",obj); if(c){ for(fd=c->fields;fd;fd=fd->next){ Value fv=map_get(obj.map,fd->name); rt_set(rt,fd->name,fv); snprintf(fieldname,sizeof(fieldname),"__type_%s",fd->name); rt_set(rt,fieldname,v_str(fd->type)); } }
 for(i=0;i<f->pcnt;i++) rt_set(rt,f->params[i], i<argc?args[i]:v_none()); rt->returning=0; exec_range(rt,f->prog,f->start,f->end); if(c){ for(fd=c->fields;fd;fd=fd->next){ Value fv=rt_get(rt,fd->name); map_put(obj.map,fd->name,fv); } }
 if(rt->returning){ rt_set(rt,"RESULT",rt->ret); rt->returning=0; }
 rt->locals=old; rt_set(rt,objname,obj); if(c){ for(fd=c->fields;fd;fd=fd->next){ Value fv=map_get(obj.map,fd->name); snprintf(fieldname,sizeof(fieldname),"%s.%s",objname,fd->name); rt_set_checked(rt,"",0,fieldname,fd->type,fv); } }
 return 1; }
static void call_function(Runtime *rt,const char *name,Value *args,int argc){ int handled=0,i; Value br=builtin_call(rt,name,args,argc,&handled); if(handled){ rt_set(rt,"RESULT",br); return; } if(call_object_method(rt,name,args,argc)) return; Function *f=find_function(rt,name); if(!f){ rt_error(rt,"",0,"Unknown function: %s",name); return;} Var *old=rt->locals; rt->locals=NULL; for(i=0;i<f->pcnt;i++) rt_set(rt,f->params[i], i<argc?args[i]:v_none()); rt->returning=0; exec_range(rt,f->prog,f->start,f->end); if(rt->returning){ rt_set(rt,"RESULT",rt->ret); rt->returning=0; } rt->locals=old; }
static int stack_has(Runtime *rt,const char *path){ int i; for(i=0;i<rt->import_depth;i++) if(strcmp(rt->import_stack[i],path)==0) return 1; return 0; }
static int export_allows(char **exports,int ec,const char *name){ int i; if(ec==0) return 1; for(i=0;i<ec;i++) if(strcmp(exports[i],name)==0) return 1; return 0; }
static void do_import(Runtime *rt,const char *path,const char *ns,const char *curfile,int line){ Program *p; char *prefix=NULL; char **exports=NULL; int ec=0,i; if(stack_has(rt,path)){ rt_error(rt,curfile,line,"Import cycle detected at: %s",path); return;} if(strstr(path,"lib/text.claro")&&ns){ add_module(rt,ns,"text"); return;} if(strstr(path,"lib/math.claro")&&ns){ add_module(rt,ns,"math"); return;} if(strstr(path,"lib/random.claro")&&ns){ add_module(rt,ns,"random"); return;} if(strstr(path,"lib/csv.claro")&&ns){ add_module(rt,ns,"csv"); return;} if(strstr(path,"lib/path.claro")&&ns){ add_module(rt,ns,"path"); return;} if(strstr(path,"lib/time.claro")&&ns){ add_module(rt,ns,"time"); return;}
 p=load_program(rt,path); if(!p){ rt_error(rt,curfile,line,"Could not import file: %s",path); return;} rt->import_stack=(char**)xrealloc(rt->import_stack,sizeof(char*)*(rt->import_depth+1)); rt->import_stack[rt->import_depth++]=xstrdup(path);
 for(i=0;i<p->count;i++){ char tmp[1024],up[64],w[64]; char *t; strncpy(tmp,p->lines[i],sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); first_word(t,w,sizeof(w)); upper_copy(up,w,sizeof(up)); if(strcmp(up,"EXPORT")==0){ t+=6; t=trim_inplace(t); if(ci_eq(t,"ALL")){ ec=0; break;} ec=parse_params(t,&exports); break; } }
 if(ns){ Str pr; str_init(&pr); str_add(&pr,ns); str_ch(&pr,'.'); prefix=str_take(&pr); scan_functions(rt,p,prefix); exec_range(rt,p,0,p->count); /* copy exported vars */ for(Var *v=rt->globals; v; v=v->next){ if(strncmp(v->name,prefix,strlen(prefix))!=0 && export_allows(exports,ec,v->name)){ char nn[256]; snprintf(nn,sizeof(nn),"%s%s",prefix,v->name); if(!rt_has(rt,nn)) rt_set_global(rt,nn,v->val); } } } else { scan_functions(rt,p,""); exec_range(rt,p,0,p->count); }
 rt->import_depth--; free(prefix); }
static void create_object_value(Runtime *rt,const char *file,int line,const char *cls,const char *var){ Value obj=v_map(); ClassDef *c=find_class(rt,cls); FieldDef *fd; char fullname[256]; if(!cls||!*cls||!var||!*var){ rt_error(rt,file,line,"NEW needs a class and a name. Try: NEW Player player"); return; } map_put(obj.map,"class",v_str(cls)); rt_set_checked(rt,file,line,var,"OBJECT",obj); if(c){ for(fd=c->fields;fd;fd=fd->next){ Value def=claro_default_for_type(fd->type); snprintf(fullname,sizeof(fullname),"%s.%s",var,fd->name); rt_set_checked(rt,file,line,fullname,fd->type,def); } } }
static void exec_line(Runtime *rt,Program *p,int *pcp,const char *raw){ char buf[4096],up[64],w[128]; char *t; int pc=*pcp; strncpy(buf,raw,sizeof(buf)-1); buf[sizeof(buf)-1]=0; t=trim_inplace(buf); if(is_blank_or_comment(t)) return; first_word(t,w,sizeof(w)); upper_copy(up,w,sizeof(up)); if(strcmp(up,"COMMENT")==0){ int end=match_block(p,pc,"COMMENT","ENDCOMMENT",NULL,NULL); *pcp=end<0?pc:end; return; }
 if(strcmp(up,"SAY")==0){ char *e=expr_after_word(t,"SAY"); Value v=eval_expr(rt,e); if(!rt->error) out_line(rt,v); free(e); return; }
 if(strcmp(up,"CLASS")==0){ int end=match_block(p,pc,"CLASS","ENDCLASS",NULL,NULL); *pcp=end<0?pc:end; return; }
 if(strcmp(up,"NEW")==0){ const char *as=find_word_ci(t,"AS"); if(as){ char *cls=substr(t+3,as); char *var=xstrdup(trim_inplace((char*)as+2)); create_object_value(rt,p->path,pc+1,trim_inplace(cls),trim_inplace(var)); free(cls); free(var); } else { const char *pcur=t+3; char *cls=unquote_token(&pcur); char *var=xstrdup(trim_inplace((char*)pcur)); create_object_value(rt,p->path,pc+1,trim_inplace(cls),trim_inplace(var)); free(cls); free(var); } return; }
 if(strcmp(up,"START")==0){ if(starts_ci(t+5," TASK")){ const char *pcur=t+10; char *name=unquote_token(&pcur); int end=match_block(p,pc,"START","ENDTASK",NULL,NULL); exec_range(rt,p,pc+1,end); if(name&&*name){ char done[256]; snprintf(done,sizeof(done),"TASK_%s_DONE",trim_inplace(name)); rt_set(rt,done,v_bool(1)); } *pcp=end<0?pc:end; free(name); return; } }
 if(strcmp(up,"YIELD")==0){ return; }
 if(strcmp(up,"WAIT")==0){ return; }
 if(strcmp(up,"TASK")==0){ if(starts_ci(t+4," STATUS")){ const char *as=find_word_ci(t,"AS"); if(as){ char *name=substr(t+11,as); char *var=xstrdup(trim_inplace((char*)as+2)); char key[256]; Value done; snprintf(key,sizeof(key),"TASK_%s_DONE",trim_inplace(name)); done=rt_get(rt,key); rt_set(rt,var,v_str(v_truth(done)?"DONE":"PENDING")); free(name); free(var); } else rt_error(rt,p->path,pc+1,"TASK STATUS needs AS. Try: TASK STATUS helloTask AS status"); return; } }
 if(strcmp(up,"OPEN")==0||strcmp(up,"CLEAR")==0||strcmp(up,"DRAW")==0||strcmp(up,"UPDATE")==0||strcmp(up,"CLOSE")==0){ graphics_note(rt,up); return; }
 if(strcmp(up,"HTTP")==0){
  const char *as=find_word_ci(t,"AS");
  if(as&&starts_ci(t+4," GET")){
   char *ue=substr(t+8,as); char *after=xstrdup(trim_inplace((char*)as+2)); const char *status_word=find_word_ci(after,"STATUS"); char *var=status_word?substr(after,status_word):xstrdup(after); char *status_var=status_word?xstrdup(trim_inplace((char*)status_word+6)):NULL; Value uv=eval_expr(rt,ue); char *url=v_to_string(uv); int code=0,http=0; char *out;
   if(!claro_url_is_safe(url)){ rt_error(rt,p->path,pc+1,"HTTP GET needs a safe http://, https://, or claro:// URL."); free(ue); free(after); free(var); free(status_var); free(url); return; }
   out=claro_http_get_text(url,&http,&code); rt_set(rt,trim_inplace(var),v_str(out)); rt_set(rt,"LASTEXIT",v_num(code)); rt_set(rt,"LASTHTTP",v_num(http)); if(status_var&&*status_var) rt_set(rt,status_var,v_num(http)); free(out); free(url); free(ue); free(after); free(var); free(status_var); return;
  }
  if(as&&starts_ci(t+4," STATUS")){
   char *ue=substr(t+11,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value uv=eval_expr(rt,ue); char *url=v_to_string(uv); int code=0,http=0; char *out;
   if(!claro_url_is_safe(url)){ rt_error(rt,p->path,pc+1,"HTTP STATUS needs a safe http://, https://, or claro:// URL."); free(ue); free(var); free(url); return; }
   out=claro_http_get_text(url,&http,&code); rt_set(rt,trim_inplace(var),v_num(http)); rt_set(rt,"LASTEXIT",v_num(code)); rt_set(rt,"LASTHTTP",v_num(http)); free(out); free(url); free(ue); free(var); return;
  }
  if(starts_ci(t+4," SAVE")){
   const char *to=find_word_ci(t,"TO"); const char *as2=find_word_ci(t,"AS"); if(to){ char *ue=substr(t+9,to); char *pe=as2?substr(to+2,as2):xstrdup(to+2); char *status_var=as2?xstrdup(trim_inplace((char*)as2+2)):NULL; Value uv=eval_expr(rt,ue), pv=eval_expr(rt,pe); char *url=v_to_string(uv), *path=v_to_string(pv); int code=0,http=0; char *out;
    if(!claro_url_is_safe(url)){ rt_error(rt,p->path,pc+1,"HTTP SAVE needs a safe http://, https://, or claro:// URL."); free(ue); free(pe); free(status_var); free(url); free(path); return; }
    out=claro_http_get_text(url,&http,&code); if(!write_text_bytes(path,out)) rt_error(rt,p->path,pc+1,"Could not save HTTP response to file."); if(status_var&&*status_var) rt_set(rt,status_var,v_num(http)); rt_set(rt,"LASTEXIT",v_num(code)); rt_set(rt,"LASTHTTP",v_num(http)); free(out); free(url); free(path); free(ue); free(pe); free(status_var); return; }
  }
  if(as&&starts_ci(t+4," CHECK")){
   char *ue=substr(t+10,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value uv=eval_expr(rt,ue); char *url=v_to_string(uv); rt_set(rt,var,v_bool(claro_url_is_safe(url))); free(url); free(ue); free(var); return;
  }
  rt_error(rt,p->path,pc+1,"HTTP needs GET, STATUS, SAVE, or CHECK. Try: HTTP GET \"claro://hello\" AS page"); return; }
 if(strcmp(up,"OBJECT")==0){ const char *as=find_word_ci(t,"AS"); if(as && starts_ci(t+6," CLASS")){ char *oe=substr(t+12,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value ov=eval_expr(rt,oe); const char *cn=object_class_name(ov); rt_set_checked(rt,p->path,pc+1,var,"TEXT",v_str(cn?cn:"")); free(oe); free(var); } else if(as && starts_ci(t+6," FIELDS")){ char *oe=substr(t+13,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value ov=eval_expr(rt,oe); Value arr=v_list(); int i; if(ov.type==V_MAP&&ov.map){ for(i=0;i<ov.map->count;i++){ if(strcmp(ov.map->keys[i],"class")!=0 && !starts_ci(ov.map->keys[i],"__type_")) list_add(arr.list,v_str(ov.map->keys[i])); } } rt_set_checked(rt,p->path,pc+1,var,"LIST",arr); free(oe); free(var); } else rt_error(rt,p->path,pc+1,"OBJECT needs CLASS or FIELDS. Try: OBJECT CLASS player AS kind"); return; }
 if(strcmp(up,"TYPE")==0 && starts_ci(t,"TYPE OF")){ const char *as=find_word_ci(t,"AS"); if(as){ char *expr=substr(t+7,as); char *var=xstrdup(trim_inplace((char*)as+2)); char dbuf[320]; const char *decl=declared_type_for_expr(rt,expr,dbuf,sizeof(dbuf)); Value v=eval_expr(rt,expr); rt_set_checked(rt,p->path,pc+1,var,"TEXT",v_str(decl?decl:claro_value_type(v))); free(expr); free(var); } else rt_error(rt,p->path,pc+1,"TYPE OF needs AS. Try: TYPE OF score AS kind"); return; }
 if(strcmp(up,"CHECK")==0 && starts_ci(t,"CHECK TYPE")){ const char *is=find_word_ci(t,"IS"); if(is){ char *expr=substr(t+10,is); char *ty=xstrdup(trim_inplace((char*)is+2)); char dbuf[320]; const char *decl=declared_type_for_expr(rt,expr,dbuf,sizeof(dbuf)); Value v=eval_expr(rt,expr); if(decl && !ci_eq(decl,ty) && !ci_eq(ty,"ANY")){ rt_error(rt,p->path,pc+1,"Type check failed: expected %s, but %s is %s.",ty,trim_inplace(expr),decl); } else if(!decl && !claro_type_matches(ty,v)){ rt_error(rt,p->path,pc+1,"Type check failed: expected %s, but got %s.",ty,claro_value_type(v)); } free(expr); free(ty); } else rt_error(rt,p->path,pc+1,"CHECK TYPE needs IS. Try: CHECK TYPE score IS NUMBER"); return; }
 if(strcmp(up,"SET")==0){ char *rest=t+3; const char *to=find_word_ci(rest,"TO"); const char *as=find_word_ci(rest,"AS"); if(as&&to&&as<to){ char *name=substr(rest,as); char *type=substr(as+2,to); char *n=trim_inplace(name); char *ty=trim_inplace(type); Value v=eval_expr(rt,to+2); rt_set_checked(rt,p->path,pc+1,n,ty,v); free(name); free(type); }
  else if(to){ char *name=substr(rest,to); char *n=trim_inplace(name); char *space=strchr(n,' '); const char *type=NULL; if(space){ *space=0; if(claro_is_type_word(trim_inplace(space+1))) type=trim_inplace(space+1); else { *space=' '; } } { Value v=eval_expr(rt,to+2); rt_set_checked(rt,p->path,pc+1,n,type,v); } free(name); }
  else { const char *pcur=rest; char *name=unquote_token(&pcur); char *n=trim_inplace(name); const char *save=pcur; char *maybe=unquote_token(&pcur); char *ty=trim_inplace(maybe); if(claro_is_type_word(ty)){ char *after=trim_inplace((char*)pcur); Value v=*after?eval_expr(rt,after):claro_default_for_type(ty); if(*n) rt_set_checked(rt,p->path,pc+1,n,ty,v); } else { Value v=eval_expr(rt,save); if(*n) rt_set_checked(rt,p->path,pc+1,n,NULL,v); } free(maybe); free(name); } return; }
 if(strcmp(up,"ASK")==0){ const char *as=find_word_ci(t,"AS"); char input[1024]; char *prompt_text=NULL; char *var=NULL; char *type=NULL; if(as){ char *prompt_expr=substr(t+3,as); const char *pcur=as+2; var=unquote_token(&pcur); { char *rest=xstrdup(trim_inplace((char*)pcur)); if(claro_is_type_word(rest)) type=rest; else free(rest); } { Value prompt=eval_expr(rt,prompt_expr); prompt_text=v_to_string(prompt); } free(prompt_expr); } else { const char *pcur=t+3; prompt_text=unquote_token(&pcur); var=unquote_token(&pcur); { char *rest=xstrdup(trim_inplace((char*)pcur)); if(claro_is_type_word(rest)) type=rest; else free(rest); } } if(prompt_text&&prompt_text[0]){ if(rt->capture){ str_add(&rt->captured,prompt_text); str_ch(&rt->captured,'\n'); } else { printf("%s\n",prompt_text); fflush(stdout); } } if(var&&*trim_inplace(var)){ Value val=v_str(""); if(fgets(input,sizeof(input),stdin)){ size_t n=strlen(input); while(n&&(input[n-1]=='\n'||input[n-1]=='\r')) input[--n]=0; } else input[0]=0; if(type&&*type){ if(!claro_value_from_text(type,input,&val)){ rt_error(rt,p->path,pc+1,"%s needs %s input. Try a value like %s.",trim_inplace(var),type,ci_eq(type,"NUMBER")?"5":(ci_eq(type,"YESNO")?"YES":"text")); } else rt_set_checked(rt,p->path,pc+1,trim_inplace(var),type,val); } else rt_set_checked(rt,p->path,pc+1,trim_inplace(var),NULL,v_str(input)); } else rt_error(rt,p->path,pc+1,"ASK needs a variable name. Try: ASK \"What is your name?\" name"); free(prompt_text); free(var); free(type); return; }
 if(strcmp(up,"IF")==0){ int elsepos=-1; int end=match_block(p,pc,"IF","ENDIF","ELSE",&elsepos); char *e=expr_after_word(t,"IF"); Value cond=eval_expr(rt,e); free(e); if(v_truth(cond)) exec_range(rt,p,pc+1,elsepos>=0?elsepos:end); else if(elsepos>=0) exec_range(rt,p,elsepos+1,end); *pcp=end<0?pc:end; return; }
 if(strcmp(up,"DO")==0){ int end=find_done(p,pc); const char *times=find_word_ci(t,"TIMES"); if(!times){ const char *pcur=t+2; char *name=unquote_token(&pcur); char **parts=NULL; int ac=0,i; Value *args=NULL; char *n=trim_inplace(name); if(*trim_inplace((char*)pcur)) ac=split_args(pcur,&parts); args=(Value*)xmalloc(sizeof(Value)*(ac?ac:1)); for(i=0;i<ac;i++) args[i]=eval_expr(rt,parts[i]); call_function(rt,n,args,ac); free(name); return; } else { char *e=substr(t+2,times); int n=(int)v_number(eval_expr(rt,e)); int i; free(e); for(i=0;i<n && !rt->error && !rt->returning;i++) exec_range(rt,p,pc+1,end); *pcp=end<0?pc:end; return; } }
 if(strcmp(up,"FOR")==0){ int end=find_done(p,pc); if(starts_ci(t,"FOR EACH")){ char *r=t+8; const char *in=find_word_ci(r,"IN"); char *vars=substr(r,in?in:r); char *expr=xstrdup(in?in+2:""); Value col=eval_expr(rt,expr); char *comma=strchr(vars,','); if(comma&&col.type==V_MAP){ *comma=0; char *k=trim_inplace(vars), *v=trim_inplace(comma+1); int i; for(i=0;i<col.map->count&&!rt->error&&!rt->returning;i++){ rt_set(rt,k,v_str(col.map->keys[i])); rt_set(rt,v,col.map->vals[i]); exec_range(rt,p,pc+1,end); } } else if(col.type==V_LIST){ char *v=trim_inplace(vars); int i; for(i=0;i<col.list->count&&!rt->error&&!rt->returning;i++){ rt_set(rt,v,col.list->items[i]); exec_range(rt,p,pc+1,end); } } free(vars); free(expr); } else { char var[128]; const char *from=find_word_ci(t,"FROM"), *to=find_word_ci(t,"TO"), *step=find_word_ci(t,"STEP"); double a,b,s=1; if(from&&to){ snprintf(var,sizeof(var),"%.*s",(int)(from-(t+3)),t+3); { char *vt=trim_inplace(var); memmove(var,vt,strlen(vt)+1); } { char *ea=substr(from+4,to); char *eb=step?substr(to+2,step):xstrdup(to+2); a=v_number(eval_expr(rt,ea)); b=v_number(eval_expr(rt,eb)); if(step) s=v_number(eval_expr(rt,step+4)); free(ea); free(eb); } if(s==0) s=1; if(s>0){ for(;a<=b&&!rt->error&&!rt->returning;a+=s){ rt_set(rt,var,v_num(a)); exec_range(rt,p,pc+1,end);} } else { for(;a>=b&&!rt->error&&!rt->returning;a+=s){ rt_set(rt,var,v_num(a)); exec_range(rt,p,pc+1,end);} } } } *pcp=end<0?pc:end; return; }
 if(strcmp(up,"REPEAT")==0){ int end=match_block(p,pc,"REPEAT","UNTIL",NULL,NULL); char *cond=p->lines[end]+5; do{ exec_range(rt,p,pc+1,end); if(rt->error||rt->returning) break; }while(!v_truth(eval_expr(rt,cond))); *pcp=end<0?pc:end; return; }
 if(strcmp(up,"TEACH")==0){ int end=match_block(p,pc,"TEACH","LEARNED",NULL,NULL); *pcp=end<0?pc:end; return; }
 if(strcmp(up,"RETURN")==0){ char *e=expr_after_word(t,"RETURN"); rt->ret=eval_expr(rt,e); rt->returning=1; free(e); return; }
 if(strcmp(up,"CALL")==0){ char *rest=t+4; const char *with=find_word_ci(rest,"WITH"); char *name=with?substr(rest,with):xstrdup(rest); char **parts=NULL; int ac=0,i; Value *args=NULL; char *n=trim_inplace(name); if(with) ac=split_args(with+4,&parts); args=(Value*)xmalloc(sizeof(Value)*(ac?ac:1)); for(i=0;i<ac;i++) args[i]=eval_expr(rt,parts[i]); call_function(rt,n,args,ac); free(name); return; }
 if(strcmp(up,"IMPORT")==0){ const char *pcur=t+6; char *path=unquote_token(&pcur); char *ns=NULL; while(*pcur&&isspace((unsigned char)*pcur)) pcur++; if(starts_ci(pcur,"AS")){ pcur+=2; ns=xstrdup(trim_inplace((char*)pcur)); } do_import(rt,path,ns,p->path,pc+1); free(path); free(ns); return; }
 if(strcmp(up,"ADD")==0){ const char *to=find_word_ci(t,"TO"); if(to){ char *ex=substr(t+3,to); char *var=xstrdup(trim_inplace((char*)to+2)); Value v=eval_expr(rt,ex); Value l=rt_get(rt,var); if(l.type==V_LIST){ list_add(l.list,v); rt_set(rt,var,l); } free(ex); free(var);} return; }
 if(strcmp(up,"COUNT")==0){ const char *as=find_word_ci(t,"AS"); if(as){ if(starts_ci(t+5," ARGUMENTS")){ char *var=xstrdup(trim_inplace((char*)as+2)); rt_set(rt,var,v_num(rt->script_argc)); free(var); } else { char *ex=substr(t+5,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value v=eval_expr(rt,ex); rt_set(rt,var,v_num(v.type==V_LIST?v.list->count:(v.type==V_MAP?v.map->count:0))); free(ex); free(var); } } return; }
 if(strcmp(up,"GET")==0){ const char *at=find_word_ci(t,"AT"), *key=find_word_ci(t,"KEY"), *as=find_word_ci(t,"AS"); if(as&&starts_ci(t+3," ALL ARGUMENTS")){ char *var=xstrdup(trim_inplace((char*)as+2)); Value arr=v_list(); int i; for(i=0;i<rt->script_argc;i++) list_add(arr.list,v_str(rt->script_argv[i])); rt_set(rt,var,arr); free(var); } else if(as&&starts_ci(t+3," ARGUMENT")){ char *ie=substr(t+12,as); char *var=xstrdup(trim_inplace((char*)as+2)); int idx=(int)v_number(eval_expr(rt,ie)); if(idx>=1&&idx<=rt->script_argc) rt_set(rt,var,v_str(rt->script_argv[idx-1])); else rt_set(rt,var,v_str("")); free(ie); free(var); } else if(as&&starts_ci(t+3," ENV")){ const char *pcur=t+7; char *name=substr(pcur,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value nv=eval_expr(rt,name); char *ns=v_to_string(nv); const char *ev=getenv(ns); rt_set(rt,var,v_str(ev?ev:"")); free(ns); free(name); free(var); } else if(as&&at){ char *ce=substr(t+3,at); char *ie=substr(at+2,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value c=eval_expr(rt,ce); int idx=(int)v_number(eval_expr(rt,ie)); if(c.type==V_LIST && idx>=1 && idx<=c.list->count) rt_set(rt,var,c.list->items[idx-1]); else rt_set(rt,var,v_str("")); free(ce); free(ie); free(var); } else if(as&&key){ char *ce=substr(t+3,key); char *ke=substr(key+3,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value c=eval_expr(rt,ce); Value kv=eval_expr(rt,ke); char *ks=v_to_string(kv); if(c.type==V_MAP) rt_set(rt,var,map_get(c.map,ks)); else rt_set(rt,var,v_str("")); free(ks); free(ce); free(ke); free(var); } return; }
 if(strcmp(up,"PUT")==0){ const char *key=find_word_ci(t,"KEY"), *val=find_word_ci(t,"VALUE"), *as=find_word_ci(t,"AS"), *into=find_word_ci(t,"INTO"); if(key&&val){ char *me=substr(t+3,key); char *ke=substr(key+3,val); char *ve=xstrdup(val+5); Value m=eval_expr(rt,me); Value k=eval_expr(rt,ke); Value v=eval_expr(rt,ve); char *ks=v_to_string(k); if(m.type==V_MAP){ char *mn=trim_inplace(me); map_put(m.map,ks,v); rt_set(rt,mn,m); } free(ks); free(me); free(ke); free(ve); } else if(as&&into){ char *ke=substr(t+3,as); char *ve=substr(as+2,into); char *mn=xstrdup(trim_inplace((char*)into+4)); Value m=rt_get(rt,mn); Value k=eval_expr(rt,ke); Value v=eval_expr(rt,ve); char *ks=v_to_string(k); if(m.type==V_MAP){ map_put(m.map,ks,v); rt_set(rt,mn,m); } free(ks); free(ke); free(ve); free(mn); } return; }
 if(strcmp(up,"WRITE")==0||strcmp(up,"APPEND")==0){ if(starts_ci(t+strlen(w)," FILE")){ const char *pcur=t+strlen(w)+5; const char *with=find_word_ci(pcur,"WITH"); if(with){ char *pe=substr(pcur,with); char *ve=xstrdup(with+4); Value pv=eval_expr(rt,pe); Value vv=eval_expr(rt,ve); char *path=v_to_string(pv), *text=v_to_string(vv); FILE *f=fopen(path,strcmp(up,"APPEND")==0?"ab":"wb"); if(!f) rt_error(rt,p->path,pc+1,"Could not write file: %s",strerror(errno)); else { fwrite(text,1,strlen(text),f); fclose(f);} free(path); free(text); free(pe); free(ve); } } return; }
 if(strcmp(up,"READ")==0){ const char *pcur=t+4; const char *as=find_word_ci(pcur,"AS"); if(as&&starts_ci(pcur," FILE")){ char *pe=substr(pcur+5,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value pv=eval_expr(rt,pe); char *path=v_to_string(pv); FILE *f=fopen(path,"rb"); if(!f) rt_error(rt,p->path,pc+1,"Could not read file: %s",strerror(errno)); else { Str b; int c; str_init(&b); while((c=fgetc(f))!=EOF) str_ch(&b,(char)c); fclose(f); rt_set(rt,var,v_str(b.s?b.s:"")); free(b.s);} free(path); free(pe); free(var); } return; }
 if(strcmp(up,"EXISTS")==0){ const char *pcur=t+6; const char *as=find_word_ci(pcur,"AS"); if(as&&starts_ci(pcur," FILE")){ char *pe=substr(pcur+5,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value pv=eval_expr(rt,pe); char *path=v_to_string(pv); rt_set(rt,var,v_bool(access(path,F_OK)==0)); free(path); free(pe); free(var);} return; }
 if(strcmp(up,"CREATE")==0){ const char *pcur=t+6; if(starts_ci(pcur," FOLDER")){ char *pe=xstrdup(pcur+7); Value pv=eval_expr(rt,pe); char *path=v_to_string(pv); if(!make_folder(path)) rt_error(rt,p->path,pc+1,"Could not create folder: %s",strerror(errno)); free(path); free(pe); } return; }
 if(strcmp(up,"COPY")==0){ const char *to=find_word_ci(t,"TO"); if(starts_ci(t+4," FILE")&&to){ char *se=substr(t+9,to); char *de=xstrdup(to+2); Value sv=eval_expr(rt,se), dv=eval_expr(rt,de); char *src=v_to_string(sv), *dst=v_to_string(dv); if(!copy_file_bytes(src,dst)) rt_error(rt,p->path,pc+1,"Could not copy file"); free(src); free(dst); free(se); free(de); } return; }
 if(strcmp(up,"MOVE")==0){ const char *to=find_word_ci(t,"TO"); if(starts_ci(t+4," FILE")&&to){ char *se=substr(t+9,to); char *de=xstrdup(to+2); Value sv=eval_expr(rt,se), dv=eval_expr(rt,de); char *src=v_to_string(sv), *dst=v_to_string(dv); if(rename(src,dst)!=0) rt_error(rt,p->path,pc+1,"Could not move file: %s",strerror(errno)); free(src); free(dst); free(se); free(de); } return; }
 if(strcmp(up,"LIST")==0){ const char *as=find_word_ci(t,"AS"); if(starts_ci(t+4," FOLDER")&&as){ char *pe=substr(t+11,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value pv=eval_expr(rt,pe); char *path=v_to_string(pv); rt_set(rt,var,list_folder_value(path)); free(path); free(pe); free(var); } return; }
 if(strcmp(up,"DELETE")==0){ const char *pcur=t+6; if(starts_ci(pcur," FILE")){ char *pe=xstrdup(pcur+5); Value pv=eval_expr(rt,pe); char *path=v_to_string(pv); remove(path); free(path); free(pe);} else if(starts_ci(pcur," FOLDER")){ char *pe=xstrdup(pcur+7); Value pv=eval_expr(rt,pe); char *path=v_to_string(pv); remove_folder(path); free(path); free(pe);} return; }
 if(strcmp(up,"PARSE")==0){ const char *as=find_word_ci(t,"AS"); if(as){ char *ex=substr(t+10,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value s=eval_expr(rt,ex); char *txt=v_to_string(s); rt_set(rt,var,parse_json_text(txt)); free(txt); free(ex); free(var);} return; }
 if(strcmp(up,"MAKE")==0){ int pretty=strstr(t,"JSON PRETTY")!=NULL; const char *as=find_word_ci(t,"AS"); if(as){ const char *st=strstr(t,pretty?"JSON PRETTY":"JSON"); char *ex=substr(st+(pretty?11:4),as); char *var=xstrdup(trim_inplace((char*)as+2)); Value v=eval_expr(rt,ex); char *js=make_json(v,pretty); rt_set(rt,var,v_str(js)); free(js); free(ex); free(var);} return; }
 if(strcmp(up,"TEXT")==0){ char restup[64],op[64]; const char *as=find_word_ci(t,"AS"); const char *pcur=t+4; first_word(pcur,op,sizeof(op)); upper_copy(restup,op,sizeof(restup)); while(*pcur&&isspace((unsigned char)*pcur)) pcur++; while(*pcur&&!isspace((unsigned char)*pcur)) pcur++; if(as){ char *var=xstrdup(trim_inplace((char*)as+2));
  if(!strcmp(restup,"STARTS")||!strcmp(restup,"ENDS")){ const char *with=find_word_ci(pcur,"WITH"); if(with){ char *left=substr(pcur,with); char *right=substr(with+4,as); Value lv=eval_expr(rt,left), rv=eval_expr(rt,right); char *ls=v_to_string(lv), *rs=v_to_string(rv); size_t ll=strlen(ls), rl=strlen(rs); int ok=!strcmp(restup,"STARTS")?(rl<=ll&&strncmp(ls,rs,rl)==0):(rl<=ll&&strcmp(ls+ll-rl,rs)==0); rt_set(rt,var,v_bool(ok)); free(left); free(right); free(ls); free(rs); } }
  else if(!strcmp(restup,"REPLACE")){ const char *from=find_word_ci(pcur,"FROM"); const char *to=from?find_word_ci(from+4,"TO"):NULL; if(from&&to){ char *src=substr(pcur,from); char *old=substr(from+4,to); char *neu=substr(to+2,as); Value sv=eval_expr(rt,src), ov=eval_expr(rt,old), nv=eval_expr(rt,neu); char *ss=v_to_string(sv), *os=v_to_string(ov), *ns=v_to_string(nv); Str b; char *pos; str_init(&b); if(os[0]){ char *cur=ss; while((pos=strstr(cur,os))){ str_addn(&b,cur,(size_t)(pos-cur)); str_add(&b,ns); cur=pos+strlen(os); } str_add(&b,cur); rt_set(rt,var,v_str(b.s?b.s:"")); } else rt_set(rt,var,v_str(ss)); free(b.s); free(src); free(old); free(neu); free(ss); free(os); free(ns); } }
  else { char *ex=substr(pcur,as); Value v=eval_expr(rt,ex); char *txt=v_to_string(v); if(!strcmp(restup,"UPPER")){ char *r=text_upper_copy(txt); rt_set(rt,var,v_str(r)); free(r); } else if(!strcmp(restup,"LOWER")){ char *r=text_lower_copy(txt); rt_set(rt,var,v_str(r)); free(r); } else if(!strcmp(restup,"TRIM")){ char *r=text_trim_copy(txt); rt_set(rt,var,v_str(r)); free(r); } else if(!strcmp(restup,"LENGTH")){ rt_set(rt,var,v_num((double)strlen(txt))); } else if(!strcmp(restup,"CONTAINS")){ char *left=NULL,*right=NULL; const char *needle=find_word_ci(pcur,"NEEDLE"); if(!needle) needle=find_word_ci(pcur,"TEXT"); if(needle){ left=substr(pcur,needle); right=substr(needle+6,as); } else { char **args=NULL; int n=split_args(pcur,&args); if(n>=2){ left=xstrdup(args[0]); right=substr(args[1],as); } } if(left&&right){ Value lv=eval_expr(rt,left), rv=eval_expr(rt,right); char *ls=v_to_string(lv), *rs=v_to_string(rv); rt_set(rt,var,v_bool(strstr(ls,rs)!=NULL)); free(ls); free(rs); } free(left); free(right); } free(txt); free(ex); }
  free(var); } return; }
 if(strcmp(up,"RANDOM")==0){ const char *as=find_word_ci(t,"AS"); if(as&&starts_ci(t+6," NUMBER")){ char *range=substr(t+13,as); char *var=xstrdup(trim_inplace((char*)as+2)); char **args=NULL; int n=split_args(range,&args); double a=1,b=100; if(n>=2){ a=v_number(eval_expr(rt,args[0])); b=v_number(eval_expr(rt,args[1])); } else { char *tmp=range; char *one=unquote_token((const char**)&tmp); char *two=unquote_token((const char**)&tmp); if(*one) a=v_number(eval_expr(rt,one)); if(*two) b=v_number(eval_expr(rt,two)); free(one); free(two); } if(b<a){ double c=a; a=b; b=c; } rt_set(rt,var,v_num((int)a + (rand()%((int)(b-a+1))))); free(range); free(var); } return; }
 if(strcmp(up,"RUN")==0){ const char *as=find_word_ci(t,"AS"); if(as&&starts_ci(t+3," COMMAND")){ char *ex=substr(t+11,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value cv=eval_expr(rt,ex); char *cmd=v_to_string(cv); int code=0; char *out=capture_command_output(cmd,&code); rt_set(rt,var,v_str(out)); rt_set(rt,"LASTEXIT",v_num(code)); free(out); free(cmd); free(ex); free(var); } return; }
 if(strcmp(up,"SORT")==0){ char *name=xstrdup(trim_inplace(t+4)); Value v=rt_get(rt,name); value_list_sort(v); rt_set(rt,name,v); free(name); return; }
 if(strcmp(up,"REVERSE")==0){ char *name=xstrdup(trim_inplace(t+7)); Value v=rt_get(rt,name); value_list_reverse(v); rt_set(rt,name,v); free(name); return; }
 if(strcmp(up,"FIND")==0){ const char *in=find_word_ci(t,"IN"), *as=find_word_ci(t,"AS"); if(in&&as){ char *needle=substr(t+4,in); char *listname=substr(in+2,as); char *var=xstrdup(trim_inplace((char*)as+2)); Value nv=eval_expr(rt,needle), lv=eval_expr(rt,listname); int found=0,i; if(lv.type==V_LIST){ for(i=0;i<lv.list->count;i++) if(value_compare(nv,lv.list->items[i])==0){ found=i+1; break; } } rt_set(rt,var,v_num(found)); free(needle); free(listname); free(var); } return; }
 if(strcmp(up,"REMOVE")==0){ const char *from=find_word_ci(t,"FROM"); if(from){ char *needle=substr(t+6,from); char *listname=xstrdup(trim_inplace((char*)from+4)); Value nv=eval_expr(rt,needle), lv=rt_get(rt,listname); int i,j; if(lv.type==V_LIST){ for(i=0;i<lv.list->count;i++) if(value_compare(nv,lv.list->items[i])==0){ for(j=i;j<lv.list->count-1;j++) lv.list->items[j]=lv.list->items[j+1]; lv.list->count--; break; } rt_set(rt,listname,lv); } free(needle); free(listname); } return; }
 if(strcmp(up,"TRY")==0){ int catchpos=-1,end=match_block(p,pc,"TRY","ENDTRY","CATCH",&catchpos); exec_range(rt,p,pc+1,catchpos>=0?catchpos:end); if(rt->error){ rt_clear_error(rt); if(catchpos>=0) exec_range(rt,p,catchpos+1,end); } *pcp=end<0?pc:end; return; }
 if(strcmp(up,"RAISE")==0){ char *e=expr_after_word(t,"RAISE"); Value v=eval_expr(rt,e); char *s=v_to_string(v); rt_error(rt,p->path,pc+1,"%s",s); free(s); free(e); return; }
 if(strcmp(up,"CREATE")==0||strcmp(up,"MOVE")==0||strcmp(up,"SHOW")==0||strcmp(up,"HIDE")==0||strcmp(up,"EXPORT")==0||strcmp(up,"LEARNED")==0||strcmp(up,"ENDIF")==0||strcmp(up,"ELSE")==0||strcmp(up,"DONE")==0||strcmp(up,"ENDTRY")==0||strcmp(up,"CATCH")==0||strcmp(up,"ENDCOMMENT")==0||strcmp(up,"END")==0||strcmp(up,"WAIT")==0){ return; }
 rt_error(rt,p->path,pc+1,"Unknown command: %s",w); }
static void exec_range(Runtime *rt,Program *p,int start,int end){ int pc; if(end<0||end>p->count) end=p->count; for(pc=start; pc<end && !rt->error && !rt->returning; pc++) exec_line(rt,p,&pc,p->lines[pc]); }
static int run_file(Runtime *rt,const char *path){ Program *p=load_program(rt,path); if(!p){ fprintf(stderr,"Could not open %s: %s\n",path,strerror(errno)); return 1;} scan_functions(rt,p,""); exec_range(rt,p,0,p->count); if(rt->error){ if(!rt->capture) fprintf(stderr,"%s:%d: %s\n",rt->err_file?rt->err_file:path,rt->err_line,rt->err_msg?rt->err_msg:"error"); return 1;} return 0; }

/* ---------- formatter/check/test runner ---------- */
static int fmt_file(const char *path){ FILE *f=fopen(path,"rb"); char line[4096]; int indent=0; if(!f){ fprintf(stderr,"Could not open %s\n",path); return 1;} while(fgets(line,sizeof(line),f)){ char *t=trim_inplace(line),w[64],up[64]; int opens=0; first_word(t,w,sizeof(w)); upper_copy(up,w,sizeof(up)); if(!strcmp(up,"ENDIF")||!strcmp(up,"LEARNED")||!strcmp(up,"DONE")||!strcmp(up,"ENDTRY")||!strcmp(up,"ELSE")||!strcmp(up,"CATCH")||!strcmp(up,"ENDCOMMENT")||!strcmp(up,"ENDCLASS")||!strcmp(up,"ENDTASK")||!strcmp(up,"END")) indent-=4; if(indent<0) indent=0; for(int i=0;i<indent;i++) putchar(' '); puts(t); opens=!strcmp(up,"TEACH")||!strcmp(up,"IF")||!strcmp(up,"FOR")||!strcmp(up,"TRY")||!strcmp(up,"CLASS")||!strcmp(up,"START")||!strcmp(up,"COMMENT")||!strcmp(up,"REPEAT")||!strcmp(up,"ELSE")||!strcmp(up,"CATCH")||(!strcmp(up,"DO")&&find_word_ci(t,"TIMES")); if(opens) indent+=4; } fclose(f); return 0; }
static const char *check_commands[]={"SAY","SET","ASK","IF","ELSE","ENDIF","DO","DONE","FOR","REPEAT","UNTIL","TEACH","LEARNED","RETURN","CALL","IMPORT","ADD","COUNT","GET","PUT","WRITE","APPEND","READ","EXISTS","DELETE","PARSE","MAKE","TRY","CATCH","ENDTRY","RAISE","CREATE","COPY","MOVE","LIST","TEXT","RANDOM","RUN","SORT","REVERSE","FIND","REMOVE","SHOW","HIDE","EXPORT","COMMENT","ENDCOMMENT","END","WAIT","YIELD","TASK","CLASS","HAS","ENDCLASS","NEW","START","ENDTASK","OPEN","CLEAR","DRAW","UPDATE","CLOSE","HTTP","OBJECT","TYPE","CHECK",NULL};
static int known_command(const char *up){ int i; for(i=0;check_commands[i];i++) if(strcmp(up,check_commands[i])==0) return 1; return 0; }
static int levenshtein(const char *a,const char *b){ int la=(int)strlen(a), lb=(int)strlen(b), i,j; int *dp=(int*)xmalloc(sizeof(int)*(la+1)*(lb+1)); for(i=0;i<=la;i++) dp[i*(lb+1)]=i; for(j=0;j<=lb;j++) dp[j]=j; for(i=1;i<=la;i++) for(j=1;j<=lb;j++){ int c=tolower((unsigned char)a[i-1])==tolower((unsigned char)b[j-1])?0:1; int x=dp[(i-1)*(lb+1)+j]+1, y=dp[i*(lb+1)+j-1]+1, z=dp[(i-1)*(lb+1)+j-1]+c; int m=x<y?x:y; if(z<m)m=z; dp[i*(lb+1)+j]=m; } i=dp[la*(lb+1)+lb]; free(dp); return i; }

static const char *suggest_command_name(const char *up){ const char *best=NULL; int bd=999,i; if(strcmp(up,"PRINT")==0||strcmp(up,"PRNT")==0||strcmp(up,"ECHO")==0||strcmp(up,"SAI")==0) return "SAY"; for(i=0;check_commands[i];i++){ int d=levenshtein(up,check_commands[i]); if(d<bd){ bd=d; best=check_commands[i]; } } return (best&&bd<=2)?best:NULL; }
static void check_add_var(Var **vars,const char *name){ char tmp[256]; char *t; Var *v; if(!name) return; strncpy(tmp,name,sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); if(!*t) return; if(env_find(*vars,t)) return; v=(Var*)xmalloc(sizeof(Var)); memset(v,0,sizeof(Var)); v->name=xstrdup(t); v->next=*vars; *vars=v; }
static char *check_var_after_as(const char *line){ const char *as=find_word_ci(line,"AS"); if(!as) return NULL; return xstrdup(trim_inplace((char*)as+2)); }
static char *check_between_words(const char *line,const char *a,const char *b){ const char *pa=find_word_ci(line,a); const char *pb; if(!pa) return NULL; pa+=strlen(a); pb=find_word_ci(pa,b); if(!pb) return NULL; return substr(pa,pb); }
typedef struct CheckBlock { const char *expect; const char *open; int line; } CheckBlock;

static int check_file(const char *path){
 FILE *f=fopen(path,"rb"); char line[4096]; int line_no=0,errs=0,sp=0; CheckBlock stack[256]; Var *vars=NULL;
 check_add_var(&vars,"RESULT"); check_add_var(&vars,"LASTERROR"); check_add_var(&vars,"LASTERRORFILE"); check_add_var(&vars,"LASTERRORLINE"); check_add_var(&vars,"LASTEXIT"); check_add_var(&vars,"LASTHTTP");
 if(!f){ fprintf(stderr,"Could not open %s\n",path); return 1;}
 while(fgets(line,sizeof(line),f)){
  char tmp[4096],up[64],w[128]; char *t; line_no++;
  strncpy(tmp,line,sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp);
  if(is_blank_or_comment(t)) continue;
  first_word(t,w,sizeof(w)); upper_copy(up,w,sizeof(up));
  if(!known_command(up)){
   const char *sug=suggest_command_name(up);
   printf("%s:%d: I do not know the command \"%s\".",path,line_no,w);
   if(sug) printf(" Did you mean \"%s\"?",sug);
   printf("\n"); errs++; continue;
  }

  if(!strcmp(up,"IF")){ if(!*trim_inplace(t+2)){ printf("%s:%d: IF needs a condition. Try: IF score = 10\n",path,line_no); errs++; } stack[sp++]=(CheckBlock){"ENDIF","IF",line_no}; }
  else if(!strcmp(up,"CLASS")){ stack[sp++]=(CheckBlock){"ENDCLASS","CLASS",line_no}; }
  else if(!strcmp(up,"START")){ if(starts_ci(t+5," TASK")) stack[sp++]=(CheckBlock){"ENDTASK","START",line_no}; }
  else if(!strcmp(up,"NEW")){ char *name=check_var_after_as(t); if(name){ check_add_var(&vars,name); free(name); } else { const char *pcur=t+3; char *cls=unquote_token(&pcur); name=unquote_token(&pcur); if(name&&*trim_inplace(name)) check_add_var(&vars,name); else { printf("%s:%d: NEW needs a class and a name. Try: NEW Player player\n",path,line_no); errs++; } free(cls); free(name); } }
  else if(!strcmp(up,"TEACH")){ if(!*trim_inplace(t+5)){ printf("%s:%d: TEACH needs a function name. Try: TEACH greet name\n",path,line_no); errs++; } else { const char *takes=find_word_ci(t,"TAKES"); const char *usingw=find_word_ci(t,"USING"); const char *params=takes?takes+5:(usingw?usingw+5:NULL); if(!params){ char *after=t+5; while(*after&&isspace((unsigned char)*after)) after++; while(*after&&!isspace((unsigned char)*after)) after++; params=after; } if(params){ char *pc=xstrdup(params); char *pp=pc; while(pp&&*pp){ char *comma=strchr(pp,','); if(comma){ *comma=0; check_add_var(&vars,pp); pp=comma+1; } else { check_add_var(&vars,pp); break; } } free(pc); } } stack[sp++]=(CheckBlock){"LEARNED","TEACH",line_no}; }
  else if(!strcmp(up,"DO")){ if(find_word_ci(t,"TIMES")){ stack[sp++]=(CheckBlock){"DONE","DO",line_no}; } }
  else if(!strcmp(up,"FOR")){
   char *name=NULL;
   if(find_word_ci(t,"EACH")){
    const char *each=find_word_ci(t,"EACH"); const char *in=find_word_ci(t,"IN");
    if(!in){ printf("%s:%d: FOR EACH needs IN. Try: FOR EACH item IN list\n",path,line_no); errs++; }
    else { name=substr(each+4,in); char *comma=strchr(name,','); if(comma){ *comma=0; check_add_var(&vars,name); check_add_var(&vars,comma+1); } else check_add_var(&vars,name); free(name); }
   } else {
    const char *from=find_word_ci(t,"FROM");
    if(!from){ printf("%s:%d: FOR needs FROM. Try: FOR i FROM 1 TO 5\n",path,line_no); errs++; }
    else { name=substr(t+3,from); check_add_var(&vars,name); free(name); if(!find_word_ci(t,"TO")){ printf("%s:%d: FOR needs TO. Try: FOR i FROM 1 TO 5\n",path,line_no); errs++; } }
   }
   stack[sp++]=(CheckBlock){"DONE","FOR",line_no};
  }
  else if(!strcmp(up,"TRY")){ stack[sp++]=(CheckBlock){"ENDTRY","TRY",line_no}; }
  else if(!strcmp(up,"COMMENT")){ stack[sp++]=(CheckBlock){"ENDCOMMENT","COMMENT",line_no}; }
  else if(!strcmp(up,"REPEAT")){ stack[sp++]=(CheckBlock){"UNTIL","REPEAT",line_no}; }
  else if(!strcmp(up,"ELSE")){ if(sp==0 || strcmp(stack[sp-1].expect,"ENDIF")!=0){ printf("%s:%d: ELSE must be inside an IF block.\n",path,line_no); errs++; } }
  else if(!strcmp(up,"CATCH")){ if(sp==0 || strcmp(stack[sp-1].expect,"ENDTRY")!=0){ printf("%s:%d: CATCH must be inside a TRY block.\n",path,line_no); errs++; } }
  else if(!strcmp(up,"ENDIF")||!strcmp(up,"LEARNED")||!strcmp(up,"DONE")||!strcmp(up,"ENDTRY")||!strcmp(up,"ENDCOMMENT")||!strcmp(up,"ENDCLASS")||!strcmp(up,"ENDTASK")||!strcmp(up,"UNTIL")||!strcmp(up,"END")){
   if(!strcmp(up,"END")){ if(sp==0){ printf("%s:%d: unexpected END\n",path,line_no); errs++; } else sp--; }
   else if(sp==0 || strcmp(stack[sp-1].expect,up)!=0){ printf("%s:%d: unexpected %s\n",path,line_no,up); errs++; } else sp--;
  }

  if(!strcmp(up,"HAS")){ const char *pcur=t+3; char *name=unquote_token(&pcur); if(name&&*trim_inplace(name)) check_add_var(&vars,name); free(name); }

  if(!strcmp(up,"SET")){
   const char *to=find_word_ci(t,"TO");
   if(!to){ const char *pcur=t+3; char *name=unquote_token(&pcur); if(!*trim_inplace(name)||!*trim_inplace((char*)pcur)){ printf("%s:%d: SET needs a name and a value. Try: SET name TO \"Alex\" or SET name \"Alex\"\n",path,line_no); errs++; } else check_add_var(&vars,name); free(name); }
   else { char *name=substr(t+3,to); if(!*trim_inplace(name)){ printf("%s:%d: SET needs a variable name. Try: SET score TO 0\n",path,line_no); errs++; } else check_add_var(&vars,name); free(name); }
  }
  if(!strcmp(up,"ASK")){
   char *name=NULL; const char *as=find_word_ci(t,"AS");
   if(as){ const char *pcur=as+2; name=unquote_token(&pcur); }
   else { const char *pcur=t+3; char *prompt=unquote_token(&pcur); free(prompt); name=unquote_token(&pcur); }
   if(!name||!*trim_inplace(name)){ printf("%s:%d: ASK needs a variable name. Try: ASK \"What is your name?\" name\n",path,line_no); errs++; } else check_add_var(&vars,name); free(name);
  }
  if(!strcmp(up,"COUNT")||!strcmp(up,"READ")||!strcmp(up,"EXISTS")||!strcmp(up,"PARSE")||!strcmp(up,"MAKE")){
   char *name=check_var_after_as(t); if(name){ check_add_var(&vars,name); free(name); }
   else if(!strcmp(up,"COUNT")){ printf("%s:%d: COUNT needs AS. Try: COUNT items AS total\n",path,line_no); errs++; }
  }
  if(!strcmp(up,"GET")){
   char *name=check_var_after_as(t); if(name){ check_add_var(&vars,name); free(name); }
   else { printf("%s:%d: GET needs AS. Try: GET items AT 1 AS item\n",path,line_no); errs++; }
  }
  if(!strcmp(up,"HTTP")){
   const char *as=find_word_ci(t,"AS");
   if(as){ char *name=xstrdup(trim_inplace((char*)as+2)); const char *status=find_word_ci(name,"STATUS"); if(status){ char *primary=substr(name,status); check_add_var(&vars,primary); check_add_var(&vars,trim_inplace((char*)status+6)); free(primary); } else check_add_var(&vars,name); free(name); }
  }
  if(!strcmp(up,"TASK")){
   char *name=check_var_after_as(t); if(name){ check_add_var(&vars,name); free(name); }
  }
  if(!strcmp(up,"CALL")){
   char *name=check_var_after_as(t); if(name){ check_add_var(&vars,name); free(name); }
  }
  if(!strcmp(up,"TEXT")||!strcmp(up,"TYPE")||!strcmp(up,"OBJECT")||!strcmp(up,"RANDOM")||!strcmp(up,"RUN")||!strcmp(up,"LIST")||!strcmp(up,"FIND")||(!strcmp(up,"GET")&&find_word_ci(t,"AS"))){
   char *name=check_var_after_as(t); if(name){ check_add_var(&vars,name); free(name); }
  }
  if(!strcmp(up,"SAY")||!strcmp(up,"IF")||!strcmp(up,"RETURN")){
   const char *expr=t+strlen(w);
   Tokens ts=tokenize(expr); int i; for(i=0;i<ts.n;i++){
    char *tok=ts.t[i];
    if(isalpha((unsigned char)tok[0]) && !ci_eq(tok,"YES")&&!ci_eq(tok,"NO")&&!ci_eq(tok,"AND")&&!ci_eq(tok,"OR")&&!ci_eq(tok,"NOT")&&!ci_eq(tok,"IS")&&!ci_eq(tok,"LIST")&&!ci_eq(tok,"MAP")&&!env_find(vars,tok)){
     Var *v=vars; char *best=NULL; int bd=999; while(v){ int d=levenshtein(tok,v->name); if(d<bd){bd=d; best=v->name;} v=v->next; }
     if(best&&bd<=2) printf("%s:%d: I do not know the variable \"%s\" yet. Did you mean \"%s\"?\n",path,line_no,tok,best);
     else printf("%s:%d: I do not know the variable \"%s\" yet.\n",path,line_no,tok);
     errs++;
    }
   }
  }
 }
 fclose(f);
 while(sp>0){ CheckBlock b=stack[--sp]; printf("%s:%d: %s block opened here needs %s\n",path,b.line,b.open,b.expect); errs++; }
 if(errs==0) printf("OK\n");
 return errs?1:0;
}

static const char *type_env_get(Var *types,const char *name){ Var *v=env_find(types,name); if(v&&v->val.type==V_STR) return v->val.str; return NULL; }
static void type_env_set(Var **types,const char *name,const char *type){ Var *v; char tmp[256]; char *t; if(!name||!type||!*type) return; strncpy(tmp,name,sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); if(!*t) return; v=env_find(*types,t); if(v){ v->val=v_str(type); return; } v=(Var*)xmalloc(sizeof(Var)); memset(v,0,sizeof(Var)); v->name=xstrdup(t); v->val=v_str(type); v->next=*types; *types=v; }
static const char *simple_expr_type(Var *types,const char *expr){ char tmp[512]; char *t; double d; size_t i=0; if(!expr) return NULL; strncpy(tmp,expr,sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); if(!*t) return NULL; if(*t=='"') return "TEXT"; if(parse_number_strict(t,&d)) return "NUMBER"; if(ci_eq(t,"YES")||ci_eq(t,"NO")||ci_eq(t,"TRUE")||ci_eq(t,"FALSE")) return "YESNO"; if(ci_eq(t,"LIST")) return "LIST"; if(ci_eq(t,"MAP")) return "MAP"; if(starts_ci(t,"NEW ")) return "OBJECT"; while(t[i]&&(isalnum((unsigned char)t[i])||t[i]=='_'||t[i]=='.')) i++; if(i>0 && t[i]==0){ return type_env_get(types,t); } return NULL; }
static int type_words_match(const char *need,const char *got){ if(!need||!*need||ci_eq(need,"ANY")) return 1; if(!got||!*got) return 1; if(ci_eq(need,got)) return 1; if(starts_ci(need,"LIST OF") && ci_eq(got,"LIST")) return 1; if(starts_ci(need,"MAP OF") && ci_eq(got,"MAP")) return 1; if((ci_eq(need,"YESNO")||ci_eq(need,"BOOL")||ci_eq(need,"BOOLEAN")) && (ci_eq(got,"YESNO")||ci_eq(got,"BOOL")||ci_eq(got,"BOOLEAN"))) return 1; if(ci_eq(need,"OBJECT") && ci_eq(got,"MAP")) return 1; return 0; }
static const char *container_member_type(const char *type,const char *kind){ const char *p; static char buf[128]; if(!type||!kind) return NULL; if(!starts_ci(type,kind)) return NULL; p=type+strlen(kind); while(*p&&isspace((unsigned char)*p)) p++; if(!starts_ci(p,"OF")) return NULL; p+=2; while(*p&&isspace((unsigned char)*p)) p++; if(!*p) return NULL; snprintf(buf,sizeof(buf),"%s",p); return trim_inplace(buf); }
static void parse_set_for_typecheck2(const char *t,char **name,char **type,char **expr){ const char *rest=t+3; const char *to=find_word_ci(rest,"TO"); const char *as=find_word_ci(rest,"AS"); *name=NULL; *type=NULL; *expr=NULL; if(as&&to&&as<to){ *name=substr(rest,as); *type=substr(as+2,to); *expr=xstrdup(to+2); return; } if(to){ char *before=substr(rest,to); const char *pcur=before; char *var=unquote_token(&pcur); char *maybe=unquote_token(&pcur); char *mt=trim_inplace(maybe); *name=xstrdup(trim_inplace(var)); if(claro_is_type_word(mt)) *type=xstrdup(mt); *expr=xstrdup(to+2); free(before); free(var); free(maybe); return; } { const char *pcur=rest; char *var=unquote_token(&pcur); const char *after_var=pcur; char *maybe=unquote_token(&pcur); char *mt=trim_inplace(maybe); *name=xstrdup(trim_inplace(var)); if(claro_is_type_word(mt)){ *type=xstrdup(mt); *expr=xstrdup(trim_inplace((char*)pcur)); } else { *expr=xstrdup(trim_inplace((char*)after_var)); } free(var); free(maybe); } }
typedef struct TypeParamCheck { char *func; char *param; char *type; int pos; struct TypeParamCheck *next; } TypeParamCheck;
static void add_type_param_check(TypeParamCheck **checks,const char *func,const char *param,const char *type,int pos){ TypeParamCheck *c; if(!func||!*func||!param||!*param||!type||!*type) return; c=(TypeParamCheck*)xmalloc(sizeof(TypeParamCheck)); c->func=xstrdup(func); c->param=xstrdup(param); c->type=xstrdup(type); c->pos=pos; c->next=*checks; *checks=c; }
static const char *type_param_check_for(TypeParamCheck *checks,const char *func,int pos,const char **param){ TypeParamCheck *c=checks; while(c){ if(c->pos==pos&&ci_eq(c->func,func)){ if(param) *param=c->param; return c->type; } c=c->next; } return NULL; }
static int param_index_named(char **params,int pcnt,const char *name){ int i; char tmp[256]; char *p; for(i=0;i<pcnt;i++){ strncpy(tmp,params[i],sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; p=trim_inplace(tmp); if(ci_eq(p,name)) return i; } return -1; }
static TypeParamCheck *collect_function_param_type_checks(FILE *f){ TypeParamCheck *checks=NULL; char line[4096]; while(fgets(line,sizeof(line),f)){ char tmp[4096],up[64],w[128]; char *t; strncpy(tmp,line,sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); if(is_blank_or_comment(t)) continue; first_word(t,w,sizeof(w)); upper_copy(up,w,sizeof(up)); if(!strcmp(up,"TEACH")){ char teachline[4096]; char *fname=NULL; char **params=NULL; int pcnt=0; strncpy(teachline,t,sizeof(teachline)-1); teachline[sizeof(teachline)-1]=0; parse_teach_parts(teachline,&fname,&params,&pcnt); while(fgets(line,sizeof(line),f)){ char inner[4096],iup[64],iw[128]; char *it; strncpy(inner,line,sizeof(inner)-1); inner[sizeof(inner)-1]=0; it=trim_inplace(inner); if(is_blank_or_comment(it)) continue; first_word(it,iw,sizeof(iw)); upper_copy(iup,iw,sizeof(iup)); if(!strcmp(iup,"END")||!strcmp(iup,"LEARNED")) break; if(!strcmp(iup,"CHECK")&&starts_ci(it,"CHECK TYPE")){ const char *is=find_word_ci(it,"IS"); if(is){ char *expr=substr(it+10,is); char *need=xstrdup(trim_inplace((char*)is+2)); char *en=trim_inplace(expr); int idx=param_index_named(params,pcnt,en); if(idx>=0) add_type_param_check(&checks,fname,en,need,idx); free(expr); free(need); } } } } } rewind(f); return checks; }
static int typecheck_file(const char *path){ FILE *f=fopen(path,"rb"); char line[4096]; int line_no=0,errs=0; Var *types=NULL; TypeParamCheck *param_checks=NULL; if(!f){ fprintf(stderr,"Could not open %s\n",path); return 1; } param_checks=collect_function_param_type_checks(f); type_env_set(&types,"RESULT","ANY"); type_env_set(&types,"LASTERROR","TEXT"); type_env_set(&types,"LASTERRORFILE","TEXT"); type_env_set(&types,"LASTERRORLINE","NUMBER"); type_env_set(&types,"LASTEXIT","NUMBER"); while(fgets(line,sizeof(line),f)){ char tmp[4096],up[64],w[128]; char *t; line_no++; strncpy(tmp,line,sizeof(tmp)-1); tmp[sizeof(tmp)-1]=0; t=trim_inplace(tmp); if(is_blank_or_comment(t)) continue; first_word(t,w,sizeof(w)); upper_copy(up,w,sizeof(up)); if(!strcmp(up,"SET")){ char *name=NULL,*type=NULL,*expr=NULL; const char *got,*old; parse_set_for_typecheck2(t,&name,&type,&expr); if(name&&*trim_inplace(name)){ char *nt=trim_inplace(name); char *tt=type?trim_inplace(type):NULL; got=simple_expr_type(types,expr); old=type_env_get(types,nt); if(tt&&*tt){ if(got&&!type_words_match(tt,got)){ printf("%s:%d: Type mismatch for %s: expected %s, but this value looks like %s.\n",path,line_no,nt,tt,got); errs++; } type_env_set(&types,nt,tt); } else if(old){ if(got&&!type_words_match(old,got)){ printf("%s:%d: Type mismatch for %s: it was first set as %s, but this value looks like %s.\n",path,line_no,nt,old,got); errs++; } } else if(got) type_env_set(&types,nt,got); else type_env_set(&types,nt,"ANY"); } free(name); free(type); free(expr); }
  else if(!strcmp(up,"ADD")){ const char *to=find_word_ci(t,"TO"); if(to){ char *expr=substr(t+3,to); char *name=xstrdup(trim_inplace((char*)to+2)); const char *listtype=type_env_get(types,name); const char *need=container_member_type(listtype,"LIST"); const char *got=simple_expr_type(types,expr); if(need&&got&&!type_words_match(need,got)){ printf("%s:%d: Type mismatch for list %s: expected %s item, but this value looks like %s.\n",path,line_no,name,need,got); errs++; } free(expr); free(name); } }
  else if(!strcmp(up,"PUT")){ const char *key=find_word_ci(t,"KEY"), *val=find_word_ci(t,"VALUE"); if(key&&val){ char *name=substr(t+3,key); char *expr=xstrdup(trim_inplace((char*)val+5)); char *nt=trim_inplace(name); const char *maptype=type_env_get(types,nt); const char *need=container_member_type(maptype,"MAP"); const char *got=simple_expr_type(types,expr); if(need&&got&&!type_words_match(need,got)){ printf("%s:%d: Type mismatch for map %s: expected %s value, but this value looks like %s.\n",path,line_no,nt,need,got); errs++; } free(name); free(expr); } }
  else if(!strcmp(up,"ASK")){ const char *as=find_word_ci(t,"AS"); char *name=NULL,*type=NULL; if(as){ const char *pcur=as+2; name=unquote_token(&pcur); { char *rest=xstrdup(trim_inplace((char*)pcur)); if(claro_is_type_word(rest)) type=rest; else free(rest); } } else { const char *pcur=t+3; char *prompt=unquote_token(&pcur); free(prompt); name=unquote_token(&pcur); { char *rest=xstrdup(trim_inplace((char*)pcur)); if(claro_is_type_word(rest)) type=rest; else free(rest); } } if(name&&*trim_inplace(name)) type_env_set(&types,trim_inplace(name),type?type:"TEXT"); free(name); free(type); }
  else if(!strcmp(up,"TYPE")&&starts_ci(t,"TYPE OF")){ char *name=check_var_after_as(t); if(name){ type_env_set(&types,name,"TEXT"); free(name); } }
  else if(!strcmp(up,"NEW")){ const char *as=find_word_ci(t,"AS"); char *name=NULL; if(as) name=xstrdup(trim_inplace((char*)as+2)); else { const char *pcur=t+3; char *cls=unquote_token(&pcur); free(cls); name=unquote_token(&pcur); } if(name&&*trim_inplace(name)) type_env_set(&types,trim_inplace(name),"OBJECT"); free(name); }
  else if((!strcmp(up,"DO")&&!find_word_ci(t,"TIMES"))||!strcmp(up,"CALL")){ char *fname=NULL; char **parts=NULL; int ac=0,i; if(!strcmp(up,"DO")){ const char *pcur=t+2; fname=unquote_token(&pcur); if(*trim_inplace((char*)pcur)) ac=split_args(pcur,&parts); } else { char *rest=t+4; const char *with=find_word_ci(rest,"WITH"); fname=with?substr(rest,with):xstrdup(rest); if(with) ac=split_args(with+4,&parts); } for(i=0;i<ac;i++){ const char *param=NULL; const char *need=type_param_check_for(param_checks,trim_inplace(fname),i,&param); const char *got=simple_expr_type(types,parts[i]); if(need&&got&&!type_words_match(need,got)){ printf("%s:%d: Type mismatch for function %s: parameter %s needs %s, but this argument looks like %s.\n",path,line_no,trim_inplace(fname),param?param:"argument",need,got); errs++; } } free(fname); }
  else if(!strcmp(up,"CHECK")&&starts_ci(t,"CHECK TYPE")){ const char *is=find_word_ci(t,"IS"); if(is){ char *expr=substr(t+10,is); char *need=xstrdup(trim_inplace((char*)is+2)); const char *got=simple_expr_type(types,expr); if(got&&!type_words_match(need,got)){ printf("%s:%d: Type check failed: expected %s, but %s looks like %s.\n",path,line_no,need,trim_inplace(expr),got); errs++; } free(expr); free(need); } else { printf("%s:%d: CHECK TYPE needs IS. Try: CHECK TYPE score IS NUMBER\n",path,line_no); errs++; } }
 }
 fclose(f); if(errs==0) printf("Type check OK\n"); return errs?1:0; }
static char *read_file_text(const char *path){ FILE *f=fopen(path,"rb"); Str b; int c; if(!f) return NULL; str_init(&b); while((c=fgetc(f))!=EOF) str_ch(&b,(char)c); fclose(f); return str_take(&b); }
static int run_one_test(const char *path){ char outpath[512]; char *dot; char *expect,*got; int rc,ok; Runtime rt; snprintf(outpath,sizeof(outpath),"%s",path); dot=strrchr(outpath,'.'); if(dot) strcpy(dot,".out"); expect=read_file_text(outpath); if(!expect) return 0; rt_init(&rt); rt.capture=1; rc=run_file(&rt,path); got=rt.captured.s?xstrdup(rt.captured.s):xstrdup(""); ok=(rc==0 && strcmp(got,expect)==0); printf("%s %s\n",ok?"PASS":"FAIL",path); if(!ok) printf("Expected:\n%s\nGot:\n%s\n",expect,got); free(expect); free(got); return ok?0:1; }
static int run_tests(void){ int fails=0;
#ifndef _WIN32
 DIR *d=opendir("tests"); struct dirent *de; if(!d){ fprintf(stderr,"No tests directory\n"); return 1;} while((de=readdir(d))){ if(strstr(de->d_name,".claro")){ char path[512]; snprintf(path,sizeof(path),"tests/%s",de->d_name); fails+=run_one_test(path); } } closedir(d);
#else
 struct _finddata_t fd; intptr_t h=_findfirst("tests/*.claro",&fd); if(h==-1){ fprintf(stderr,"No tests directory\n"); return 1;} do { char path[512]; snprintf(path,sizeof(path),"tests/%s",fd.name); fails+=run_one_test(path); } while(_findnext(h,&fd)==0); _findclose(h);
#endif
 printf("%s: %d failure(s)\n",fails?"FAIL":"PASS",fails); return fails?1:0; }

static int write_text_file_simple(const char *path,const char *text){ FILE *f=fopen(path,"wb"); if(!f) return 0; fputs(text,f); fclose(f); return 1; }
static int create_new_project(const char *name){ char path[512]; char text[1024]; if(!name||!*name){ fprintf(stderr,"Project needs a name. Try: claro new MyProject\n"); return 1; } if(!make_folder(name)){ fprintf(stderr,"Could not create project folder: %s\n",name); return 1; } snprintf(path,sizeof(path),"%s/main.claro",name); write_text_file_simple(path,"SAY \"Welcome to Claro!\"\n\nSET name TO \"Learner\"\nSAY \"Hello \" + name\n\nTEACH greet person\n    SAY \"Nice to meet you, \" + person\nEND\n\nDO greet \"Friend\"\n"); snprintf(path,sizeof(path),"%s/packages",name); make_folder(path); snprintf(path,sizeof(path),"%s/claro.project",name); snprintf(text,sizeof(text),"name: %s\nmain: main.claro\nversion: v1.18.26\npackages:\n",name); write_text_file_simple(path,text); snprintf(path,sizeof(path),"%s/claro.lock",name); write_text_file_simple(path,"# Claro package lock\nversion: v1.18.26\n"); snprintf(path,sizeof(path),"%s/README.md",name); write_text_file_simple(path,"# My Claro Project\n\nBuild Claro, then run this project with:\n\n```bash\nclaro run\n```\n\nUse packages with:\n\n```bash\nclaro package add text\nclaro package list\nclaro package doctor\n```\n"); printf("Created Claro project: %s\n",name); printf("Next steps:\n  cd %s\n  claro run\n",name); return 0; }
static int run_repl(void){ Runtime rt; char line[4096]; Program p; rt_init(&rt); memset(&p,0,sizeof(p)); p.path=xstrdup("<repl>"); p.count=1; p.cap=1; p.lines=(char**)xmalloc(sizeof(char*)); printf("%s\n",CLARO_VERSION); printf("Type HELP for help, or EXIT to leave.\n"); while(1){ int pc=0; printf("> "); fflush(stdout); if(!fgets(line,sizeof(line),stdin)) break; { size_t n=strlen(line); while(n&&(line[n-1]=='\n'||line[n-1]=='\r')) line[--n]=0; } { char *t=trim_inplace(line); if(ci_eq(t,"EXIT")||ci_eq(t,"QUIT")) break; if(ci_eq(t,"HELP")){ printf("Try: SAY \"Hello\"\n"); printf("Try: SET name TO \"Jon\"\n"); printf("Try: SAY name\n"); continue; } if(!*t) continue; p.lines[0]=t; exec_line(&rt,&p,&pc,t); if(rt.error){ fprintf(stderr,"%s:%d: %s\n",rt.err_file?rt.err_file:"<repl>",rt.err_line,rt.err_msg?rt.err_msg:"error"); rt_clear_error(&rt); } } } return 0; }

static int file_exists_simple(const char *path);
static int path_exists_simple(const char *path){ struct stat st; return path&&*path&&stat(path,&st)==0; }
static int package_name_safe(const char *name){ int i; if(!name||!*name) return 0; if(name[0]=='.'||name[0]=='-'||name[0]=='_') return 0; for(i=0;name[i];i++){ unsigned char c=(unsigned char)name[i]; if(!(isalnum(c)||c=='_'||c=='-')) return 0; } return 1; }
static void package_checksum(const char *name,char *out,size_t n){ unsigned long h=5381; const char *p=name?name:""; while(*p){ h=((h<<5)+h)+(unsigned char)(*p++); } p="|local|1|claro"; while(*p){ h=((h<<5)+h)+(unsigned char)(*p++); } snprintf(out,n,"%08lx",h); }
static void ensure_project_file(void){ if(!file_exists_simple("claro.project")) write_text_file_simple("claro.project","manifest-version: 1\nname: ClaroProject\nmain: main.claro\nversion: v1.18.26\npackages:\n"); }
static char *project_value(const char *key){ char *txt=read_file_text("claro.project"); size_t kn=strlen(key); char *p,*out=NULL; if(!txt) return NULL; p=txt; while(*p){ char *line=p; char save; while(*p&&*p!='\n'&&*p!='\r') p++; save=*p; *p=0; { char *t=trim_inplace(line); if(strnicmp2(t,key,kn)==0 && t[kn]==':'){ out=xstrdup(trim_inplace(t+kn+1)); break; } } if(save) p++; while(*p=='\n'||*p=='\r') p++; } free(txt); return out; }
static int package_has_name(const char *name){ char *txt=read_file_text("claro.project"); char *p; int found=0; if(!txt) return 0; p=txt; while(*p){ char *line=p; char save; while(*p&&*p!='\n'&&*p!='\r') p++; save=*p; *p=0; { char *t=trim_inplace(line); if(strnicmp2(t,"package:",8)==0){ char *pkg=trim_inplace(t+8); if(strcmp(pkg,name)==0){ found=1; break; } } } if(save) p++; while(*p=='\n'||*p=='\r') p++; } free(txt); return found; }
static int write_package_lock(void){ char *txt=read_file_text("claro.project"); FILE *f; char *p; if(!txt) return 0; f=fopen("claro.lock","wb"); if(!f){ free(txt); return 0; } fputs("# Claro package lock\nlock-version: 1\nversion: v1.18.26\n",f); p=txt; while(*p){ char *line=p; char save; while(*p&&*p!='\n'&&*p!='\r') p++; save=*p; *p=0; { char *t=trim_inplace(line); if(strnicmp2(t,"package:",8)==0){ char *pkg=trim_inplace(t+8); if(*pkg){ char sum[32]; package_checksum(pkg,sum,sizeof(sum)); fprintf(f,"package: %s\nchecksum: %s\n",pkg,sum); } } } if(save) p++; while(*p=='\n'||*p=='\r') p++; } fclose(f); free(txt); return 1; }
static int append_package_to_project(const char *name){ FILE *f; if(!package_name_safe(name)){ fprintf(stderr,"Package names may use only letters, numbers, dash, and underscore.\n"); return 0; } ensure_project_file(); if(package_has_name(name)){ printf("Package already listed: %s\n",name); return 1; } f=fopen("claro.project","ab"); if(!f) return 0; fprintf(f,"package: %s\n",name); fclose(f); write_package_lock(); return 1; }
static int remove_package_from_project(const char *name){ char *txt=read_file_text("claro.project"); FILE *f; char *p; int removed=0; if(!txt) return 0; f=fopen("claro.project","wb"); if(!f){ free(txt); return 0; } p=txt; while(*p){ char *line=p; char save; int skip=0; while(*p&&*p!='\n'&&*p!='\r') p++; save=*p; *p=0; { char *copy=xstrdup(line); char *t=trim_inplace(copy); if(strnicmp2(t,"package:",8)==0){ char *pkg=trim_inplace(t+8); if(strcmp(pkg,name)==0){ skip=1; removed=1; } } free(copy); } if(!skip) fprintf(f,"%s\n",line); if(save) p++; while(*p=='\n'||*p=='\r') p++; } fclose(f); free(txt); write_package_lock(); return removed; }
static void create_package_folder(const char *name){ char path[512], meta[512], readme[512], sum[32]; make_folder("packages"); snprintf(path,sizeof(path),"packages/%s",name); make_folder(path); snprintf(meta,sizeof(meta),"%s/claro.package",path); package_checksum(name,sum,sizeof(sum)); { char text[1024]; snprintf(text,sizeof(text),"manifest-version: 1\nname: %s\nversion: 1\nsource: local\nchecksum: %s\n",name,sum); write_text_file_simple(meta,text); } snprintf(readme,sizeof(readme),"%s/README.md",path); if(!file_exists_simple(readme)){ char text[512]; snprintf(text,sizeof(text),"# %s\n\nThis is a local Claro package folder.\n",name); write_text_file_simple(readme,text); } }
static int list_project_packages(void){ char *txt=read_file_text("claro.project"); char *p; int count=0; printf("Packages in claro.project:\n"); if(!txt){ printf("  (no claro.project yet)\n"); return 0; } p=txt; while(*p){ char *line=p; char save; while(*p&&*p!='\n'&&*p!='\r') p++; save=*p; *p=0; { char *t=trim_inplace(line); if(strnicmp2(t,"package:",8)==0){ char *pkg=trim_inplace(t+8); if(*pkg){ printf("  %s\n",pkg); count++; } } } if(save) p++; while(*p=='\n'||*p=='\r') p++; } if(!count) printf("  (none)\n"); free(txt); return 0; }
static int package_doctor(void){ int ok=1; char *mainfile; char *txt; printf("%s\n",CLARO_VERSION); printf("Package/project doctor:\n"); printf("  %s claro.project\n",file_exists_simple("claro.project")?"OK":"MISSING"); if(!file_exists_simple("claro.project")) ok=0; mainfile=project_value("main"); if(mainfile&&*mainfile){ printf("  %s main script: %s\n",file_exists_simple(mainfile)?"OK":"MISSING",mainfile); if(!file_exists_simple(mainfile)) ok=0; } else { printf("  MISSING main setting\n"); ok=0; } printf("  %s packages folder\n",path_exists_simple("packages")?"OK":"MISSING"); if(!path_exists_simple("packages")) ok=0; printf("  %s claro.lock\n",file_exists_simple("claro.lock")?"OK":"MISSING"); if(!file_exists_simple("claro.lock")) ok=0; txt=read_file_text("claro.project"); if(txt){ char *p=txt; while(*p){ char *line=p; char save; while(*p&&*p!='\n'&&*p!='\r') p++; save=*p; *p=0; { char *t=trim_inplace(line); if(strnicmp2(t,"package:",8)==0){ char *pkg=trim_inplace(t+8); if(*pkg){ char meta[512], *mt, sum[32]; snprintf(meta,sizeof(meta),"packages/%s/claro.package",pkg); mt=read_file_text(meta); if(mt&&strstr(mt,"manifest-version: 1")&&strstr(mt,"checksum:")){ printf("  OK package manifest: %s\n",pkg); package_checksum(pkg,sum,sizeof(sum)); if(strstr(mt,sum)) printf("  OK package checksum: %s\n",pkg); else { printf("  BAD package checksum: %s\n",pkg); ok=0; } } else { printf("  MISSING package manifest: %s\n",pkg); ok=0; } free(mt); } } } if(save) p++; while(*p=='\n'||*p=='\r') p++; } free(txt); } free(mainfile); printf("%s\n",ok?"Package/project files look ready.":"Package/project files need attention."); return ok?0:1; }
static int run_package_cmd(int argc,char **argv,int arg){ if(arg>=argc){ printf("Package commands:\n  claro package init\n  claro package add NAME\n  claro package remove NAME\n  claro package list\n  claro package doctor\n  claro package lock\n"); return 0; } if(strcmp(argv[arg],"init")==0){ ensure_project_file(); make_folder("packages"); write_package_lock(); printf("Package project ready: claro.project, claro.lock, packages/\n"); return 0; } if(strcmp(argv[arg],"add")==0&&arg+1<argc){ const char *name=argv[arg+1]; int already; if(!package_name_safe(name)){ fprintf(stderr,"Package names may use only letters, numbers, dash, and underscore.\n"); return 1; } ensure_project_file(); make_folder("packages"); already=package_has_name(name); if(!append_package_to_project(name)) return 1; create_package_folder(name); write_package_lock(); if(!already) printf("Added package: %s\n",name); return 0; } if(strcmp(argv[arg],"remove")==0&&arg+1<argc){ const char *name=argv[arg+1]; if(!package_name_safe(name)){ fprintf(stderr,"Package names may use only letters, numbers, dash, and underscore.\n"); return 1; } if(remove_package_from_project(name)) printf("Removed package from project: %s\n",name); else printf("Package was not listed: %s\n",name); return 0; } if(strcmp(argv[arg],"list")==0) return list_project_packages(); if(strcmp(argv[arg],"doctor")==0) return package_doctor(); if(strcmp(argv[arg],"lock")==0||strcmp(argv[arg],"update")==0){ ensure_project_file(); make_folder("packages"); if(write_package_lock()){ printf("Updated claro.lock\n"); return 0; } fprintf(stderr,"Could not write claro.lock\n"); return 1; } printf("Unknown package command. Try: claro package init\n"); return 1; }
static int print_ide_info(void){
 printf("{\n");
 printf("  \"language\": \"Claro\",\n");
 printf("  \"version\": \"v1.18.26\",\n");
 printf("  \"file_extensions\": [\".claro\"],\n");
 printf("  \"keywords\": [\"SAY\",\"ASK\",\"SET\",\"IF\",\"ELSE\",\"ENDIF\",\"END\",\"REPEAT\",\"UNTIL\",\"TEACH\",\"LEARNED\",\"DO\",\"RETURN\",\"CLASS\",\"HAS\",\"NEW\",\"IMPORT\",\"TRY\",\"CATCH\",\"ENDTRY\",\"START TASK\",\"YIELD\",\"WAIT TASK\",\"TASK STATUS\",\"HTTP CHECK\",\"HTTP GET\",\"HTTP SAVE\",\"OPEN WINDOW\"],\n");
 printf("  \"types\": [\"NUMBER\",\"TEXT\",\"YESNO\",\"LIST\",\"LIST OF TEXT\",\"LIST OF NUMBER\",\"LIST OF YESNO\",\"MAP\",\"MAP OF TEXT\",\"MAP OF NUMBER\",\"MAP OF YESNO\",\"OBJECT\",\"ANY\"],\n");
 printf("  \"commands\": [\n");
 printf("    {\"name\": \"run\", \"usage\": \"claro run\", \"description\": \"Run main.claro or the project main script\"},\n");
 printf("    {\"name\": \"check\", \"usage\": \"claro check file.claro\", \"description\": \"Check beginner syntax and block mistakes\"},\n");
 printf("    {\"name\": \"typecheck\", \"usage\": \"claro typecheck file.claro\", \"description\": \"Check static types before running\"},\n");
 printf("    {\"name\": \"fmt\", \"usage\": \"claro fmt file.claro\", \"description\": \"Print a formatted version of a script\"},\n");
 printf("    {\"name\": \"test\", \"usage\": \"claro test\", \"description\": \"Run golden tests\"}\n");
 printf("  ],\n");
 printf("  \"snippets\": [\n");
 printf("    {\"name\": \"hello\", \"prefix\": \"say\", \"body\": \"SAY \\\"Hello!\\\"\"},\n");
 printf("    {\"name\": \"if_else\", \"prefix\": \"if\", \"body\": \"IF condition\\n    SAY \\\"Yes\\\"\\nELSE\\n    SAY \\\"No\\\"\\nENDIF\"},\n");
 printf("    {\"name\": \"function\", \"prefix\": \"teach\", \"body\": \"TEACH name item\\n    SAY item\\nLEARNED\"},\n");
 printf("    {\"name\": \"typed_list\", \"prefix\": \"listof\", \"body\": \"SET names AS LIST OF TEXT TO LIST\\nADD \\\"Ada\\\" TO names\"},\n");
 printf("    {\"name\": \"task\", \"prefix\": \"task\", \"body\": \"START TASK helloTask\\n    SAY \\\"Inside task\\\"\\n    YIELD\\nENDTASK\\nTASK STATUS helloTask AS status\\nSAY status\\nWAIT TASK helloTask\"}\n");
 printf("  ],\n");
 printf("  \"diagnostics\": [\n");
 printf("    {\"source\": \"claro check\", \"format\": \"path:line: message\", \"description\": \"Syntax and block-structure diagnostics\"},\n");
 printf("    {\"source\": \"claro typecheck\", \"format\": \"path:line: message\", \"description\": \"Static type diagnostics for variables and containers\"}\n");
 printf("  ]\n");
 printf("}\n");
 return 0;
}
static void print_help(void){
 printf("%s\n",CLARO_VERSION);
 printf("Usage:\n");
 printf("  claro file.claro              Run a Claro script\n");
 printf("  claro run                     Run main.claro in this folder\n");
 printf("  claro test                    Run the built-in tests\n");
 printf("  claro check file.claro        Check a script for beginner mistakes\n");
 printf("  claro typecheck file.claro    Check simple static types\n");
 printf("  claro fmt file.claro          Print a formatted version\n");
 printf("  claro repl                    Try one line at a time\n");
 printf("  claro new MyProject           Create a starter project\n");
 printf("  claro examples                List included examples\n");
 printf("  claro doctor                  Check this Claro folder\n");
 printf("  claro validate                Run stable package validation\n");
 printf("  claro package init|add|remove|list|doctor   Manage Claro packages\n");
 printf("  claro ide                     Print editor keyword metadata\n");
}
static int show_examples(void){ const char *items[]={"hello.claro","name_input.claro","quiz.claro","calculator.claro","guessing_game.claro","shopping_list.claro","save_and_load_file.claro","simple_functions.claro","text_and_lists.claro","text_polish.claro","practical_scripting.claro","type_hardening.claro","typed_ask.claro","objects_classes.claro","networking.claro",NULL}; int i; printf("Included beginner examples:\n"); for(i=0;items[i];i++) printf("  examples/%s\n",items[i]); printf("\nRun one with: claro examples/hello.claro\n"); return 0; }
static int file_exists_simple(const char *path){ FILE *f=fopen(path,"rb"); if(f){ fclose(f); return 1; } return 0; }
static int run_doctor(void){ int ok=1; const char *files[]={"src/claro.c","README.md","assets/Claro_Logo.jpg","lessons/01_hello.claro","examples/hello.claro","tests/01_hello.claro",NULL}; int i; printf("%s\n",CLARO_VERSION); printf("Doctor check:\n"); for(i=0;files[i];i++){ int has=file_exists_simple(files[i]); printf("  %s %s\n",has?"OK":"MISSING",files[i]); if(!has) ok=0; } printf("%s\n",ok?"Claro folder looks ready.":"Some Claro files are missing."); return ok?0:1; }
static int run_validate(void){ int fails=0, i; const char *checks[]={"lessons/01_hello.claro","lessons/02_ask_name.claro","lessons/03_variables.claro","lessons/04_math.claro","lessons/05_if_else.claro","lessons/06_loops.claro","lessons/07_lists.claro","lessons/08_functions.claro","lessons/09_files.claro","lessons/10_final_quiz.claro","examples/hello.claro","examples/name_input.claro","examples/quiz.claro","examples/calculator.claro","examples/guessing_game.claro","examples/shopping_list.claro","examples/save_and_load_file.claro","examples/simple_functions.claro","examples/text_and_lists.claro","examples/text_polish.claro","examples/practical_scripting.claro","examples/type_hardening.claro","examples/objects_classes.claro","examples/networking.claro",NULL}; printf("%s\n",CLARO_VERSION); printf("Stable package validation:\n"); fails+=run_doctor(); fails+=run_tests(); printf("Checking lessons and main examples:\n"); for(i=0;checks[i];i++){ printf("  %s\n",checks[i]); fails+=check_file(checks[i]); } fails+=typecheck_file("tests/typecheck_good.claro"); fails+=typecheck_file("tests/typecheck_container_good.claro"); fails+=typecheck_file("tests/typecheck_function_good.claro"); fails+=typecheck_file("tests/typecheck_function_multi_good.claro"); if(typecheck_file("tests/typecheck_bad.claro")==0) fails++; if(typecheck_file("tests/typecheck_container_bad.claro")==0) fails++; if(typecheck_file("tests/typecheck_function_bad.claro")==0) fails++; if(typecheck_file("tests/typecheck_function_multi_bad.claro")==0) fails++; printf("%s\n",fails?"Validation found problems.":"Validation passed. Claro v1.18.26 foundation checks are ready for use."); return fails?1:0; }

int main(int argc,char **argv){ int arg=1, trace=0; if(argc<2){ print_help(); return 0;} if(strcmp(argv[arg],"--trace")==0||strcmp(argv[arg],"trace")==0){ trace=1; arg++; } if(arg>=argc) return 0; if(strcmp(argv[arg],"help")==0||strcmp(argv[arg],"--help")==0){ print_help(); return 0; } if(strcmp(argv[arg],"test")==0) return run_tests(); if(strcmp(argv[arg],"repl")==0) return run_repl(); if(strcmp(argv[arg],"examples")==0) return show_examples(); if(strcmp(argv[arg],"doctor")==0) return run_doctor(); if(strcmp(argv[arg],"validate")==0) return run_validate(); if(strcmp(argv[arg],"package")==0) return run_package_cmd(argc,argv,arg+1); if(strcmp(argv[arg],"ide")==0) return print_ide_info(); if(strcmp(argv[arg],"new")==0&&arg+1<argc) return create_new_project(argv[arg+1]); if(strcmp(argv[arg],"fmt")==0&&arg+1<argc) return fmt_file(argv[arg+1]); if(strcmp(argv[arg],"check")==0&&arg+1<argc) return check_file(argv[arg+1]); if(strcmp(argv[arg],"typecheck")==0&&arg+1<argc) return typecheck_file(argv[arg+1]); if(strcmp(argv[arg],"version")==0||strcmp(argv[arg],"--version")==0){ puts(CLARO_VERSION); return 0; } if(strcmp(argv[arg],"run")==0){ arg++; if(arg>=argc){ Runtime rt; int rc; char *mainfile=project_value("main"); if(!mainfile||!*mainfile){ if(mainfile) free(mainfile); mainfile=xstrdup("main.claro"); } rt_init(&rt); rt.trace=trace; rt.script_argc=0; rt.script_argv=NULL; rc=run_file(&rt,mainfile); free(mainfile); return rc; } } { Runtime rt; int rc; rt_init(&rt); rt.trace=trace; rt.script_argc=argc-arg-1; rt.script_argv=argv+arg+1; rc=run_file(&rt,argv[arg]); return rc; } }
