// add.cpp (C++ 代码)
// sudo apt install python3-pybind11
// g++ -O3 -Wall -shared -std=c++11 -fPIC     -I/usr/include/python3.12     -I/usr/lib/python3/dist-packages/pybind11/include     cpp_to_python.cpp     -o cpp_to_python$(python3-config --extension-suffix)
#include <pybind11/pybind11.h>

int add(int i, int j) {
    return i + j;
}

// 使用 pybind11 暴露给 Python
PYBIND11_MODULE(cpp_to_python, m) {
    m.doc() = "pybind11 cpp_to_python plugin"; // 模块文档
    m.def("add", &add, "A function which adds two numbers",
          pybind11::arg("i"), pybind11::arg("j"));
}