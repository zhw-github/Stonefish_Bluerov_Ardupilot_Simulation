# Bluerov Mav2ros
## Description
Bridge between MAVlink to ROS2 adapted from https://github.com/bvibhav/bluerov2_interface/tree/master and originally adapted from https://github.com/patrickelectric/bluerov_ros_playground. 

## Requirements
- ROS2 Humble or similar (not tested)
- Pymavlink

## Instalation
Clone the proyect in your workspace/src
```
git clone https://gitlab.com/slopezb/bluerov_mav2ros.git
cd ..
colcon build --event-handlers console_direct+ --cmake-args --symlink-install --packages-select bluerov_mav2ros
source install/setup.bash
ros2 launch bluerov_mav2ros bluerov_mav2ros_launch.py
```
## Usage
This bridge was adapted for stonfish simulator CIRTESU package and real deployment of the bluerov2 at CIRTESU.
Other packages can be found in:
- [Cirtesu Stonefish](https://gitlab.com/slopezb/cirtesu_stonefish.git)
- [Bluerov2 Cirtesu Core](https://gitlab.com/slopezb/bluerov2_cirtesu_core.git)

### Arming the robot
`$ros2 service call /bluerov/arm std_srvs/srv/SetBool data:\ true\ `

### Select the flight mode
`$ros2 service call /bluerov/setmode bluerov_mav2ros/srv/SetMode "{data: 'manual'}`

Posible modes:
- manual
- stabilize
- alt_hold
- poshold
- circle
- guided

### Send rc_channels
`$ros2 topic pub -r 1 /bluerov/set_rc_channels std_msgs/msg/UInt16MultiArray "{layout: {dim: [], data_offset: 0}, data: [1300, 1500, 1500, 1500, 1500, 1500, 1500, 1500]}"`

Important to enable MAVlink fordwarding at the host name: localhost:14445 (qground -> application setings -> MAVlink ->Ground station)
### Moving the robot
The bluerov/set_rc_channels works like the joystick, input is from 1100 to 1900
- channel1 -> pitch    1100 (down) 
- channel2 -> roll     1100 (left)
- channel3 -> z axis   1100 (down)
- channel4 -> yaw axis 1100 (left turn)
- channel5 -> x axis   1100 (back)
- channel6 -> y axis   1100 (left)
- channel7 -> Fix      1500
- channel8 -> Fix      1500
## Authors and acknowledgment
Thanks to the previous versions of this bridge mentioned in the description.

## License
CIRTESU licence

## Topics
It can be added more topics or services in the future
###subscribers
- /bluerov/rc_channels
read the topic and send the array using pymavlink to the SITL or robot
### services
- /bluerov/arm
- /bluerov/setmode

