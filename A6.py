import mysql.connector
from datetime import datetime
import os

mydb = None
cursor = None

#*************************************************************************************************
# These could change based on what your database and password for it are 
dbPassword = "1234"                                # INPUT YOUR DATABASE PASSWORD HERE
database = "mydatabase"                                 # INPUT YOUR DATABASE NAME HERE
path = "/Users/georgesalib/Downloads/327a4-main/A6/"    # INPUT YOUR FULL PROJECT DIRECTORY
#*************************************************************************************************

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

# HERE IS THE MEMBERS FOR A TEAM, AND TEAMS THAT A USER HAS
createUserTeamTable = """ 
    CREATE TABLE IF NOT EXISTS userteam( 
        userTeamID INT AUTO_INCREMENT PRIMARY KEY, 
        userID INT, 
        teamID INT, 
        FOREIGN KEY (userID) REFERENCES user (userID) ON DELETE CASCADE, 
        FOREIGN KEY (teamID) REFERENCES team (teamID) ON DELETE CASCADE 
        ); 
    """


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
def fetch_query(query: str, data = None):
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


def get_userID(username):
    query = "SELECT userID FROM user WHERE username = %s"
    data = (username,)
    result = fetch_query(query, data)
    if result:
        return result[0][0]
    else:
        return None


def get_projectID(project_name):
    query = "SELECT projectID FROM project WHERE projectName = %s"
    data = (project_name,)
    result = fetch_query(query, data)
    if result:
        return result[0][0]
    else:
        return None


def get_taskID(task_name, projectID):
    query = "SELECT taskID FROM task WHERE taskName = %s AND projectID = %s"
    data = (task_name, projectID)
    result = fetch_query(query, data)
    if result:
        return result[0][0]
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
            self.current_user = User(result[0][0])
            return True
        else:
            return False


def get_teamID(team_name):
    query = "SELECT teamID FROM team WHERE teamName = %s"
    data = (team_name,)
    result = fetch_query(query, data)
    if result:
        return result[0][0]
    else:
        return None


class User(App):

    def __init__(self, userID):
        self.current_user_userID = userID
        self.teamFocus = None

    def __str__(self):
        return self.current_user_userID

    # Create team, and assign self user to it
    def createTeam(self, newTeamName) -> bool:
        query = "SELECT EXISTS(SELECT * FROM team WHERE teamName = %s)"
        data = (newTeamName,)
        teamExists = fetch_query(query, data)[0][0]
        if teamExists:
            return False
        query = "INSERT INTO team (teamName) VALUES (%s)"
        data = (newTeamName,)
        teamID = execute_query_and_commit(query, data)
        query = "INSERT INTO userteam (userID, teamID) VALUES (%s, %s)"
        data = (self.current_user_userID, teamID)
        execute_query_and_commit(query, data)
        return True

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
            self.teamFocus = Team(teamID)
            return True
        else:
            return False

    def deleteTeam(self, teamName):
        teamID = get_teamID(teamName)
        if teamID is not None:
            data = (teamID,)
            query = "DELETE FROM team WHERE teamID = %s"
            execute_query_and_commit(query, data)
            query = "DELETE FROM userteam WHERE teamID = %s"
            execute_query_and_commit(query, data)
            return True
        else:
            return False


