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

    mode=input("give input for map creating(map) or navigtion(nav)")
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

    if  mode =="map":
      #slam nodelaunch
      slam = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("slam_toolbox"),"launch","online_async_launch.py"))
      slamlaunch = IncludeLaunchDescription(slam,launch_arguments={"use_sim_time":"True"}.items())


      rviznode = launch_ros.actions.Node(
               package="rviz2",
               executable="rviz2",
               name="rviz2",
               output="screen")


    if mode =="nav":

      rviznode = launch_ros.actions.Node(
               package="rviz2",
               executable="rviz2",
               name="rviz2",
               output="screen")
      #map node
      map_path = os.path.join(get_package_share_directory(packagename),"launch","slammap.yaml")
      maplaunch = launch_ros.actions.Node(
                package="nav2_map_server",
                executable="map_server",
                name="map_server",
                parameters=[{"use_sim_time":True,"yaml_filename":map_path}] )

      #localization
      local_params = os.path.join(get_package_share_directory(packagename),"launch","local_params.yaml")
      localization = launch_ros.actions.Node(
                   package="nav2_amcl",
                   executable="amcl",
                   name="amcl",
                   parameters=[local_params,{"use_sim_time":True}])


      extra_node = launch_ros.actions.Node(
                 package="nav2_lifecycle_manager",
                 executable="lifecycle_manager",
                 name="nav_manager",
                 parameters=[{"use_sim_time":True,"autostart":True,"node_names":["map_server","amcl"]}])


      #map_path = "/home/sathvik/Documents/slammap.yaml"
      #maplaunchfile = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory("nav2_map_server"),"launch","map_saver_server.launch.py"))
      #maplaunch = IncludeLaunchDescription(maplaunchfile,launch_arguments={"map":map_path,"use_sim_time":"True"}.items())

      param_file=os.path.join(get_package_share_directory(packagename),"launch","nav2params.yaml")
      #navgatio node with another launch file
      navlaunchfile = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py'))
      #we need to include this launch description
      navlaunch = IncludeLaunchDescription(navlaunchfile,launch_arguments={"map":map_path,'params_file':param_file}.items())


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
    if mode=="map":
      Launch.add_action(slamlaunch)
    Launch.add_action(rviznode)
    if mode=="nav":
      Launch.add_action(maplaunch)
      Launch.add_action(localization)
      Launch.add_action(extra_node)
      Launch.add_action(navlaunch)
      #Launch.add_action(jointstategui)

    return Launch
