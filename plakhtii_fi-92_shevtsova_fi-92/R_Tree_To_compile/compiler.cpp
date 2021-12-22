#include "R_Tree/R_Tree.h"
#include "R_Tree/Rect.h"
#include <pybind11/pybind11.h>


namespace py = pybind11;

PYBIND11_MODULE(R_Tree, m) {
py::class_<Rect>(m, "Rect")
.def(py::init<float,float,float,float>(), py::arg("ltx"),py::arg("lty"),py::arg("rbx"),py::arg("rby"))
.def("get_ltx", &Rect::get_ltx, "get ltx")
.def("get_lty", &Rect::get_lty, "get lty")
.def("get_rbx", &Rect::get_rbx, "get rbx")
.def("get_rby", &Rect::get_rby, "get rby")
.def("__repr__", &Rect::to_string);

py::class_<R_Tree>(m, "R_Tree")
.def(py::init<>())
.def("insert", &R_Tree::incert, "insert Rect into tree", py::arg("Rect"))
.def("search", &R_Tree::search , "search elements in rect", py::arg("Rect"))
.def("to_string", &R_Tree::to_string, "tree to string")
.def("print_tree", &R_Tree::print_tree, "print tree")
.def("get_root", &R_Tree::get_root, "get_root")
.def("nn", &R_Tree::nn, "get nn", py::arg("Rect"))
.def("is_contain", &R_Tree::is_contain, "is contain rect", py::arg("Rect"));
}