class Team(App):
    def __init__(self, teamID):
        # Initialize a Team object with a teamID
        self.teamID = teamID
        self.projectFocus = None

    def __str__(self):
        # Return a string representation of the Team object
        return self.teamID

    def assignToTeam(self, username):

        #WHITE BOX TESTING
        with open(path + 'WBTeamOutput.txt', 'a') as f:
            f.write("---->Block 4\n")

            # Assign a user (member) to the team
            if username.isalnum():
                f.write("---->Block 5\n")
                f.write("Check, Username is alphanumeric\n")

                userID = get_userID(username)

                if userID:
                    f.write("---->Block 6\n")
                    f.write("Check, Username has been found within the database\n")

                    print("")
                    query = "SELECT EXISTS(SELECT * FROM team WHERE teamID = %s);"
                    data = (self.teamID,)
                    teamResultExists = fetch_query(query, data)

                    if teamResultExists:
                        f.write("---->Block 7\n")
                        f.write("Check, Team has been found within the database\n")


                        query = "SELECT * FROM userteam WHERE userID = %s and teamID = %s"
                        data = (userID, self.teamID)
                        intersection = fetch_query(query, data)

                        if intersection:
                            f.write("---->Block 8\n")
                            print("This user is already assigned to this team")
                            return False

                        else:
                            f.write("---->Block 9\n")
                            query = "INSERT INTO userteam (userID, teamID) VALUES (%s,%s)"
                            data = (userID, self.teamID)
                            execute_query_and_commit(query, data)
                            return True

                    else:
                        f.write("---->Block 10\n")
                        f.write("FAILED, team does not exist in the database\n")
                        return False
                else:
                    f.write("---->Block 11\n")
                    f.write("FAILED, username does not exist in the database")
                    return False

            else:
                f.write("---->Block 12\n")
                f.write("FAILED, username passed is not alphanumeric")
                # write here to an open text file
                return False

    def createProject(self, newProjectName, priority) -> bool:
        query = "SELECT EXISTS(SELECT * FROM project WHERE projectName = %s)"
        data = (newProjectName,)
        projectExists = fetch_query(query, data)[0][0]
        if projectExists:
            print("Project name already exists. Please choose another name.")
            return False
        try:
            priority = int(priority)
        except ValueError:
            print("Priority must be an integer.")
            return False
        query = "INSERT INTO project (projectName, priority, teamID) VALUES (%s, %s, %s)"
        data = (newProjectName, priority, self.teamID)
        execute_query_and_commit(query, data)
        return True

    def listProjects(self) -> list:
        # List all projects associated with the team
        query = "SELECT projectName, priority FROM project WHERE teamID = %s"
        data = (self.teamID,)
        projects = fetch_query(query, data)
        return projects

    def deleteProject(self, project_name) -> bool:
        projectID = get_projectID(project_name)
        if projectID:
            query = "DELETE FROM project WHERE projectID = %s"
            data = (projectID,)
            execute_query_and_commit(query, data)
            return True
        else:
            return False

    def selectProject(self, project_name) -> bool:
        projectID = get_projectID(project_name)
        if projectID:
            self.projectFocus = Project(projectID)
            return True
        else:
            return False
    
    def listTeammates(self):
        # List all teammates associated with the team
        # Get the userID from the userteam
        query = "SELECT userID FROM userteam WHERE teamID = %s"
        data = (self.teamID,)  # Convert list to tuple for IN clause
        result = fetch_query(query, data)
        userIDs = [user[0] for user in result]

        # Get the username from the user
        placeholders = ', '.join(['%s'] * len(userIDs))
        query = "SELECT username FROM user WHERE userID IN (%s)" % placeholders
        data = userIDs  # Convert list to tuple for IN clause
        result = fetch_query(query, data)
        usernames = [user[0] for user in result]

        return usernames


class Project(App):
    def __init__(self, projectID):
        # Initialize a Project object with a projectID.
        self.projectID = projectID
        self.task = Task(self.projectID)

    def __str__(self):
        # Convert the Project object to a string, returning its projectID.
        return str(self.projectID)

    # Takes in project name and sorts it with all projects based on priority. Returns bool for success/fail.
    def addProjectDeadlinePriority(self, priority):
        pass

    def trackProgressProject(self):
        # Calculate the progress of the project by summing completed tasks.
        with open(path + 'WBProjectOutput.txt', 'a') as f:
            query = "SELECT taskID FROM task WHERE projectID = %s AND completed = 1"  # Statement 1
            f.write("Statement 1\n")
            data = (self.projectID,)  # Statement 2
            f.write("Statement 2\n")
            tasks_completed = fetch_query(query, data)  # Statement 3
            f.write("Statement 3\n")
            query = "SELECT taskID FROM task WHERE projectID = %s"  # Statement 4
            f.write("Statement 4\n")
            data = (self.projectID,)  # Statement 5
            f.write("Statement 5\n")
            tasks_total = fetch_query(query, data)  # Statement 6
            f.write("Statement 6\n")
            if tasks_total:  # Statement 7
                f.write("Statement 7\n")
                ratio = len(tasks_completed) / len(tasks_total)  # Statement 8
                f.write("Statement 8\n")
                return ratio # Return the completion ratio.
            else:  # Statement 9
                f.write("Statement 9\n")
                return 0.0  # If there are no tasks, return 0.0.

    def createTask(self, title):
        # Create a new task associated with the project in the database.
        query = "SELECT EXISTS(SELECT * FROM task WHERE taskName = %s AND projectID = %s)"
        data = (title, self.projectID)
        taskExists = fetch_query(query, data)[0][0]
        if taskExists:
            return False
        query = "INSERT INTO task (projectID, taskName, completed) VALUES (%s, %s, 0)"
        data = (self.projectID, title)
        execute_query_and_commit(query, data)
        return True

    def listTasks(self):
        # List all the tasks associated with the project.
        query = "SELECT taskName, completed FROM task WHERE projectID = %s"
        data = (self.projectID,)
        tasks = fetch_query(query, data)
        if tasks:
            print("Tasks:")
            for task in tasks:
                taskName, completed = task
                print(f"Task Name: {taskName}, Completed: {'Yes' if completed else 'No'}")
        else:
            print("No tasks found for this project.")
        return tasks

    def deleteTask(self, taskName):
        # Delete a specific task associated with the project.
        taskID = get_taskID(taskName, self.projectID)
        if taskID is not None:
            query = "DELETE FROM task WHERE taskID = %s"
            data = (taskID,)
            execute_query_and_commit(query, data)
            return True
        else:
            return False

    def selectTask(self, taskName):
        # Select a task associated with the project.
        taskID = get_taskID(taskName, self.projectID)
        if taskID is not None:
            self.current_task = Task(taskID)
            return True
        else:
            return False


