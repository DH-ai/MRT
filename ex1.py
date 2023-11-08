


class Rover:

    rover_geometry = [None,None,None]
    def __init__(self,swarm_id:str,rover_id:str,rover_location:list):
        assert len(rover_location)<=3, "location can not have more than 3 parameters"
        self.swarm_id=swarm_id
        self.rover_id=rover_id
        self.rover_location=rover_location
    def rover_locate(self)->str:
        return f"The rover with Swarm Id {self.swarm_id} and Rover Id {self.rover_id} is currently at "


rover1 = Rover("23b1010","huehue",(10,-1,13)) 
rover_loc= rover1.rover_locate()

print(rover_loc)