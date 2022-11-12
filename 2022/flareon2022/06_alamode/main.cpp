#include <iostream>
#include <windows.h>

using namespace std;

/* run this program using the console pauser or add your own getch, system("pause") or input loop */

int main(int argc, char** argv) {
	HMODULE base = LoadLibraryA("./HowDoesThisWork.dll");
	unsigned long long key_gen_addr = (unsigned long long)base + 0x11EF;
	unsigned long long decrypt_flag = (unsigned long long)base + 0x1187;
	unsigned long long seed_addr = (unsigned long long)base + 0x15000;
	unsigned long long enc_pass_addr = (unsigned long long)base + 0x15028;
	unsigned long long enc_flag_addr = (unsigned long long)base + 0x15008;
	
	int key[258];
	((int (*)(int*, int, int))key_gen_addr)(key, seed_addr, 8);
	
	((int (*)(int*, int, int))decrypt_flag)(key, enc_pass_addr, 9);
	((int (*)(int*, int, int))decrypt_flag)(key, enc_flag_addr, 31);
	
	printf("%s\n", (char*)enc_flag_addr);
	
	return 0;
}
