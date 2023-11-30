# This file tests various functionalities of the code ensuring it works

import A5 as application
import unittest

test_instance = application.App()
test_user_instance = None
team_focus = None

class Tests(unittest.TestCase):
    #********************************************
    # Black Box Partitioning Test 1: Registration
    #********************************************
    # Test function to make sure registration works
    def test_Register_1(self):
        # User data to be inserted
        demoUsername = "MyUserName"
        demoPassword = "12345678"

        global test_instance

        self.assertIsNotNone(test_instance)

        # Inserting user data through function to database and seing if it is on database
        success = test_instance.register(demoUsername, demoPassword)
        does_exist = application.userExists(demoUsername, demoPassword)

        # Asserting registration was sucessful and values in database match original data
        self.assertTrue(success)
        self.assertTrue(does_exist)

    # Test function to make sure registration fails if user already exists
    def test_Register_2(self):
        # User data to be inserted
        demoUsername = "MyUserName"
        demoPassword = "12345678"

        global test_instance

        self.assertIsNotNone(test_instance)

        # Inserting user data through function to database and seing if it is on database
        success = test_instance.register(demoUsername, demoPassword)
        does_exist = application.userExists(demoUsername, demoPassword)

        # Asserting registration was not sucessful
        self.assertFalse(success)
        self.assertTrue(does_exist)
    
    # Test function to make sure registration fails if no password given
    def test_Register_3(self):
        # User data to be inserted
        demoUsername = "MyUserName"
        demoPassword = ""

        global test_instance

        self.assertIsNotNone(test_instance)

        # Inserting user data through function to database and seing if it is on database
        success = test_instance.register(demoUsername, demoPassword)
        does_exist = application.userExists(demoUsername, demoPassword)

        # Asserting registration was not sucessful
        self.assertFalse(success)
        self.assertTrue(does_exist)

    # Test function to make sure registration fails if no username given
    def test_Register_4(self):
        # User data to be inserted
        demoUsername = ""
        demoPassword = "12345678"

        global test_instance

        self.assertIsNotNone(test_instance)

        # Inserting user data through function to database and seing if it is on database
        success = test_instance.register(demoUsername, demoPassword)
        does_exist = application.userExists(demoUsername, demoPassword)

        # Asserting registration was not sucessful
        self.assertFalse(success)
        self.assertTrue(does_exist)
    
    # Test function to make sure registration fails if nothing is given
    def test_Register_5(self):
        # User data to be inserted
        demoUsername = ""
        demoPassword = ""

        global test_instance

        self.assertIsNotNone(test_instance)

        # Inserting user data through function to database and seing if it is on database
        success = test_instance.register(demoUsername, demoPassword)
        does_exist = application.userExists(demoUsername, demoPassword)

        # Asserting registration was not sucessful
        self.assertFalse(success)
        self.assertTrue(does_exist)

    #********************************************
    # Black Box Partitioning Test 2: Login
    #********************************************
    # Test function to make sure login works with valid login credentials in the database
    def test_Login_1(self):
        # User data to be inserted
        demoUsername = "MyUserName"
        demoPassword = "12345678"

        global test_instance, test_user_instance

        # Insterting into the database 
        success = test_instance.login(demoUsername, demoPassword)
        test_user_instance = test_instance.current_user

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)

        self.assertTrue(success, 'The username \"{0}\" and password \"{1}\" does not exist in the database'.format(demoUsername, demoPassword))

    # Entering login information that is valid but not in the database
    def test_Login_2(self):
        # User data to be inserted
        demoUsername = "random"
        demoPassword = "12345678"

        global test_instance, test_user_instance

        # Insterting into the database 
        success = test_instance.login(demoUsername, demoPassword)
        test_user_instance = test_instance.current_user

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)

        self.assertFalse(success, 'The username \"{0}\" and password \"{1}\" does not exist in the database'.format(demoUsername, demoPassword))

    # Entering login information without a password
    def test_Login_3(self):
        # User data to be inserted
        demoUsername = "MyUserName"
        demoPassword = None

        global test_instance, test_user_instance

        # Insterting into the database 
        success = test_instance.login(demoUsername, demoPassword)
        test_user_instance = test_instance.current_user

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)

        self.assertFalse(success, 'The username \"{0}\" and password \"{1}\" does not exist in the database'.format(demoUsername, demoPassword))

    # Entering login information without a username
    def test_Login_4(self):
        # User data to be inserted
        demoUsername = None
        demoPassword = "12345678"

        global test_instance, test_user_instance

        # Insterting into the database 
        success = test_instance.login(demoUsername, demoPassword)
        test_user_instance = test_instance.current_user

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)

        self.assertFalse(success, 'The username \"{0}\" and password \"{1}\" does not exist in the database'.format(demoUsername, demoPassword))
    
    def test_Login_5(self):
        # User data to be inserted
        demoUsername = None
        demoPassword = None

        global test_instance, test_user_instance

        # Insterting into the database 
        success = test_instance.login(demoUsername, demoPassword)
        test_user_instance = test_instance.current_user

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)

        self.assertFalse(success, 'The username \"{0}\" and password \"{1}\" does not exist in the database'.format(demoUsername, demoPassword))

    # Test if team creation works
    def test_TeamCreation(self):
        # Team name to be inserted
        demo_team = "MyTeam"

        global test_instance, test_user_instance, team_focus
        
        # Create team and see if it exists in database
        test_user_instance.createTeam(demo_team)
        team_created = test_user_instance.selectTeam(demo_team)
        team_focus = test_user_instance.teamFocus

        self.assertIsNotNone(test_instance)
        self.assertIsNotNone(test_user_instance)
        self.assertIsNotNone(team_focus)

        # Assert that the team was created
        self.assertTrue(team_created)

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
        project_created = team_focus.selectProject(demo_project)

        # Assert that the project was created
        self.assertTrue(project_created)

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

        task1 = application.Task(project_focus.projectID)

        # Assuming 'completed' is the second column in the task table
        #self.assertEqual(task1.complete("task1"), "true")

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

        new_priority = project_focus.addProjectDeadlinePriority(demo_project_priority)

        # Assert if priority function works
        self.assertEqual(new_priority, 1)


    #********************************************
    # White Box Test 1: assignToTeam()
    #********************************************
    # Tests if task completion works
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
        
        # Create project and see if it exists in database
        assignment_sucess = team_focus.assignToTeam(demoUsername)
        self.assertTrue(assignment_sucess)


    #********************************************
    # White Box Test 2: trackProgressProject()
    #********************************************
    
    #     assign_3.Project.trackProgressProject(self):
    #         # Calculate the progress of the project by summing completed tasks.
    #         query = "SELECT completed FROM task WHERE projectID = %s"
    #         data = (self.projectID, )
    #         tasks_completion = fetch_query(query, data)
    #         if tasks_completion:
    #             completed_sum = sum(completed == 1 for completed in tasks_completion)
    #             num_tasks = len(tasks_completion)
    #             return completed_sum / num_tasks  # Return the completion ratio.
    #         else:
    #             return 0.0  # If there are no tasks, return 0.0.

    def insert_test_task(db, cursor, projectID, completed):
        query = "INSERT INTO task (projectID, taskName, completed) VALUES (%s, %s, 1)"
        data = (projectID, 'testTask')
        cursor.execute(query, data)
        db.commit()

    class YourClassTests(unittest.TestCase):

        def setUp(self):
            # This method is called before each test to set up the initial state of the database.
            # These could change based on what you set them to
            projectID = 0
            self.project = A5.Project(projectID)
            self.mydb = A5.mydb
            self.cursor = A5.mydb.cursor()
            self.cursor.execute("DELETE FROM projects")
            self.cursor.execute("DELETE FROM tasks")
            self.mydb.commit()
            query = "INSERT INTO project (projectName, priority, teamID) VALUES (%s, %s, %s)"
            data = ("testProject", 0, 0)
            self.cursor.execute(query, data)
            self.mydb.commit()


        def tearDown(self):
            # This method is called after each test to clean up any changes made to the database during the test.
            self.cursor.execute("DELETE FROM projects")
            self.cursor.execute("DELETE FROM tasks")
            self.mydb.commit()

        def test_track_progress_project_no_tasks(self):
            # Test when there are no tasks in the project.
            result = self.project.trackProgressProject()
            self.assertEqual(result, 0.0)

        def test_track_progress_project_all_tasks_completed(self):
            # Test when all tasks in the project are completed.
            insert_test_task(self.mydb, self.cursor, self.project.projectID, 1)

            result = self.project.trackProgressProject()
            self.assertEqual(result, 1.0)

        def test_track_progress_project_mixed_completed_tasks(self):
            # Test when there are both completed and incomplete tasks in the project.
            insert_test_task(self.mydb, self.cursor, self.project.projectID, 1)
            insert_test_task(self.mydb, self.cursor, self.project.projectID, 0)

            result = self.project.trackProgressProject()
            self.assertEqual(result, 0.5)  # Since half of the tasks are completed.

        def test_track_progress_project_no_completed_tasks(self):
            # Test when there are tasks in the project, but none of them are completed.
            insert_test_task(self.mydb, self.cursor, self.project.projectID, 0)

            result = self.project.trackProgressProject()
            self.assertEqual(result, 0.0)

        def test_track_progress_project_invalid_project_id(self):
            # Test when an invalid project ID is provided.
            invalid_project = assign_3.Project(-1)  # Assuming project IDs are non-negative integers.
            result = invalid_project.trackProgressProject()
            self.assertEqual(result, 0.0)  # Since there are no tasks for an invalid project.

if __name__ == '__main__':
    unittest.main()