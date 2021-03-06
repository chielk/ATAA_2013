class Agent(object):
    
    NAME = "Django"
    
    def __init__(self, id, team, settings=None, field_rects=None, field_grid=None, nav_mesh=None, blob=None, **kwargs):
        """ Each agent is initialized at the beginning of each game.
            The first agent (id==0) can use this to set up global variables.
            Note that the properties pertaining to the game field might not be
            given for each game.
        """
        self.id = id
        self.team = team
        self.mesh = nav_mesh
        self.grid = field_grid
        self.settings = settings
        self.goal = None
        self.callsign = '%s-%d'% (('BLU' if team == TEAM_BLUE else 'RED'), id)
        self.blobpath = None
        self.blobcontent = None
        self.speed = None
        
        # Read the binary blob, we're not using it though
        if blob is not None:
            # Remember the blob path so we can write back to it
            self.blobpath = blob.name
            self.blobcontent = pickle.loads(blob.read())
            print "Agent %s received binary blob of %s" % (
               self.callsign, type(self.blobcontent))
            # Reset the file so other agents can read it too.
            blob.seek(0) 
        
        # Recommended way to share variables between agents.
        if id == 0:
            self.all_agents = self.__class__.all_agents = []
        self.all_agents.append(self)

        # state space -- positions on the grid for x axis
        self.grid_x = [[0, 48], [49, 113], [114, 218], [219, 324], [325, 388], [389, 442]]
        self.grid_y = [[0, 0], [0, 0], [0, 0]]
    
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

    def eGreedy(self, current_state, cps):
        moves = []
        for i in range(-1,2):
            for j in range(-1,2):
                if self.observation.walls[2+j][2+i] == 0:
                    position = (current_state[0]+i, current_state[1]+j)
                    moves.append(position)
        if random.random() < self.epsilon :
            r = math.floor(random.random() * len(moves))
            return (moves[int(r)][0], moves[int(r)][1])
        else:
            bestMoves = []
            bestValue = 0.0
            for move in moves:
                value = self.qtable[current_state][cps][move]
                if value > bestValue:
                    bestMoves = []
                    bestMoves.append(move)
                    bestValue = value
                    action  = move
                if value == bestValue:
                    bestMoves.append(move)
            r = math.floor(random.random() * len(bestMoves))
            return (bestMoves[int(r)][0], bestMoves[int(r)][1])

    def find_state(self, location):
        x = 0
        y = 0
        for i in range(len(self.grid_x)):
            if location[0] >= self.grid_x[i][0] and location[0] <= self.grid_x[i][1]:
                x = i
                break

        y = location[1] / 80
        return x,y
                    
    def action(self):
        """ This function is called every step and should
            return a tuple in the form: (turn, speed, shoot)
        """
        obs = self.observation
        if self.id == 0:
            print self.find_state(self.all_agents[0].observation.loc),self.find_state(self.all_agents[1].observation.loc),self.find_state(self.all_agents[2].observation.loc)

        # Check if agent reached goal.
        if self.goal is not None and point_dist(self.goal, obs.loc) < self.settings.tilesize:
            self.goal = None
            
        # Walk to ammo
        ammopacks = filter(lambda x: x[2] == "Ammo", obs.objects)
        if ammopacks:
            self.goal = ammopacks[0][0:2]
            
        # Drive to where the user clicked
        # Clicked is a list of tuples of (x, y, shift_down, is_selected)
        if self.selected and self.observation.clicked:
            self.goal = self.observation.clicked[0][0:2]
        
        # Walk to random CP
        if self.goal is None:
            self.goal = obs.cps[random.randint(0,len(obs.cps)-1)][0:2]
        
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
            speed = (dx**2 + dy**2)**0.5
            if turn > self.settings.max_turn or turn < -self.settings.max_turn:
                shoot = False
            if abs(math.degrees(turn)) >= 45:
                if self.speed is not None:
                    speed = max(0.9 * self.speed, 1)
            
        else:
            turn = 0
            speed = 0
        self.speed = speed        
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
        if self.id == 0 and self.blobpath is not None:
            try:
                # We simply write the same content back into the blob.
                # in a real situation, the new blob would include updates to 
                # your learned data.
                blobfile = open(self.blobpath, 'wb')
                pickle.dump(self.blobcontent, blobfile, pickle.HIGHEST_PROTOCOL)
            except:
                # We can't write to the blob, this is normal on AppEngine since
                # we don't have filesystem access there.        
                print "Agent %s can't write blob." % self.callsign