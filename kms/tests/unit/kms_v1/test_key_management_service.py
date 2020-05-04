# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import grpc_helpers
from google.auth import credentials
from google.cloud.kms_v1.services.key_management_service import KeyManagementServiceClient
from google.cloud.kms_v1.services.key_management_service import pagers
from google.cloud.kms_v1.services.key_management_service import transports
from google.cloud.kms_v1.types import resources
from google.cloud.kms_v1.types import service
from google.oauth2 import service_account
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert KeyManagementServiceClient._get_default_mtls_endpoint(None) is None
    assert KeyManagementServiceClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert KeyManagementServiceClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert KeyManagementServiceClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert KeyManagementServiceClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert KeyManagementServiceClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_key_management_service_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = KeyManagementServiceClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = KeyManagementServiceClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == 'cloudkms.googleapis.com:443'


def test_key_management_service_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch('google.cloud.kms_v1.services.key_management_service.KeyManagementServiceClient.get_transport_class') as gtc:
        transport = transports.KeyManagementServiceGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = KeyManagementServiceClient(transport=transport)
        gtc.assert_not_called()

    # Check mTLS is not triggered with empty client options.
    options = client_options.ClientOptions()
    with mock.patch('google.cloud.kms_v1.services.key_management_service.KeyManagementServiceClient.get_transport_class') as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = KeyManagementServiceClient(client_options=options)
        transport.assert_called_once_with(
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is not triggered if api_endpoint is provided but
    # client_cert_source is None.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch('google.cloud.kms_v1.services.key_management_service.transports.KeyManagementServiceGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = KeyManagementServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )

    # Check mTLS is triggered if client_cert_source is provided.
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch('google.cloud.kms_v1.services.key_management_service.transports.KeyManagementServiceGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = KeyManagementServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is triggered if api_endpoint and client_cert_source are provided.
    options = client_options.ClientOptions(
        api_endpoint="squid.clam.whelk",
        client_cert_source=client_cert_source_callback
    )
    with mock.patch('google.cloud.kms_v1.services.key_management_service.transports.KeyManagementServiceGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = KeyManagementServiceClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host="squid.clam.whelk",
        )

def test_key_management_service_client_client_options_from_dict():
    with mock.patch('google.cloud.kms_v1.services.key_management_service.transports.KeyManagementServiceGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = KeyManagementServiceClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_list_key_rings(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.ListKeyRingsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_key_rings),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListKeyRingsResponse(
            next_page_token='next_page_token_value',
            total_size=1086,
        )

        response = client.list_key_rings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListKeyRingsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.total_size == 1086


def test_list_key_rings_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListKeyRingsRequest(
        parent='parent/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_key_rings),
            '__call__') as call:
        call.return_value = service.ListKeyRingsResponse()
        client.list_key_rings(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent/value',
    ) in kw['metadata']


def test_list_key_rings_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_key_rings),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListKeyRingsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_key_rings(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == 'parent_value'


def test_list_key_rings_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_key_rings(
            service.ListKeyRingsRequest(),
            parent='parent_value',
        )


def test_list_key_rings_pager():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_key_rings),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
                next_page_token='abc',
            ),
            service.ListKeyRingsResponse(
                key_rings=[],
                next_page_token='def',
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                ],
                next_page_token='ghi',
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.list_key_rings(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, resources.KeyRing)
                   for i in results)

