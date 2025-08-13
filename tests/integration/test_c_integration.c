#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

int main() {
    int32_t results[3];
    
    FILE* fp = popen("check_cred_bin", "r");
    if (!fp) {
        perror("Failed to run command");
        return EXIT_FAILURE;
    }

    size_t read = fread(results, sizeof(int32_t), 3, fp);
    pclose(fp);
    
    if (read != 3) {
        fprintf(stderr, "Incomplete data\n");
        return EXIT_FAILURE;
    }
    
    printf("Security check results:\n");
    printf("Directory: %s\n", results[0] == 0 ? "OK" : "FAIL");
    printf("Credentials: %s\n", results[1] == 0 ? "OK" : "FAIL");
    printf("Encryption Key: %s\n", results[2] == 0 ? "OK" : "FAIL");
    
    return (results[0] == 0 && results[1] == 0 && results[2] == 0) ? 
        EXIT_SUCCESS : EXIT_FAILURE;
}