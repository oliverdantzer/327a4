import mysql.connector

mydb = None
cursor = None
 
 
# TODO: Doc comment what ever that means, figure it out, the TA wrote it 
 
class App: 
 
    def __init__(self): 
 
        # These could change based on what your database and password for it are 
        dbPassword = "Queensiscool5" 
        database = "mydatabase" 
 
    # Connect to MySQL 
        mydb = mysql.connector.connect( 
            host="localhost", 
            user="root", 
            password=dbPassword, 
        ) 
        cursor = mydb.cursor() 
 
        # Set up a database, delete the old one (testing) 
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + database) 
        cursor.execute("USE " + database) 
        # create Users and Teams table 
        # create also a junction table to show many to many relationships 
 
        createUserTable = """ 
            CREATE TABLE IF NOT EXISTS user( 
            userID INT AUTO_INCREMENT PRIMARY KEY, 
            username VARCHAR(255) NOT NULL, 
            password VARCHAR(255) NOT NULL 
            ); 
            """ 
 
        createTeamTable = """ 
            CREATE TABLE IF NOT EXISTS team( 
            teamID INT AUTO_INCREMENT PRIMARY KEY, 
            teamName VARCHAR(255) NOT NULL 
            ); 
            """ 
 
        #HERE IS THE MEMBERS FOR A TEAM, AND TEAMS THAT A USER HAS 
        createUserTeamTable = """ 
            CREATE TABLE IF NOT EXISTS userteam( 
                userTeamID INT AUTO_INCREMENT PRIMARY KEY, 
                userID INT, 
                teamID INT, 
                FOREIGN KEY (userID) REFERENCES user (userID) ON DELETE CASCADE, 
                FOREIGN KEY (teamID) REFERENCES team (teamID) ON DELETE CASCADE 
                ); 
            """ 
 
        #TODO add the required parameters 
        createProjectTable = """ 
            CREATE TABLE IF NOT EXISTS project( 
            projectID INT AUTO_INCREMENT PRIMARY KEY, 
            projectName VARCHAR(255) NOT NULL, 
            priority INT, 
            teamID INT, 
            FOREIGN KEY (teamID) REFERENCES team (teamID) ON DELETE CASCADE 
            ); 
            """ 
 
        createTaskTable = """ 
            CREATE TABLE IF NOT EXISTS task( 
            taskID INT AUTO_INCREMENT PRIMARY KEY, 
            comleted VARCHAR(255) NOT NULL, 
            projectID INT, 
            userID INT,
            completed BOOLEAN,
            FOREIGN KEY (projectID) REFERENCES project (projectID) ON DELETE CASCADE, 
            FOREIGN KEY (userID) REFERENCES user (userID) ON DELETE CASCADE 
            ); 
            """ 
 
        cursor.execute(createUserTable) 
        cursor.execute(createTeamTable) 
        cursor.execute(createUserTeamTable) 
        cursor.execute(createProjectTable) 
        cursor.execute(createTaskTable) 
        mydb.commit() 
        # print("----------------------------->Finished initializing \n") 
 
    def userExists(self, username, password):
        # Check if a user with the given username and password exists
        query = "SELECT * FROM user WHERE username = %s AND password = %s;"
        data = (username, password)
        cursor.execute(query, data)
        result = cursor.fetchall()
        mydb.commit()

        if result:
            return True
        else:
            return False

    def register(self):
        # Register a new user
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        if self.userExists(username, password):
            print("User already exists")
            return False
        data = (username, password)
        query = "INSERT INTO user (username, password) VALUES (%s, %s);"
        cursor.execute(query, data)
        mydb.commit()
        print("Successful Registration")

    def login(self):
        # User login
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if self.userExists(username, password):
            print("Login Successful")
            data = (self.username,)
            query = "SELECT userID FROM user WHERE username = %s;"
            cursor.execute(query, data)
            userID = cursor.fetchone()
            return userID
        else:
            print("Login Failed")
            return False
 
 
