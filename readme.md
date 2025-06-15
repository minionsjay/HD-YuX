# YuX Cryptanalysis

This repository contains code for testing and analyzing the YuX cipher's algebraic degree, high-order differential distinguishers, and key recovery attacks.

## Directory Structure

1. **`Sum-test`**: This directory contains the code for testing the zero-sum property of the YuX cipher. It performs tests on the YuX cipher for different configurations and evaluates the zero-sum property, which is crucial for constructing higher-order differential distinguishers.

2. **`GMP-Yu2X`**: This folder includes the code for the generalized monomial prediction technique (GMP) to search the algebraic degree upper bounds for Yu2X. The code applies this technique to evaluate the algebraic degree of the Yu2X cipher over different rounds, providing a deeper understanding of its algebraic structure.

## How to Use

### 1. **Testing Zero-Sum Property in YuX**

The `Sum-test` folder contains scripts to test the zero-sum property for YuX. To run the tests:

* Navigate to the `Sum-test` directory.
* Execute the script to test various configurations of the YuX cipher.

```bash
cd Sum-test
./dec-sum-Yu2x-16
```
```
input round (i.e., 12): 3
Enter number of input positions to vary: 9
Enter input index 0: 0
Enter max val (exclusive) for input index 0: 4
Enter input index 1: 1
Enter max val (exclusive) for input index 1: 8
Enter input index 2: 2
Enter max val (exclusive) for input index 2: 8
Enter input index 3: 3
Enter max val (exclusive) for input index 3: 4
Enter input index 4: 4
Enter max val (exclusive) for input index 4: 4
Enter input index 5: 8
Enter max val (exclusive) for input index 5: 4
Enter input index 6: 9
Enter max val (exclusive) for input index 6: 4
Enter input index 7: 12
Enter max val (exclusive) for input index 7: 4
Enter input index 8: 13
Enter max val (exclusive) for input index 8: 4
```
```
==== Decrypted Word Sums ====
Word[0] =
decrypt sum GF(2^16): [00 00]
Word[1] =
decrypt sum GF(2^16): [00 00]
Word[2] =
decrypt sum GF(2^16): [00 00]
Word[3] =
decrypt sum GF(2^16): [00 00]
Word[4] =
decrypt sum GF(2^16): [00 00]
Word[5] =
decrypt sum GF(2^16): [00 00]
Word[6] =
decrypt sum GF(2^16): [00 00]
Word[7] =
decrypt sum GF(2^16): [00 00]
Word[8] =
decrypt sum GF(2^16): [00 00]
Word[9] =
解密总和 GF(2^16): [00 00]
Word[10] =
decrypt sum GF(2^16): [00 00]
Word[11] =
decrypt sum GF(2^16): [00 00]
Word[12] =
decrypt sum GF(2^16): [00 00]
Word[13] =
decrypt sum GF(2^16): [00 00]
Word[14] =
decrypt sum GF(2^16): [00 00]
Word[15] =
decrypt sum GF(2^16): [00 00]
```
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This `README` provides a basic overview of how to navigate the repository and use the code in both directories. You can modify it further based on the exact files and setup you have.
