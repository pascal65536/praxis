#include <iostream>
#include <string>
#include <windows.h>
#include <openssl/evp.h>
#include <sstream>
#include <iomanip>
#include <conio.h>

std::string GetCurrentUserName() {
    char username[257];
    DWORD size = sizeof(username);
    if (GetUserNameA(username, &size))
        return std::string(username);
    return "";
}

std::string Sha256(const std::string& input) {
    EVP_MD_CTX* context = EVP_MD_CTX_new();
    EVP_DigestInit_ex(context, EVP_sha256(), nullptr);
    EVP_DigestUpdate(context, input.data(), input.size());

    unsigned char hash[EVP_MAX_MD_SIZE];
    unsigned int lengthOfHash = 0;
    EVP_DigestFinal_ex(context, hash, &lengthOfHash);
    EVP_MD_CTX_free(context);

    std::stringstream ss;
    for (unsigned int i = 0; i < lengthOfHash; i++) {
        ss << std::hex << std::setw(2) << std::setfill('0') << (int)hash[i];
    }
    return ss.str();
}

std::string GeneratePassword(const std::string& input) {
    static const char Alphabet[] =
        "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\\()*+,-./:;<=>?@[\\]^_`{|}~ ";
    std::string hashHex = Sha256(input);
    std::string password;
    for (int i = 0; i < 16; ++i) {
        std::string byteStr = hashHex.substr(i * 2, 2);
        unsigned int byteVal = std::stoul(byteStr, nullptr, 16);
        char c = Alphabet[byteVal % (sizeof(Alphabet) - 1)];
        password += c;
    }
    return password;
}

int main() {
    std::string userName = GetCurrentUserName();
    std::cout << "Enter your phrase: ";
    std::string phrase;
    std::getline(std::cin, phrase);
    std::string input = userName + phrase;
    std::string password = GeneratePassword(input);
    std::cout << password << std::endl;
    std::cout << "Press any key for continue ...";
    _getch();
    return 0;
}
