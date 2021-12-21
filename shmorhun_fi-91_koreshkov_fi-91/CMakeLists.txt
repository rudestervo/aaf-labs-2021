cmake_minimum_required(VERSION 3.10)


# set the project name
project(aalab)

# add the executable

add_executable(aalab src/main.cpp "src/Set.h" "src/Set.cpp" "src/Parser.h" "src/Collection.h" "src/Collection.cpp" "src/Request.h"  "src/UI.h")

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)
