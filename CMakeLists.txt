cmake_minimum_required(VERSION 2.8.11)
project(cmake_wrapper)

include(conanbuildinfo.cmake)
conan_basic_setup()

if (CONAN_COMPILE_DEFINITIONS_FLANN MATCHES "FLANN_STATIC")
    set(FLANN_USE_STATIC ON)
endif()

add_subdirectory(source_subfolder)
