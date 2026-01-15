#include <iostream>
#include <fstream>
#include <string>
#include <windows.h>
#include <winhttp.h>

#pragma comment(lib, "winhttp.lib")

void createFile() {
    std::string filename;
    std::cout << "Enter filename to create: ";
    std::getline(std::cin, filename);

    std::ofstream file(filename);
    if (file.is_open()) {
        file << "This file was created by the program.\n";
        file.close();
        std::cout << "File '" << filename << "' created successfully.\n";
    }
    else {
        std::cout << "Failed to create file.\n";
    }
}

void createRegistryRecord() {
    HKEY hKey;
    const char* subkey = "SOFTWARE\\MyTestApp";
    LONG result = RegCreateKeyExA(HKEY_CURRENT_USER, subkey, 0, NULL,
        REG_OPTION_NON_VOLATILE, KEY_WRITE, NULL, &hKey, NULL);
    if (result == ERROR_SUCCESS) {
        const char* data = "Test Data";
        result = RegSetValueExA(hKey, "TestValue", 0, REG_SZ,
            reinterpret_cast<const BYTE*>(data), (DWORD)strlen(data) + 1);
        RegCloseKey(hKey);

        if (result == ERROR_SUCCESS) {
            std::cout << "Registry record created successfully.\n";
        }
        else {
            std::cout << "Error creating registry record.\n";
        }
    }
    else {
        std::cout << "Error creating registry key.\n";
    }
}

void requestUrl() {
    std::wstring urlW;
    std::wcout << L"Enter URL (e.g. https://example.com): ";
    std::getline(std::wcin, urlW);

    URL_COMPONENTS urlComp;
    ZeroMemory(&urlComp, sizeof(urlComp));
    urlComp.dwStructSize = sizeof(urlComp);

    wchar_t hostName[256];
    wchar_t urlPath[1024];
    urlComp.lpszHostName = hostName;
    urlComp.dwHostNameLength = sizeof(hostName) / sizeof(wchar_t);
    urlComp.lpszUrlPath = urlPath;
    urlComp.dwUrlPathLength = sizeof(urlPath) / sizeof(wchar_t);

    if (!WinHttpCrackUrl(urlW.c_str(), 0, 0, &urlComp)) {
        std::wcout << L"Failed to parse URL\n";
        return;
    }

    HINTERNET hSession = WinHttpOpen(L"MyUserAgent/1.0",
        WINHTTP_ACCESS_TYPE_DEFAULT_PROXY,
        WINHTTP_NO_PROXY_NAME,
        WINHTTP_NO_PROXY_BYPASS, 0);

    if (!hSession) {
        std::wcout << L"WinHttpOpen failed\n";
        return;
    }

    HINTERNET hConnect = WinHttpConnect(hSession, urlComp.lpszHostName, urlComp.nPort, 0);
    if (!hConnect) {
        std::wcout << L"WinHttpConnect failed\n";
        WinHttpCloseHandle(hSession);
        return;
    }

    DWORD flags = (urlComp.nScheme == INTERNET_SCHEME_HTTPS) ? WINHTTP_FLAG_SECURE : 0;

    HINTERNET hRequest = WinHttpOpenRequest(hConnect, L"GET", urlComp.lpszUrlPath,
        NULL, WINHTTP_NO_REFERER,
        WINHTTP_DEFAULT_ACCEPT_TYPES,
        flags);

    if (!hRequest) {
        std::wcout << L"WinHttpOpenRequest failed\n";
        WinHttpCloseHandle(hConnect);
        WinHttpCloseHandle(hSession);
        return;
    }

    BOOL bResults = WinHttpSendRequest(hRequest,
        WINHTTP_NO_ADDITIONAL_HEADERS,
        0, WINHTTP_NO_REQUEST_DATA, 0,
        0, 0);

    if (bResults)
        bResults = WinHttpReceiveResponse(hRequest, NULL);
    else
        std::wcout << L"Failed to send request\n";

    if (bResults) {
        DWORD dwSize = 0;
        do {
            DWORD dwDownloaded = 0;
            if (!WinHttpQueryDataAvailable(hRequest, &dwSize)) {
                std::wcout << L"Error querying data size\n";
                break;
            }
            if (dwSize == 0) break;

            char* buffer = new char[dwSize + 1];
            ZeroMemory(buffer, dwSize + 1);

            if (!WinHttpReadData(hRequest, (LPVOID)buffer, dwSize, &dwDownloaded)) {
                std::wcout << L"Error reading data\n";
                delete[] buffer;
                break;
            }
            std::cout.write(buffer, dwDownloaded);
            delete[] buffer;
        } while (dwSize > 0);
    }
    else {
        std::wcout << L"Failed to receive response\n";
    }

    WinHttpCloseHandle(hRequest);
    WinHttpCloseHandle(hConnect);
    WinHttpCloseHandle(hSession);

    std::cout << "\n"; // Перевод строки после вывода ответа
}

int main() {
    // Переключаем поток ввода-вывода в режим Unicode
    SetConsoleOutputCP(CP_UTF8);
    SetConsoleCP(CP_UTF8);

    while (true) {
        std::cout << "\nChoose an action:\n"
            << "1 - Create file\n"
            << "2 - Create Windows registry record\n"
            << "3 - Enter URL and send HTTP GET request\n"
            << "0 - Exit\n"
            << "Your choice: ";

        std::string choice;
        std::getline(std::cin, choice);

        if (choice == "1") {
            createFile();
        }
        else if (choice == "2") {
            createRegistryRecord();
        }
        else if (choice == "3") {
            requestUrl();
        }
        else if (choice == "0") {
            break;
        }
        else {
            std::cout << "Invalid choice, try again.\n";
        }
    }

    std::cout << "Program finished.\n";
    return 0;
}
