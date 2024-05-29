#!/usr/bin/env python
import rospy
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

def publish_msg(q1, q2, q3, q4, q5):
    state = JointTrajectory()
    state.header.stamp = rospy.Time.now()
    state.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5"]
    point = JointTrajectoryPoint()
    point.positions = [q1, q2, q3, q4, q5]
    point.time_from_start = rospy.Duration(0.5)
    state.points.append(point)
    pub.publish(state)
    print('State published successfully')

# Sequentially publish pose in each joint with a publish rate
def sequential_publish(x):
    for i in range(len(x)):
        qL[i] = x[i]
        publish_msg(qL[0], qL[1], qL[2], qL[3], qL[4])
        print("J{0} updated: {1}".format(i + 1, qL))
        rate.sleep()

def joint_publisher():
    global pub, qL, rate

    pub = rospy.Publisher('/joint_trajectory', JointTrajectory, queue_size = 0)
    rospy.init_node('joint_publisher', anonymous = False)
    rate = rospy.Rate(2)

    # HOME position
    p1 = [-2.6128766536712646, -0.5726853013038635, 1.7436223030090332, -0.43974050879478455, 2.597537040710449]
    # Selected pose
    p2 = [-1.569771409034729, 0.9152738451957703, 1.206729769706726, 1.1760501861572266, -0.5880250930786133]

    qL = p2.copy()
    while not rospy.is_shutdown():
        print("\nHOME:\n")
        sequential_publish(p1)
        print("\nX2:\n")
        sequential_publish(p2)

if __name__ == '__main__':
    try:
        joint_publisher()
    except rospy.ROSInterruptException:
        pass