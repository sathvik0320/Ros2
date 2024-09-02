import launch_ros as lr
import launch as l
import os
import xacro
import launch.LaunchDescription as Launch
import launch.actions.IncludeLaunchDescription as Include
import launch.launch_description_sources.PythonLaunchDescriptonSource as psource 
import ament_index_python.packages.get_package_share_directory as get
import launch.substitutions.LaunchConfiguration as input

def generate_launch_description()

   packagename="package"
   robotname="drone"
   urdf_path = os.path.join(get(packagename),"urdf/drone.urdf")
   with open(urdf_path) as file :
           x=file.read()
           print("urdf"+"str(x)")
   robot_info = {"robot_description":x}

   #creating the nodes
   robotstate =lr.actions.Node(
               package="robot_state_publisher",
               executable="robot_state_publisher",
               output="screen",
               parameters=[robot_info])

   jointstate=lr.actions.Node(
               package="",
               executable="",
               name="",
               condtion=)
   jointgui = lr.actions.Node(
               package="",
               executable="",
               output="screen",
               )

   return
