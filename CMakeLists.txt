cmake_minimum_required(VERSION 3.16)
project(time_optimal_trajectory_generation)

include(FetchContent)
fetchcontent_declare(
  trajectories
  GIT_REPOSITORY https://github.com/tobiaskunz/trajectories.git
  GIT_TAG 8fd7a4b1c586e1e3d160dae16fced86db5ac7e2a
)
fetchcontent_makeavailable(trajectories)

find_package(Python REQUIRED COMPONENTS Interpreter Development)
find_package(Eigen3 REQUIRED)

# Get version from version.hpp
file(READ include/time_optimal_trajectory_generation/version.hpp version_hpp)
if(NOT version_hpp MATCHES
   "TIME_OPTIMAL_TRAJECTORY_GENERATION_VERSION ([0-9]+)([0-9][0-9])([0-9][0-9])"
)
  message(
    FATAL_ERROR
      "Cannot get TIME_OPTIMAL_TRAJECTORY_GENERATION_VERSION from version.hpp"
  )
endif()
# Use math to skip leading zeros if any.
math(EXPR CPACK_PACKAGE_VERSION_MAJOR ${CMAKE_MATCH_1})
math(EXPR CPACK_PACKAGE_VERSION_MINOR ${CMAKE_MATCH_2})
math(EXPR CPACK_PACKAGE_VERSION_PATCH ${CMAKE_MATCH_3})
# cmake-lint: disable=C0103
set(${PROJECT_NAME}_VERSION
    "${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH}"
)
message(STATUS "${PROJECT_NAME} version: ${${PROJECT_NAME}_VERSION}")

add_library(
  time_optimal_trajectory_generation SHARED
  ${trajectories_SOURCE_DIR}/Path.cpp ${trajectories_SOURCE_DIR}/Trajectory.cpp
)
target_compile_features(time_optimal_trajectory_generation PRIVATE cxx_std_20)
target_include_directories(
  time_optimal_trajectory_generation
  PUBLIC $<BUILD_INTERFACE:${trajectories_SOURCE_DIR}>
         $<INSTALL_INTERFACE:include>
)
set_target_properties(
  time_optimal_trajectory_generation
  PROPERTIES VERSION ${${PROJECT_NAME}_VERSION} SOVERSION
                                                ${CPACK_PACKAGE_VERSION_MAJOR}
)

target_link_libraries(time_optimal_trajectory_generation PUBLIC Eigen3::Eigen)

add_executable(
  time_optimal_trajectory_generation_example
  ${trajectories_SOURCE_DIR}/Example.cpp
)
target_link_libraries(
  time_optimal_trajectory_generation_example
  PRIVATE time_optimal_trajectory_generation
)

# Set PYBIND11_FINDPYTHON before finding pybind11
set(PYBIND11_FINDPYTHON ON)
add_subdirectory(pybind11)
pybind11_add_module(
  time_optimal_trajectory_generation_py # NO_EXTRAS
  src/time_optimal_trajectory_generation_py.cpp
)
target_link_libraries(
  time_optimal_trajectory_generation_py
  PRIVATE time_optimal_trajectory_generation
)
target_compile_features(
  time_optimal_trajectory_generation_py PRIVATE cxx_std_20
)

include(CMakePackageConfigHelpers)
# Generate the version, config and target files into the build directory.
write_basic_package_version_file(
  ${PROJECT_NAME}-config-version.cmake
  VERSION ${${PROJECT_NAME}_VERSION}
  COMPATIBILITY AnyNewerVersion
)
configure_package_config_file(
  ${CMAKE_CURRENT_SOURCE_DIR}/cmake/${PROJECT_NAME}-config.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
  INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)

include(GNUInstallDirs)
# Determine the python installation directory
set(PYTHON_SITE_PACKAGES
    ${CMAKE_INSTALL_LIBDIR}/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/site-packages
)
message(STATUS "Python site-packages directory: " ${PYTHON_SITE_PACKAGES})

install(TARGETS time_optimal_trajectory_generation_py
        LIBRARY DESTINATION ${PYTHON_SITE_PACKAGES}
)
install(
  TARGETS time_optimal_trajectory_generation
  COMPONENT time_optimal_trajectory_generation-core
  EXPORT ${PROJECT_NAME}-targets
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}
)

# Use a namespace because CMake provides better diagnostics for namespaced
# imported targets.
export(
  TARGETS time_optimal_trajectory_generation
  NAMESPACE ${PROJECT_NAME}::
  FILE ${PROJECT_NAME}-targets.cmake
)
install(FILES ${trajectories_SOURCE_DIR}/Path.h
              ${trajectories_SOURCE_DIR}/Trajectory.h
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/
)
# Install version, config and target files.
install(
  FILES ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
        ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
  COMPONENT ${PROJECT_NAME}-core
)
install(
  EXPORT ${PROJECT_NAME}-targets
  NAMESPACE ${PROJECT_NAME}::
  COMPONENT ${PROJECT_NAME}-core
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}
)
