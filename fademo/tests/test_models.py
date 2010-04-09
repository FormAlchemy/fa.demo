from sqlalchemy.exceptions import IntegrityError
from fademo.tests import *
# from fademo.tests import Session, metadata, Individual, create_all, drop_all

class TestMyModel(TestModel):
    pass
    # def test_simpleassert(self):
    #     """test description
    #     """
    #     einstein = Individual('einstein')
    # 
    #     Session.commit()
    # 
    #     ind1 = Individual.get_by(name = 'einstein')
    #     assert ind1 == einstein
    # 
    # def test_exception(self):
    #     me = Individual('giuseppe')
    #     me_again = Individual('giuseppe')
    #     self.assertRaises(IntegrityError, Session.commit)
    #     Session.rollback()