class User(App): 
 
    def __init__(self, userID): 
        self.userID = userID
 
    def __str__(self): 
        return self.userID
 
    def createTeam(self, newTeamName): 
        query = "INSERT INTO team (teamName) VALUES (%s, %s, %s)"
        data = (newTeamName, )
        cursor.execute(query, data)
        mydb.commit()
 
    def listTeams(self): 
 
        query = "SELECT teamName FROM team" 
        cursor.execute(query) 
        teamNames = cursor.fetchall() 
        mydb.commit() 
 
        print("Listing Personal User Teams:\n") 
        for teamName in teamNames: 
            print(str(teamName) + "\n") 
        return str(teamNames) 
 
 
    def assignUserToTeam(self, user, team): 
        team.assignToTeam(user) 
 
class Team(App):
    def __init__(self, teamID):
        # Initialize a Team object with a teamID
        self.teamID = teamID

    def __str__(self):
        # Return a string representation of the Team object
        return self.teamID

    def deleteTeam(self, teamName):
        # Delete a team from the database based on teamID
        if self.teamID:
            data = (self.teamID,)

            # Delete the team from the userteam table
            query = "DELETE FROM userteam WHERE teamID = %s"
            cursor.execute(query, data)

            # Delete the team from the team table
            query = "DELETE FROM team WHERE teamID = %s"
            cursor.execute(query, data)
            mydb.commit()

            # Set teamID to None to mark it as deleted
            self.teamID = None
            return True
        else:
            print(f"Team '{teamName}' not found.")
            return False

    def assignToTeam(self, member):
        # Assign a user (member) to the team
        userID = member.getUserID()
        print("This is userID -> " + str(userID))
        print("This is teamID -> " + str(self.teamID))

        query = "INSERT INTO userteam (userID,teamID) VALUES (%s,%s)"
        data = (userID, self.teamID)
        cursor.execute(query, data)
        mydb.commit()

    def createProject(self, newProjectName, priority):
        # Create a new project for the team
        if self.teamID:
            query = "INSERT INTO project (projectName, priority, teamID) VALUES (%s, %s, %s)"
            data = (newProjectName, priority, self.teamID)
            cursor.execute(query, data)
            mydb.commit()
            print(f"Project '{newProjectName}' created successfully.")
            return True
        else:
            print("Cannot create a project for an invalid team.")
            return False

    def listProjects(self):
        # List all projects associated with the team
        if self.teamID:
            query = "SELECT projectName, priority FROM project WHERE teamID = %s"
            data = (self.teamID,)
            cursor.execute(query, data)
            projects = cursor.fetchall()

            if projects:
                print("Projects for Team ID:", self.teamID)
                for project in projects:
                    project_name, project_priority = project
                    print(f"Project Name: {project_name}, Priority: {project_priority}")
            else:
                print("No projects found for this team.")
        else:
            print("Cannot list projects for an invalid team.")
        
 
 
class Project(App):
    def __init__(self, projectID):
        # Initialize a Project object with a projectID.
        self.projectID = projectID

    def __str__(self):
        # Convert the Project object to a string, returning its projectID.
        return str(self.projectID)

    def deleteProject(self):
        # Delete the project from the database by its projectID.
        cursor.execute("DELETE FROM project WHERE projectID = ?", (self.projectID,))
        mydb.commit()
        return True

    def addProjectDeadlinePriority(self, priority):
        # Update the priority of the project in the database.
        cursor.execute("UPDATE project SET priority = ? WHERE projectID = ?", (priority, self.projectID))
        mydb.commit()

    def trackProgressProject(self):
        # Calculate the progress of the project by summing completed tasks.
        cursor.execute("SELECT SUM(completed), COUNT(*) FROM task WHERE projectID = ?", (self.projectID,))
        result = cursor.fetchone()
        if result and result[1] > 0:
            completed, total = result
            return completed / total  # Return the completion ratio.
        else:
            return 0.0  # If there are no tasks, return 0.0.

    def createTask(self, title):
        # Create a new task associated with the project in the database.
        cursor.execute("INSERT INTO task (projectID, title, completed) VALUES (?, ?, 0)", (self.projectID, title))
        mydb.commit()

    def listTasks(self):
        # List all the tasks associated with the project.
        cursor.execute("SELECT title FROM task WHERE projectID = ?", (self.projectID,))
        tasks = [row[0] for row in cursor.fetchall()]
        return tasks

    def deleteTask(self, title):
        # Delete a specific task associated with the project.
        cursor.execute("DELETE FROM task WHERE projectID = ? AND title = ?", (self.projectID, title))
        mydb.commit()
 
 
