cmake_minimum_required(VERSION 3.4...3.18)
project(R_Tree LANGUAGES CXX)

add_subdirectory(pybind11)
pybind11_add_module(R_Tree compiler.cpp R_Tree/R_Tree.cpp R_Tree/Rect.cpp)