# import ekscore.config
from .config import SERVICE_ROLE_NAME
from .cluster import createEKSRole
from .cluster import deleteEKSRole

def run():
    deleteEKSRole(SERVICE_ROLE_NAME)
    serviceRoleARN = createEKSRole(SERVICE_ROLE_NAME)
