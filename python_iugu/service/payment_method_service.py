from typing import Dict, Any

from python_iugu.expcetion import RequiredParameter
from python_iugu.service.base_service import BaseService
from python_iugu.model.payment_method_model import PaymentMethodModel
from python_iugu.request.payment_method_request import PaymentMethodRequest


class CustomerService(BaseService):
    _PREFIX = "payment_methods"
    _SUFFIX = "payment_methods"

    def create(self, payment_method: PaymentMethodRequest) -> PaymentMethodModel:
        if payment_method.customer_id is None:
            raise RequiredParameter('Customer ID not informed')

        url = f"{self._SUFFIX}/{payment_method.customer_id}/{self._SUFFIX}"

        response = self.client.post(url, payment_method)
        return self._deserialize(PaymentMethodModel, response)