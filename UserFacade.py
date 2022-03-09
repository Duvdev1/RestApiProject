from abc import ABC

import MyLogger1
from MyLogger1 import Logger
from Db3_config import local_session
from User_db import User
from db_customer_repo import DbRepo

repo = DbRepo
logger = Logger.get_instance()


class userFacade2(ABC):
    def __init__(self):
        self.repo = DbRepo(local_session)

    def update_user(self, user):
        logger.logger.info(f'userFacade: starting update procedure for user id: {user.id}')
        logger.logger.info(f'userFacade: getting user by id {user.id}')
        my_user = self.repo.get_by_id(User, user.id)
        if my_user:
            try:
                logger.logger.info(f'userFacade: updating user')
                updated_user = self.repo.update_by_id(User, user)
                if updated_user:
                    logger.logger.info(f'userFacade: successfully updated user')
            except():
                logger.logger.error(f'userFacade: failed to update user')

    def get_by_id(self, id):
        logger.logger.info(f'userFacade: getting user by id: {id}')
        try:
            return self.repo.get_by_id(User, id)
        except():
            logger.logger.error(f'userFacade: failed to get user by id: {id}')

    def get_by_name(self, name):
        logger.logger.info(f'userFacade: getting user by name: {name}')
        try:
            user1 = self.repo.get_by_ilike(User, User.user_name, name)
            return user1
        except():
            logger.logger.error(f'userFacade: failed to get user by name: {name}')

    def get_by_user_and_password(self, name, password):
        logger.logger.info(f'userFacade: getting user by name: {name}')
        user = self.repo.get_by_name_and_password(User, User.user_name, User.password, name, password)
        if user is None:
            return None
        else:
            return user

    def get_all_users(self):
        logger.logger.info(f'userFacade: getting users')
        try:
            users = self.repo.get_all(User)
            if users:
                logger.logger.info(f'userFacade: successfully got users')
        except():
            logger.logger.error(f'userFacade: failed to get users')

    def add_user(self, user):
        logger.logger.info(f'userFacade: adding user')
        logger.logger.info(f'userFacade: getting user by id {user.id}')
        user1 = self.repo.get_by_id(User, user.id)
        if user1 is None:
            try:
                logger.logger.info(f'userFacade: adding user')
                self.repo.add(user)
            except():
                logger.logger.error(f'userFacade: failed to add user')

    def remove_user(self, user):
        logger.logger.info(f'userFacade: removing user')
        logger.logger.info(f'userFacade: getting user')
        user1 = self.repo.get_by_id(User, user.id)
        if user1 is None:
            try:
                logger.logger.info(f'userFacade: deleting user by id {user.id}')
                self.repo.delete_by_id(User, User.id, user.id)
                return True
            except():
                logger.logger.error(f'userFacade: failed to remove user')
