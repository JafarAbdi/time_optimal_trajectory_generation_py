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

add_library(
  time_optimal_trajectory_generation SHARED
  ${trajectories_SOURCE_DIR}/Path.cpp ${trajectories_SOURCE_DIR}/Trajectory.cpp
)
target_compile_features(time_optimal_trajectory_generation PRIVATE cxx_std_20)
target_include_directories(
  time_optimal_trajectory_generation PUBLIC ${trajectories_SOURCE_DIR}
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
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