class Task:
    # Constructor for the Task class
    def __init__(self, projectID):
        self.projectID = projectID

    # Mark the task as completed in the database
    def complete(self, taskName):
        taskID = get_taskID(taskName, self.projectID)
        if taskID is not None:
            query = "UPDATE task SET completed = 1 WHERE taskID = %s"
            data = (taskID,)
            execute_query_and_commit(query, data)
            return True
        else:
            return False

    # Assign a member to the task in the database
    def assignMember(self, taskName, username) -> bool:
        taskID = get_taskID(taskName, self.projectID)
        userID = get_userID(username)
        if userID is None:
            print("User not found.")
            return False
        if taskID is None:
            print("Task not found.")
            return False
        query = "UPDATE task SET userID = %s WHERE taskID = %s"
        data = (userID, taskID)
        execute_query_and_commit(query, data)
        return True


def get_input(prompt: str):
    print("----\n" + prompt)
    return input("  -> ")


def list_users():
    # show all users
    query = "SELECT username FROM user"
    users = fetch_query(query)
    print("Listing all users:")
    for user in users:
        print(user)


def get_project_team_teammates(project: Project):
    # show all users that share the team containing the task's projectID
    
    # Get the teamID from the project
    query = "SELECT teamID FROM project WHERE projectID = %s"
    data = (project.projectID,)
    teamID = fetch_query(query, data)[0][0]

    team = Team(teamID)

    return team.listTeammates()


