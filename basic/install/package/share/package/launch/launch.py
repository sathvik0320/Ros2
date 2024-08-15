import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():

     folderpath = launch_ros.substitutions.FindPackageShare(package="package").find("package")
     filepath = os.path.join(folderpath,"urdf/ro.urdf")

     #getting the content of the urdf file robot description
     with open(filepath,"r") as f:
             roboinfo=f.read()
             print(str(roboinfo)+"urdf contents")


     roboinfo={"robot_description":roboinfo}

     #now we create nodes for simulating the robot description with gazebo or rviz
     #parameters are robot description indirectly urdf content
     robot_state_publisher_node=launch_ros.actions.Node(
      package="robot_state_publisher",
      executable="robot_state_publisher",
      output ="screen",
      parameters=[roboinfo])


     #joint_state_publisher_node node
     joint_state_publisher_node = launch_ros.actions.Node(
      package="joint_state_publisher",
      executable="joint_state_publisher",
      name="joint_state_publisher",
      parameters=[roboinfo],
      condition = launch.conditions.UnlessCondition(LaunchConfiguration("gui")))

     #joint_state_publisher_gui_node
     joint_state_publisher_gui_node =launch_ros.actions.Node(
      package ="joint_state_publisher_gui",
      executable = "joint_state_publisher_gui",
      name ="joint_state_publisher_gui",
      condition = launch.conditions.IfCondition(LaunchConfiguration("gui")))


     #rviz node creatition
     rviz_node = launch_ros.actions.Node(
      package ="rviz2",
      executable="rviz2",
      name="rviz2",
      output ="screen")


     return launch.LaunchDescription([
          launch.actions.DeclareLaunchArgument(name="gui",default_value="True",description="this is the flag"),
          launch.actions.DeclareLaunchArgument(name="ro",default_value=filepath,description="path to urdffile"),
          robot_state_publisher_node,
          joint_state_publisher_node,
          joint_state_publisher_gui_node,
          rviz_node ])
