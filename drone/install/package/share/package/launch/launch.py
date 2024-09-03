import launch_ros as lr
import launch as l
import os
import xacro
from launch import LaunchDescription as Launch
from launch.actions import IncludeLaunchDescription as Include
from launch.actions import DeclareLaunchArgument as Declare
from launch.launch_description_sources import PythonLaunchDescriptionSource as psource
from ament_index_python.packages import get_package_share_directory as get
from launch.substitutions import LaunchConfiguration as input

def generate_launch_description():

   packagename="package"
   robotname="drone"
   urdf_path = os.path.join(get(packagename),"urdf/drone.urdf")
   with open(urdf_path) as file :
           x=file.read()
           print("urdf"+ str(x))
   robot_info = {"robot_description":x}
   gui=Declare(name="gui",default_value="True",description="with gui or without gui")
   #creating the nodes
   robotstate =lr.actions.Node(
               package="robot_state_publisher",
               executable="robot_state_publisher",
               output="screen",
               parameters=[robot_info])

   jointstate=lr.actions.Node(
               package="joint_state_publisher",
               executable="joint_state_publisher",
               name="joint_state_publisher",
               condition= l.conditions.UnlessCondition(input("gui")))
   jointgui = lr.actions.Node(
               package="joint_state_publisher_gui",
               executable="joint_state_publisher_gui",
               output="screen",
               name="joint_state_publisher",
               condition = l.conditions.IfCondition(input("gui"))
               )

   rvizlaunch =lr.actions.Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen")


   object =Launch()
   object.add_action(gui)
   object.add_action(robotstate)
   object.add_action(jointstate)
   object.add_action(jointgui)
   object.add_action(rvizlaunch)

   return object
