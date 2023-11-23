import mysql.connector

mydb = None
cursor = None
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

# TODO add the required parameters
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
    def createTeam(self, newTeamName):
        query = "INSERT INTO team (teamName) VALUES (%s)"
        data = (newTeamName,)
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
        return projects

    def deleteProject(self, project_name):
        projectID = get_projectID(project_name)
        if projectID:
            query = "DELETE FROM project WHERE projectID = %s"
            data = (projectID,)
            execute_query_and_commit(query, data)
            return True
        else:
            return False

    def selectProject(self, project_name):
        projectID = get_projectID(project_name)
        if projectID:
            self.projectFocus = Project(projectID)
            return True
        else:
            return False


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
        # I don't understand what this method is supposed to do.
        pass

    def trackProgressProject(self):
        # Calculate the progress of the project by summing completed tasks.
        query = "SELECT completed FROM task WHERE projectID = %s"
        data = (self.projectID,)
        tasks_completion = fetch_query(query, data)
        if tasks_completion:
            completed_sum = sum(completed == 1 for completed in tasks_completion)
            num_tasks = len(tasks_completion)
            return completed_sum / num_tasks  # Return the completion ratio.
        else:
            return 0.0  # If there are no tasks, return 0.0.

    def createTask(self, title):
        # Create a new task associated with the project in the database.
        query = "INSERT INTO task (projectID, taskName, completed) VALUES (%s, %s, 0)"
        data = (self.projectID, title)
        execute_query_and_commit(query, data)

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
    def assignMember(self, taskName, username):
        taskID = get_taskID(taskName, self.projectID)
        query = "SELECT userID FROM user WHERE username = %s"
        data = (username,)
        userID = fetch_query(query, data)
        if taskID is not None:
            query = "UPDATE task SET userID = %s WHERE taskID = %s"
            data = (userID, taskID)
            execute_query_and_commit(query, data)
            return True
        else:
            return False


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
    query = "SELECT username FROM user WHERE userID IN (SELECT userID FROM userteam WHERE teamID IN (SELECT teamID FROM project WHERE projectID = %s))"
    data = (project.projectID,)
    users = fetch_query(query, data)
    return users


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
                To delete a team type 'delete'
                To select a team  type 'select'
                To go back to the login page type 'back'""")

            if userInput == 'create':
                teamName = get_input("Enter a team name: ")
                app.current_user.createTeam(teamName)
                print("Team created.")

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
                project = teamFocus.createProject(project_name, project_priority)

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

                teamFocus.deleteProject(project_name)

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
                """To create a task type 'create'
                To list your tasks type 'list'
                To delete a task type 'delete' 
                To mark a task as completed type 'complete' 
                To assign a task to a team member type 'assign'
                To go back to the project page type 'back'""")

            if userInput == 'create':
                task_name = get_input("Enter a task name: ")
                projectFocus.createTask(task_name)
                print("Task created.")

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
                for username in get_project_team_teammates(projectFocus):
                    print(username)
                username = get_input("Enter the username of the teammate you wish to assign the task to:")
                projectFocus.task.assignMember(task_name, username)
                print(f"{username} assigned to {task_name}.")


            elif userInput == 'completion':
                completion = projectFocus.trackProgressProject()

                print(f"Project is {completion * 100}% percent complete")

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


