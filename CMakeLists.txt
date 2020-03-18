cmake_minimum_required(VERSION 3.1)

project(SV_paper)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS 1 )

set(include_dirs "")
set(lib_dir "lib")

# Pybind11
add_subdirectory(${lib_dir}/pybind11)

# Boost
list(APPEND include_dirs ${lib_dir}/boost)

set(source_dir simulation}

set(source_files
    ${source_dir}/surface_process_brent.cpp
    )


include_directories(${source_dir} ${include_dirs})
