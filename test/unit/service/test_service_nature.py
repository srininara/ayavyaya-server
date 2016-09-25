from mock import Mock, patch
from ayavyaya.service import service_nature


@patch('ayavyaya.service.service_nature.enq')
def test_service_nature_getting_nature_listing(mock_enq):
    mock_enq.get_nat_listing.return_value = [
        {"id": 1, "name": "testNature", "description": "testNatureDescription"}]
    output = service_nature.get_nat_listing()
    print(output)
    assert mock_enq.get_nat_listing.called

