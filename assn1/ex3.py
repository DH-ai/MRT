class Rover:

    rover_geometry = [10,5,6]
    def __init__(self,swarm_id:str,rover_id:str,rover_location:list):
        assert len(rover_location)<=3, "location can not have more than 3 parameters"
        self.swarm_id=swarm_id
        self.rover_id=rover_id
        self.rover_location=rover_location
    def rover_locate(self)->str:
        return f"The rover with Swarm Id {self.swarm_id} and Rover Id {self.rover_id} is currently at {self.rover_location}"

    def rover_move(self,swarm_id:str,rover_id:str,dist:str):
        if (self.swarm_id == swarm_id and self.rover_id ==rover_id):
            return "Move"
        else: return "do nothing "


        
rover1 = Rover("1","huehue",(10,-1,13)) 


# print (rover1.rover_move("1","23",4567890))
class daughter_rover(Rover):
    daughter_rover_geometry=[Rover.rover_geometry[0]/2,Rover.rover_geometry[1]/2,Rover.rover_geometry[2]/2]
    def __init__(self, swarm_id: str, rover_id: str, rover_location: list):
        super().__init__(swarm_id, rover_id, rover_location)