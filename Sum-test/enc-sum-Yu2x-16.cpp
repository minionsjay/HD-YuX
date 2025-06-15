#include <NTL/GF2E.h>
#include <NTL/GF2X.h>
#include <cstdio>
#include <iostream>
#include "../Yux/Yu2x-16.h"
using namespace std;
using namespace NTL;

// extern "C" {
//     void Yu2x_16_KeyExpansion(unsigned char RoundKey[], long round, long blockByte, unsigned char Key[]);
//     void Yu2x_16_encryption(unsigned char* output, unsigned char* input, Vec<GF2E>& RoundKey, int ROUND);
// }


GF2E gf2e_from_bytes(unsigned char hi, unsigned char lo) {
    unsigned char bytes[2] = {hi, lo};
    return conv<GF2E>(GF2XFromBytes(bytes, 2));
}


int main() {
    const int ROUND = 1;
    const int BLOCK_BITS = 256;
    const int BLOCK_BYTES = BLOCK_BITS / 8; // 32 bytes
    const int Nk = BLOCK_BYTES / 2;         // 16 GF2E elements


    uint8_t polyBytes16[] = {0x0B, 0x10, 0x01}; 
    GF2X poly = GF2XFromBytes(polyBytes16, 3);
    GF2E::init(poly);


    unsigned char Key[32];
    for (int i = 0; i < 32; i++) Key[i] = i;


    unsigned char RoundKeyCh[BLOCK_BYTES * (ROUND + 1)];
    Yu2x_16_KeyExpansion(RoundKeyCh, ROUND, BLOCK_BYTES, Key);

    Vec<GF2E> RoundKey;
    RoundKey.SetLength(Nk * (ROUND + 1));
    for (int i = 0; i < Nk * (ROUND + 1); i++) {
        unsigned char tmp[2] = {RoundKeyCh[2 * i], RoundKeyCh[2 * i + 1]};
        RoundKey[i] = conv<GF2E>(GF2XFromBytes(tmp, 2));
    }


    GF2E sum;
    clear(sum); // sum = 0

    unsigned char input[32], output[32];


    for (int i = 1; i < 16; i++) {
        input[2 * i] = 0x00;
        input[2 * i + 1] = 0x01;
    }


    for (unsigned int val = 0; val < 4; val++) {
        input[0] = (val >> 8) & 0xFF;
        input[1] = val & 0xFF;
        // cout<<"input"<< input[0]<< endl;
        Yu2x_16_encryption(output, input, RoundKey, ROUND);
        // Yu2x_16_decryption(output, input, RoundKey, ROUND);

        GF2E out0 = gf2e_from_bytes(output[0], output[1]); 
        cout << out0 <<endl;
        sum += out0;

        if ((val & 0xFFF) == 0) {
            printf("Progress: %04X / FFFF\r", val);
            fflush(stdout);
        }
    }


    unsigned char sum_bytes[2];
    BytesFromGF2X(sum_bytes, rep(sum), 2);
    printf("\nsum = [%02X %02X]\n", sum_bytes[0], sum_bytes[1]);

    return 0;
}
