/* Native-OS evidence helper, not part of the Claro interpreter. */
#include <windows.h>
#include <stdio.h>
#include <string.h>
int main(int argc, char **argv) {
    OSVERSIONINFOA info;
    HMODULE module;
    int wine, want98, match98;
    memset(&info, 0, sizeof(info));
    info.dwOSVersionInfoSize = sizeof(info);
    if (!GetVersionExA(&info)) {
        fprintf(stderr, "Could not identify the reported Windows API version.\n");
        return 3;
    }
    module = GetModuleHandleA("ntdll.dll");
    wine = module && GetProcAddress(module, "wine_get_version") != NULL;
    want98 = argc > 1 && strcmp(argv[1], "--require-win98se") == 0;
    match98 = info.dwPlatformId == VER_PLATFORM_WIN32_WINDOWS &&
              info.dwMajorVersion == 4 && info.dwMinorVersion == 10 &&
              (info.dwBuildNumber & 0xffffUL) == 2222;
    printf("{\"wine\":%s,\"reported_api_major\":%lu,\"reported_api_minor\":%lu,\"reported_build\":%lu,\"platform_id\":%lu,\"matches_win98se\":%s}\n",
           wine ? "true" : "false", (unsigned long)info.dwMajorVersion,
           (unsigned long)info.dwMinorVersion,
           (unsigned long)(info.dwBuildNumber & 0xffffUL),
           (unsigned long)info.dwPlatformId, match98 ? "true" : "false");
    if (wine) {
        fprintf(stderr, "Wine detected: this is NOT native Windows acceptance.\n");
        return 2;
    }
    if (want98 && !match98) {
        fprintf(stderr, "This is not the required Windows 98 SE 4.10.2222 target.\n");
        return 2;
    }
    return 0;
}
