import unittest
from app.models import User,Pitch,Comment
from app import db


class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.new_user = User(password = '1234')

    def test_password_setter(self):
        self.assertTrue(self.new_user.pass_secure is not None)

    def test_no_access_password(self):
            with self.assertRaises(AttributeError):
                self.new_user.password

    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('1234'))


class TestPitch(unittest.TestCase):

    def setUp(self):
        self.new_pitch = Pitch(pitch_content = "pitch one", pitch_category='Business')
        self.new_comment = Comment(comment_content = "One comment", pitch=self.new_pitch)
    
    def tearDown(self):
        db.session.delete(self)
        User.query.commit()
        

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))


    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.comment_content,"One comment")
        self.assertEquals(self.new_comment.pitch,self.new_pitch, 'pitch one')


