from app.BLL.Interfaces.IRoleService import IRoleService
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from app.GUI.model.models import Roles
from typing import List

class RoleService(IRoleService):
    def __init__(self, roleRepository: IRoleRepository) -> None:
        self.roleRepository = roleRepository

    def get_roles_all(self) -> List[Roles]:
        return self.roleRepository.get_roles_all(), 200  

    def get_role_by_name(self, role_name: str) -> Roles:
        return self.roleRepository.get_role_by_name(rolename=role_name)
    
    def get_list_role(self, roles: List[str]) -> List[Roles]:
        return self.roleRepository.get_list_role(roles=roles)
    
    def check_role(self, role_name: str) -> bool:
        return self.roleRepository.check_role(role_name=role_name)

    def add_role(self, role: Roles) -> bool:
        flag = self.roleRepository.add_role(role=role)
        if (not flag):
            return {'error': 'Lỗi trong quá trình tạo thêm ROLE'}, 400
        return {'success': 'Đã thêm thành công ROLE'}, 200
    
    def delete_role(self, role_name: str):
        if (not self.roleRepository.delete_role(role_name=role_name)):
            return {'error': 'Không tồn tại role để xóa'}, 404
        return {'success': 'Đã xóa role thành công'}, 204
        
