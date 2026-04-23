#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16MultiArray
from std_srvs.srv import SetBool
from sensor_msgs.msg import FluidPressure 
from bluerov_mav2ros.srv import SetMode
from include.bridge import Bridge

class Bluerov2(Node, Bridge):
    def __init__(self):
        Node.__init__(self, node_name="bluerov2_mav2ros", namespace="bluerov")
        Bridge.__init__(self, device="udp:127.0.0.1:14445", baudrate=115200)

        # Suscripción al tópico set_pwm
        self.create_subscription(UInt16MultiArray, "set_rc_channels", self._pwm_callback, 1)

        self.create_subscription(
            FluidPressure, 
            "/bluerov2/pressure", 
            self._pressure_callback, 
            10
        )

        # Creación de servicios
        self.create_service(SetBool, "arm", self._service_arm)
        self.create_service(SetMode, "setmode", self._service_setmode)

    def _pwm_callback(self, msg):
        # Aquí enviarías los valores de PWM a Mavlink
        print("PWM data received:", msg.data)
        # Ejemplo de código para enviar el mensaje a Mavlink:
        self.set_rc_channels_pwm(list(msg.data))

    def _pressure_callback(self, msg):
        press_abs_hpa = msg.fluid_pressure / 100.0
        time_boot_ms = msg.header.stamp.sec * 1000 + msg.header.stamp.nanosec // 1000000
        self.set_pressure_scaled(time_boot_ms, press_abs_hpa)
        
    def _service_arm(self, request, response):
        # Código para el servicio de armado
        if request.data:
            self.arm_throttle(True)
            response.success = True
            response.message = "Armed"
        else:
            self.arm_throttle(False)
            response.success = True
            response.message = "Disarmed"
        return response

    def _service_setmode(self, request, response):
        # Código para el servicio de modo
        self.set_mode(request.data)
        response.success = True
        return response

def main(args=None):
    rclpy.init(args=args)
    bluerov = Bluerov2()

    try:
        rclpy.spin(bluerov)
    except KeyboardInterrupt:
        pass
    finally:
        bluerov.arm_throttle(False)  # Desarmar motores al finalizar
        bluerov.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

