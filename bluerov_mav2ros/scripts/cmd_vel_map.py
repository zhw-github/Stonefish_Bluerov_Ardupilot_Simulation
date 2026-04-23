#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16MultiArray
import numpy as np

class CmdVelMapper(Node):
    def __init__(self):
        super().__init__('cmd_vel_mapper')
        
        # Inicializa el publisher para el tópico de canales RC
        self.publisher_ = self.create_publisher(UInt16MultiArray, '/bluerov/set_rc_channels', 1)
        
        # Suscriptor para el tópico de velocidad
        self.subscription = self.create_subscription(Twist, '/bluerov/cmd_vel', self.cmd_vel_callback, 1)
        
        # Tabla de velocidades PWM
        self.velocities = self.generate_pwm_table()
        self.get_logger().info("CmdVelMapper node initialized")

    def generate_pwm_table(self):
        # Genera la tabla de velocidades PWM
        a, b, c, d, e, f, g, h, i, j, k = [1.3871668161975536e-25, -2.080750463000313e-21, 1.3983334487807407e-17, 
                                            -5.543948233018681e-14, 1.4359451930265564e-10, -2.5387836010458446e-07, 
                                            0.0003102899349247361, -0.25886076958834003, 141.07497402237286, 
                                            -45353.82880615414, 6531725.54047377]
        coefficients = np.array([a, b, c, d, e, f, g, h, i, j, k])
        x = np.linspace(1100, 1900, 801)
        y = np.polyval(coefficients, x)
        velocities = np.zeros(801)
        z = 0
        for i in range(len(x)):
            if z < 400:
                velocities[z] = -y[i]
            else:
                velocities[z] = y[i]
            z += 1
        return velocities

    def map_velocity_to_pwm(self, velocity):
        # Mapea la velocidad a PWM basado en la tabla generada
        diff = np.abs(self.velocities - velocity)
        pwm_value = np.argmin(diff) + 1100
        return pwm_value

    def cmd_vel_callback(self, msg):
        # Inicializa el mensaje de UInt16MultiArray para los canales
        channels_msg = UInt16MultiArray()
        channels_msg.data = [1500] * 8  # Valores PWM iniciales

        # Mapeo de velocidades lineales y angulares a PWM
        if -1.0 <= msg.linear.x <= 1.0 and msg.linear.x != 0.0:
            channels_msg.data[4] = self.map_velocity_to_pwm(msg.linear.x)
        if -1.0 <= msg.linear.y <= 1.0 and msg.linear.y != 0.0:
            channels_msg.data[5] = self.map_velocity_to_pwm(msg.linear.y)
        if -1.0 <= msg.linear.z <= 1.0 and msg.linear.z != 0.0:
            channels_msg.data[2] = self.map_velocity_to_pwm(msg.linear.z)
        if -1.0 <= msg.angular.z <= 1.0 and msg.angular.z != 0.0:
            channels_msg.data[3] = self.map_velocity_to_pwm(msg.angular.z)
        if -1.0 <= msg.angular.y <= 1.0 and msg.angular.y != 0.0:
            channels_msg.data[0] = self.map_velocity_to_pwm(msg.angular.y)
        if -1.0 <= msg.angular.x <= 1.0 and msg.angular.x != 0.0:
            channels_msg.data[1] = self.map_velocity_to_pwm(msg.angular.x)

        # Publica los canales mapeados
        self.publisher_.publish(channels_msg)
        self.get_logger().info(f'Published PWM values: {channels_msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelMapper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
