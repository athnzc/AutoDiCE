#----------------------------------------------------------------
# Generated CMake target import file for configuration "release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ncnn_cuda_lib" for configuration "release"
set_property(TARGET ncnn_cuda_lib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(ncnn_cuda_lib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libncnn_cuda_lib.so"
  IMPORTED_SONAME_RELEASE "libncnn_cuda_lib.so"
  )

list(APPEND _cmake_import_check_targets ncnn_cuda_lib )
list(APPEND _cmake_import_check_files_for_ncnn_cuda_lib "${_IMPORT_PREFIX}/lib/libncnn_cuda_lib.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
