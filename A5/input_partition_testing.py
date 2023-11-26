import assign_3
import unittest
import mysql.connector

# assign_3.Project.trackProgressProject(self):
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
        self.project = assign_3.Project(projectID)
        self.mydb = assign_3.mydb
        self.cursor = assign_3.mydb.cursor()
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