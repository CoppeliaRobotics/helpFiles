cmake_minimum_required(VERSION 3.12)
project(helpFiles)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

if(NOT COPPELIASIM_INCLUDE_DIR)
    if(DEFINED ENV{COPPELIASIM_ROOT_DIR})
        set(COPPELIASIM_INCLUDE_DIR $ENV{COPPELIASIM_ROOT_DIR}/programming/include)
    else()
        set(COPPELIASIM_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../include)
    endif()
endif()
list(APPEND CMAKE_MODULE_PATH ${COPPELIASIM_INCLUDE_DIR}/cmake)
find_package(CoppeliaSim 4.5.0.7 REQUIRED)

add_custom_target(genRegularApi ALL
    COMMAND ${Python3_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/genRegularApi.py
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/en/regularApi_deprecated ${CMAKE_CURRENT_SOURCE_DIR}/en/regularApi
)

file(GLOB HELP_FILES CONFIGURE_DEPENDS *.html *.lua *.class *.css *.txt)
list(FILTER HELP_FILES EXCLUDE REGEX "/CMakeLists\\.txt$")
foreach(HELP_FILE IN LISTS HELP_FILES)
    coppeliasim_add_helpfile(${HELP_FILE} SUBDIR .)
endforeach()
coppeliasim_add_helpfile_directory(en)
coppeliasim_add_helpfile_directory(index)
coppeliasim_add_helpfile_directory(wb_img)
coppeliasim_add_helpfile_directory(js)
