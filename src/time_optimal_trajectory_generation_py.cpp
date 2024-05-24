#include <Path.h>
#include <Trajectory.h>
#include <memory>
#include <pybind11/eigen.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

PYBIND11_MODULE(time_optimal_trajectory_generation_py, m) {
  py::class_<Path>(m, "Path")
      .def(py::init<std::list<Eigen::VectorXd>, double>())
      .def("getLength", &Path::getLength)
      .def("getConfig", &Path::getConfig)
      .def("getTangent", &Path::getTangent)
      .def("getCurvature", &Path::getCurvature)
      .def("getNextSwitchingPoint", &Path::getNextSwitchingPoint)
      .def("getSwitchingPoints", &Path::getSwitchingPoints);

  py::class_<Trajectory>(m, "Trajectory")
      .def(py::init<Path, Eigen::VectorXd, Eigen::VectorXd, double>(),
           py::arg("path"), py::arg("maxVelocity"), py::arg("maxAcceleration"),
           py::arg("timeStep") = 0.001)
      .def("isValid", &Trajectory::isValid)
      .def("getDuration", &Trajectory::getDuration)
      .def("getPosition", &Trajectory::getPosition)
      .def("getVelocity", &Trajectory::getVelocity)
      .def("outputPhasePlaneTrajectory",
           &Trajectory::outputPhasePlaneTrajectory);
}
