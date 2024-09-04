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
   world_path = os.path.join(get(packagename),"urdf/file.world")

   with open(urdf_path) as file :
           x=file.read()
           print("urdf"+ str(x))
   robot_info = {"robot_description":x}

   gui=Declare(name="gui",default_value="False",description="with gui or without gui")
   rvi =Declare(name="rvi",default_value="False",description="condition for rviz and jointstate pulisher")
   joint = Declare(name="joint",default_value="False",description="for join states")

   #creating the nodes
   robotstate =lr.actions.Node(
               package="robot_state_publisher",
               executable="robot_state_publisher",
               output="screen",
               parameters=[robot_info])

   #jointstate=lr.actions.Node(
   #            package="joint_state_publisher",
   #            executable="joint_state_publisher",
   #            name="joint_state_publisher",
   #            condition= l.conditions.IfCondition(input("joint")))
   #jointgui = lr.actions.Node(
   #            package="joint_state_publisher_gui",
   #            executable="joint_state_publisher_gui",
   #            output="screen",
   #            name="joint_state_publisher",
   #            condition = l.conditions.IfCondition(input("gui")))

   rvizlaunch =lr.actions.Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                condition = l.conditions.IfCondition(input("rvi"))
                )

   gazebo = psource(os.path.join(get("gazebo_ros"),"launch","gazebo.launch.py"))
   gazebolaunch = Include(gazebo,launch_arguments={"world":world_path}.items())

   spawning = lr.actions.Node(
               package="gazebo_ros",
               executable="spawn_entity.py",
               arguments=["-topic","robot_description","-entity",robotname],
               output ="screen")

   object =Launch()
   object.add_action(gazebolaunch)
   object.add_action(robotstate)
   object.add_action(spawning)

   object.add_action(gui)
   object.add_action(rvi)
   object.add_action(joint)

   #object.add_action(jointstate)
   #object.add_action(jointgui)
   object.add_action(rvizlaunch)

   return object
