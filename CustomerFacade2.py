from abc import ABC

from MyLogger1 import Logger
from db_customer_repo import DbRepo
from Db_Customers import Customer
from Db3_config import local_session

repo = DbRepo
logger = Logger.get_instance()


class CustomerFacade2(ABC):
    def __init__(self):
        self.repo = DbRepo(local_session)

    def update_customer(self, customer):
        logger.logger.info(f'CustomerFacade: starting update procedure for customer id: {customer.id}')
        logger.logger.info(f'CustomerFacade: getting customer by id {customer.id}')
        my_customer = self.repo.get_by_id(Customer, customer.id)
        if my_customer:
            try:
                logger.logger.info(f'CustomerFacade: updating customer')
                updated_customer = self.repo.update_by_id(Customer, customer)
                if updated_customer:
                    logger.logger.info(f'CustomerFacade: successfully updated customer')
            except():
                logger.logger.error(f'CustomerFacade: failed to update customer')

    def get_by_id(self, id):
        logger.logger.info(f'CustomerFacade: getting customer by id: {id}')
        try:
            return self.repo.get_by_id(Customer, id)
        except():
            logger.logger.error(f'CustomerFacade: failed to get customer by id: {id}')

    def get_all_customers(self):
        logger.logger.info(f'CustomerFacade: getting customers')
        try:
            customers = self.repo.get_all(Customer)
            if customers:
                logger.logger.info(f'CustomerFacade: successfully got customers')
        except():
            logger.logger.error(f'CustomerFacade: failed to get customers')

    def add_customer(self, customer):
        logger.logger.info(f'CustomerFacade: adding customer')
        logger.logger.info(f'CustomerFacade: getting customer by id {customer.id}')
        customer1 = self.repo.get_by_id(Customer, customer.id)
        if customer1 is None:
            try:
                logger.logger.info(f'CustomerFacade: adding customer')
                self.repo.add(customer)
            except():
                logger.logger.error(f'CustomerFacade: failed to add customer')

    def remove_customer(self, customer):
        logger.logger.info(f'CustomerFacade: removing customer')
        logger.logger.info(f'CustomerFacade: getting customer')
        customer1 = self.repo.get_by_id(Customer, customer.id)
        if customer1 is None:
            try:
                logger.logger.info(f'CustomerFacade: deleting customer by id {customer.id}')
                self.repo.delete_by_id(Customer, Customer.id, customer.id)
                return True
            except():
                logger.logger.error(f'CustomerFacade: failed to remove customer')
