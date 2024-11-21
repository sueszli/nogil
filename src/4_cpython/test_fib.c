#include <Python.h>

// dependency: https://github.com/python/cpython/blob/main/Include/Python.h

int fib(int n) {
    return n < 2 ? n : fib(n - 2) + fib(n - 1);
}

// python wrapper: 
// 1. PyArg_ParseTuple: parse the input arguments as C types
// 2. Py_BEGIN_ALLOW_THREADS: release the GIL
// 3. Py_END_ALLOW_THREADS: reacquire the GIL
// 4. Py_BuildValue: convert to Python types
static PyObject* fibmodule_fib(PyObject* self, PyObject* args) {
    int n;
    int result;

    if (!PyArg_ParseTuple(args, "i", &n)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    result = fib(n);
    Py_END_ALLOW_THREADS

    return Py_BuildValue("i", result);
}

static PyMethodDef fib_methods[] = { // list of methods
    {"fib", fibmodule_fib, METH_VARARGS, "Calculate the nth Fibonacci"}, // function definition: name, function, flags, docstring
    {NULL, NULL, 0, NULL} // sentinel (end of list)
};

static struct PyModuleDef fibmodule = { // module definition : name, docstring, flag, methods
    PyModuleDef_HEAD_INIT,
    "fibmodule", 
    "Efficient Fibonacci number calculator",
    -1, 
    fib_methods
};

PyMODINIT_FUNC PyInit_fibmodule(void) { // module initialization
    return PyModule_Create(&fibmodule);
}
