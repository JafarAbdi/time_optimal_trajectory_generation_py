import time_optimal_trajectory_generation_py as totg
import numpy as np

np.set_printoptions(formatter={"float_kind": "{:7.4f}".format})

waypoints = np.asarray(
    [
        [0.0, 0.0, 0.0],
        [0.0, 0.2, 1.0],
        [0.0, 3.0, 0.5],
        [1.1, 2.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
    ]
)

max_acceleration = np.asarray([1.0, 1.0, 1.0])
max_velocity = np.asarray([1.0, 1.0, 1.0])

trajectory = totg.Trajectory(totg.Path(waypoints, 0.1), max_velocity, max_acceleration)
# For debugging purposes
# trajectory.outputPhasePlaneTrajectory()
if trajectory.isValid():
    duration = trajectory.getDuration()
    print(f"Trajectory duration: {duration}s")
    dt = 0.1
    for t in np.arange(0.0, duration, dt):
        print(
            f"Time: {t:6.4f} - Position: {trajectory.getPosition(t)} - Velocity: {trajectory.getVelocity(t)}"
        )
    print(
        f"Time: {duration:6.4f} - Position: {trajectory.getPosition(duration)} - Velocity: {trajectory.getVelocity(duration)}"
    )
else:
    print("Trajectory generation failed")
