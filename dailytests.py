# Daily tests file ensuring main code functions execute properly on a daily bases

import A6 as application
import unittest
from datetime import datetime

test_instance = application.App()
test_user_instance = None
team_focus = None
project_focus = None

class Tests(unittest.TestCase):
    # Test function to make sure registration works
    def test_Register(self):
        # User data to be inserted
        demoUsername = "MyDailyUserName"
        demoPassword = "12345678"

        global test_instance

        self.assertIsNotNone(test_instance)

        # Inserting user data through function to database and seing if it is on database
        result = test_instance.register(demoUsername, demoPassword)
        does_exist = application.userExists(demoUsername, demoPassword)

        # Asserting registration was sucessful and values in database match original data
        self.assertTrue(result)
        self.assertTrue(does_exist)

    # Test function to make sure login works with valid login credentials in the database
    def test_Login(self):
        # User data to be inserted
        demoUsername = "MyDailyUserName"
        demoPassword = "12345678"

        global test_instance, test_user_instance

        # Insterting into the database 
        result = test_instance.login(demoUsername, demoPassword)
        test_user_instance = test_instance.current_user

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)

        self.assertTrue(result, 'The username \"{0}\" and password \"{1}\" does not exist in the database'.format(demoUsername, demoPassword))

    # Test if team creation works
    def test_TeamCreation(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus
        
        # Create team and see if it exists in database
        test_user_instance.createTeam(demo_team)
        result = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)

        # Assert that the team was created
        self.assertTrue(result)

    # Tests if team listing works
    def test_listTeams(self):
        # Second team name to be inserted
        demo_second_team = "MyTeam2"

        global test_instance, test_user_instance, team_focus
        
        # Create team and see if it exists in database
        test_user_instance.createTeam(demo_second_team)
        team_created = test_user_instance.selectTeam(demo_second_team)
        team_focus = test_user_instance.teamFocus

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)

        # Assert that the team was created
        self.assertTrue(team_created)

        # Get list of teams
        result = test_user_instance.listTeams()

        self.assertEqual(result, [("MyTeam",), ("MyTeam2",)])

    # Tests if team selection works
    def test_selectTeam(self):
        global test_instance, test_user_instance, team_focus
        
        # Select team
        result = test_user_instance.selectTeam("MyTeam")

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)

        # Check if the team was selected sucessfully
        self.assertTrue(result)

    # Test if project creation works
    def test_ProjectCreation(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus
        
        # Create team and set as focus
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "MyProject"
        demo_project_priority = 1

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        project = team_focus.createProject(demo_project, demo_project_priority)
        result = team_focus.selectProject(demo_project)

        # Assert that the project was created
        self.assertTrue(result)

    # Tests if project listing works
    def test_listProjects(self):
        # Team name
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus
        
        # Create team and set as focus
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Second project name to be inserted
        demo_second_project = "MyProject2"
        demo_second_project_priority = 2

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        project = team_focus.createProject(demo_second_project, demo_second_project_priority)
        project_created = team_focus.selectProject(demo_second_project)

        # Assert that the project was created
        self.assertTrue(project_created)

        # Get list of projects
        result = team_focus.listProjects()

        self.assertEqual(result, [("MyProject", 1), ("MyProject2", 2)])

    # Tests if project selection works
    def test_selectProject(self):
        global test_instance, test_user_instance, team_focus
        
        # Select project
        result = team_focus.selectProject("MyProject")

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)

        # Check if the team was selected sucessfully
        self.assertTrue(result)

    # Tests if task creation works
    def test_createTask(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus, project_focus
        
        # Create team and set as focus
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "MyProject"
        demo_project_priority = 1

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        project = team_focus.createProject(demo_project, demo_project_priority)
        project_created = team_focus.selectProject(demo_project)

        # Set project focus
        project_focus = team_focus.projectFocus
        self.assertIsNotNone(project_focus)

        # Task name to be inserted
        demo_task = "MyTask"

        # Create task and see if it exists in database
        task = project_focus.createTask(demo_task)
        result = project_focus.selectTask(demo_task)

        # Assert that the task was created
        self.assertTrue(result)

    # Tests if task listing works
    def test_listTasks(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus, project_focus
        
        # Create team and set as focus
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "MyProject"
        demo_project_priority = 1

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        project = team_focus.createProject(demo_project, demo_project_priority)
        project_created = team_focus.selectProject(demo_project)

        # Set project focus
        project_focus = team_focus.projectFocus

        self.assertIsNotNone(project_focus)

        # Second task name to be inserted
        demo_second_task = "MyTask2"

        # Create task and see if it exists in database
        task = project_focus.createTask(demo_second_task)
        result = project_focus.listTasks()

        # Assert that the task was created
        self.assertEqual(result, [("MyTask", 1), ("MyTask2", 0)])

    # Tests if task selection works
    def test_selectTask(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus, project_focus
        
        # Create team and set as focus
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "MyProject"
        demo_project_priority = 1

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        project = team_focus.createProject(demo_project, demo_project_priority)
        project_created = team_focus.selectProject(demo_project)

        # Set project focus
        project_focus = team_focus.projectFocus

        self.assertIsNotNone(project_focus)

        result = project_focus.selectTask("MyTask")

        # Check if task selected sucessfully
        self.assertTrue(result)

    # Tests if task completion works
    def test_MarkedAsComplete(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus
        
        # Create team and set as focus
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "MyProject"
        demo_project_priority = 1

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        team_focus.createProject(demo_project, demo_project_priority)
        project_created = team_focus.selectProject(demo_project)
        project_focus = team_focus.projectFocus

        self.assertIsNotNone(project_focus)

        # Task name to be inserted
        demo_task = "MyTask"

        # Create task and assigning it as complete
        task = project_focus.createTask(demo_task)
        result = project_focus.task.complete(demo_task)

        # Check if task is completed
        self.assertTrue(result)

    # Test if progress tracking works
    def test_ProgressTrack(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus
        
        # Create team and set as focus
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "MyProject"
        demo_project_priority = 1

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        team_focus.createProject(demo_project, demo_project_priority)
        project_created = team_focus.selectProject(demo_project)
        project_focus = team_focus.projectFocus
        
        # Create project and tasks
        task1 = application.Task(project_focus.projectID)
        task2 = application.Task(project_focus.projectID)
        task3 = application.Task(project_focus.projectID)
        
        # Assign completion status of each task
        task1.completed = True
        task2.completed = True
        task3.completed = True

        # Assign tasks to croject
        project_focus.tasks = [task1, task2, task3]

        # Assert if track progress works
        #self.assertEqual(project_focus.trackProgressProject(), 1)

    # Test if projects can be prioritised
    def test_SetPriority(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus
        
        # Create team and set as focus
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "MyProject"
        demo_project_priority = 1

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        team_focus.createProject(demo_project, demo_project_priority)
        project_created = team_focus.selectProject(demo_project)
        project_focus = team_focus.projectFocus

        result = project_focus.addProjectDeadlinePriority(demo_project_priority)

        # Assert if priority function works
        self.assertEqual(result, 1)

    # Tests if member assignment to team works
    def test_AssignToTeam(self):
        # Team name to be inserted
        demoUsername = "MyUserName"
        demoPassword = "12345678"
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus
        
        # Create team and set as focus
        test_instance.login(demoUsername, demoPassword)
        test_user_instance = test_instance.current_user
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Assign to team
        result = team_focus.assignToTeam(demoUsername)
        self.assertTrue(result)

    # Tests if user task assignment works
    def test_assignToTask(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus, project_focus
        
        # Create team and set as focus
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "MyProject"
        demo_project_priority = 1

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)
        
        # Create project and see if it exists in database
        project = team_focus.createProject(demo_project, demo_project_priority)
        project_created = team_focus.selectProject(demo_project)

        # Set project focus
        project_focus = team_focus.projectFocus
        self.assertIsNotNone(project_focus)

        # Task name to be inserted
        demo_task = "MyTask"

        # Create task and see if it exists in database
        task = project_focus.createTask(demo_task)

        result = project_focus.task.assignMember(demo_task, "MyUserName")

        # Assert that the task assignment succeded
        self.assertTrue(result)

    # Tests if task deletion works
    def test_deleteTask(self):
        local_test_instance = application.App()
        local_test_instance.register("deleteUser", "deletePass")
        local_test_instance.login("deleteUser", "deletePass")
        local_test_user_instance = local_test_instance.current_user
        
        # Team name to be inserted
        demo_team = "DeleteTeam"
        
        # Create team and set as focus
        local_test_user_instance.createTeam(demo_team)
        team_created = local_test_user_instance.selectTeam(demo_team)
        local_team_focus = local_test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "DeleteProject"
        demo_project_priority = 1

        self.assertIsNotNone(local_test_instance)
        self.assertIsNotNone(local_test_user_instance)
        self.assertIsNotNone(local_team_focus)
        
        # Create project and see if it exists in database
        project = local_team_focus.createProject(demo_project, demo_project_priority)
        project_created = local_team_focus.selectProject(demo_project)

        # Set project focus
        local_project_focus = local_team_focus.projectFocus
        self.assertIsNotNone(local_project_focus)

        # Task name to be inserted
        demo_task = "DeleteTask"

        # Create task and then delete it
        task = local_project_focus.createTask(demo_task)
        result = local_project_focus.deleteTask(demo_task)

        # Check is deletion suceeded
        self.assertTrue(result)

    # Tests if project deletion works
    def test_deleteProject(self):
        local_test_instance = application.App()
        local_test_instance.register("deleteUser", "deletePass")
        local_test_instance.login("deleteUser", "deletePass")
        local_test_user_instance = local_test_instance.current_user
        
        # Team name to be inserted
        demo_team = "DeleteTeam"
        
        # Create team and set as focus
        local_test_user_instance.createTeam(demo_team)
        team_created = local_test_user_instance.selectTeam(demo_team)
        local_team_focus = local_test_user_instance.teamFocus
        
        # Project name to be inserted
        demo_project = "DeleteProject"
        demo_project_priority = 1

        self.assertIsNotNone(local_test_instance)
        self.assertIsNotNone(local_test_user_instance)
        self.assertIsNotNone(local_team_focus)
        
        # Create project and see if it exists in database
        project = local_team_focus.createProject(demo_project, demo_project_priority)
        result = local_team_focus.deleteProject(demo_project)

        # Check is deletion suceeded
        self.assertTrue(result)

    # Tests if team deletion works
    def test_deleteTeam(self):
        local_test_instance = application.App()
        local_test_instance.register("deleteUser", "deletePass")
        local_test_instance.login("deleteUser", "deletePass")
        local_test_user_instance = local_test_instance.current_user
        
        # Team name to be inserted
        demo_team = "DeleteTeam"
        
        # Create team and set as focus
        local_test_user_instance.createTeam(demo_team)
        result = local_test_user_instance.deleteTeam(demo_team)

        # Check is deletion suceeded
        self.assertTrue(result)



if __name__ == '__main__':

    # Using a context manager to ensure the file is properly closed
    with open(application.path + "daily_test_results.txt", "a") as f:
        f.write(f"\n\n\n**************************************************************\n")
        f.write(f"Daily testing performance on {datetime.now()}:\n")
        f.write(f"**************************************************************\n\n")

        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(Tests)

        runner = unittest.TextTestRunner(verbosity=2, stream=f)
        result = runner.run(suite)