def test_list_key_rings_pages():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_key_rings),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
                next_page_token='abc',
            ),
            service.ListKeyRingsResponse(
                key_rings=[],
                next_page_token='def',
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                ],
                next_page_token='ghi',
            ),
            service.ListKeyRingsResponse(
                key_rings=[
                    resources.KeyRing(),
                    resources.KeyRing(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_key_rings(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_list_crypto_keys(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.ListCryptoKeysRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_keys),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeysResponse(
            next_page_token='next_page_token_value',
            total_size=1086,
        )

        response = client.list_crypto_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCryptoKeysPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.total_size == 1086


def test_list_crypto_keys_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCryptoKeysRequest(
        parent='parent/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_keys),
            '__call__') as call:
        call.return_value = service.ListCryptoKeysResponse()
        client.list_crypto_keys(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent/value',
    ) in kw['metadata']


def test_list_crypto_keys_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_keys),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeysResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_crypto_keys(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == 'parent_value'


def test_list_crypto_keys_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crypto_keys(
            service.ListCryptoKeysRequest(),
            parent='parent_value',
        )


def test_list_crypto_keys_pager():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_keys),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
                next_page_token='abc',
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[],
                next_page_token='def',
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                ],
                next_page_token='ghi',
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.list_crypto_keys(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, resources.CryptoKey)
                   for i in results)

def test_list_crypto_keys_pages():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_keys),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
                next_page_token='abc',
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[],
                next_page_token='def',
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                ],
                next_page_token='ghi',
            ),
            service.ListCryptoKeysResponse(
                crypto_keys=[
                    resources.CryptoKey(),
                    resources.CryptoKey(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_crypto_keys(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_list_crypto_key_versions(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.ListCryptoKeyVersionsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_key_versions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeyVersionsResponse(
            next_page_token='next_page_token_value',
            total_size=1086,
        )

        response = client.list_crypto_key_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListCryptoKeyVersionsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.total_size == 1086


def test_list_crypto_key_versions_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListCryptoKeyVersionsRequest(
        parent='parent/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_key_versions),
            '__call__') as call:
        call.return_value = service.ListCryptoKeyVersionsResponse()
        client.list_crypto_key_versions(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent/value',
    ) in kw['metadata']


def test_list_crypto_key_versions_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_key_versions),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListCryptoKeyVersionsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_crypto_key_versions(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == 'parent_value'


def test_list_crypto_key_versions_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_crypto_key_versions(
            service.ListCryptoKeyVersionsRequest(),
            parent='parent_value',
        )


def test_list_crypto_key_versions_pager():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_key_versions),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
                next_page_token='abc',
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[],
                next_page_token='def',
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                ],
                next_page_token='ghi',
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.list_crypto_key_versions(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, resources.CryptoKeyVersion)
                   for i in results)

def test_list_crypto_key_versions_pages():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_crypto_key_versions),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
                next_page_token='abc',
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[],
                next_page_token='def',
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                ],
                next_page_token='ghi',
            ),
            service.ListCryptoKeyVersionsResponse(
                crypto_key_versions=[
                    resources.CryptoKeyVersion(),
                    resources.CryptoKeyVersion(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_crypto_key_versions(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_list_import_jobs(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.ListImportJobsRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_import_jobs),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListImportJobsResponse(
            next_page_token='next_page_token_value',
            total_size=1086,
        )

        response = client.list_import_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListImportJobsPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.total_size == 1086


def test_list_import_jobs_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.ListImportJobsRequest(
        parent='parent/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_import_jobs),
            '__call__') as call:
        call.return_value = service.ListImportJobsResponse()
        client.list_import_jobs(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent/value',
    ) in kw['metadata']


def test_list_import_jobs_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_import_jobs),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.ListImportJobsResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.list_import_jobs(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == 'parent_value'


def test_list_import_jobs_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_import_jobs(
            service.ListImportJobsRequest(),
            parent='parent_value',
        )


def test_list_import_jobs_pager():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_import_jobs),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
                next_page_token='abc',
            ),
            service.ListImportJobsResponse(
                import_jobs=[],
                next_page_token='def',
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                ],
                next_page_token='ghi',
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.list_import_jobs(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, resources.ImportJob)
                   for i in results)

def test_list_import_jobs_pages():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.list_import_jobs),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
                next_page_token='abc',
            ),
            service.ListImportJobsResponse(
                import_jobs=[],
                next_page_token='def',
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                ],
                next_page_token='ghi',
            ),
            service.ListImportJobsResponse(
                import_jobs=[
                    resources.ImportJob(),
                    resources.ImportJob(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_import_jobs(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_get_key_ring(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.GetKeyRingRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_key_ring),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing(
            name='name_value',
        )

        response = client.get_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.KeyRing)
    assert response.name == 'name_value'


def test_get_key_ring_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetKeyRingRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_key_ring),
            '__call__') as call:
        call.return_value = resources.KeyRing()
        client.get_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_key_ring_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_key_ring),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_key_ring(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'


def test_get_key_ring_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_key_ring(
            service.GetKeyRingRequest(),
            name='name_value',
        )


def test_get_crypto_key(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.GetCryptoKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_crypto_key),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey(
            name='name_value',
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
        )

        response = client.get_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == 'name_value'
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT


def test_get_crypto_key_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCryptoKeyRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_crypto_key),
            '__call__') as call:
        call.return_value = resources.CryptoKey()
        client.get_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_crypto_key_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_crypto_key),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_crypto_key(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'


def test_get_crypto_key_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_crypto_key(
            service.GetCryptoKeyRequest(),
            name='name_value',
        )


def test_get_crypto_key_version(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.GetCryptoKeyVersionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name='name_value',
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job='import_job_value',
            import_failure_reason='import_failure_reason_value',
        )

        response = client.get_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == 'name_value'
    assert response.state == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.algorithm == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    assert response.import_job == 'import_job_value'
    assert response.import_failure_reason == 'import_failure_reason_value'


def test_get_crypto_key_version_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetCryptoKeyVersionRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_crypto_key_version),
            '__call__') as call:
        call.return_value = resources.CryptoKeyVersion()
        client.get_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_crypto_key_version(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'


def test_get_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_crypto_key_version(
            service.GetCryptoKeyVersionRequest(),
            name='name_value',
        )


def test_get_public_key(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.GetPublicKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_public_key),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PublicKey(
            pem='pem_value',
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
        )

        response = client.get_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.PublicKey)
    assert response.pem == 'pem_value'
    assert response.algorithm == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION


