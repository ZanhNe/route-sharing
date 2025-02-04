from app.BLL.Interfaces.IRoleService import IRoleService
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from app.GUI.model.models import Roles
from typing import List
from injector import inject
from sqlalchemy.orm import Session

class RoleService(IRoleService):
    @inject
    def __init__(self, roleRepository: IRoleRepository) -> None:
        self.roleRepository = roleRepository

    def get_roles_all(self, session: Session) -> List[Roles]:
        return self.roleRepository.get_roles_all(session=session), 200  

    def get_role_by_name(self, session: Session, role_name: str) -> Roles:
        return self.roleRepository.get_role_by_name(session=session, rolename=role_name)
    
    def get_list_role(self, session: Session, roles: List[str]) -> List[Roles]:
        return self.roleRepository.get_list_role(session=session, roles=roles)
    
    def check_role(self, session: Session, role_name: str) -> bool:
        return self.roleRepository.check_role(session=session, role_name=role_name)

    def add_role(self, session: Session, role: Roles) -> bool:
        flag = self.roleRepository.add_role(session=session, role=role)
        if (not flag):
            return {'error': 'Lỗi trong quá trình tạo thêm ROLE'}, 400
        return {'success': 'Đã thêm thành công ROLE'}, 200
    
    def delete_role(self, session: Session, role_name: str):
        if (not self.roleRepository.delete_role(session=session, role_name=role_name)):
            return {'error': 'Không tồn tại role để xóa'}, 404
        return {'success': 'Đã xóa role thành công'}, 204
        
