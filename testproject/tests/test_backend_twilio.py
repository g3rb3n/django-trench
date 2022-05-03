import pytest

from trench.backends.twilio import TwilioMessageDispatcher
from twilio.rest.api.v2010.account.message import MessageList
from twilio.base.exceptions import TwilioRestException
from unittest.mock import patch


def create_with_exception(a,body,to,from_):
    raise TwilioRestException(status=400, uri='http://')


def create(a,body,to,from_):
    return


@patch.object(MessageList, 'create', create_with_exception)
@pytest.mark.django_db
def test_twilio_backend_failure(active_user_with_twilio_otp, settings):
    auth_method = active_user_with_twilio_otp.mfa_methods.get(name="sms_twilio")
    conf = settings.TRENCH_AUTH["MFA_METHODS"]["sms_twilio"]
    response = TwilioMessageDispatcher(
        mfa_method=auth_method, config=conf
    ).dispatch_message()
    assert response.data['details'] == ''


@patch.object(MessageList, 'create', create)
@pytest.mark.django_db
def test_twilio_backend_no_failure(active_user_with_twilio_otp, settings):
    auth_method = active_user_with_twilio_otp.mfa_methods.get(name="sms_twilio")
    conf = settings.TRENCH_AUTH["MFA_METHODS"]["sms_twilio"]
    response = TwilioMessageDispatcher(
        mfa_method=auth_method, config=conf
    ).dispatch_message()
    assert response.data['details'] == 'SMS message with MFA code has been sent.'
