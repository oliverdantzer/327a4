import mysql.connector


mydb = None
cursor = None
# These could change based on what your database and password for it are 
dbPassword = "1234" 
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
    completed VARCHAR(255) NOT NULL, 
    taskName VARCHAR(255) NOT NULL,
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

# Executes query with data and returns the result as list
def fetch_query(query: str, data: tuple = ()):
    # print(query, data)
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    assert result != None
    return result


# Executes query with data and commits the changes
def execute_query_and_commit(query: str, data: tuple):
    # print(query, data)
    cursor.execute(query, data)
    mydb.commit()
    return cursor.lastrowid


def userExists(username, password):
    # Check if a user with the given username and password exists
    query = "SELECT * FROM user WHERE username = %s AND password = %s;"
    data = (username, password)

    return bool(fetch_query(query, data))

def get_projectID(project_name):
    query = "SELECT projectName FROM project WHERE projectName = %s" 
    data = (project_name, ) 
    result = fetch_query(query, data)
    if result:
        return result[0]
    else:
        return None

def get_taskID(task_name, projectID):
    query = "SELECT taskID FROM task WHERE taskName = %s AND projectID = %s" 
    data = (task_name, projectID) 
    result = fetch_query(query, data)
    if result:
        return result[0]
    else:
        return None


class App:
    def __init__(self):
        self.current_user: User | None = None

    def register(self, username, password):
        # Register a new user
        if userExists(username, password):
            return False
        data = (username, password)
        query = "INSERT INTO user (username, password) VALUES (%s, %s);"
        execute_query_and_commit(query, data)
        return True

    def login(self, username, password):
        # User login
        data = (username, password)
        query = "SELECT userID FROM user WHERE username = %s AND password = %s;"
        result = fetch_query(query, data)
        if result:
            self.current_user = User(result[0])
            return True
        else:
            return False
 

def get_teamID(team_name):
    query = "SELECT teamID FROM team WHERE teamName = %s" 
    data = (team_name, )
    result = fetch_query(query, data)
    if result:
        return result[0]
    else:
        return None

 
class User(App): 
 
    def __init__(self, userID): 
        self.current_user_userID = userID
        self.teamFocus = None
 
    def __str__(self): 
        return self.current_user_userID
    
    # Create team, and assign self user to it
    def createTeam(self, newTeamName):
        query = "INSERT INTO team (teamName) VALUES (%s, %s, %s)"
        data = (newTeamName, )
        teamID = execute_query_and_commit(query, data)
        query = "INSERT INTO userteam (userID, teamID) VALUES (%s, %s)"
        data = (self.current_user_userID, teamID)
        execute_query_and_commit(query, data)
        
    # List teams user is in
    def listTeams(self): 
        # query = "SELECT teamID FROM userteam WHERE userID = %s"
        # data = (self.userID,)
        # teamIDs = fetch_query(query, data)
        # teamNames = []
        # for teamID in teamIDs:
        #     query = "SELECT teamName FROM team WHERE teamID = %s" 
        #     data = (teamID,)
        #     teamName = fetch_query(query, data)[0]
        #     teamNames.append(teamName)
        query = """
            SELECT team.teamName 
            FROM team 
            JOIN userteam ON team.teamID = userteam.teamID 
            WHERE userteam.userID = %s
        """
        data = (self.current_user_userID,)
        teamNames = fetch_query(query, data)
        return teamNames
    
    def selectTeam(self, teamName):
        teamID = get_teamID(teamName)
        if teamID is not None:
            self.team = Team(teamID)
            return True
        else:
            return False
    
    def deleteTeam(self, teamName):
        teamID = get_teamID(teamName)
        if teamID is not None:
            data = (teamID,)
            query = "DELETE FROM team WHERE teamName = %s"
            query = "DELETE FROM userteam WHERE teamName = %s"
            execute_query_and_commit(query, data)
            return True
        else:
            return False

 
class Team(App):
    def __init__(self, teamID):
        # Initialize a Team object with a teamID
        self.teamID = teamID

    def __str__(self):
        # Return a string representation of the Team object
        return self.teamID

    def assignToTeam(self, username):
        # Assign a user (member) to the team
        query = "SELECT userID FROM user WHERE username = %s"
        data = (username,)
        result = fetch_query(query, data)
        if result:
            userID = result[0]
            query = "INSERT INTO userteam (userID, teamID) VALUES (%s,%s)"
            data = (userID, self.teamID)
            execute_query_and_commit(query, data)
        else:
            return False

    def createProject(self, newProjectName, priority):
        query = "INSERT INTO project (projectName, priority, teamID) VALUES (%s, %s, %s)"
        data = (newProjectName, priority, self.teamID)
        execute_query_and_commit(query, data)

    def listProjects(self):
        # List all projects associated with the team
        query = "SELECT projectName, priority FROM project WHERE teamID = %s"
        data = (self.teamID,)
        projects = fetch_query(query, data)

        if projects:
            print("Projects:")
            for project in projects:
                project_name, project_priority = project
                print(f"Project Name: {project_name}, Priority: {project_priority}")
        else:
            print("No projects found for this team.")
    
    def deleteProject(self, project_name):
        projectID = get_projectID(project_name)
        if projectID:
            query = "DELETE FROM project WHERE projectID = %s"
            data = (projectID,)
            execute_query_and_commit(query, data)
            return True
        else:
            return False
        
 
 
