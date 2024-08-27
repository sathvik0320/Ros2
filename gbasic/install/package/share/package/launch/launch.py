import launch
import launch_ros
import os
import xacro
import launch.conditions
import launch.actions
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration

def generate_launch_description():


    #launch.actions.DeclareLaunchArgument(name="gui",default_value="False",description="this is for joint state publisher true for gui")
    #gui = LaunchConfiguration("gui")
    #print(gui)

    robotname="car"
    packagename="package"

    #package path to urdf and launch
    path = "urdf/robo.urdf"
    worldpath = "urdf/file.world"
    #actual path to urdf file
    actual = os.path.join(get_package_share_directory(packagename),path)
    #path to world file actual path
    wactual =os.path.join(get_package_share_directory(packagename),worldpath)
    #getting robot description from urdf file
    with open(actual,"r") as file:
       x=file.read()
       print(str(x)+"urdf content")

    robot_info ={"robot_description":x}
    #starting servers for gazebo gzserver and gzclient
    gazebolaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("gazebo_ros"),"launch","gazebo.launch.py"))
    #if you want to include a specific world into gazebo
    #gazebo = IncludeLaunchDescription(gazebolaunch,launch_arguments={}.items())
    gazebo =IncludeLaunchDescription(gazebolaunch,launch_arguments={"world":wactual}.items())
    #robot_state_pulisher node
    robotstate = launch_ros.actions.Node(
                  package="robot_state_publisher",
                  executable="robot_state_publisher",
                  output="screen",
                  parameters=[robot_info,{"use_sim_time":True}])

    #spawn the urdf content into gazebo simulation
    #Node or lauch_ros.actions.Node same
    #jointstate = launch_ros.actions.Node(
    #             package="joint_state_publisher",
    #             executable="joint_state_publisher",
    #             name="joint_state_publisher",
    #             parameters=[{"use_sim_time":True}])

    spawning = launch_ros.actions.Node(
               package="gazebo_ros",
               executable="spawn_entity.py",
               arguments=["-topic","robot_description","-entity",robotname],
               output="screen")

    #condition = launch.conditions.UnlessCondition(LaunchConfiguration("gui")))
    #jointstategui =launch_ros.actions.Node(
    #               package="joint_state_publisher_gui",
    #               executable="joint_state_publisher_gui",
    #               name="joint_state_publisher_gui",
    #               condition =launch.conditions.IfCondition(LaunchConfiguration("")))

    #creating a lauch object a add all the launchs we created to it
    Launch=LaunchDescription()
    Launch.add_action(gazebo)
    Launch.add_action(robotstate)
    #Launch.add_action(jointstate)
    Launch.add_action(spawning)
    #Launch.add_action(jointstategui)

    return Launch