def test_get_public_key_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetPublicKeyRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_public_key),
            '__call__') as call:
        call.return_value = resources.PublicKey()
        client.get_public_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_public_key_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_public_key),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.PublicKey()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_public_key(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'


def test_get_public_key_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_public_key(
            service.GetPublicKeyRequest(),
            name='name_value',
        )


def test_get_import_job(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.GetImportJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_import_job),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob(
            name='name_value',
            import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
        )

        response = client.get_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ImportJob)
    assert response.name == 'name_value'
    assert response.import_method == resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.state == resources.ImportJob.ImportJobState.PENDING_GENERATION


def test_get_import_job_field_headers():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
  )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = service.GetImportJobRequest(
        name='name/value',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_import_job),
            '__call__') as call:
        call.return_value = resources.ImportJob()
        client.get_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name/value',
    ) in kw['metadata']


def test_get_import_job_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.get_import_job),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.get_import_job(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'


def test_get_import_job_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_import_job(
            service.GetImportJobRequest(),
            name='name_value',
        )


def test_create_key_ring(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.CreateKeyRingRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_key_ring),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing(
            name='name_value',
        )

        response = client.create_key_ring(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.KeyRing)
    assert response.name == 'name_value'


def test_create_key_ring_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_key_ring),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.KeyRing()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_key_ring(
            parent='parent_value',
            key_ring_id='key_ring_id_value',
            key_ring=resources.KeyRing(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == 'parent_value'
        assert args[0].key_ring_id == 'key_ring_id_value'
        assert args[0].key_ring == resources.KeyRing(name='name_value')


def test_create_key_ring_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_key_ring(
            service.CreateKeyRingRequest(),
            parent='parent_value',
            key_ring_id='key_ring_id_value',
            key_ring=resources.KeyRing(name='name_value'),
        )


def test_create_crypto_key(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.CreateCryptoKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_crypto_key),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey(
            name='name_value',
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
        )

        response = client.create_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == 'name_value'
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT


def test_create_crypto_key_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_crypto_key),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_crypto_key(
            parent='parent_value',
            crypto_key_id='crypto_key_id_value',
            crypto_key=resources.CryptoKey(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == 'parent_value'
        assert args[0].crypto_key_id == 'crypto_key_id_value'
        assert args[0].crypto_key == resources.CryptoKey(name='name_value')


def test_create_crypto_key_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_crypto_key(
            service.CreateCryptoKeyRequest(),
            parent='parent_value',
            crypto_key_id='crypto_key_id_value',
            crypto_key=resources.CryptoKey(name='name_value'),
        )


def test_create_crypto_key_version(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.CreateCryptoKeyVersionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name='name_value',
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job='import_job_value',
            import_failure_reason='import_failure_reason_value',
        )

        response = client.create_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == 'name_value'
    assert response.state == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.algorithm == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    assert response.import_job == 'import_job_value'
    assert response.import_failure_reason == 'import_failure_reason_value'


def test_create_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_crypto_key_version(
            parent='parent_value',
            crypto_key_version=resources.CryptoKeyVersion(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == 'parent_value'
        assert args[0].crypto_key_version == resources.CryptoKeyVersion(name='name_value')


def test_create_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_crypto_key_version(
            service.CreateCryptoKeyVersionRequest(),
            parent='parent_value',
            crypto_key_version=resources.CryptoKeyVersion(name='name_value'),
        )


def test_import_crypto_key_version(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.ImportCryptoKeyVersionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.import_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name='name_value',
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job='import_job_value',
            import_failure_reason='import_failure_reason_value',
        )

        response = client.import_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == 'name_value'
    assert response.state == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.algorithm == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    assert response.import_job == 'import_job_value'
    assert response.import_failure_reason == 'import_failure_reason_value'


def test_create_import_job(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.CreateImportJobRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_import_job),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob(
            name='name_value',
            import_method=resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            state=resources.ImportJob.ImportJobState.PENDING_GENERATION,
        )

        response = client.create_import_job(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.ImportJob)
    assert response.name == 'name_value'
    assert response.import_method == resources.ImportJob.ImportMethod.RSA_OAEP_3072_SHA1_AES_256
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.state == resources.ImportJob.ImportJobState.PENDING_GENERATION


def test_create_import_job_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.create_import_job),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.ImportJob()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.create_import_job(
            parent='parent_value',
            import_job_id='import_job_id_value',
            import_job=resources.ImportJob(name='name_value'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].parent == 'parent_value'
        assert args[0].import_job_id == 'import_job_id_value'
        assert args[0].import_job == resources.ImportJob(name='name_value')


def test_create_import_job_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_import_job(
            service.CreateImportJobRequest(),
            parent='parent_value',
            import_job_id='import_job_id_value',
            import_job=resources.ImportJob(name='name_value'),
        )


def test_update_crypto_key(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.UpdateCryptoKeyRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_crypto_key),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey(
            name='name_value',
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
        )

        response = client.update_crypto_key(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == 'name_value'
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT


def test_update_crypto_key_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_crypto_key),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_crypto_key(
            crypto_key=resources.CryptoKey(name='name_value'),
            update_mask=field_mask.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].crypto_key == resources.CryptoKey(name='name_value')
        assert args[0].update_mask == field_mask.FieldMask(paths=['paths_value'])


def test_update_crypto_key_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key(
            service.UpdateCryptoKeyRequest(),
            crypto_key=resources.CryptoKey(name='name_value'),
            update_mask=field_mask.FieldMask(paths=['paths_value']),
        )


def test_update_crypto_key_version(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.UpdateCryptoKeyVersionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name='name_value',
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job='import_job_value',
            import_failure_reason='import_failure_reason_value',
        )

        response = client.update_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == 'name_value'
    assert response.state == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.algorithm == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    assert response.import_job == 'import_job_value'
    assert response.import_failure_reason == 'import_failure_reason_value'


def test_update_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_crypto_key_version(
            crypto_key_version=resources.CryptoKeyVersion(name='name_value'),
            update_mask=field_mask.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].crypto_key_version == resources.CryptoKeyVersion(name='name_value')
        assert args[0].update_mask == field_mask.FieldMask(paths=['paths_value'])


def test_update_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key_version(
            service.UpdateCryptoKeyVersionRequest(),
            crypto_key_version=resources.CryptoKeyVersion(name='name_value'),
            update_mask=field_mask.FieldMask(paths=['paths_value']),
        )


def test_encrypt(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.EncryptRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.encrypt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.EncryptResponse(
            name='name_value',
            ciphertext=b'ciphertext_blob',
        )

        response = client.encrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.EncryptResponse)
    assert response.name == 'name_value'
    assert response.ciphertext == b'ciphertext_blob'


def test_encrypt_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.encrypt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.EncryptResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.encrypt(
            name='name_value',
            plaintext=b'plaintext_blob',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'
        assert args[0].plaintext == b'plaintext_blob'


def test_encrypt_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.encrypt(
            service.EncryptRequest(),
            name='name_value',
            plaintext=b'plaintext_blob',
        )


def test_decrypt(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.DecryptRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.decrypt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.DecryptResponse(
            plaintext=b'plaintext_blob',
        )

        response = client.decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.DecryptResponse)
    assert response.plaintext == b'plaintext_blob'


def test_decrypt_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.decrypt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.DecryptResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.decrypt(
            name='name_value',
            ciphertext=b'ciphertext_blob',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'
        assert args[0].ciphertext == b'ciphertext_blob'


def test_decrypt_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.decrypt(
            service.DecryptRequest(),
            name='name_value',
            ciphertext=b'ciphertext_blob',
        )


def test_asymmetric_sign(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.AsymmetricSignRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.asymmetric_sign),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricSignResponse(
            signature=b'signature_blob',
        )

        response = client.asymmetric_sign(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.AsymmetricSignResponse)
    assert response.signature == b'signature_blob'


def test_asymmetric_sign_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.asymmetric_sign),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricSignResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.asymmetric_sign(
            name='name_value',
            digest=service.Digest(sha256=b'sha256_blob'),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'
        assert args[0].digest == service.Digest(sha256=b'sha256_blob')


def test_asymmetric_sign_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.asymmetric_sign(
            service.AsymmetricSignRequest(),
            name='name_value',
            digest=service.Digest(sha256=b'sha256_blob'),
        )


def test_asymmetric_decrypt(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.AsymmetricDecryptRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.asymmetric_decrypt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricDecryptResponse(
            plaintext=b'plaintext_blob',
        )

        response = client.asymmetric_decrypt(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, service.AsymmetricDecryptResponse)
    assert response.plaintext == b'plaintext_blob'


def test_asymmetric_decrypt_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.asymmetric_decrypt),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = service.AsymmetricDecryptResponse()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.asymmetric_decrypt(
            name='name_value',
            ciphertext=b'ciphertext_blob',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'
        assert args[0].ciphertext == b'ciphertext_blob'


def test_asymmetric_decrypt_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.asymmetric_decrypt(
            service.AsymmetricDecryptRequest(),
            name='name_value',
            ciphertext=b'ciphertext_blob',
        )


def test_update_crypto_key_primary_version(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.UpdateCryptoKeyPrimaryVersionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_crypto_key_primary_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey(
            name='name_value',
            purpose=resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT,
        )

        response = client.update_crypto_key_primary_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKey)
    assert response.name == 'name_value'
    assert response.purpose == resources.CryptoKey.CryptoKeyPurpose.ENCRYPT_DECRYPT


def test_update_crypto_key_primary_version_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.update_crypto_key_primary_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKey()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.update_crypto_key_primary_version(
            name='name_value',
            crypto_key_version_id='crypto_key_version_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'
        assert args[0].crypto_key_version_id == 'crypto_key_version_id_value'


def test_update_crypto_key_primary_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_crypto_key_primary_version(
            service.UpdateCryptoKeyPrimaryVersionRequest(),
            name='name_value',
            crypto_key_version_id='crypto_key_version_id_value',
        )


def test_destroy_crypto_key_version(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.DestroyCryptoKeyVersionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.destroy_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name='name_value',
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job='import_job_value',
            import_failure_reason='import_failure_reason_value',
        )

        response = client.destroy_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == 'name_value'
    assert response.state == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.algorithm == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    assert response.import_job == 'import_job_value'
    assert response.import_failure_reason == 'import_failure_reason_value'


def test_destroy_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.destroy_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.destroy_crypto_key_version(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'


def test_destroy_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.destroy_crypto_key_version(
            service.DestroyCryptoKeyVersionRequest(),
            name='name_value',
        )


def test_restore_crypto_key_version(transport: str = 'grpc'):
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = service.RestoreCryptoKeyVersionRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.restore_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion(
            name='name_value',
            state=resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION,
            protection_level=resources.ProtectionLevel.SOFTWARE,
            algorithm=resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION,
            import_job='import_job_value',
            import_failure_reason='import_failure_reason_value',
        )

        response = client.restore_crypto_key_version(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, resources.CryptoKeyVersion)
    assert response.name == 'name_value'
    assert response.state == resources.CryptoKeyVersion.CryptoKeyVersionState.PENDING_GENERATION
    assert response.protection_level == resources.ProtectionLevel.SOFTWARE
    assert response.algorithm == resources.CryptoKeyVersion.CryptoKeyVersionAlgorithm.GOOGLE_SYMMETRIC_ENCRYPTION
    assert response.import_job == 'import_job_value'
    assert response.import_failure_reason == 'import_failure_reason_value'


def test_restore_crypto_key_version_flattened():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.restore_crypto_key_version),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = resources.CryptoKeyVersion()

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.restore_crypto_key_version(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].name == 'name_value'


def test_restore_crypto_key_version_flattened_error():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.restore_crypto_key_version(
            service.RestoreCryptoKeyVersionRequest(),
            name='name_value',
        )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.KeyManagementServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = KeyManagementServiceClient(
            credentials=credentials.AnonymousCredentials(),
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.KeyManagementServiceGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = KeyManagementServiceClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client._transport,
        transports.KeyManagementServiceGrpcTransport,
    )


def test_key_management_service_base_transport():
    # Instantiate the base transport.
    transport = transports.KeyManagementServiceTransport(
        credentials=credentials.AnonymousCredentials(),
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'list_key_rings',
        'list_crypto_keys',
        'list_crypto_key_versions',
        'list_import_jobs',
        'get_key_ring',
        'get_crypto_key',
        'get_crypto_key_version',
        'get_public_key',
        'get_import_job',
        'create_key_ring',
        'create_crypto_key',
        'create_crypto_key_version',
        'import_crypto_key_version',
        'create_import_job',
        'update_crypto_key',
        'update_crypto_key_version',
        'encrypt',
        'decrypt',
        'asymmetric_sign',
        'asymmetric_decrypt',
        'update_crypto_key_primary_version',
        'destroy_crypto_key_version',
        'restore_crypto_key_version',
        )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())


def test_key_management_service_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, 'default') as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        KeyManagementServiceClient()
        adc.assert_called_once_with(scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/cloudkms',
        ))


def test_key_management_service_host_no_port():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='cloudkms.googleapis.com'),
        transport='grpc',
    )
    assert client._transport._host == 'cloudkms.googleapis.com:443'


def test_key_management_service_host_with_port():
    client = KeyManagementServiceClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='cloudkms.googleapis.com:8000'),
        transport='grpc',
    )
    assert client._transport._host == 'cloudkms.googleapis.com:8000'


def test_key_management_service_grpc_transport_channel():
    channel = grpc.insecure_channel('http://localhost/')

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.KeyManagementServiceGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_key_management_service_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.KeyManagementServiceGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        ssl_credentials=mock_ssl_cred,
        scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
            'https://www.googleapis.com/auth/cloudkms',
        ),
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_key_management_service_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.KeyManagementServiceGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            ssl_credentials=mock_ssl_cred,
            scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/cloudkms',
            ),
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_import_job_path():
    project = "squid"
    location = "clam"
    key_ring = "whelk"
    import_job = "octopus"

    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/importJobs/{import_job}".format(project=project, location=location, key_ring=key_ring, import_job=import_job, )
    actual = KeyManagementServiceClient.import_job_path(project, location, key_ring, import_job)
    assert expected == actual


