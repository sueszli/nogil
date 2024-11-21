#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <stdbool.h>
#include <stdlib.h>
#include <assert.h>
#include <Python.h>

#define MAX_LENGTH 8

char* hashcat(const char *target_hash) {
    const char alphabet[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    const int alphabet_size = 62;

    char *current = malloc(MAX_LENGTH + 1);
    if (!current) {
        return NULL;
    }

    int position[MAX_LENGTH] = {0};
    for (int length = 1; length <= MAX_LENGTH; length++) {
        while (true) {
            for (int i = 0; i < length; i++) {
                current[i] = alphabet[position[i]];
            }
            current[length] = '\0';

            char hashed[SHA_DIGEST_LENGTH * 2 + 1];
            unsigned char hash[SHA_DIGEST_LENGTH];
            SHA_CTX ctx;
            SHA1_Init(&ctx);
            SHA1_Update(&ctx, current, strlen(current));
            SHA1_Final(hash, &ctx);
            
            for(int i = 0; i < SHA_DIGEST_LENGTH; i++) {
                sprintf(hashed + (i * 2), "%02x", hash[i]);
            }
            hashed[SHA_DIGEST_LENGTH * 2] = '\0';
            if (strcmp(hashed, target_hash) == 0) {
                return current;
            }

            int idx = 0;
            while (idx < length) {
                position[idx]++;
                if (position[idx] < alphabet_size) {
                    break;
                }
                position[idx] = 0;
                idx++;
            }

            if (idx == length) {
                break;
            }
        }
    }

    free(current);
    return NULL;
}

static PyObject* hashcatmodule_hashcat(PyObject* self, PyObject* args) {
    const char *target_hash;
    char *result;
    PyObject *return_value;

    if (!PyArg_ParseTuple(args, "s", &target_hash)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    result = hashcat(target_hash);
    Py_END_ALLOW_THREADS

    if (result == NULL) {
        PyErr_SetString(PyExc_RuntimeError, "hash cracking failed");
        return NULL;
    }

    return_value = Py_BuildValue("s", result);
    free(result);
    return return_value;
}

static PyMethodDef hashcat_methods[] = {
    {"hashcat", hashcatmodule_hashcat, METH_VARARGS, "crack a hash using hashcat"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef hashcatmodule = {
    PyModuleDef_HEAD_INIT,
    "hashcatmodule",
    "python interface for hashcat hash cracking",
    -1,
    hashcat_methods
};

PyMODINIT_FUNC PyInit_hashcatmodule(void) {
    return PyModule_Create(&hashcatmodule);
}