class Task(App):
    # Constructor for the Task class
    def __init__(self, taskID):
        super().__init__()
        self.taskID = taskID

    # Mark the task as completed in the database
    def complete(self):
        cursor.execute("UPDATE task SET completed = 1 WHERE taskID = %s", (self.taskID,))
        mydb.commit()

    # Assign a member to the task in the database
    def assignMember(self, member):
        cursor.execute("UPDATE task SET userID = %s WHERE taskID = %s", (member, self.taskID))
        mydb.commit()

        
        
        
        
 
 
def taskPage(project): 
    print("To create a task type 'create' \nTo show your uncompleted tasks type 'show'" 
          "\nTo delete a task type 'delete'\nTo show your completed tasks type 'showCompleted' \n" 
          "\nTo go back to the team page type 'back'") 
    userInput = input("->") 
 
    if userInput == 'create': 
        print("Enter a task title: ") 
        title = input("-> ") 
        project = project.createTask(title) 
 
    elif userInput == 'show': 
        for task in project.tasks: 
            if not task.completed: 
                print(task.title) 
 
    elif userInput == 'showCompleted': 
        for task in project.tasks: 
            if task.completed: 
                print(task.title) 
 
    elif userInput == 'delete': 
 
        # Get input 
        print("Enter title of the task you wish to delete") 
        title = input("-> ") 
 
        for task in project.tasks: 
            if title == task.title: 
                project.deleteTask(title) 
 
    elif userInput == 'back': 
        return 'break' 
 
    else: 
        print("Please pick either create, delete, show, or showCompleted") 
 
 
