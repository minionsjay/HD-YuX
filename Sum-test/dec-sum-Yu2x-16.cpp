#include <NTL/GF2E.h>
#include <NTL/GF2X.h>
#include <cstdio>
#include <iostream>
#include <vector>
#include "../Yux/Yu2x-16.h"
using namespace std;
using namespace NTL;


GF2E gf2e_from_bytes(unsigned char hi, unsigned char lo) {
    unsigned char b[2] = {hi, lo};
    return conv<GF2E>(GF2XFromBytes(b, 2));
}

int main() {

    int ROUND, input_index, output_index, max_val;
    cout << "input test round (i.e. 12): ";
    cin >> ROUND;

    int input_count;
    cout << "Enter number of input positions to vary: ";
    cin >> input_count;

    vector<int> input_indices(input_count);
    vector<int> val_limits(input_count);
    for (int i = 0; i < input_count; ++i) {
        cout << "Enter input index " << i << ": ";
        cin >> input_indices[i];
        cout << "Enter max val (exclusive) for input index " << i << ": ";
        cin >> val_limits[i];
    }



    // const int ROUND = 2;
    const int BLOCK_BITS = 256;
    const int BLOCK_BYTES = BLOCK_BITS / 8;
    const int Nk = BLOCK_BYTES / 2;


    uint8_t polyBytes16[] = {0x0B, 0x10, 0x01}; // x^16 + x^12 + x^3 + x + 1
    GF2X poly = GF2XFromBytes(polyBytes16, 3);
    GF2E::init(poly);


    // unsigned char Key[32];
    // for (int i = 0; i < 32; i++) Key[i] = i;
    unsigned char Key[32] = {
        0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,
        0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F,
        0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,
        0x08,0x09,0x0A,0x0B,0x0C,0x0D,0x0E,0x0F
    };


    unsigned char RoundKeyCh[BLOCK_BYTES * (ROUND + 1)];
    Yu2x_16_KeyExpansion(RoundKeyCh, ROUND, BLOCK_BYTES, Key);

    Vec<GF2E> RoundKey;
    RoundKey.SetLength(Nk * (ROUND + 1));
    for (int i = 0; i < Nk * (ROUND + 1); i++) {
        unsigned char tmp[2] = {RoundKeyCh[2 * i], RoundKeyCh[2 * i + 1]};
        RoundKey[i] = conv<GF2E>(GF2XFromBytes(tmp, 2));
    }


    Vec<GF2E> RoundKey_invert;
    RoundKey_invert.SetLength(Nk * (ROUND + 1));
    Yu2x_16_decRoundKey(RoundKey_invert, RoundKey, ROUND, Nk);


    GF2E sums[16];
    for (int i = 0; i < 16; ++i) sums[i] = GF2E::zero();

    vector<int> vals(input_count, 0);
    bool done = false;

    while (!done) {
        unsigned char ciphertext[32] = {};
        for (int i = 0; i < input_count; ++i) {
            int idx = input_indices[i];
            ciphertext[2 * idx] = (vals[i] >> 8) & 0xFF;
            ciphertext[2 * idx + 1] = vals[i] & 0xFF;
        }

        unsigned char plaintext[32];
        Yu2x_16_decryption(plaintext, ciphertext, RoundKey_invert, ROUND);

        for (int word_idx = 0; word_idx < Nk; ++word_idx) {
            int pos = word_idx * 2;
            // unsigned short word = (plaintext[pos] << 8) | plaintext[pos + 1];
            GF2E word = gf2e_from_bytes(plaintext[pos], plaintext[pos + 1]);
            sums[word_idx] += word;
        }


        for (int i = input_count - 1; i >= 0; --i) {
            vals[i]++;
            if (vals[i] < val_limits[i]) break;
            if (i == 0) done = true;
            vals[i] = 0;
        }
    }

    cout << "\n==== Decrypted Word Sums ====\n";
    for (int i = 0; i < Nk; ++i) {
        unsigned char sum_bytes[2];
        BytesFromGF2X(sum_bytes, rep(sums[i]), 2);
        cout << "Word[" << i << "] = ";
        printf("\ndecrypt sum  GF(2^16): [%02X %02X]\n", sum_bytes[0], sum_bytes[1]);

    }


    return 0;
}
