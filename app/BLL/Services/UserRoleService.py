# from app.BLL.Interfaces.IUserRoleService import IUserRoleService
# from typing import List
# from app.DAL.Interfaces.IUserRoleRepository import IUserRoleRepository
# from app.GUI.model.models import User, Roles

# class UserRoleService(IUserRoleService):
#     def __init__(self, user_role_repository: IUserRoleRepository) -> None:
#         self.user_role_repository = user_role_repository
    
#     def add_role_user(self, user: User, roles: List[Roles]) -> bool:
#         flag = self.user_role_repository.add_role_user(user=user, roles=roles)
#         if (not flag):
#             return {'error': 'Lỗi trong quá trình thêm role'}, 400
#         return flag, 200
    
    