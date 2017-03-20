#!/usr/bin/env python
"""
ROS node with service that allows for controlling the YuMi remotely
"""

import logging
import argparse
import rospy
try:
    from yumipy.yumi_arm import *
    from yumipy.srv import *
except ImportError:
    raise RuntimeError("yumi_ros_service unavailable outside of catkin package")

if __name__ == '__main__':
    # Initialize server. Name is generic as it will be overwritten by launch anyways
    rospy.init_node('arm_server')
    
    name = rospy.get_param('~name')
    verbose = rospy.get_param('~display_output')
    
    # Get local YuMiArm and its method dict
    arm = YuMiArmFactory.YuMiArm('local', name)
    yumi_methods = YuMiArm.__dict__

    # Define how requests are handled (Call the corresponding method in the local class)
    def handle_request(req):
        func = pickle.loads(req.func)
        args = pickle.loads(req.args)
        kwargs = pickle.loads(req.kwargs)
        if verbose:
            rospy.loginfo("Handling request to call method {0} for {1} arm".format(func, name))
        return ROSYumiArmResponse(pickle.dumps(yumi_methods[func](arm, *args, **kwargs)))
    
    s = rospy.Service('{0}_arm'.format(name), ROSYumiArm, handle_request)
    rospy.loginfo("{0} arm is ready".format(name))

    # Keep process alive
    rospy.spin()
        