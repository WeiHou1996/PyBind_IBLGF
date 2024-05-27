cmake_minimum_required(VERSION 3.22)
if(EXISTS "${CMAKE_CURRENT_LIST_DIR}/CMakeLists.txt.user")
    include(${CMAKE_CURRENT_LIST_DIR}/CMakeLists.txt.user)
else()
endif()
project(Python_Hypergeom VERSION 0.0.0)

cmake_policy(SET CMP0048 NEW)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_FLAGS "-march=native -Wno-error=deprecated-declarations")

set(default_build_type "Release")
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    message(STATUS "Setting build type to '${default_build_type}' as none was specified.")
    set(CMAKE_BUILD_TYPE "${default_build_type}" CACHE STRING "Choose the type of build." FORCE)
    # Set the possible values of build type for cmake-gui
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

if(${CMAKE_CXX_COMPILER_ID} STREQUAL "Intel")
    #set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3  -fmax-errors=4 ")
    #set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -ipo -O3 -static-intel -Wall -fmax-errors=4")
else()
    message("Using compiler of family: " ${CMAKE_CXX_COMPILER_ID})
endif()

list(APPEND CMAKE_PREFIX_PATH {CONDA_PREFIX})

find_package(Boost)
find_package(pybind11)
#include_directories($ENV{Boost_INCLUDE_DIRS})
include_directories(${Boost_INCLUDE_DIRS})

pybind11_add_module(cpp_funcs cpp_funcs.cpp)
target_link_libraries(cpp_funcs INTERFACE Boost::boost)
target_link_libraries(cpp_funcs INTERFACE Boost::math)