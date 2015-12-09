# coding=utf-8
"""
Permission logic module
"""
from permission.logics.base import PermissionLogic
from permission.logics.author import AuthorPermissionLogic
from permission.logics.collaborators import CollaboratorsPermissionLogic
from permission.logics.groupin import GroupInPermissionLogic
from permission.logics.oneself import OneselfPermissionLogic
from permission.logics.staff import StaffPermissionLogic
