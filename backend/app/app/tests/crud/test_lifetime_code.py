from sqlalchemy.orm import Session

from app import crud

def test_check_code(db : Session):
    # non valid code
    result = crud.lifetime_code.check_code(db=db, code="hello")
    assert result == None

    # valid non used code
    result = crud.lifetime_code.check_code(db=db, code="test_unused_code")
    assert result == False

    # valid used code
    result = crud.lifetime_code.check_code(db=db, code="test_used_code")
    assert result == True

def test_redeem_code(db: Session):
    code = crud.lifetime_code.redeem_code(db=db, code="test_unused_code")
    result = crud.lifetime_code.check_code(db=db, code="test_unused_code")
    assert result == True