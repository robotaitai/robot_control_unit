import actionlib
import rospy
from common.srv import ModeSelect
from common.msg import CalibrateAction, CalibrateGoal, RobotCommand
from std_msgs.msg import String
from sensor_msgs.msg import Joy

STEP_RATIO = 0.05

class RobotCommandParams:


    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.robot_commands_pub = rospy.Publisher("/robot_commands", RobotCommand, queue_size=10)


    def update_vals(self, val_x, val_y, val_w):
        self.x += val_x * STEP_RATIO
        self.y += val_y * STEP_RATIO
        self.w += val_w * STEP_RATIO

    def reset_vals(self):
        self.x = 0
        self.y = 0
        self.w = 0

    def publish_command(self):
        cmd = RobotCommand()
        cmd.x = self.x
        cmd.y = self.y
        cmd.w = self.w
        self.robot_commands_pub.publish(cmd)
        print(f"Published: x: {self.x}, y: {self.y}, w: {self.w}")

    def print_all(self):
        print(f"x: {self.x}, y: {self.y}, w: {self.w}")




class RobotControl:
    def __init__(self, cfg):
        rospy.init_node('robot_control_unit', anonymous=True)
        self.conf = cfg
        self.imu_handler_pub = rospy.Publisher("/imu/commander", String, queue_size=10)
        self.ser_motor_mode = rospy.ServiceProxy('/motors_mode', ModeSelect)
        self.robot_commands_pub = rospy.Publisher("/robot_commands", RobotCommand, queue_size=10)
        self.joy_subs = rospy.Subscriber('/joy', Joy, self.joy_callback)
        # self.motors_to_calibrate = ["right_hip_yaw"]
        self.rob_commands = RobotCommandParams()


    def joy_callback(self, joy_teleop):

        if joy_teleop.buttons[0] == 1:
            # self.all_to_init_pos()
            self.imu_handler_pub.publish("reset")
            print("IMU RESET")

        if joy_teleop.buttons[1] == 1:
            self.rob_commands.reset_vals()
            print("Reset Commands values")

        if joy_teleop.buttons[4] == 1:
            self.ser_motor_mode(3)
            print("Motors: INIT Pos Mode on Impedance mode Activated")

        if joy_teleop.axes[2] == -1:
            self.ser_motor_mode(2)
            print("Motors: POLICY Mode")

        self.rob_commands.update_vals(joy_teleop.axes[1], joy_teleop.axes[0], joy_teleop.axes[6])
        self.rob_commands.publish_command()

        # if joy_teleop.buttons[5] == 1:
        #     self.call_calibrator_server()
        #     print("Motors: left_knee CALIBRATE")
        #
        # if joy_teleop.buttons[5] == 1:
        #     self.call_calibrator_server()
        #     print("Motors: left_knee CALIBRATE")

        # if joy_teleop.buttons[5] == 1:
        #     self.ser_calibrator(["left_knee"], ["CALIBRATE"])
        #     print("Motors: left_knee CALIBRATE")

    # def call_calibrator_server(self):
    #     calibrator_client = actionlib.SimpleActionClient("calibrator", CalibrateAction)
    #     print(f"RobotControlUnit - : Calibration request for: {self.motors_to_calibrate}")
    #     calibrator_client.wait_for_server()
    #     goal = CalibrateGoal()
    #     # goal_list = []
    #     # for i in range(len(self.motors_to_calibrate)):
    #     #     goal_list.append("CALIBRATED")
    #     goal.calibrate_motors = self.motors_to_calibrate
    #     calibrator_client.send_goal(goal)
    #     # calibrator_client.wait_for_result(timeout=rospy.Duration())
    #     result = calibrator_client.get_result()
    #     print(f"RobotControlUnit - Calibration Result: {result}")


    def run(self):
        rospy.spin()