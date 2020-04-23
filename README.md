# Phoenix <a href="url"><img src="https://github.com/mbiuki/Phoenix/blob/master/earthToCartesian/archive/phoenix.png" align="left" height="48" width="48" ></a>
### Phoenix is a toolbox for detecting fake drones from real ones. Phoenix relies on the behavior of nonlinear dynamical systems by using the underlying stability criteria used to control drones during their flight.
The toolbox is for distinuguishing between the fake and real nodes in an IoT netowork. Real nodes are the nodes that have physical presence in the network. Fake nodes could be virtual nodes that do not have physical appearance in the netowrk.
We have tested the toolbox particularly in this release for drones data (telemetry). But the implementation can be extended to any nonlinear dynamic system that has a closed control loop. A demonstration of our DoS attack by a virtual node (laptop) can be found [here](https://youtu.be/SrJvO4RwMUQ).

### YouTube Links
To evaluate Phoenix in a real-world environment, we have also constructed a custom-made drone. Links below show some of the trials that we have had in the field for recording traces:
- [Link1](https://youtu.be/qs08zkw28QA)
- [Link2](https://youtu.be/7CvK-T6ByXU)
- [Link3](https://youtu.be/-af6N7HLg3Y)

## Below is the folder hierarchy
### Trajectory
List of sample trajecotries in different drone modes of operation.
### Phoenix folder
The authentication code that reads traces and tells if the trace is fake or real.
### DoS_attack folder
Scripts for flooding telemetry and experiencing drones with DoS.
- A short video of possible drone DoS attack is [here](https://youtu.be/SrJvO4RwMUQ).
### earthToCartesian
converting the earth coordinates to cartesian and then referencing from the origin of flight.
