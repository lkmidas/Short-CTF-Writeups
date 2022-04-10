#define _GNU_SOURCE
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>

#include <sys/ptrace.h>
#include <signal.h>
#include <sys/user.h>
#include <sys/types.h>
#include <sys/wait.h>


const char * sus[] = {
    "STANDARD-ANTIVIRUS-TEST-FILE!$H+H*",
    "crypt_defenses","crypt_badstuff"
};

void sig_handler(int signum){
    printf("TIMEOUT\n");
    exit(1);
}

int detect_string(char* fname){
    FILE* fp = fopen(fname, "r");

    fseek(fp, 0, SEEK_END); 
    int elfbuffer_len = ftell(fp);
    fseek(fp, 0, SEEK_SET); 

    char* elfbuffer = (char*)malloc(elfbuffer_len);

    fread(elfbuffer, 1, elfbuffer_len, fp);

    int ret = 0;
    for(int i = 0 ; i < sizeof(sus) / sizeof(char *); i++) {
        ret |= (memmem(elfbuffer, elfbuffer_len, sus[i], strlen(sus[i])) != NULL);
    }

    free(elfbuffer);
    return ret;
}

int main(int argc, char* argv[]){
    signal(SIGALRM,sig_handler); // Register signal handler
    alarm(10);

    if (argc == 1){
        exit(-2);
    }

    if (detect_string(argv[1])){
        printf("SUSSY STRING DETECTED\n");
        printf("MALWARE\n");
        exit(1);
    }

    int status = 0, pid;
    struct user_regs_struct uregs;

    if ((pid = fork()) == 0) { // child
        ptrace(PTRACE_TRACEME, 0, 0, 0);
        raise(SIGSTOP);

        execl(argv[1], "DIANO", "WAYTOODONK", "KEKC", "OMEGALUL", NULL);

    } else {
        while (1){
            ptrace(PTRACE_SYSCALL, pid, 0, 0);
            waitpid(pid, &status, 0);
            ptrace(PTRACE_GETREGS, pid, 0, &uregs);

            int blocked = 0;

            int syscall_no = uregs.orig_rax;
            if (syscall_no == 1){ // write
                unsigned int buf[1000];
                char* addr = (char*)uregs.rsi;
                int len = uregs.rdx;
                if (len < 100){
                    const char* sussy = "STANDARD-ANTIVIRUS-TEST-FILE!$H+H*";
                    for (int i = 0; i < len/4; i += 1){
                        buf[i] = ptrace(PTRACE_PEEKDATA, pid, addr + 4*i, 0);
                    }
                    if (memmem((char*)buf, len, sussy, strlen(sussy)) != NULL){
                        printf("MALWARE\n");
                        uregs.orig_rax = -1;
                        ptrace(PTRACE_SETREGS, pid, 0, &uregs);
                        exit(1);
                    }
                }

            } else if (syscall_no == 0){ // read
                if (uregs.rdi == 0){
                    uregs.orig_rax = -1;
                    ptrace(PTRACE_SETREGS, pid, 0, &uregs);
                    blocked = 1;
                }

            } else if (syscall_no == 35){ // nanosleep
                uregs.orig_rax = -1;
                ptrace(PTRACE_SETREGS, pid, 0, &uregs);
                blocked = 1;

            } else if (syscall_no == 57){ // fork
                printf("BLOCKED FORK\n");
                uregs.orig_rax = -1;
                ptrace(PTRACE_SETREGS, pid, 0, &uregs);
                blocked = 1;

            } else if (syscall_no == 101){ // ptrace
                uregs.orig_rax = -1;
                ptrace(PTRACE_SETREGS, pid, 0, &uregs);
                blocked = 1;
            }  

            ptrace(PTRACE_SYSCALL, pid, 0, 0);
            waitpid(pid, &status, 0);

            if (blocked){
                uregs.rax = 0;
                ptrace(PTRACE_SETREGS, pid, 0, &uregs);
            }
            
            if (WIFEXITED(status))
                break;
        }
        printf("SAFE\n");
        exit(0);
    }

}
