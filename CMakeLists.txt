cmake_minimum_required(VERSION 3.16)
project(time_optimal_trajectory_generation)

if(NOT "${CMAKE_CXX_STANDARD}")
  set(CMAKE_CXX_STANDARD 17)
endif()
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

include(FetchContent)
FetchContent_Declare(trajectories
  GIT_REPOSITORY https://github.com/tobiaskunz/trajectories.git
  GIT_TAG 8fd7a4b1c586e1e3d160dae16fced86db5ac7e2a
)
FetchContent_MakeAvailable(trajectories)

find_package(Python REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG)
find_package(Eigen3 REQUIRED)

add_library(time_optimal_trajectory_generation
  SHARED
  ${trajectories_SOURCE_DIR}/Path.cpp
  ${trajectories_SOURCE_DIR}/Trajectory.cpp
)

target_include_directories(time_optimal_trajectory_generation PUBLIC
  ${trajectories_SOURCE_DIR}
)

target_link_libraries(time_optimal_trajectory_generation PUBLIC Eigen3::Eigen)

add_executable(time_optimal_trajectory_generation_example ${trajectories_SOURCE_DIR}/Example.cpp)
target_link_libraries(time_optimal_trajectory_generation_example PRIVATE time_optimal_trajectory_generation)

pybind11_add_module(time_optimal_trajectory_generation_py src/time_optimal_trajectory_generation_py.cpp)
target_link_libraries(time_optimal_trajectory_generation_py PRIVATE time_optimal_trajectory_generation)
pybind11_extension(time_optimal_trajectory_generation_py)
pybind11_strip(time_optimal_trajectory_generation_py)

include(GNUInstallDirs)
# Determine the python installation directory
set(PYTHON_SITE_PACKAGES ${CMAKE_INSTALL_LIBDIR}/python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}/site-packages)
message(STATUS "Python site-packages directory: " ${PYTHON_SITE_PACKAGES})

install(TARGETS time_optimal_trajectory_generation_py
  LIBRARY DESTINATION ${PYTHON_SITE_PACKAGES}
)
install(TARGETS time_optimal_trajectory_generation
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