class Project(App):
    def __init__(self, projectID):
        # Initialize a Project object with a projectID.
        self.projectID = projectID

    def __str__(self):
        # Convert the Project object to a string, returning its projectID.
        return str(self.projectID)

    # Takes in project name and sorts it with all projects based on priority. Returns bool for success/fail. 
    def addProjectDeadlinePriority(self, priority):
        # I don't understand what this method is supposed to do.
        pass

    def trackProgressProject(self):
        # Calculate the progress of the project by summing completed tasks.
        query = "SELECT completed FROM task WHERE projectID = %s"
        data = (self.projectID, )
        tasks_completion = fetch_query(query, data)
        if tasks_completion:
            completed_sum = sum(completed == 1 for completed in tasks_completion)
            num_tasks = len(tasks_completion)
            return completed_sum / num_tasks  # Return the completion ratio.
        else:
            return 0.0  # If there are no tasks, return 0.0.

    def createTask(self, title):
        # Create a new task associated with the project in the database.
        query = "INSERT INTO task (projectID, title, completed) VALUES (%s, %s, 0)"

        cursor.execute(, (self.projectID, title))
        mydb.commit()

    def listTasks(self):
        # List all the tasks associated with the project.
        query = "SELECT taskName, completed FROM task WHERE projectID = %s"
        data = (self.projectID,)
        tasks = fetch_query(query, data)
        if tasks:
            print("Tasks:")
            for task in tasks:
                taskName, completed = task
                print(f"Project Name: {project_name}, Priority: {project_priority}")
        else:
            print("No tasks found for this project.")

    def deleteTask(self, taskName):
        # Delete a specific task associated with the project.
        taskID = get_taskID(taskName, self.projectID)
        if taskID is not None:
            query = "DELETE FROM task WHERE taskID = %s"
            data = (self.projectID, taskName)
            execute_query_and_commit(query, data)
            return True
        else:
            return False
    
    def selectTask(self, taskName):
        # Select a task associated with the project.
        taskID = get_taskID(taskName)
        if taskID is not None:
            self.current_task = Task(taskID)
            return True
        else:
            return False
 
 
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
 
 
def get_input(prompt: str):
    print(prompt)
    input("  -> ")

def list_users():
    print("Listing all users:") 
    # show all users 
    query = "SELECT username FROM user"
    users = fetch_query(query)
    for user in users:
        print(user)

def main(): 
 
    # Initialization 
    app = App() 
    is_logged_in = False 
    onTeamPage = False 
    onProjectPage = False 
    onTaskPage = False 
    teamFocus = None 
    projectFocus = None
 
    # Login / Registry 
    while is_logged_in == False: 
        userInput = get_input("Enter 'l' to login or 'r' to register.")
 
        if userInput == 'r': 
            username = get_input("Enter a username: ")
            password = get_input("Enter a password: ")
            is_registered = app.register(username, password)
            if is_registered is True: 
                print("Registration successful. Proceed to login.") 
            else: 
                print("Username already exists.")
        elif userInput == 'l': 
            username = get_input("Enter your username: ")
            password = get_input("Enter your password: ")
            is_logged_in = app.login(username, password) 
            if is_logged_in is True: 
                print("Login successful.")
                onTeamPage = True
            else:
                print("Invalid username or password.")
        else: 
            print("Please pick either l or p") 
 
    # print("Thank you for loggin in" + user.username) 
 
    # Teams / Home Page 
    while onTeamPage == True:
        assert app.current_user != None
        # if there is a team show teams, if they arent, print show teams 
        userInput = get_input("To create a Team type 'create' \nTo list your teams type 'list' \nTo delete a team type 'delete' \nTo " 
              "select a team  type 'select' \nTo assign a team  type 'assign'")
 
        if userInput == 'create': 
            teamName = get_input("Enter a team name: ")
            team = app.current_user.createTeam(teamName) 
 
        elif userInput == 'list': 
            print("Listing all of your teams:")
            teamName = app.current_user.listTeams() 
 
        elif userInput == 'select': 
            team_name = get_input("Enter the team name you wish to select:")
 
            is_successful = app.current_user.selectTeam(team_name)
            if is_successful: 
                print(f"You are viewing the project page associated to team {team_name}.")
                onProjectPage = True 
                onTeamPage = False 
            else: 
                print("Select a valid team") 
 
        # elif userInput == 'assign': 
        #     list_users()
 
        #     print("From the provided list above choose a user to assign to a team") 
        #     teamChosen = get_input("Choose a team:") 
        #     userChosen = get_input("Choose a user:") 
        #     user.assignUserToTeam(userSelected, teamSelected) 
        #     print("Team " + teamChosen + " has been assign to " + userChosen) 
 
        elif userInput == 'delete': 
            # Get input 
            print("Enter the team name you wish to delete") 
            team_name = input("-> ") 
            app.current_user.deleteTeam(team_name) 
 
        else: 
            print("Please pick either create or show, error checking") 
 
    # Projects Page 
    while onProjectPage == True: 
        # if there is a team show teams, if they arent, print show teams 
        userInput = get_input( 
            "To create a project type 'create' \nTo show your projects type 'show' \nTo delete a project type 'delete' " 
            "\nTo select a project type 'select' \nTo assign deadline priority to a project type 'priority'" 
            "\nTo view project completion type 'completion' \nTo go back to the team page type 'back'")
 
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
 

 