def main():
    # Initialization
    app = App()
    is_logged_in = False
    onTeamPage = False
    onProjectPage = False
    onTaskPage = False
    onTaskFocus = False
    while True:
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
            userInput = get_input(
                """To create a Team type 'create'
                To list your teams type 'list'
                To list members of a team type 'members'
                To delete a team type 'delete'
                To select a team  type 'select'
                To add a member to a team type 'assign'
                To go back to the login page type 'back'""")

            if userInput == 'create':
                teamName = get_input("Enter a team name: ")
                result = app.current_user.createTeam(teamName)
                if result:
                    print("Team created.")
                else:
                    print("Team name already exists. Please choose another name.")

            elif userInput == 'list':
                result = app.current_user.listTeams()
                if result:
                    print("Listing all of your teams:")
                    for team in result:
                        print(team[0])
                else:
                    print("There are no teams associated with your account. Please create a team.")

            elif userInput == 'select':
                team_name = get_input("Enter the team name you wish to select:")

                is_successful = app.current_user.selectTeam(team_name)
                if is_successful:

                    onProjectPage = True
                    onTeamPage = False
                else:
                    print("Select a valid team")

            elif userInput == 'delete':
                # Get input
                team_name = get_input("Enter the team name you wish to delete")
                result = app.current_user.deleteTeam(team_name)
                if result:
                    print("Team deleted.")
                else:
                    print("Team not found.")
            
            elif userInput == 'members':
                team_name = get_input("Enter the team name:")
                teamID = get_teamID(team_name)
                if teamID is None:
                    print("Team not found.")
                else:
                    team = Team(teamID)
                    result = team.listTeammates()
                    if result:
                        print(f"Listing all members of {team_name}:")
                        for teammate in result:
                            print(teammate)
                    else:
                        print(f"There are no teammates associated with {team_name}.")

            elif userInput == 'assign':

                # WHITE BOX TESTING
                # Create empty file if it doesn't exist, then close it
                if not os.path.exists('WBTeamOutput.txt'):
                    open(path + 'WBTeamOutput.txt', 'w').close()
                # Add test in append mode
                with open(path + 'WBTeamOutput.txt', 'a') as f:
                    f.write(f"\n\nassignToTeam 'white box block coverage test' {datetime.now()}:\n")
                    f.write("---->Block 1\n")
                    team_name = get_input("Enter the team name you wish to add members to:")
                    teamID = get_teamID(team_name)

                    # Check if selecting the team is successful
                    if teamID is not None:
                        f.write("---->Block 3\n")
                        team = Team(teamID)
                        f.flush() # flush the buffer to ensure the file is written to before the test is run
                        username = get_input("Enter the username you wish to add to this team:")
                        result = team.assignToTeam(username)

                        if result:
                            print(f"{username} assigned to {team_name}.\n")
                    else:
                        f.write("---->Block 13\n")
                        print("Select a valid team\n")
                    f.write(f"TEST COMPLETE\n")

            elif userInput == 'back':
                onTeamPage = False
                is_logged_in = False

            else:
                print("Please pick a valid option.")

        while onProjectPage:
            assert app.current_user
            assert app.current_user.teamFocus
            teamFocus = app.current_user.teamFocus
            # if there is a team show teams, if they arent, print show teams
            userInput = get_input(
                """To create a project type 'create'
                To list your projects type 'list'
                To delete a project type 'delete' 
                To select a project type 'select' 
                To go back to the team page type 'back'""")

            if userInput == 'create':
                project_name = get_input("Enter a project name: ")
                project_priority = get_input("Enter a project priority: ")
                result = teamFocus.createProject(project_name, project_priority)
                if result:
                    print("Project created.")

            elif userInput == 'list':

                projects = teamFocus.listProjects()
                if projects:
                    print("Listing projects:")
                    for project in projects:
                        project_name, project_priority = project
                        print(f"Project Name: {project_name}, Priority: {project_priority}")
                else:
                    print("No projects found for this team.")

            elif userInput == 'select':
                project_name = get_input("Enter the project name you wish to select:")
                is_successful = teamFocus.selectProject(project_name)
                if is_successful:

                    onProjectPage = False
                    onTaskPage = True
                else:
                    print("Select a valid team")

            elif userInput == 'delete':
                # Get input
                project_name = get_input("Enter the project you wish to delete")

                result = teamFocus.deleteProject(project_name)
                if result:
                    print("Project deleted.")
                else:
                    print("Project not found.")

            elif userInput == 'back':
                onProjectPage = False
                onTeamPage = True

            else:
                print("Please enter valid input")

                # Task Page
        while onTaskPage == True:
            assert app.current_user
            assert app.current_user.teamFocus
            assert app.current_user.teamFocus.projectFocus
            projectFocus = app.current_user.teamFocus.projectFocus

            userInput = get_input(
                """
                To get project completion percentage type 'completion'
                To create a task type 'create'
                To list your tasks type 'list'
                To delete a task type 'delete' 
                To mark a task as completed type 'complete' 
                To assign a task to a team member type 'assign'
                To go back to the project page type 'back'""")

            if userInput == 'create':
                task_name = get_input("Enter a task name: ")
                result = projectFocus.createTask(task_name)
                if result:
                    print("Task created.")
                else:
                    print("Task name already exists. Please choose another name.")

            elif userInput == 'list':
                projectFocus.listTasks()

            elif userInput == "complete":
                task_name = get_input("Enter the task name you wish to select:")
                result = projectFocus.task.complete(task_name)
                if result:
                    print("Task completed")
                else:
                    print("Task name not found")

            elif userInput == 'assign':
                task_name = get_input("Enter the task name you wish to select:")
                print("Listing your teammates:")
                teammates = get_project_team_teammates(projectFocus)
                for username in teammates:
                    print(username)
                username = get_input("Enter the username of the teammate you wish to assign the task to:")
                result = projectFocus.task.assignMember(task_name, username)
                if result:
                    print(f"{username} assigned to {task_name}.")


            elif userInput == 'completion':
                # get the completion percentage of the project
                # WHITE BOX TESTING
                # Create empty file if it doesn't exist, then close it
                if not os.path.exists('WBProjectOutput.txt'):
                    open(path + 'WBProjectOutput.txt', 'w').close()
                # Add test in append mode
                with open(path + 'WBProjectOutput.txt', 'a') as f:
                    f.write(f"\n\ntrackProgressProject 'white box statement coverage test' {datetime.now()}:\n")
                    f.flush() # flush the buffer to ensure the file is written to before the test is run
                    completion = projectFocus.trackProgressProject()
                    print(f"Project is {completion * 100}% percent complete")

                    f.write(f"TEST COMPLETE\n")
                    f.flush()

            elif userInput == 'delete':
                # Get input
                task_name = get_input("Enter the task name you wish to delete")
                result = projectFocus.deleteTask(task_name)
                if result:
                    print("Task deleted.")
                else:
                    print("Task not found.")

            elif userInput == 'back':
                onProjectPage = True
                onTaskPage = False

            else:
                print("Please enter valid input")


if __name__ == "__main__":
    main()


