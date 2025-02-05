from app.BLL.Interfaces.IRoleService import IRoleService
from app.DAL.Interfaces.IRoleRepository import IRoleRepository
from app.GUI.model.models import Roles
from typing import List
from injector import inject
from sqlalchemy.orm import Session
from app.custom.Helper.Helper import TransactionManager

class RoleService(IRoleService):
    @inject
    def __init__(self, roleRepository: IRoleRepository, tm: TransactionManager) -> None:
        self.roleRepository = roleRepository
        self.tm = tm

    def get_roles_all(self) -> List[Roles]:
        with self.tm.transaction('') as session:
            return self.roleRepository.get_roles_all(session=session), 200  

    def get_role_by_name(self, role_name: str) -> Roles:
        with self.tm.transaction('') as session:
            return self.roleRepository.get_role_by_name(session=session, rolename=role_name)
    
    def get_list_role(self, roles: List[str]) -> List[Roles]:
        with self.tm.transaction('') as session:
            return self.roleRepository.get_list_role(session=session, roles=roles)
    
    def check_role(self, role_name: str) -> bool:
        with self.tm.transaction('') as session:
            return self.roleRepository.check_role(session=session, role_name=role_name)

    def add_role(self, role: Roles) -> bool:
        with self.tm.transaction('Lỗi khi thêm role') as session:
            flag = self.roleRepository.add_role(session=session, role=role)
            if (not flag):
                return {'error': 'Lỗi trong quá trình tạo thêm ROLE'}, 400
            return {'success': 'Đã thêm thành công ROLE'}, 200
    
    def delete_role(self, role_name: str):
        with self.tm.transaction() as session:
            if (not self.roleRepository.delete_role(session=session, role_name=role_name)):
                return {'error': 'Không tồn tại role để xóa'}, 404
            return {'success': 'Đã xóa role thành công'}, 204
        
