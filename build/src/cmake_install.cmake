# Install script for directory: /home/gkorod/AutoDiCE/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/gkorod/AutoDiCE/build/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libncnn_cuda_lib.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libncnn_cuda_lib.so")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libncnn_cuda_lib.so"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE SHARED_LIBRARY FILES "/home/gkorod/AutoDiCE/build/src/libncnn_cuda_lib.so")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libncnn_cuda_lib.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libncnn_cuda_lib.so")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/libncnn_cuda_lib.so")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/gkorod/AutoDiCE/build/src/libncnn.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ncnn" TYPE FILE FILES
    "/home/gkorod/AutoDiCE/src/allocator.h"
    "/home/gkorod/AutoDiCE/src/benchmark.h"
    "/home/gkorod/AutoDiCE/src/blob.h"
    "/home/gkorod/AutoDiCE/src/c_api.h"
    "/home/gkorod/AutoDiCE/src/command.h"
    "/home/gkorod/AutoDiCE/src/cpu.h"
    "/home/gkorod/AutoDiCE/src/datareader.h"
    "/home/gkorod/AutoDiCE/src/gpu.h"
    "/home/gkorod/AutoDiCE/src/layer.h"
    "/home/gkorod/AutoDiCE/src/layer_shader_type.h"
    "/home/gkorod/AutoDiCE/src/layer_type.h"
    "/home/gkorod/AutoDiCE/src/mat.h"
    "/home/gkorod/AutoDiCE/src/modelbin.h"
    "/home/gkorod/AutoDiCE/src/net.h"
    "/home/gkorod/AutoDiCE/src/option.h"
    "/home/gkorod/AutoDiCE/src/paramdict.h"
    "/home/gkorod/AutoDiCE/src/pipeline.h"
    "/home/gkorod/AutoDiCE/src/pipelinecache.h"
    "/home/gkorod/AutoDiCE/src/simpleocv.h"
    "/home/gkorod/AutoDiCE/src/simpleomp.h"
    "/home/gkorod/AutoDiCE/src/simplestl.h"
    "/home/gkorod/AutoDiCE/src/vulkan_header_fix.h"
    "/home/gkorod/AutoDiCE/build/src/ncnn_export.h"
    "/home/gkorod/AutoDiCE/build/src/layer_shader_type_enum.h"
    "/home/gkorod/AutoDiCE/build/src/layer_type_enum.h"
    "/home/gkorod/AutoDiCE/build/src/platform.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/ncnn" TYPE FILE FILES "/home/gkorod/AutoDiCE/src/cuda_util.h")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn/ncnn_cuda_lib_targets.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn/ncnn_cuda_lib_targets.cmake"
         "/home/gkorod/AutoDiCE/build/src/CMakeFiles/Export/790e04ecad7490f293fc4a38f0c73eb1/ncnn_cuda_lib_targets.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn/ncnn_cuda_lib_targets-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn/ncnn_cuda_lib_targets.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn" TYPE FILE FILES "/home/gkorod/AutoDiCE/build/src/CMakeFiles/Export/790e04ecad7490f293fc4a38f0c73eb1/ncnn_cuda_lib_targets.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn" TYPE FILE FILES "/home/gkorod/AutoDiCE/build/src/CMakeFiles/Export/790e04ecad7490f293fc4a38f0c73eb1/ncnn_cuda_lib_targets-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn/ncnn.cmake")
    file(DIFFERENT _cmake_export_file_changed FILES
         "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn/ncnn.cmake"
         "/home/gkorod/AutoDiCE/build/src/CMakeFiles/Export/790e04ecad7490f293fc4a38f0c73eb1/ncnn.cmake")
    if(_cmake_export_file_changed)
      file(GLOB _cmake_old_config_files "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn/ncnn-*.cmake")
      if(_cmake_old_config_files)
        string(REPLACE ";" ", " _cmake_old_config_files_text "${_cmake_old_config_files}")
        message(STATUS "Old export file \"$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn/ncnn.cmake\" will be replaced.  Removing files [${_cmake_old_config_files_text}].")
        unset(_cmake_old_config_files_text)
        file(REMOVE ${_cmake_old_config_files})
      endif()
      unset(_cmake_old_config_files)
    endif()
    unset(_cmake_export_file_changed)
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn" TYPE FILE FILES "/home/gkorod/AutoDiCE/build/src/CMakeFiles/Export/790e04ecad7490f293fc4a38f0c73eb1/ncnn.cmake")
  if(CMAKE_INSTALL_CONFIG_NAME MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn" TYPE FILE FILES "/home/gkorod/AutoDiCE/build/src/CMakeFiles/Export/790e04ecad7490f293fc4a38f0c73eb1/ncnn-release.cmake")
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/cmake/ncnn" TYPE FILE FILES "/home/gkorod/AutoDiCE/build/src/ncnnConfig.cmake")
endif()

