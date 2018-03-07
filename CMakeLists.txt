cmake_minimum_required(VERSION 3.5)
project(conan_uvlinkt)

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_library(uv_link_t STATIC
    ./src/defaults.c
    ./src/uv_link_observer_t.c
    ./src/uv_link_source_t.c
    ./src/uv_link_t.c
)

target_include_directories(uv_link_t PUBLIC ./include)
target_include_directories(uv_link_t PRIVATE .)
target_link_libraries(uv_link_t PUBLIC CONAN_PKG::libuv)
