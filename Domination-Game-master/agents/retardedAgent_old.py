
class Agent(object):
    
    NAME = "PedoBear"
    
    def __init__(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None, matchinfo=None):
        """ Each agent is initialized at the beginning of each game.
            The first agent (id==0) can use this to set up global variables.
            Note that the properties pertaining to the game field might not be
            given for each game.
        """
        #matchinfo=kwargs['matchinfo']

        self.id = id
        self.team = team
        self.mesh = nav_mesh
        self.grid = field_grid
        self.settings = settings
        self.goal = None
        self.callsign = '%s-%d'% (('BLU' if team == TEAM_BLUE else 'RED'), id)
        self.count =0
        # Read the binary blob, we're not using it though
        if blob is not None:
            print "Agent %s received binary blob of %s" % (
               self.callsign, type(pickle.loads(blob.read())))
            # Reset the file so other agents can read it.
            blob.seek(0) 
        
        # Recommended way to share variables between agents.
        if id == 0:
            self.all_agents = self.__class__.all_agents = []
        self.all_agents.append(self)
    
    def observe(self, observation):
        """ Each agent is passed an observation using this function,
            before being asked for an action. You can store either
            the observation object or its properties to use them
            to determine your action. Note that the observation object
            is modified in place.
        """
        self.observation = observation
        self.selected = observation.selected

        if observation.selected:
            print observation
                    
    def action(self):
        """ This function is called every step and should
            return a tuple in the form: (turn, speed, shoot)
        """
        if self.id==0:    
            obs = self.observation
            shoot =False
            


            # Check if agent reached goal.
            if self.goal is not None and point_dist(self.goal, obs.loc) < self.settings.tilesize:
                self.goal = None
                
            # Walk to ammo
            ammopacks = filter(lambda x: x[2] == "Ammo", obs.objects)
            if ammopacks:
                pass
                
            # Drive to where the user clicked
            # Clicked is a list of tuples of (x, y, shift_down, is_selected)
            if self.selected and self.observation.clicked:
                pass
            
            # Walk to random CP
            if self.goal is None and (obs.cps[0][2]==0 or obs.cps[0][2]==2):
                self.goal = obs.cps[0][0:2]
             
        



            # Shoot enemies
            shoot = False
            if (obs.ammo > 0 and 
                obs.foes and 
                point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and
                not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
                pass



            # Compute path, angle and drive
            if obs.cps[0][2]!=1:
                path = find_path(obs.loc, self.goal, self.mesh, self.grid, self.settings.tilesize)
                if path:
                    dx = path[0][0] - obs.loc[0]
                    dy = path[0][1] - obs.loc[1]
                    turn = angle_fix(math.atan2(dy, dx) - obs.angle)
                    if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                        shoot = False
                    speed = (dx**2 + dy**2)**0.5
                else:
                    turn = 0
                    speed = 0
            
                return (turn,speed,shoot)
            else: 
                return (0,0,shoot)

        elif self.id==2:    
            obs = self.observation
            shoot = False
            




            # Check if agent reached goal.
            if self.goal is not None and point_dist(self.goal, obs.loc) < self.settings.tilesize:
                self.goal = None
                
            # Walk to ammo
            ammopacks = filter(lambda x: x[2] == "Ammo", obs.objects)
            if ammopacks:
                pass
                
            # Drive to where the user clicked
            # Clicked is a list of tuples of (x, y, shift_down, is_selected)
            if self.selected and self.observation.clicked:
                pass
            
            # Walk to random CP
            if self.goal is None and (obs.cps[1][2]==0 or obs.cps[1][2]==2):
                self.goal = obs.cps[1][0:2]
                        
            
                
                        
            # Shoot enemies
            shoot = False
            if (obs.ammo > 0 and 
                obs.foes and 
                point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and
                not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
                pass

            # Compute path, angle and drive
            if obs.cps[1][2]!=1:
                path = find_path(obs.loc, self.goal, self.mesh, self.grid, self.settings.tilesize)
                if path:
                    dx = path[0][0] - obs.loc[0]
                    dy = path[0][1] - obs.loc[1]
                    turn = angle_fix(math.atan2(dy, dx) - obs.angle)
                    if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                        shoot = False
                    speed = (dx**2 + dy**2)**0.5
                else:
                    turn = 0
                    speed = 0
                
                return (turn,speed,shoot)
            else:
                return(0,0,shoot)

        else:
                    """ This function is called every step and should
            return a tuple in the form: (turn, speed, shoot)
        """
        
        
        obs = self.observation
        shoot = False


        if self.goal is None and self.count%4==0:
            self.goal = (152,136)
            self.count =self.count+1

        if self.goal is None and self.count%4==1:
            self.goal = (312,136)
            self.count=self.count+1
        if self.goal is None and self.count%4==2:
            self.goal = (216,56)
            self.count=self.count+1
        if self.goal is None and self.count%4==3:
            self.goal = (248,216)
            self.count=self.count+1

        # Check if agent reached goal.
        if self.goal is not None and point_dist(self.goal, obs.loc) < self.settings.tilesize:
            if self.count%4==1:
                self.goal=(312,136)
                self.count = self.count+1
            elif self.count%4==0:
                self.goal=(152,136)
                self.count = self.count+1
            elif self.count%4==2:
                self.goal=(216,56)
                self.count = self.count+1
            elif self.count%4==3:
                self.goal=(248,216)
                self.count = self.count+1
            

       

        # Shoot enemies
        shoot = False
        if (obs.ammo > 0 and 
            obs.foes and 
            point_dist(obs.foes[0][0:2], obs.loc) < self.settings.max_range and
            not line_intersects_grid(obs.loc, obs.foes[0][0:2], self.grid, self.settings.tilesize)):
            self.goal = obs.foes[0][0:2]
            shoot = True

        # Compute path, angle and drive
        path = find_path(obs.loc, self.goal, self.mesh, self.grid, self.settings.tilesize)
        if path:
            dx = path[0][0] - obs.loc[0]
            dy = path[0][1] - obs.loc[1]
            turn = angle_fix(math.atan2(dy, dx) - obs.angle)
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            speed = (dx**2 + dy**2)**0.5
        else:
            turn = 0
            speed = 0
        
        return (turn,speed,shoot)
        
    def debug(self, surface):
        """ Allows the agents to draw on the game UI,
            Refer to the pygame reference to see how you can
            draw on a pygame.surface. The given surface is
            not cleared automatically. Additionally, this
            function will only be called when the renderer is
            active, and it will only be called for the active team.
        """
        import pygame
        # First agent clears the screen
        if self.id == 0:
            surface.fill((0,0,0,0))
        # Selected agents draw their info
        if self.selected:
            if self.goal is not None:
                pygame.draw.line(surface,(0,0,0),self.observation.loc, self.goal)
        
    def finalize(self, interrupted=False):
        """ This function is called after the game ends, 
            either due to time/score limits, or due to an
            interrupt (CTRL+C) by the user. Use it to
            store any learned variables and write logs/reports.
        """
        pass
        