def main(): 
 
    # Initialization 
    app = App() 
    loggedIn = False 
    onTeamPage = False 
    onProjectPage = False 
    onTaskPage = False 
    teamFocus = None 
    projectFocus = None 
 
    # Login / Registry 
    while loggedIn == False: 
        print("Enter 'l' to login or 'r' to register.") 
        userInput = input("->") 
 
        if userInput == 'r': 
            user = app.register() 
        elif userInput == 'l': 
            loggedIn = app.login() 
            if loggedIn == True: 
                onTeamPage = True 
        else: 
            print("Please pick either l or p") 
 
    # print("Thank you for loggin in" + user.username) 
 
    # Teams / Home Page 
    while onTeamPage == True: 
        # if there is a team show teams, if they arent, print show teams 
        print("To create a Team type 'create' \nTo show your teams type 'show' \nTo delete a team type 'delete' \nTo " 
              "select a team  type 'select' \nTo assign a team  type 'assign'") 
        userInput = input("->") 
 
        if userInput == 'create': 
            print("Enter a team name: ") 
            teamName = input("-> ") 
            team = user.createTeam(teamName) 
 
        elif userInput == 'show': 
            teamName = user.listTeams() 
 
        elif userInput == 'select': 
            teamName = user.listTeams() 
 
            # Get input 
            print("Enter the team name you wish to select") 
            teamNameSel = input("-> ") 
 
            teamExists = False 
 
            query = "SELECT teamName FROM team WHERE teamName = %s" 
            data = (teamNameSel,) 
            app.cursor.execute(query, data) 
            result = app.cursor.fetchone() 
 
            # If the team exists, use it and move to the next page 
            if result: 
                print("You are viewing the projects associated to team: " + teamNameSel + "\n") 
                teamExists = True 
                teamFocus = Team(teamNameSel) # TODO keep working here 
                onProjectPage = True 
                onTeamPage = False 
            else: 
                print("Select a valid team") 
 
        elif userInput == 'assign': 
 
            # show all teams 
            teamName = user.listTeams() 
 
            print("Showing all users") 
            # show all users 
            for displayUser in app.users: 
                print(str(displayUser)) 
 
            print("From the provided list above choose a team and user to assign") 
            teamChosen = input("Chosen Team -> ") 
            userChosen = input("Chosen User -> ") 
 
            # get the team from the string input 
            for team in user.personalTeams: 
                if str(team) == teamChosen: 
                    teamSelected = team 
                    break 
 
 
 
            # get the User from the string input 
            userSelected = None 
            for sUser in app.users: 
                if sUser.username == userChosen: 
                    userSelected = sUser 
                    break 
 
            user.assignUserToTeam(userSelected, teamSelected) 
            print("Team " + teamChosen + " has been assign to " + userChosen) 
 
        elif userInput == 'delete': 
            teamName = user.listTeams() 
 
            # Get input 
            print("Enter the team name you wish to delete") 
            teamNameDel = input("-> ") 
            team.deleteTeam(teamNameDel) 
 
        else: 
            print("Please pick either create or show, error checking") 
 
    # Projects Page 
    while onProjectPage == True: 
        # if there is a team show teams, if they arent, print show teams 
        print( 
            "To create a project type 'create' \nTo show your projects type 'show' \nTo delete a project type 'delete' " 
            "\nTo select a project type 'select' \nTo assign deadline priority to a project type 'priority'" 
            "\nTo view project completion type 'completion' \nTo go back to the team page type 'back'") 
        userInput = input("->") 
 
        if userInput == 'create': 
            print("Enter a project name: ") 
            projectName = input("-> ") 
            project = teamFocus.createProject(projectName) 
 
        elif userInput == 'show': 
            teamName = teamFocus.listProjects() 
 
        elif userInput == 'select': 
            print("Enter the project name you wish to select:") 
            selection = input("->") 
 
            for project in teamFocus.projects: 
                if selection == project.name: 
                    projectFocus = project 
                    onTaskPage = True 
                    onProjectPage = False 
                    break 
            print("Project not found") 
 
        elif userInput == 'priority': 
 
            # show all projects 
            projectName = teamFocus.listProjects() 
 
            print("From the provided list above choose a project and assign a priority") 
            projectChosen = input("Chosen Project -> ") 
            priorityChosen = input("Chosen Priority -> ") 
 
            # get the project from the string input 
            for project in teamFocus.projects: 
                if str(project) == projectChosen: 
                    project.addProjectDeadlinePriority(priorityChosen) 
                    break 
 
            print("Project " + projectChosen + " has been prioritized to " + priorityChosen) 
 
        elif userInput == 'completion': 
 
            # show all projects 
            projectName = teamFocus.listProjects() 
 
            print("From the provided list above choose a project to get completion rate") 
            projectChosen = input("Chosen Project -> ") 
 
            # get the project from the string input 
            completion = None 
            for project in teamFocus.projects: 
                if str(project) == projectChosen: 
                    completion = project.trackProgressProject() 
                    break 
 
            print("Project " + projectChosen + " is " + completion + " percent complete") 
 
        elif userInput == 'delete': 
            projectName = teamFocus.listProjects() 
 
            # Get input 
            print("Enter the project you wish to delete") 
            projectNameDel = input("-> ") 
 
            for project in teamFocus.pojects: 
                if (projectNameDel == str(project)): 
                    teamFocus.deleteProject(projectNameDel) 
 
        elif userInput == 'back': 
            onProjectPage = False 
            onTeamPage = True 
 
        else: 
            print("Please pick either create or show, error checking") 
 
    # Task Page 
    while onTaskPage == True: 
        if taskPage(projectFocus) == "break": 
            onTaskPage = False 
            onProjectPage = True 
 
 
if __name__ == "__main__": 
    main() 
 

 