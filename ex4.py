class Rover:

    rover_geometry = [10,5,6]
    rover_ids= []
    def __init__(self,swarm_id:str,rover_id:str,rover_location:list):
        assert len(rover_location)<=3, "location can not have more than 3 parameters"
        self.swarm_id=swarm_id
        self.rover_id=rover_id
        self.rover_location=rover_location
        self.rover_ids.append(self.rover_id)
    def rover_locate(self)->str:
        return f"The rover with Swarm Id {self.swarm_id} and Rover Id {self.rover_id} is currently at {self.rover_location}"

    def rover_move(self,swarm_id:str,rover_id:str,dist:str):
        if (self.swarm_id == swarm_id and self.rover_id ==rover_id):
            return "Move " +str(dist)
        else: return "do nothing "


# print(Rover.rover_ids)
        
rover1 = Rover("1","hie",(10,-1,13)) 
rover2 = Rover("2","lol",(100,-1,213)) 
rover3 = Rover("3","f",(10,-13,13)) 
rover4 = Rover("4","curiosity",(102,-12,123)) 
print(rover1.rover_move("1","lol","56m north"))

# print (rover1.rover_move("1","23",4567890))
class daughter_rover(Rover):
    daughter_rover_geometry=[Rover.rover_geometry[0]/2,Rover.rover_geometry[1]/2,Rover.rover_geometry[2]/2]
    def __init__(self, swarm_id: str, rover_id: str, rover_location: list):
        super().__init__(swarm_id, rover_id, rover_location)
      


class User (Rover):
    
    def __init__(self,user_id:str):
        self.user_id=user_id
    def user_id_is(self):
        return self.user_id  
    


user1= User("Dhruv2005")# the one and only user




# print(user1.user_id)



class Scientist(User):
    def __init__(self, sci_id,user_id = user1):
        self.scientist = sci_id

    def view_rover_location(self,rover):# scintist can view the locatio of the rover only 
        if hasattr(rover,"rover_location"):
            return "rover location: "+ str(rover.rover_location)
        else:return "The specified rover does not exist"

Scientist1= Scientist("s001")

print(Scientist1.view_rover_location(rover1))

class Operator(User):


    def move_rover(self, rover, location:list): 
        message = f"MOVE,{rover.rover_id},{str(location)}"
        print(message)
        if isinstance(self, Rover):
            print("message sent")

            rover.rover_location=location
            print("new location: ", rover1.rover_location)

        else:
            print("Invalid msg")
        


class Manager(User):
    
    def __init__(self,man):
        self.user_id= user1.user_id;self.manager_id=man
        
    def add_rover(self, rover_id):
        Rover.rover_ids.append(rover_id)
        print("Manager adds rover:", rover_id)

    def remove_rover(self, rover_id):
        if rover_id in self.rover_ids:
            self.rover_ids.remove(rover_id)
            print("Manager removes rover:", rover_id)
        else:
            print("Rover is not under manager's control.")  

man1 = Manager("dhruv")
print(man1.user_id)
# print(Rover.rover_ids)
# man1.add_rover("hulk")
# print(Rover.rover_ids)