def test_parse_import_job_path():
    expected = {
    "project": "oyster",
    "location": "nudibranch",
    "key_ring": "cuttlefish",
    "import_job": "mussel",

    }
    path = KeyManagementServiceClient.import_job_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_import_job_path(path)
    assert expected == actual

def test_key_ring_path():
    project = "squid"
    location = "clam"
    key_ring = "whelk"

    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}".format(project=project, location=location, key_ring=key_ring, )
    actual = KeyManagementServiceClient.key_ring_path(project, location, key_ring)
    assert expected == actual


def test_parse_key_ring_path():
    expected = {
    "project": "octopus",
    "location": "oyster",
    "key_ring": "nudibranch",

    }
    path = KeyManagementServiceClient.key_ring_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_key_ring_path(path)
    assert expected == actual

def test_crypto_key_version_path():
    project = "squid"
    location = "clam"
    key_ring = "whelk"
    crypto_key = "octopus"
    crypto_key_version = "oyster"

    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}/cryptoKeyVersions/{crypto_key_version}".format(project=project, location=location, key_ring=key_ring, crypto_key=crypto_key, crypto_key_version=crypto_key_version, )
    actual = KeyManagementServiceClient.crypto_key_version_path(project, location, key_ring, crypto_key, crypto_key_version)
    assert expected == actual


def test_parse_crypto_key_version_path():
    expected = {
    "project": "nudibranch",
    "location": "cuttlefish",
    "key_ring": "mussel",
    "crypto_key": "winkle",
    "crypto_key_version": "nautilus",

    }
    path = KeyManagementServiceClient.crypto_key_version_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_crypto_key_version_path(path)
    assert expected == actual

def test_crypto_key_path():
    project = "squid"
    location = "clam"
    key_ring = "whelk"
    crypto_key = "octopus"

    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(project=project, location=location, key_ring=key_ring, crypto_key=crypto_key, )
    actual = KeyManagementServiceClient.crypto_key_path(project, location, key_ring, crypto_key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
    "project": "oyster",
    "location": "nudibranch",
    "key_ring": "cuttlefish",
    "crypto_key": "mussel",

    }
    path = KeyManagementServiceClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = KeyManagementServiceClient.parse_crypto_key_path(path)
    assert expected == actual
