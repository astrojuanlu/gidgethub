import pytest

from .. import exceptions
from .. import sansio


class TestValidate:

    """Tests for gidgethub.sansio.validate()."""

    secret = "123456"
    payload = "gidget".encode("UTF-8")
    hash_signature = "6ea124f8bfc2e6f5a0a40687201c351716110bec"
    signature = "sha1=" + hash_signature

    def test_malformed_signature(self):
        """Error out if the signature doesn't start with "sha1="."""
        with pytest.raises(exceptions.ValidationFailure):
            sansio.validate(self.payload, secret=self.secret,
                            signature=self.hash_signature)

    def test_validation(self):
        """Success case."""
        sansio.validate(self.payload, secret=self.secret,
                        signature=self.signature)

    def test_failure(self):
        with pytest.raises(exceptions.ValidationFailure):
            sansio.validate(self.payload + b'!', secret=self.secret,
                            signature=self.signature)


class TestEvent:

    """Tests for gidgethub.sansio.Event."""

    def test_init(self):
        event = "event"
        delivery_id = "delivery_id"
        data = {"id": 42}
        ins = sansio.Event(data, event=event, delivery_id=delivery_id)
        assert ins.event == event
        assert ins.delivery_id == delivery_id
        assert ins.data == data