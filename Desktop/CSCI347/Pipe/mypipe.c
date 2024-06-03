/*****************************************************************************
 *Write a program that executes two commands using a pipe*
 *The two commands should be entered by the user as arguments enclosed by " " and separated by |, e.g. ./mypipe "command1 | command2"
 *If no arguments are entered by the user, the program will assume command 1 is ls -l and command 2 is sort.
 *The correctness of both commands is totally at the discretion of the user                           *
 *The program should execute  the commands in pipe and show the output (if any)
 *****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h> /* strsep, etc. */

#define MAX_NUM_ARGS 20 /* Maximum number of arguments allowed */
#define MAX_STR_LEN 200 /* Maximum string length */

int main(int argc, char *argv[])
{
       int fd[2];                                        /* Two ends of the pipe */
       char *lhs = NULL;                                 /* Left hand side command of the pipe */
       char *rhs = NULL;                                 /* Right hand side command of the pipe */
       char *lhscommand = "ls";                          /* Default command name on left hand side of pipe */
       char *rhscommand = "sort";                        /* Default command name on right hand side of pipe */
       char *lhsargs[MAX_NUM_ARGS] = {"ls", "-l", NULL}; /* Default LHS args */
       char *rhsargs[MAX_NUM_ARGS] = {"sort", NULL};     /* Default RHS args */

       /*Parse the user input to extract the commands and their arguments*/
       /*Hint: read about strsep(3) */
       if (argc == 2)
       {
              char *input = argv[1];

              if ((lhs = strsep(&input, "|")) == NULL || (rhs = strsep(&input, "|")) == NULL){
                     printf("Usage:\n");
                     printf("./mypipe [\"<LHS-command>|<RHS-command>\"]\n");
                     exit(1);
              }

              char *t;
              int i = 0;
              while ((t = strsep(&lhs, " ")) != NULL){
                     if (*t != '\0')
                     {
                            lhsargs[i++] = t;
                     }
              }
              lhsargs[i] = NULL;

              i = 0;
              while ((t = strsep(&rhs, " ")) != NULL)
              {
                     if (*t != '\0')
                     {
                            rhsargs[i++] = t;
                     }
              }
              rhsargs[i] = NULL;
       }
       else if (argc > 2)
       {
              printf("Usage:\n");
              printf("./mypipe [\"<LHS-command>|<RHS-command>\"]\n");
              exit(1);
       }

       /* Create the pipe */
       if (pipe(fd) < 0)
       {
              perror("Pipe error");
              exit(1);
       }; /* fd[0] is read end, fd[1] is write end */
       pid_t pid = fork();

       /* Do the forking */
       switch (pid)
       {
       case -1:
              perror("Fork error");
              exit(1);

       case 0:
              /* The LHS of command 'ls -l|sort' i.e. 'ls' should be
              executed in the child. */

              close(fd[0]);
              dup2(fd[1], STDOUT_FILENO);
              close(fd[1]);
              execvp(lhsargs[0], lhsargs);
              perror("execvp error");
              exit(1);

       default:
              /*The RHS of command 'ls -l|sort' i.e. 'sort' should be
              executed in the parent. */
              close(fd[1]);
              dup2(fd[0], STDIN_FILENO);
              close(fd[0]);

              execvp(rhsargs[0], rhsargs);
              perror("execvp");
              exit(1);
       }
       return 0;
}
