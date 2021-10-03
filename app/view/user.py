from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from app.core.view import create_access_token
from app.models.user import User
from app.schema.user import UserIn, Token

router = InferringRouter()


@cbv(router)
class UserRoute:
    @router.post("/register/", response_model=Token, tags=["Auth"])
    async def create_user(self, user: UserIn):
        user_obj = await User.filter(login=user.login, deleted_at=None).get_or_none()
        if user_obj is not None:
            raise HTTPException(status_code=409, detail="User with this login already exists")
        user_obj = await User.create(login=user.login, password=user.password)
        access_token = create_access_token(data={"sub": user_obj.login})
        return Token(access_token=access_token, token_type="bearer")

    @router.post("/token/", response_model=Token, tags=["Auth"])
    async def token(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user_obj = await User.filter(login=form_data.username, deleted_at=None).get_or_none()
        if user_obj is None:
            raise HTTPException(status_code=404, detail="User with this login not found")
        elif not user_obj.check_password(form_data.password):
            raise HTTPException(status_code=403, detail="Incorrect password")
        await user_obj.save()
        access_token = create_access_token(data={"sub": user_obj.login})
        return Token(access_token=access_token, token_type="bearer")
